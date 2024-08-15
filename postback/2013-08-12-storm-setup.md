---
layout: post
title: CentOS下 Storm0.8.2 环境搭建记录
date: 2013-08-12 17:48 +0800
author: onecoder
comments: true
tags: [Storm]
thread_key: 1484
---
<p>
	 Storm是Twitter开源的一个实时计算框架，它需要依赖Zookeeper，ZeroMQ；同时还需要你的系统环境中有Java和Python。所以整个搭建步骤如下：</p>
<blockquote>
	<p>
		1. 搭建Zookeeper集群。<br />
		2. 在控制节点机[ Nimbus ]和工作节点机[ Supervisor ]上安装相同的环境（ZeroMQ，JZMQ，Java，Python等）<br />
		3. 在控制节点机[ Nimbus ]和工作节点机[ Supervisor ]上安装Storm框架<br />
		4. 配置Storm，通过storm.yaml文件<br />
		5. 用命令启动Storm(需要分别启动Nimbus、Supervisor、ui)</p>
</blockquote>
<p>
	<br />
	1. 搭建Zookeeper</p>
<p>
	由于 storm并不用zookeeper来传递消息。所以zookeeper上的负载是非常低的，单个节点的zookeeper在大多数情况下都已经足够了，因此这里我们搭建单节点zookeeper。<br />
	下载最新版3.4.5：http://zookeeper.apache.org/releases.html#download<br />
	解压，在conf下增加配置文件zoo.cfg，可参考zoo-sample.cfg的配置修改，主要修改dataDir路径位置</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/FRU4s.jpg" /></p>
<p>
	启动zookeeper：</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
bin/zkServer.sh start
</pre>
<p>
	启动后，可通过：</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
bin/zkCli.sh -server 127.0.0.1:2181
</pre>
<p>
	验证启动状况和客户端连接状况</p>
<p>
	2、搭建ZeroMq2.1.7版：<br />
	官方提到，不要安装2.1.0版，如果使用2.1.7版遇到问题，可尝试降级到2.1.4版本。<br />
	下载：http://download.zeromq.org/<br />
	解压后，在目录中执行：</p>

```bash
shell/>./configure
```

<p style="text-align: center;">
	<img alt="" src="/images/oldposts/13ZgiQ.jpg" /></p>
<p>
	<br />
	遇到uuid-dev的错误，说明需要安装uuid包：<br />
	在ubuntu下安装uuid-dev，在centos上安装：</p>

```bash
yum install libuuid-devel.x86_64
```

<p>
	然后再执行configure即可。<br />
	然后：</p>

```bash
make
sudo make install
```

<p>
	3、安装JZMQ<br />
	下载：https://codeload.github.com/nathanmarz/jzmq/zip/master<br />
	解压后执行：</p>

```bash
./autogen.sh
./configure
make
sudo make install
```

<p>
	./configure时会检查你的JAVA_HOME是否正确，不正确会报错，并提示。</p>
<p>
	4、安装Storm</p>
<p>
	下载：https://github.com/nathanmarz/storm<br />
	解压，配置storm.yaml配置文件。主要配置：<br />
	1) storm.zookeeper.servers: Storm集群使用的Zookeeper集群地址，其格式如下：</p>


```
storm.zookeeper.servers:
  - "111.222.333.444"
  - "555.666.777.888"
```

<p>
	如果Zookeeper集群使用的不是默认端口，那么还需要storm.zookeeper.port选项。<br />
	2) storm.local.dir: Nimbus和Supervisor进程用于存储少量状态，如jars、confs等的本地磁盘目录，需要提前创建该目录并给以足够的访问权限。然后在storm.yaml中配置该目录，如：<br />
	</p>

```
	storm.local.dir: "/home/admin/storm/workdir"
```

<p>
	3) java.library.path: Storm使用的本地库（ZMQ和JZMQ）加载路径，默认为"/usr/local/lib:/opt/local/lib:/usr/lib"，一般来说ZMQ和JZMQ默认安装在/usr/local/lib 下，因此不需要配置即可。<br />
	4) nimbus.host: Storm集群Nimbus机器地址，各个Supervisor工作节点需要知道哪个机器是Nimbus，以便下载Topologies的jars、confs等文件，如：<br />
	nimbus.host: "111.222.333.444"<br />
	5) supervisor.slots.ports: 对于每个Supervisor工作节点，需要配置该工作节点可以运行的worker数量。每个worker占用一个单独的端口用于接收消息，该配置选项即 用于定义哪些端口是可被worker使用的。默认情况下，每个节点上可运行4个workers，分别在6700、6701、6702和6703端口，如：<br />
</p>	

```
	supervisor.slots.ports:
	    - 6700
	    - 6701
	    - 6702
	    - 6703
```

<p>
	启动Storm最后一步，启动Storm的所有后台进程。和Zookeeper一样，Storm也是快速失败（fail-fast)的系统，这样Storm才能在 任意时刻被停止，并且当进程重启后被正确地恢复执行。这也是为什么Storm不在进程内保存状态的原因，即使Nimbus或Supervisors被重 启，运行中的Topologies不会受到影响。<br />
	以下是启动Storm各个后台进程的方式：</p>
<p>
	1. Nimbus: 在Storm主控节点上运行"bin/storm nimbus >/dev/null 2>&amp;1 &amp;"启动Nimbus后台程序，并放到后台执行；<br />
	2. Supervisor: 在Storm各个工作节点上运行"bin/storm supervisor >/dev/null 2>&amp;1 &amp;"启动Supervisor后台程序，并放到后台执行；<br />
	3. UI: 在Storm主控节点上运行"bin/storm ui >/dev/null 2>&amp;1 &amp;"启动UI后台程序，并放到后台执行，启动后可以通过http://{nimbus host}:8080观察集群的worker资源使用情况、Topologies的运行状态等信息。</p>
<p>
	注意事项：</p>
<p>
	1. Storm后台进程被启动后，将在Storm安装部署目录下的logs/子目录下生成各个进程的日志文件。<br />
	2. 经测试，Storm UI必须和Storm Nimbus部署在同一台机器上，否则UI无法正常工作，因为UI进程会检查本机是否存在Nimbus链接。<br />
	3. 为了方便使用，可以将bin/storm加入到系统环境变量中。</p>
<p>
	至此，Storm集群已经部署、配置完毕，可以向集群提交拓扑运行了。<br />
	附：Storm的主要依赖：<br />
	Apache Zookeeper、&Oslash;MQ、JZMQ、Java 6和Python 2.6.6<br />
	 </p>