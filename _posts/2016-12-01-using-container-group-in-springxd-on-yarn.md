---
layout: post
title: SpringXD on yarn 使用Container工作组
tags: [Spring]
categories: [Java技术研究]
date: 2016-12-01 15:56:57 +0800
comments: true
author: onecoder
thread_key: 1905
---
SpringXD on Yarn支持Container分组。可以更好的控制admin和container分配。

* 控制组内成员
* 以组单位整体控制生命周期
* 动态创建组
* 重启失败的容器

<!--break-->

实际上，XD on Yarn有内置分组admin和container。结合例子使用：

**查看分组列表：**

```bash
bin/xd-yarn clustersinfo -a application_1472450074786_0160
  CLUSTER ID
  ----------
  container
  admin
```

**创建新的分组**

```bash
bin/xd-yarn clustercreate -a application_1472450074786_0160 -c lihongzhe -i container-nolocality-template -p default -w 2
Cluster lihongzhe created.
```

**查看分组列表**

```bash
bin/xd-yarn clustersinfo -a application_1472450074786_0160
  CLUSTER ID
  ----------
  container
  lihongzhe
  admin
```

**启动分组**

```bash
bin/xd-yarn clusterstart -a application_1472450074786_0160 -c lihongzhe
```

**查看分组状态**

```bash
bin/xd-yarn clusterinfo -a application_1472450074786_0160 -c lihongzhe -v
  CLUSTER STATE  MEMBER COUNT  ANY PROJECTION  HOSTS PROJECTION  RACKS PROJECTION  ANY SATISFY  HOSTS SATISFY  RACKS SATISFY
  -------------  ------------  --------------  ----------------  ----------------  -----------  -------------  -------------
  RUNNING        2             2               {}                {}                0            {}             {}
```

可见，启动后，分组变成RUNNING态。此时Yarn上会新启动Container（原来是6）。

![](/images/post/xd-on-yarn-groups/yarn-rm-containers-8.png)

XD的Container也会随之启动

![](/images/post/xd-on-yarn-groups/xd-container-list.png)


进一步，体验向yarn申请指定资源的container，并将job部署到指定的container上执行，达到资源的动态控制。

**1、配置资源申请模板**

xd中，container默认申请内存为512MB，这里修改server.yml配置文件，改成256MB

```yaml
xd:
  appmasterMemory: 512M
  adminServers: 1
  adminMemory: 512M
  adminJavaOpts: -XX:MaxPermSize=128m
  adminLocality: false
  containers: 3
  containerMemory: 256M
  containerJavaOpts: -XX:MaxPermSize=128m
  containerLocality: false
```

push并submit新版本

```bash
bin/xd-yarn push
bin/xd-yarn submmit
```

再次创建并启动名为lihongzhe-256的分组，包含一个容器

```bash
bin/xd-yarn clustercreate -a application_1472450074786_0186 -c lihongzhe-256 -i container-nolocality-template -p default -w 1 -g lihongzhe-256
bin/xd-yarn clusterstart -a application_1472450074786_0186 -c lihongzhe-256
```

从yarn上查看新创建的容器状态

![](/images/post/xd-on-yarn-groups/yarn-container-info.png)

可见确实申请了256MB大小的container。

xd admin-ui上来看

![](/images/post/xd-on-yarn-groups/xd-container-groups.png)

然后通过指定groupid将任务部署到该container上去

```bash
xd:>job deploy --name jobsleepend --properties "module.sleepend.criteria=groups.equals('lihongzhe-256')"
```

job跑在了指定的container上。

![](/images/post/xd-on-yarn-groups/deploy-to-groups.png)