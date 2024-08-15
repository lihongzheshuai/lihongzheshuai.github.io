---
layout: post
title: 事无巨细 HBase-1.2.1 集群搭建
tags: [HBase]
date: 2016-04-29 11:12:57 +0800
comments: true
thread_key: 1894
---
继续搭建**HBase**集群环境。**HBase**版本也比较杂，目前也有两大稳定的分支，**1.1.x**和**1.2.x**。从官方文档了解到，支持**Hadoop2.6.1+**对应版本应该是**1.2.x**系列，因此这里选择**1.2.1**稳定版。**1.1.x**在**Hadoop 2.6.1+**上是***未测试***的。

<!--break-->

### 下载HBase

同样，通过镜像站下载

```bash
wget http://mirrors.cnnic.cn/apache/hbase/1.2.1/hbase-1.2.1-bin.tar.gz
```

解压

```bash
tar -xvzf hbase-1.2.1-bin.tar.gz -C ~/
```

配置环境变量

```bash
vim ~/.bashrc
```

内容

```bash
export HBASE_HOME=$HOME/hbase-1.2.1
export $PATH:$HBASE_HOME/bin
```

### 配置HBase

**HBase**依赖于**Zookeeper**环境，之前在搭建**Kakfa**集群的时候已经配置好了**Zookeeper**集群。直接配置。因为是集群模式，还需要制定**RegionServer**节点主机名；因为要使用主备**Master**，因此需要制定主备**Master**节点信息；**HBase**依赖于**HDFS**存储数据，因此需要配置**HDFS**的路径。那么配置如下。

#### 配置**hbase-site.xml**

```bash
vim conf/hbase-site.xml
```

内容如下

```xml
<property>
    <name>hbase.rootdir</name>
    <value>hdfs://master:54000/hbase</value>
  </property>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>
    <property>
<name>hbase.zookeeper.quorum</name>
<value>master:2181,slave15:2181,slave16:2181</value>
</property>
```

这里的**54000**是我们之前**HDFS**集群配置的端口号

#### 配置主备Master

**backup-masters**配置文件默认不存在

```xml
vim conf/backup-masters
```

内容

```
slave15
```

#### 配置regionservers

```bash
vim conf/regionervers
```

内容

```
slave15
slave16
```

#### 配置hbase-env.sh

修改**HBase**配置，修改对内存，不用**HBase**管理**Zookeeper**集群等

```bash
vim conf/hbase-env.sh
```

内容

```bash
export HBASE_HEAPSIZE=4G
export HBASE_MANAGES_ZK=false
```

安装文件拷贝到其他节点

```bash
scp -r hbase-1.2.1/ slave15:~/
scp -r hbase-1.2.1/ slave16:~/
```

### 启动HBase

主节点执行

```bash
bin/start-hbase.sh
```

### 验证安装

通过Web UI查看即可。默认地址
http://master:16010/master-status

![](/images/post/setup-hbase-cluster/hbase-web-ui.png)