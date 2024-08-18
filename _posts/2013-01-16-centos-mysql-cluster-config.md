---
layout: post
title: CentOS下 MySQL Cluster NDB 7.2 部署实践
date: 2013-01-16 14:33 +0800
author: onecoder
comments: true
tags: [MySQL]
thread_key: 1286
---
<p>
	实验需要，<a href="http://www.coderli.com">OneCoder</a>打算亲自部署一下MySQL Cluster环境。VMware环境中，虚拟化三台CentOS5.4 x64虚拟机。</p>
<blockquote>
	<p>
		10.4.44.201 SQL<br />
		10.4.44.202 Data<br />
		10.4.44.203 Manager</p>
</blockquote>
<p>
	用于部署。</p>
<p>
	官方文档自然是最好的部署手册，先简单了解一下。</p>
<p>
	<strong>MySQL Cluster构成</strong></p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/PrQHF.jpg" style="width: 583px; height: 372px;" /></p>
<blockquote>
	<p>
		Each MySQL Cluster host computer must have the correct executable programs installed. A host running an SQL node must have installed on it a MySQL Server binary (mysqld). Management nodes require the management server daemon (ndb_mgmd); data nodes require the data node daemon (ndbd or ndbmtd). It is not necessary to install the MySQL Server binary on management node hosts and data node hosts. It is recommended that you also install the management client (ndb_mgm) on the management server host.</p>
</blockquote>
<p>
	SQL节点，必须部署MySQL Server binary(mysqld)；管理(Management) 节点，需要部署management server daemon(ndb_mgmd)；数据(data)节点，需要部署data node daemon(ndbd 或者 ndbmtd)。无需在管理和数据节点上部署MySQL Server binary。推荐在管理节点上，也部署management client(ndb_mgm)。</p>
<p>
	<strong>MySQL Cluster配置（翻译自官方文档）</strong></p>
<p>
	每个data和SQL节点都需要一个my.cnf文件，其中包含了两条重要的信息：一个链接串指明management节点位置，一条针对data节点，告诉MySQL服务器开启NDBCLUSTER存储引擎。<br />
	management节点需要config.ini配置文件，里面保存着它需要管理的集群节点的信息、保存数据和各data节点数据索引所需的内存信息，data节点的位置信息，<br />
	有了这些理论基础，下面我们来动手操作一下</p>
<p>
	先部署data和SQL节点， 下载MysQL Cluster压缩包 ，通过putty自带的pscp工具，拷贝到各个节点linux虚拟机中。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/MxanW.jpg" /></p>
<p>
	解压。</p>
<p>
	先配置SQL和Data节点。在/etc下放置my.cnf配置文件。内容如下：</p>
<pre class="brush:plain;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
[ndbcluster]
ndb-connectstring=10.4.44.203
[mysql_cluster]
ndb-connectstring=10.4.44.203
</pre>
<p>
	再配置Manager</p>
<p>
	同样先将压缩包拷贝，然后在/var/lib/mysql-cluster/config.ini 配置：<span style="font-size: 12px;">[ndbd default]</span></p>
<pre class="brush:plain;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
# Options affecting ndbd processes on all data nodes:
NoOfReplicas=1    # Number of replicas
DataMemory=80M    # How much memory to allocate for data storage
IndexMemory=18M   # How much memory to allocate for index storage
                  # For DataMemory and IndexMemory, we have used the
                  # default values. Since the &quot;world&quot; database takes up
                  # only about 500KB, this should be more than enough for
                  # this example Cluster setup.

[ndb_mgmd]

# Management process options:
hostname=10.4.44.203           # Hostname or IP address of MGM node
datadir=/var/lib/mysql-cluster  # Directory for MGM node log files

[ndbd]
# Options for data node &quot;A&quot;:
                                # (one [ndbd] section per data node)
hostname=10.4.44.202          # Hostname or IP address
datadir=/usr/local/mysql/data   # Directory for this data node&#39;s data files

[mysqld]
# SQL node options:
hostname=10.4.44.201          # Hostname or IP address
                                            # (additional mysqld connections can be
                                        # specified for this node for various
                                                # purposes such as running ndb_restore)
</pre>
<p>
	启动MySQL Cluster：</p>
<p>
	先启动Management节点:</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
shell&gt; ndb_mgmd -f /var/lib/mysql-cluster/config.ini
</pre>
<p>
	再启动data</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
shell&gt;ndbd
</pre>
<p>
	和SQL节点<span style="font-size: 12px;">shell&gt; groupadd mysql</span></p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
shell&gt; useradd -r -g mysql mysql
shell&gt; cd /usr/local
shell&gt; tar zxvf /path/to/mysql-VERSION-OS.tar.gz
shell&gt; ln -s full-path-to-mysql-VERSION-OS mysql
shell&gt; cd mysql
shell&gt; chown -R mysql .
shell&gt; chgrp -R mysql .
shell&gt; scripts/mysql_install_db
shell&gt; bin&gt;mysqld
</pre>
<p>
	成功。在management节点，利用./ndb_mgm查看状态。</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
ndb_mgm&gt;show.</pre>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/5ZH0A.jpg" /></p>
<p>
	部署成功。</p>
<p>
	<strong><a href="http://www.coderli.com">OneCoder</a>注：这里一开始有一个误区，就是我根据文档误以为SQL节点部署的MySQL Server版本而不是Cluster版本，导致耽误了很多时间。今天看一个错误出神的时候，才突然醒悟，我是不是搞错了。连忙替换了版本，这才成功。</strong></p>

