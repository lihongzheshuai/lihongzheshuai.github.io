---
layout: post
title: 事无巨细 Apache Kafka 0.9.0.1 集群环境搭建
tags: [kafka]
date: 2016-04-29 09:30:57 +0800
comments: true
thread_key: 1892
---
**Kafka**集群环境依赖于**Zookeeper**环境。因此我们的环境搭建实际分为两部分。**Zookeeper**环境搭建和**Kafka**环境搭建。

<!--break-->

### Zookeeper 3.4.8集群搭建

#### 部署安装包

下载

```bash
wget http://mirrors.cnnic.cn/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz
```

解压

```bash
tar -xvzf zookeeper-3.4.8.tar.gz -C ~/
```

#### 配置Zookeeper

按照理解，应该只需制定**Zookeeper**集群的节点信息即可。老套路，拷贝配置文件模版

```bash
cp conf/zoo_sample.cfg conf/zoo.cfg
```

配置集群信息

```bash
vim conf/zoo.cfg
```

修改内容如下

```
server.14=master:2888:3888
server.15=slave15:2888:3888
server.16=slave16:2888:3888
```

拷贝到其他节点

```bash
scp -r zookeeper-3.4.8/ slave15:~/
scp -r zookeeper-3.4.8/ slave16:~/
```

#### 启动Zookeeper

在集群的每个节点上执行

```bash
bin/zkServer.sh start
```

通过查看日志发现启动失败，异常信息：

> Caused by: java.lang.IllegalArgumentException: /home/dps-hadoop/zookeeper-3.4.8/data/myid file is missing
        at org.apache.zookeeper.server.quorum.QuorumPeerConfig.parseProperties(QuorumPeerConfig.java:341)
        at org.apache.zookeeper.server.quorum.QuorumPeerConfig.parse(QuorumPeerConfig.java:119)
        ... 2 more

缺少**myid**标识文件，即一个给节点标识的文件。解决方案，在每个创建该文件并写入该节点标识即可。例如，主节点上：

```bash
echo 14 > /home/dps-hadoop/zookeeper-3.4.8/data/myid
```

注意，这里的myid编号，要跟**zoo.cfg**里配置的**server.${myid}**匹配，否则会报错：

> java.lang.RuntimeException: My id xx not in the peer list

### Kafka集群搭建

#### 下载安装包

```bash
wget http://mirrors.cnnic.cn/apache/kafka/0.9.0.1/kafka_2.11-0.9.0.1.tgz
```

解压

```bash
tar -xvf kafka_2.11-0.9.0.1.tgz -C ~/
```

#### 配置Kafka

按照理解，应该需要配置**zookeeper**的地址即可。修改**server.properties**配置文件

```bash
vim config/server.properties
```

修改内容如下

```
broker.id=14
log.dirs=/home/dps-hadoop/logs/kafka-logs
zookeeper.connect=master:2181,slave15:2181,slave16:2181
```

拷贝到其他节点，在其他节点上对应修改**broker.id**即可。

```bash
scp -r kafka_2.11-0.9.0.1/ slave15:~/
scp -r kafka_2.11-0.9.0.1/ slave16:~/
```

#### 启动Kafka

在每个节点上执行

```bash
bin/kafka-server-start.sh -daemon config/server.properties
```

#### 验证安装

***创建一个topic***

```bash
bin/kafka-topics.sh --create --zookeeper master:2181,slave15:2181,slave16:2181 --replication-factor 3 --partitions 1 --topic dps-kafka-test-topic
```

***查看集群状态***

```bash
bin/kafka-topics.sh --describe --zookeeper master:2181,slave15:2181,slave16:2181 --topic dps-kafka-test-topic
```

![](/images/post/setup-kafka-cluster/cluster-info.png)

可见，此时**15**节点被选为**Leader**，**topic**有三个备份分别在我集群的3个节点上。

***生产消息***

```bash
bin/kafka-console-producer.sh --broker-list master:9092,slave15:9092,slave16:9092 --topic dps-kafka-test-topic
```

```
...
message one
;
message tow
^C
```

***消费消息***

```bash
bin/kafka-console-consumer.sh --zookeeper master:2181,slave15:2181,slave16:2181 --from-beginning --topic dps-kafka-test-topic
```

![](/images/post/setup-kafka-cluster/consume-message.png)

一切ok。高可用的测试，这里就不做了。可参考官方文档。

- <a href="http://kafka.apache.org/documentation.html#quickstart" target="\_blank">http://kafka.apache.org/documentation.html#quickstart</a> 