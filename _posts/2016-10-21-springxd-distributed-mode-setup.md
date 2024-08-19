---
layout: post
title: SpringXD分布式模式部署
tags: [Spring]
categories: [Java技术研究]
date: 2016-10-21 15:11:51 +0800
comments: true
author: onecoder
thread_key: 1901
---
Spring XD有两种运行模式：单机和分布式模式。这里关注分布式模式的部署和运行时特点。

<!--break-->

# 分布式集群组件

Spring XD分布式环境包含以下组件：

- Admin 管理节点。管理Stream和Job的配置和发布，提供REST接口等。
- Container 运行流式任何和批量任务的节点，部署在独立的主机上。
- Zookeeper 管理XD集群的运行时环境
- Spring Batch Job 数据库，存储Spring Batch需要的数据信息。
- 消息中间件 - XD支持Rabbit MQ和Redis做流式处理和任务处理是的消息载体。Kafka目前仅可用于流式处理。
- 分析仓库 - XD使用Redis来存储统计分析数据。

# 部署

## 安装JDK

Spring XD基于Java编写，需要JDK 7以上的运行时环境。具体部署略。

## 下载解压Spring XD 1.3.1-RELEASE

当前最近版为1.3.1，下载并解压。

```bash
wget http://repo.spring.io/libs-release/org/springframework/xd/spring-xd/1.3.1.RELEASE/spring-xd-1.3.1.RELEASE-dist.zip
tar
unzip spring-xd-1.3.1.RELEASE-dist.zip -d /data
```

## 配置关系型数据库

上面提到XD依赖于一个关系型数据库来作为其底层依赖的Spring Batch的支撑库。这么我们使用MySQL，部署MySQL的过程不再赘述，重点关注XD中关于db的配置部分。

修改xd/config/servers.yml配置文件中，spring:datasource中MySQL样例部分。同时，需要将mysql jdbc驱动的jar包放置到lib文件夹下

```yaml
#Config for use with MySQL - uncomment and edit with relevant values for your environment
spring:
  datasource:
    url: jdbc:mysql://10.200.48.:3306/xd
    username: yourUsername
    password: yourPassword
    driverClassName: com.mysql.jdbc.Driver
    validationQuery: select 1
```

配置spring:batch，启用数据库初始化

```yaml
spring:
  batch:
# Configure other Spring Batch repository values.  Most are typically not needed
#    isolationLevel: ISOLATION_READ_COMMITTED
#    clobType:
#    dbType:
#    maxVarcharLength: 2500
#    tablePrefix: BATCH_
#    validateTransactionState: true
    initializer:
       enabled: true
```

## 配置Zookeeper

Spring XD兼容 3.4.6版本的zookeeper。  如果没有部署zookeeper你需要先部署zookeeper，因为spring XD没有内嵌Zookeeper，在笔者是实验环境中，有事前部署好的zookeeper实例。因此此处主要配置spring xd跟zookeeper的连接等信息即可。同样修改server.yml

```yaml
# Zookeeper properties
# namespace is the path under the root where XD's top level nodes will be created
# client connect string: host1:port1,host2:port2,...,hostN:portN
zk:
  namespace: xd
  client:
     connect: 10.200.48.66:2181,10.200.48.67:2181,10.200.48.68:2181
```

## 配置Kafka

Spring XD消息传递需要载体，根据文档可选择redis、rabbitMQ和kafka。不过kafka仅支持实时数据处理。不过笔者还是决定直接使用集群中已有的kafka作为消息中间件，因为也想顺便弄清楚到底哪里使用了这些消息载体。配置kafka：

```yaml
xd:
  transport: kafka
  messagebus:
   kafka:
      brokers:                                 10.200.48.69:9092,10.200.48.70:9092,10.200.48.71:9092
      zkAddress:                               10.200.48.66:2181,10.200.48.67:2181,10.200.48.68:2181
```

## 配置Redis
虽然我们不适用Redis做消息传递的载体，但是Spring XD还需要使用Redis来存储分析数据。虽然Spring XD在其安装包中附带了Redis的安装包，不过我们还是考虑使用独立部署的Redis服务：

```yaml
spring:
  redis:
   port: 6379
   host: 10.200.48.126
```

## 启动Spring XD admin

在admin节点，执行

```bash
xd/bin/xd-admin
```

在container节点，执行命令

```bash
xd/bin/xd-container
```

启动服务。
web-ui默认端口为9393。
例如：http://10.200.48.123:9393/admin-ui

至此，springxd启动完成。