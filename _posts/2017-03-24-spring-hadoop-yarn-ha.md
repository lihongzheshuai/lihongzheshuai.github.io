---
layout: post
title: Spring Hadoop Yarn HA问题调研
tags: [Hadoop]
categories: [大数据]
date: 2017-03-24 14:39:39 +0800
comments: true
author: onecoder
thread_key: 1906
---

Spring XD on Yarn在使用过程中发现不论是YarnClient还是AppMaster对Yarn HA的支持都不好。在Yarn的RM重启或切换的情况下，YarnClient必须修改配置文件中的RM地址才可以继续使用，即使在配置文件中配置了Yarn HA的相关配置也不生效。而AppMaster同样会因为长时间监测不到心跳而被Yarn Kill掉，导致XD服务挂掉。
因此，此调研的目标实际是为了解决XD on Yarn对RM HA的支持问题。

<!--break-->
 
#  YarnClient问题调研

## Apache YarnClient

官方的YarnClient通过 ClientRMProxy#createRMProxy 来创建底层通信用proxy。而在改函数中，会判断是否开启了Yarn HA。即

```xml
<property>
    <name>yarn.resourcemanager.ha.enabled</name>
    <value>true</value>
</property>
```

```java
/**
 * Create a proxy for the specified protocol. For non-HA,
 * this is a direct connection to the ResourceManager address. When HA is
 * enabled, the proxy handles the failover between the ResourceManagers as
 * well.
 */
@Private
protected static <T> T createRMProxy(final Configuration configuration,
    final Class<T> protocol, RMProxy instance) throws IOException {
  YarnConfiguration conf = (configuration instanceof YarnConfiguration)
      ? (YarnConfiguration) configuration
      : new YarnConfiguration(configuration);
  RetryPolicy retryPolicy = createRetryPolicy(conf);
  if (HAUtil.isHAEnabled(conf)) {
    RMFailoverProxyProvider<T> provider =
        instance.createRMFailoverProxyProvider(conf, protocol);
    return (T) RetryProxy.create(protocol, provider, retryPolicy);
  } else {
    InetSocketAddress rmAddress = instance.getRMAddress(conf, protocol);
    LOG.info("Connecting to ResourceManager at " + rmAddress);
    T proxy = RMProxy.<T>getProxy(conf, protocol, rmAddress);
    return (T) RetryProxy.create(protocol, proxy, retryPolicy);
  }
}
```

如果开启了HA，则会创建一个Proxy的动态代码
RetryInvocationHandler。Client执行具体的任务时，会执行RetryInvocationHandler#invoke方法

```java
@Override
public Object invoke(Object proxy, Method method, Object[] args)
  throws Throwable {
  RetryPolicy policy = methodNameToPolicyMap.get(method.getName());
  if (policy == null) {
    policy = defaultPolicy;
  }
  
  // The number of times this method invocation has been failed over.
  int invocationFailoverCount = 0;
  final boolean isRpc = isRpcInvocation(currentProxy.proxy);
  final int callId = isRpc? Client.nextCallId(): RpcConstants.INVALID_CALL_ID;
  int retries = 0;
  while (true) {
    // The number of times this invocation handler has ever been failed over,
    // before this method invocation attempt. Used to prevent concurrent
    // failed method invocations from triggering multiple failover attempts.
    long invocationAttemptFailoverCount;
    synchronized (proxyProvider) {
      invocationAttemptFailoverCount = proxyProviderFailoverCount;
    }

    if (isRpc) {
      Client.setCallIdAndRetryCount(callId, retries);
    }
    try {
      Object ret = invokeMethod(method, args);
      hasMadeASuccessfulCall = true;
      return ret;
    } catch (Exception e) {
      boolean isIdempotentOrAtMostOnce = proxyProvider.getInterface()
          .getMethod(method.getName(), method.getParameterTypes())
          .isAnnotationPresent(Idempotent.class);
      if (!isIdempotentOrAtMostOnce) {
        isIdempotentOrAtMostOnce = proxyProvider.getInterface()
            .getMethod(method.getName(), method.getParameterTypes())
            .isAnnotationPresent(AtMostOnce.class);
      }
      RetryAction action = policy.shouldRetry(e, retries++,
          invocationFailoverCount, isIdempotentOrAtMostOnce);
      if (action.action == RetryAction.RetryDecision.FAIL) {
        if (action.reason != null) {
          LOG.warn("Exception while invoking " + currentProxy.proxy.getClass()
              + "." + method.getName() + " over " + currentProxy.proxyInfo
              + ". Not retrying because " + action.reason, e);
        }
        throw e;
      } else { // retry or failover
        // avoid logging the failover if this is the first call on this
        // proxy object, and we successfully achieve the failover without
        // any flip-flopping
        boolean worthLogging = 
          !(invocationFailoverCount == 0 && !hasMadeASuccessfulCall);
        worthLogging |= LOG.isDebugEnabled();
        if (action.action == RetryAction.RetryDecision.FAILOVER_AND_RETRY &&
            worthLogging) {
          String msg = "Exception while invoking " + method.getName()
              + " of class " + currentProxy.proxy.getClass().getSimpleName()
              + " over " + currentProxy.proxyInfo;

          if (invocationFailoverCount > 0) {
            msg += " after " + invocationFailoverCount + " fail over attempts"; 
          }
          msg += ". Trying to fail over " + formatSleepMessage(action.delayMillis);
          LOG.info(msg, e);
        } else {
          if(LOG.isDebugEnabled()) {
            LOG.debug("Exception while invoking " + method.getName()
                + " of class " + currentProxy.proxy.getClass().getSimpleName()
                + " over " + currentProxy.proxyInfo + ". Retrying "
                + formatSleepMessage(action.delayMillis), e);
          }
        }
        
        if (action.delayMillis > 0) {
          Thread.sleep(action.delayMillis);
        }
        
        if (action.action == RetryAction.RetryDecision.FAILOVER_AND_RETRY) {
          // Make sure that concurrent failed method invocations only cause a
          // single actual fail over.
          synchronized (proxyProvider) {
            if (invocationAttemptFailoverCount == proxyProviderFailoverCount) {
              proxyProvider.performFailover(currentProxy.proxy);
              proxyProviderFailoverCount++;
            } else {
              LOG.warn("A failover has occurred since the start of this method"
                  + " invocation attempt.");
            }
            currentProxy = proxyProvider.getProxy();
          }
          invocationFailoverCount++;
        }
      }
    }
  }
}
```

在该方法中处理了如果访问失败后会根据配置进行重试处理。具体的FailoverProvider配置在：

```xml
<property>
    <name>yarn.client.failover-proxy-provider</name>
    <value>org.apache.hadoop.yarn.client.ConfiguredRMFailoverProxyProvider</value>
</property>
```

因此官方的YarnClient实际是支持Yarn HA的。
Spring YarnClient
在Spring Hadoop中，底层操作封装在xxTemplate中，在YarnRpcAccessor中，创建底层通信proxy：

```java
@Override
public void afterPropertiesSet() throws Exception {
   Assert.notNull(configuration, "Yarn configuration must be set");
   Assert.notNull(protocolClazz, "Rpc protocol class must be set");
   if (UserGroupInformation.isSecurityEnabled()) {
      UserGroupInformation.setConfiguration(configuration);
   }
   address = getRpcAddress(configuration);
   proxy = createProxy();
}
```

而此处创建的proxy，并没有相关HA逻辑的处理。
修改方案
 
修改YarnRpcAccessor类中，创建proxy的逻辑如下： 

```java
@Override
    public void afterPropertiesSet() throws Exception {
        Assert.notNull(configuration, "Yarn configuration must be set");
        Assert.notNull(protocolClazz, "Rpc protocol class must be set");
        if (UserGroupInformation.isSecurityEnabled()) {
            UserGroupInformation.setConfiguration(configuration);
        }
        address = getRpcAddress(configuration);
//    proxy = createProxy();
        if (protocolClazz.isAssignableFrom(ClientRMProtocols.class)) {
            proxy = ClientRMProxy.createRMProxy(configuration, protocolClazz);
        } else {
            proxy = createProxy();
        }
    }
```

对于Client和AM-RM通信，走原生的ClientRMProxy创建逻辑，对于AM-NM通信，走原Spring逻辑。

## AppMaster HA

AppMaster的高可用，除了需要支持多RM配置和连接重试外，还需要支持在RM重启后，re-register AM。这个同样在Apache原生的AMRMClientAsyncImpl中，有相应处理：

```java
@Override
public AllocateResponse allocate(float progressIndicator) 
    throws YarnException, IOException {
  Preconditions.checkArgument(progressIndicator >= 0,
      "Progress indicator should not be negative");
  AllocateResponse allocateResponse = null;
  List<ResourceRequest> askList = null;
  List<ContainerId> releaseList = null;
  AllocateRequest allocateRequest = null;
  List<String> blacklistToAdd = new ArrayList<String>();
  List<String> blacklistToRemove = new ArrayList<String>();
  
  try {
    synchronized (this) {
      askList = new ArrayList<ResourceRequest>(ask.size());
      for(ResourceRequest r : ask) {
        // create a copy of ResourceRequest as we might change it while the 
        // RPC layer is using it to send info across
        askList.add(ResourceRequest.newInstance(r.getPriority(),
            r.getResourceName(), r.getCapability(), r.getNumContainers(),
            r.getRelaxLocality(), r.getNodeLabelExpression()));
      }
      releaseList = new ArrayList<ContainerId>(release);
      // optimistically clear this collection assuming no RPC failure
      ask.clear();
      release.clear();

      blacklistToAdd.addAll(blacklistAdditions);
      blacklistToRemove.addAll(blacklistRemovals);
      
      ResourceBlacklistRequest blacklistRequest =
          ResourceBlacklistRequest.newInstance(blacklistToAdd,
              blacklistToRemove);
      
      allocateRequest =
          AllocateRequest.newInstance(lastResponseId, progressIndicator,
            askList, releaseList, blacklistRequest);
      // clear blacklistAdditions and blacklistRemovals before 
      // unsynchronized part
      blacklistAdditions.clear();
      blacklistRemovals.clear();
    }

    try {
      allocateResponse = rmClient.allocate(allocateRequest);
    } catch (ApplicationMasterNotRegisteredException e) {
      LOG.warn("ApplicationMaster is out of sync with ResourceManager,"
          + " hence resyncing.");
      synchronized (this) {
        release.addAll(this.pendingRelease);
        blacklistAdditions.addAll(this.blacklistedNodes);
        for (Map<String, TreeMap<Resource, ResourceRequestInfo>> rr : remoteRequestsTable
          .values()) {
          for (Map<Resource, ResourceRequestInfo> capabalities : rr.values()) {
            for (ResourceRequestInfo request : capabalities.values()) {
              addResourceRequestToAsk(request.remoteRequest);
            }
          }
        }
      }
      // re register with RM
      registerApplicationMaster();
      allocateResponse = allocate(progressIndicator);
      return allocateResponse;
    }

    synchronized (this) {
      // update these on successful RPC
      clusterNodeCount = allocateResponse.getNumClusterNodes();
      lastResponseId = allocateResponse.getResponseId();
      clusterAvailableResources = allocateResponse.getAvailableResources();
      if (!allocateResponse.getNMTokens().isEmpty()) {
        populateNMTokens(allocateResponse.getNMTokens());
      }
      if (allocateResponse.getAMRMToken() != null) {
        updateAMRMToken(allocateResponse.getAMRMToken());
      }
      if (!pendingRelease.isEmpty()
          && !allocateResponse.getCompletedContainersStatuses().isEmpty()) {
        removePendingReleaseRequests(allocateResponse
            .getCompletedContainersStatuses());
      }
    }
  } finally {
    // TODO how to differentiate remote yarn exception vs error in rpc
    if(allocateResponse == null) {
      // we hit an exception in allocate()
      // preserve ask and release for next call to allocate()
      synchronized (this) {
        release.addAll(releaseList);
        // requests could have been added or deleted during call to allocate
        // If requests were added/removed then there is nothing to do since
        // the ResourceRequest object in ask would have the actual new value.
        // If ask does not have this ResourceRequest then it was unchanged and
        // so we can add the value back safely.
        // This assumes that there will no concurrent calls to allocate() and
        // so we dont have to worry about ask being changed in the
        // synchronized block at the beginning of this method.
        for(ResourceRequest oldAsk : askList) {
          if(!ask.contains(oldAsk)) {
            ask.add(oldAsk);
          }
        }
        
        blacklistAdditions.addAll(blacklistToAdd);
        blacklistRemovals.addAll(blacklistToRemove);
      }
    }
  }
  return allocateResponse;
}
```

而Spring Hadoop 所使用的AM**Template没有如此逻辑，因此修改如下，在AppmasterRmTemplate中增加如下接口和实现：

```java
@Override
public AllocateResponse allocate(final AllocateRequest request, final String host, final Integer rpcPort, final String trackUrl) {
    return execute(new YarnRpcCallback<AllocateResponse, ApplicationMasterProtocol>() {
        @Override
        public AllocateResponse doInYarn(ApplicationMasterProtocol proxy) throws YarnException, IOException {
            return doAllocate(proxy, request, host, rpcPort, trackUrl);
        }
        
        private AllocateResponse doAllocate(ApplicationMasterProtocol proxy, AllocateRequest request, final String host, final Integer rpcPort, final String trackUrl) throws IOException, YarnException {
            AllocateResponse allocateResponse = null;
            try {
                allocateResponse = proxy.allocate(request);
            } catch (ApplicationMasterNotRegisteredException e) {
                log.warn("ApplicationMaster is out of sync with ResourceManager,"
                                 + " hence resyncing.");
                // re register with RM
                log.info("Re-register am with RM.");
                registerApplicationMaster(host, rpcPort, trackUrl);
                allocateResponse = doAllocate(proxy, request, host, rpcPort, trackUrl);
                return allocateResponse;
            }
            return allocateResponse;
        }
    });
}
```

调用者DefaultContainerAllocator修改：

```java
AppmasterService appmasterClientService = YarnContextUtils.getAppmasterClientService(getBeanFactory());
AppmasterTrackService appmasterTrackService = YarnContextUtils.getAppmasterTrackService(getBeanFactory());
String host = appmasterClientService == null ? "" : appmasterClientService.getHost();
int port = appmasterClientService == null ? 0 : appmasterClientService.getPort();
String trackUrl = appmasterTrackService == null ? null : appmasterTrackService.getTrackUrl();
log.info("Host: " + host + " ,port: " + port + ", trackUrl: " + trackUrl);
AllocateResponse allocate = getRmTemplate().allocate(request, host, port, trackUrl);
```

即可。
重新打包次此spring-yarn-core.jar，替换springxd中的jar，即可实现Yarn的HA支持。

# 配置文件

```yml
# Hadoop properties
spring:
  hadoop:
    fsUri: hdfs://xxx
    resourceManagerHost: xxx
#    resourceManagerHost: yarn-cluster
    resourceManagerPort: 8032
 #   rmAddress: yarn-cluster
#    resourceManagerSchedulerAddress: ${spring.hadoop.resourceManagerHost}:8030
 #   jobHistoryAddress: xxx
 
 ## For phd30 only (values for version 3.0.1.0, also change resourceManagerPort above to 8050)
#    config:
#      mapreduce.application.framework.path: '/phd/apps/3.0.1.0-1/mapreduce/mapreduce.tar.gz#mr-framework'
#      mapreduce.application.classpath: '$PWD/mr-framework/hadoop/share/hadoop/mapreduce/*:$PWD/mr-framework/hadoop/share/hadoop/mapreduce/lib/*:$PWD/mr-framework/hadoop/share/hadoop/common/*:$PWD/mr-framework/hadoop/share/hadoop/common/lib/*:$PWD/mr-framework/hadoop/share/hadoop/yarn/*:$PWD/mr-framework/hadoop/share/hadoop/yarn/lib/*:$PWD/mr-framework/hadoop/share/hadoop/hdfs/*:$PWD/mr-framework/hadoop/share/hadoop/hdfs/lib/*:/usr/phd/3.0.1.0-1/hadoop/lib/hadoop-lzo-0.6.0.3.0.1.0-1.jar:/etc/hadoop/conf/secure'
## For hdp22 only (values for version 2.2.8.0, also change resourceManagerPort above to 8050)
    config:
      mapreduce.application.framework.path: ${spring.yarn.config.mapreduce.application.framework.path}
      mapreduce.application.classpath: ${spring.yarn.config.mapreduce.application.classpath}
      net.topology.script.file.name: /etc/hadoop/conf/topology_script.py
      dfs.namenode.rpc-address: xxx.xxx.xxx.xxx:8020
      dfs.nameservices: xxx
      dfs.ha.namenodes.xxx: nn1,nn2
      dfs.namenode.rpc-address.xxx.nn1: xxx.xxx.xxx.xxx:8020
      dfs.namenode.rpc-address.xxx.nn2: xxx.xxx.xxx.xxx:8020
      dfs.client.failover.proxy.provider.xxx: org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider
      yarn.resourcemanager.ha.enabled: true
      yarn.resourcemanager.ha.rm-ids: rm1,rm2
      yarn.resourcemanager.cluster-id: yarn-cluster
      yarn.resourcemanager.address.rm1: xxx.xxx.xxx.xxx
      yarn.resourcemanager.scheduler.address.rm1: xxx.xxx.xxx.xxx:8030
      yarn.resourcemanager.admin.address.rm1: xxx.xxx.xxx.xxx:8033
      yarn.resourcemanager.webapp.address.rm1: xxx.xxx.xxx.xxx:8088
      yarn.resource.resource-tracker.address.rm1: xxx.xxx.xxx.xxx:8031
      yarn.resourcemanager.address.rm2: xxx.xxx.xxx.xxx
      yarn.resourcemanager.scheduler.address.rm2: xxx.xxx.xxx.xxx:8030
      yarn.resourcemanager.admin.address.rm2: xxx.xxx.xxx.xxx:8033
      yarn.resourcemanager.webapp.address.rm2: xxx.xxx.xxx.xxx:8088
      yarn.resource.resource-tracker.address.rm2: xxx.xxx.xxx.xxx:8031
      yarn.resourcemanager.zk-address: xxx.xxx.xxx.xxx:2181,xxx.xxx.xxx.xxx:2181,xxx.xxx.xxx.xxx:2181
      yarn.resourcemanager.recovery.enabled: true
```

需要在Spring->hadoop->config 下，增加yarn高可用相关配置。
