---
layout: post
title: Elasticsearch 集群部署说明
tags: [Elasticsearch]
categories: [大数据]
date: 2016-08-15 17:29:49 +0800
comments: true
thread_key: 1897
---
记录Elasticsearch集群搭建的过程。

<!--break-->

# 安装JDK 8

官方推荐的版本是1.8.0_73 以上。因此首先安装jdk。安装之前下载的jdk-8u77版

```bash
rpm -i jdk-8u77-linux-x64.rpm
```

# 安装ElasticSearch

下载安装包

```bash
curl -L -O https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.5/elasticsearch-2.3.5.tar.gz
```

解压

```bash
tar -xvf elasticsearch-2.3.5.tar.gz
```

修改**config/elasticsearch.yml**配置文件

```yml
cluster.name: es-dps-cluster
#节点名
node.name: es-node4
network.host: ip
discovery.zen.ping.multicast.enabled: false
discovery.zen.ping.unicast.hosts：["10.200.48.17","10.200.48.18","10.200.48.19","10.200.48.20"]
```

## 启动

```bash
cd elasticsearch-2.3.5/bin
ES_JAVA_OPTS="-Xms10g -Xmx10g" nohup ./elasticsearch >/dev/null 2>&1 &
```

注意，不能以root身份启动。

## 验证部署

```bash
curl 'localhost:9200/_cat/health?v'
curl 'localhost:9200/_cat/nodes?v'
```

![](/images/post/setup-es-cluster/curl-cluster-info.png)

# 安装elasticsearch-head 监控插件

```bash
plugin install mobz/elasticsearch-head
```