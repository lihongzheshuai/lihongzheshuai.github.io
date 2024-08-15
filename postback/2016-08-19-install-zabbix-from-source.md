---
layout: post
title: Zabbix源码编译安装
tags: [Zabbix]
date: 2016-08-19 13:36:24 +0800
comments: true
author: onecoder
thread_key: 1898
---

Zabbix 源码编译部署说明。

<!--break-->

# 源码编译

## 源码下载

```bash
wget http://jaist.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/3.0.4/zabbix-3.0.4.tar.gz
tar -xzvf zabbix-3.0.4.tar.gz
```

## 创建zabbix用户

```bash
groupadd zabbix
useradd -g zabbix zabbix
```

## 安装MySQL

zabbix-server需要数据库

```bash
wget http://repo.mysql.com//mysql57-community-release-el7-8.noarch.rpm
rpm -Uvh mysql57-community-release-el7-8.noarch.rpm
yum install mysql-community-server
```

配置数据存放目录，修改**/ete/my.cnf**

```properties
[mysqld]
datadir=/data/mysql/data
socket=/data/mysql/data/mysql.sock
symbolic-links=0
log-error=/data/mysql/mysqld.log
[mysqld_safe]
socket=/data/mysql/data/mysql.sock
log-error=/data/mysql/mysqld_safe.log
pid-file=/data/mysql/data/mysqld.pid
[mysql]
socket=/data/mysql/data/mysql.sock
[mysqladmin]
socket=/data/mysql/data/mysql.sock
```

## 初始化zabbix mysql数据库

```bash
shell> mysql -uroot -p<password>
mysql> create database zabbix character set utf8 collate utf8_bin;
mysql> grant all privileges on zabbix.* to zabbix@localhost identified by '<password>';
mysql> quit;
shell> cd database/mysql
shell> mysql -uzabbix -p<password> zabbix < schema.sql
shell> mysql -uzabbix -p<password> zabbix < images.sql
shell> mysql -uzabbix -p<password> zabbix < data.sql
```

## 安装依赖库

```bash
yum install mysql-devel
否则报错：configure: error: MySQL library not found
yum install libxml2-devel
否则报错：configure: error: LIBXML2 library not found
yum install net-snmp-devel
否则报错：configure: error: Invalid Net-SNMP directory - unable to find net-snmp-config
yum install curl curl-dev
否则报错：configure: error: Curl library not found
```

## 编译Zabbix Server和 Agent

```bash
./configure --enable-server --enable-agent --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2
make install
```

配置zabbix server和zabbix agent，配置文件存放在**/usr/local/etc/zabbix_*.conf**
配置server，主要配置数据库连接

```bash
vim /usr/local/etc/zabbix_server.conf
```

内容如下

```properties
LogFile=/data/logs/zabbix_server.log
DBName=zabbix
DBUser=zabbix
DBPassword=<password>
DBSocket=/data/mysql/data/mysql.sock
DBPort=3306
```

配置agent，主要配置server的连接地址，内容如下

```properties
LogFile=/data/logs/zabbix_agentd.log
Server=10.200.48.23
ServerActive=10.200.48.23
```

注：日志目录需要事先创建

## 启动server、agent

```bash
zabbix_server
zabbix_agent
```

# 安装web ui
zabbix ui是用php开发，因此需要部署php环境。

## 安装apache

```bash
yum install httpd
```

## 安装php

```bash
yum install php
```

## 部署zabbix ui

拷贝zabbix web ui文件

```bash
mkdir /var/www/html/zabbix
cd frontends/php/
cp -a . /var/www/html/zabbix/
```

设置php参数
因为zabbix frontend 会检查php参数设置，不满足无法通过

```bash
vim /etc/php.ini
```

需要修改的几个核心参数如下

```properties
memory_limit = 512M
post_max_size = 32M
max_execution_time = 300
max_input_time = 300
date.timezone = Asia/Shanghai
```

## 启动apahce

```bash
service httpd start
```

## 浏览器登录

* **http://10.200.48.23/zabbix**

进行配置即可。具体可参考：
https://www.zabbix.com/documentation/3.0/manual/installation/install

登录
默认用户名密码：Admin/zabbix

官方文档：

* https://www.zabbix.com/documentation/3.0/manual/installation/install#installation_from_sources