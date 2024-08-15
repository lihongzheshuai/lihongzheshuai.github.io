---
layout: post
title: SpirngXD on YARN模式部署说明
tags: [SpringXD]
date: 2016-11-01 10:39:42 +0800
comments: true
author: onecoder
thread_key: 1902
---
Spring XD可以on yarn运行。

下载on yarn运行包并解压

```bash
wget http://repo.spring.io/release/org/springframework/xd/spring-xd/1.3.1.RELEASE/spring-xd-1.3.1.RELEASE-yarn.zip
unzip spring-xd-1.3.1.RELEASE-yarn.zip
```

## 部署本地Hadoop环境

要on yarn运行需要依赖本地的Hadoop环境。下载Hadoop安装包并解压。笔者试验环境中已经提供了针对Hadoop的自动化配置脚本，这里不再赘述。

## xd on yarn配置

修改**servers.yml**配置文件，配置**siteYarnAppClasspath**和**siteMapreduceAppClasspath**

```yaml
spring:
  yarn:
    siteYarnAppClasspath: "$HADOOP_HOME/etc/hahoop,$HADOOP_HOME/share/hadoop/common/*,$HADOOP_HOME/share/hadoop/common/lib/*,$HADOOP_HOME/share/hadoop/hdfs/*,$HADOOP_HOME/share/hadoop/hdfs/lib/*,$HADOOP_HOME/share/hadoop/yarn/*,$HADOOP_HOME/share/hadoop/yarn/lib/*"
    siteMapreduceAppClasspath: "$HADOOP_HOME/share/hadoop/mapreduce/*,$HADOOP_HOME/share/hadoop/mapreduce/lib/*"
```

## 配置xd相关选项

可配置在yarn上运行几个admin几个container等，这里采用默认配置：

```yaml
xd:
  appmasterMemory: 512M
  adminServers: 1
  adminMemory: 512M
  adminJavaOpts: -XX:MaxPermSize=128m
  adminLocality: false
  containers: 3
  containerMemory: 512M
  containerJavaOpts: -XX:MaxPermSize=128m
  containerLocality: false
```

## 配置yarn环境地址

```yaml
spring:
  hadoop:
    fsUri: hdfs://10.200.48.52:8020
    resourceManagerHost: 10.200.48.52
    resourceManagerPort: 8032
```

## 配置Zookeeper地址：

```yaml
zk:
  namespace: xdonyarn
  client:
    connect: 10.200.48.66:2181,10.200.48.67:2181,10.200.48.68:2181
```

与分布式环境相同，配置redis，jdbc等信息，这里略过。

## 部署到yarn

```bash
bin/xd-yarn push
```

**列出已安装的应用**

```bash
bin/xd-yarn pushed
  NAME  PATH
  ----  --------------------
  app   hdfs://node1:8020/xd
```

**启动应用**

```bash
bin/xd-yarn submit
```

**查看状态信息**

```bash
bin/xd-yarn submitted
  APPLICATION ID                  USER  NAME       QUEUE    TYPE  STARTTIME         FINISHTIME  STATE    FINALSTATUS  ORIGINAL TRACKING URL
  ------------------------------  ----  ---------  -------  ----  ----------------  ----------  -------  -----------  -------------------------
  application_1472450074786_0046  rc    spring-xd  default  XD    10/28/16 2:46 PM  N/A         RUNNING  UNDEFINED    http://10.200.48.54:46604
```

**查看admin-ui地址**

```bash
bin/xd-yarn admininfo
Admins: [http://10.200.48.55:47832]
```

**通过浏览器访问**

用浏览器打开地址http://10.200.48.55:47832/admin-ui
即可访问到springxd的ui界面。至此，部署完成。

## 通过xd-shell连接到管理节点

```bash
bin/xd-shell
```
然后在xd-shell下执行

```bash
xd:>admin config server --uri http://10.200.48.55:47832
Successfully targeted http://10.200.48.55:47832
```

即可像分布式模式一样执行操作。
