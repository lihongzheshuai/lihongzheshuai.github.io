---
layout: post
title: Cloudera CDH4卸载
date: 2013-04-27 21:09 +0800
author: onecoder
comments: true
tags: [Hadoop]
categories: [大数据]
thread_key: 1461
---
<p>
	记录卸载过程和问题。现有环境Cloudera Manager + (1 + 2 )的CDH环境。</p>
<p>
	1、先在Manage管理端移除所有服务。<br />
	2、删除Manager Server<br />
	在Manager节点运行</p>

```bash
$ sudo /usr/share/cmf/uninstall-cloudera-manager.sh
```

<p>
	如果没有该脚本，则可以手动删除，先停止服务：</p>

```bash
sudo service cloudera-scm-server stop
sudo service cloudera-scm-server-db stop
```

<p>
	然后删除：</p>

```bash
sudo yum remove cloudera-manager-server
sudo yum remove cloudera-manager-server-db
```

<p>
	3、删除所有CDH节点上的CDH服务，先停止服务：</p>

```bash
sudo service cloudera-scm-agent hard_stop
```

<p>
	卸载安装的软件：</p>

```bash
sudo yum remove 'cloudera-manager-*' hadoop hue-common 'bigtop-*'
```

<p>
	4、删除残余数据：</p>

```bash
sudo rm -Rf /usr/share/cmf /var/lib/cloudera* /var/cache/yum/cloudera*
```

<p>
	5、kill掉所有Manager和Hadoop进程（选作，如果你正确停止Cloud Manager和所有服务则无须此步）</p>

```bash
$ for u in hdfs mapred cloudera-scm hbase hue zookeeper oozie hive impala flume; do sudo kill $(ps -u $u -o pid=); done
```

<p>
	6、删除Manager的lock文件<br />
	在Manager节点运行：</p>

```bash
sudo rm /tmp/.scm_prepare_node.lock
```

<p>
	至此，删除完成。<br />
	&nbsp;</p>