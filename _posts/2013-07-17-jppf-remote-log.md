---
layout: post
title: JPPF-log4j远程日志管理
date: 2013-07-17 20:43 +0800
author: onecoder
comments: true
tags: [JPPF]
categories: [Java技术研究,JPPF]
thread_key: 1476
---
<p>
	利用JPPF进行并行计算，计算任务运行在远端节点上，那么如何收集运行在远端的任务日志，用于跟踪和分析呢？</p>
<p>
	JPPF框架对此也有封装，主要的实现思路是，通过自定义实现一个log4j的appender，对外提供JMX服务。客户端（监控端）实现一个监听器，监听远端日志，这样即可把远端日志采集到本地进行统一的管理。这对于我们收集和管理并行计算实时日志是非常有用的。具体看一下：</p>
<p>
	在没个执行任务的Node节点，修改log4j的配置，启用jppf提供的JmxAppender：<br />
	log4j-node.properties</p>

```properties
log4j.appender.JMX=org.jppf.logging.log4j.JmxAppender
log4j.appender.JMX.layout=org.apache.log4j.PatternLayout
log4j.appender.JMX.layout.ConversionPattern=%d [%-5p][%c.%M(%L)]: %m\n

### set log levels - for more verbose logging change &#39;info&#39; to &#39;debug&#39; ###
#log4j.rootLogger=DEBUG, JPPF
log4j.rootLogger=INFO, JPPF, JMX
```

<p>
	客户端代码如下：</p>

```java
/**
* @author lihzh
* @alia OneCoder
* @blog http://www.coderli.com
* @date 2013年7月17日 上午10:34:44
*/
public class RemoteLog {
     public static void main(String args[]) throws Exception {
            // get a JMX connection to the node MBean server
           JMXNodeConnectionWrapper jmxNode = new JMXNodeConnectionWrapper("localhost" ,
                     12001);
           jmxNode.connectAndWait(500000L);
            // get a proxy to the MBean
           JmxLogger nodeProxy = jmxNode.getProxy(JmxLogger.DEFAULT_MBEAN_NAME ,
                     JmxLogger. class);
            // use a handback object so we know where the log messages come from
           String source = "node   " + jmxNode.getHost() + ":" + jmxNode.getPort();
            // subbscribe to all notifications from the MBean
           NotificationListener listener = new MyLoggingHandler();
           nodeProxy.addNotificationListener(listener, null, source);
           String source167 = "node   " + jmxNode167.getHost() + ":" + jmxNode167.getPort();
     }
}

public class MyLoggingHandler implements NotificationListener {
            // handle the logging notifications
            public void handleNotification(Notification notification,
                     Object handback) {
                String message = notification.getMessage();
                String toDisplay = handback.toString() + ": " + message;
                System. out.println(toDisplay);
           }
     }
```

<p>
	简单介绍下，就是通过ip和端口与需要监听的node节点建立jmx链接，然后讲自己事先的监听处理类MyLoggingHandler实例，注册到nodeProxy上。这样如果node端有日志出现，就会通知到监听端，可以进行自己的分类处理。试验一下，启动JPPF环境和启动监听，运行之前介绍的JPPF任务，可以看到在本地成功打印出任务日志信息,这样，并行计算任务分节点的日志收集处理也就很容易实现了。</p>

