---
layout: post
title: 事无巨细 Hive1.2.1 Hiveserver搭建详解
tags: [Hive]
date: 2016-04-27 19:30:18 +0800
comments: true
thread_key: 1891
---

上文介绍**了Hadoop2.6.4**集群搭建的详细步骤。现在我们在此基础上，搭建**Hiveserver**。同样，事无巨细，难免跑题。
<!--break-->

### 环境需求列表

- **Hive1.2**版本开始，依赖**Java1.7+**，**0.14-1.1**版本依赖**Java1.6+**。推荐用**Java1.8**
- 推荐使用**Hadoop2.x** 系列。**Hive2.0**开始不再支持**Hadoop1.x**系列。**0.13**版之前的**Hive**也仍支持**Hadoop0.20.x**和**0.23.x**系列。
- 在生产环境下推荐使用**Linux**或**Windows**系统。**Mac**系统仅推荐在试验环境使用。

### 下载安装Hive

从镜像列表<a href="http://www.apache.org/mirrors/" target="\_blank">http://www.apache.org/mirrors</a> 找个速度快的国内镜像。

#### 下载Hive安装包

```bash
wget http://mirrors.cnnic.cn/apache/hive/hive-1.2.1/apache-hive-1.2.1-bin.tar.gz
```

解压到当前用户目录下(我的安装包都下载在用户的download的目录下。)

```bash
tar -xzvf apache-hive-1.2.1-bin.tar.gz -C ~/
```

强迫症，改个和**Hadoop**统一的名字。

```bash
mv apache-hive-1.2.1-bin/ hive-1.2.1
```

#### 设置环境变量

需要配置**HIVE_HOME**和**HIVE_BIN**

```bash
vim ~/.bashrc
```

修改内容如下：

```bash
export HIVE_HOME=$HOME/hive-1.2.1
export PATH=$PATH:$HOME/bin:$HIVE_HOME/binsour
```

立即生效

```bash
source ~/.bashrc
```

### Metadata Store MySQL安装

Hive有三种元数据存储的模式。

- Embedded mode
- Local mode
- Remote mode

很多文章里都有介绍，但是很少有人具体解释其区别和原理。OneCoder很不满意，这里找到一篇介绍，至少对我来说，算是能看懂他所介绍的。
<a href="http://www.cloudera.com/documentation/enterprise/5-2-x/topics/cdh_ig_hive_metastore_configure.html#topic_18_4_1" target="\_blank">Metastore Deployment Modes</a>


这里采用**Remote mode**。因此我们先要部署**MySQL**。

#### 安装MySQL5.7.12

下载

```bash
wget http://cdn.mysql.com//Downloads/MySQL-5.7/mysql-community-server-5.7.12-1.el6.x86_64.rpm
```

安装

```bash
sudo rpm -i mysql-community-server-5.7.12-1.el6.x86_64.rpm
```

发现缺少依赖

```
mysql-community-common-5.7.12、mysql-community-client-5.7.12和mysql-community-libs-5.7.12
```

下载依赖：

```bash
wget http://repo.mysql.com/yum/mysql-5.7-community/el/6/x86_64/mysql-community-common-5.7.12-1.el6.x86_64.rpm
wget http://repo.mysql.com/yum/mysql-5.7-community/el/6/x86_64/mysql-community-client-5.7.12-1.el6.x86_64.rpm
wget http://repo.mysql.com/yum/mysql-5.7-community/el/6/x86_64/mysql-community-libs-5.7.12-1.el6.x86_64.rpm
```

赋予可执行权限

```bash
chmod 700 mysql-community-*
```

安装依赖

```bash
sudo rpm -i mysql-community-libs-5.7.12-1.el6.x86_64.rpm
sudo rpm -i mysql-community-common-5.7.12-1.el6.x86_64.rpm
sudo rpm -i mysql-community-client-5.7.12-1.el6.x86_64.rpm
```

安装MySQL

```bash
sudo rpm -i mysql-community-server-5.7.12-1.el6.x86_64.rpm
```

创建自己的MySQL数据目录，在当前用户的主目录下执行

```bash
mkdir -p metastore-mysql/data
mkdir -p metastore-mysql/logs
```

赋予权限，由于**mysql**实际是使用**mysql**用户启动服务。而我们的数据目录改在了**dps-hadoop**用户的根目录下，所以得从根上，给**mysql**用户以**RX**权限

```bash
sudo chmod -R 755 /home/dps-hadoop
```

修改my.cnf配置文件

```bash
vim /etc/my.cnf
```

内容如下

```
[mysqld]
datadir=/home/dps-hadoop/metastore-mysql/data
socket=/home/dps-hadoop/metastore-mysql/data/mysql.sock
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
[mysqld_safe]
socket=/home/dps-hadoop/metastore-mysql/data/mysql.sock
log-error=/home/dps-hadoop/mysqllog/mysqld.log
pid-file=/home/dps-hadoop/metastore-mysql/data/mysqld.pid
[mysql]
socket=/home/dps-hadoop/metastore-mysql/data/mysql.sock
[mysqladmin]
socket=/home/dps-hadoop/metastore-mysql/data/mysql.sock
datadir=/home/dps-hadoop/metastore-mysql/data
socket=/home/dps-hadoop/metastore-mysql/data/mysql.sock
log-error=/home/dps-hadoop/mysqllog/mysqld.log
```

其中**log-error**对应的路径需要提前创建，而**datadir**路径会自动创建。

关闭**Selinux**，否则会因为无法创建数据目录而报错。

```bash
setenforce 0
```

启动mysql

```bash
sudo service mysqld start
```

在启动日志里会发现**root**用户的临时密码：
**qkkmgd.Np0?N** 登录后修改密码即可。

```bash
mysql -u root -p
```

创建数据库hive

```bash
mysql> create database hive;
```

创建hive用户并授权

```bash
mysql> grant all on hive.* to hive@'%'  identified by '密码';
```

### 配置Hive

**Hive**在**conf**目录下提供了一个配置文件模版**hive-default.xml.template**供我们修改。而**Hive**会默认加载**hive-site.xml**配置文件。因此，拷贝一份。

```bash
cp conf/hive-default.xml.template conf/hive-site.xml
```

同样，按照了解，我们需要配置**metastore**的相关信息，如数据库连接，驱动，用户名，密码等。

```xml
<property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hive</value>
    <description>Username to use against metastore database</description>
  </property>
<property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>数据库密码</value>
    <description>password to use against metastore database</description>
  </property>
<property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://master:3306/hive?createDatabaseIfNotExist=true&amp;useSSL=false;</value>
    <description>JDBC connect string for a JDBC metastore</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.jdbc.Driver</value>
    <description>Driver class name for a JDBC metastore</description>
  </property>
<property>
    <name>hive.metastore.uris</name>
    <value>thrift://master:9083</value>
    <description>Thrift URI for the remote metastore. Used by metastore client to connect to remote metastore.</description>
  </property>
```

这里，**metastore**服务的默认端口为**9083**。

还需要配置本地数据仓库路径

```xml
<property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/home/dps-hadoop/warehouse</value>
    <description>location of default database for the warehouse</description>
  </property>
```

由于我们需要连接**MySQL**数据库，而**Hive**并没有提供相应的驱动，所以需要下载**MySQL JDBC**驱动，并放在**Hive**的**lib**目录下。直接进入**lib**目录执行

```bash
wget http://central.maven.org/maven2/mysql/mysql-connector-java/5.1.38/mysql-connector-java-5.1.38.jar
```

#### 修改log日志文件位置

**Hive**默认将日志**存放在/tmp/${user.name}**下。为了方便维护和查看，修改日志文件位置。

```bash
cp conf/hive-log4j.properties.template conf/hive-log4j.properties
```

修改

```
hive.log.dir=/home/dps-hadoop/logs/hive
```

### 启动HiveServer服务

启动MetaStore Service

```bash
bin/hive --service metastore &
```

启动HiveServer

```bash
bin/hive --service hiveserver2 &
```

查看日志一切正常。

#### 验证Hive客户端

```bash
bin/hive
```

发现报错

> Exception in thread "main" java.lang.IncompatibleClassChangeError: Found class jline.Terminal, but interface was expected

这是由于**jline**的版本冲突，在**hadoop**的**lib**带的版本低。解决办法，修改**hive-env.sh**

```bash
vim conf/hive-env.sh
```

添加

```bash
export HADOOP_USER_CLASSPATH_FIRST=true
```

即用**hive**里的高版本覆盖**Hadoop**里的低版本。

再次启动客户端，一切OK。通过**beeline**客户端验证也ok。至此**Hiveserver2**部署完成。