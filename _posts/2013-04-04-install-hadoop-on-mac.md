---
layout: post
title: Mac下 Hadoop部署简介(Mac OSX 10.8.3 + Hadoop-1.0.4)
date: 2013-04-04 16:30 +0800
author: onecoder
comments: true
tags: [Hadoop]
thread_key: 1444
---
<p>
	OneCoder在自己的笔记本上部署Hadoop环境用于研究学习，记录部署过程和遇到的问题。</p>
<p>
	1、安装JDK。<br />
	2、下载Hadoop(1.0.4)，在Hadoop中配置JAVA_HOME环境变量。修改hadoop-env.sh文件。<br />
	export JAVA_HOME= /Library/Java/JavaVirtualMachines/jdk1.7.0_10.jdk/Contents/Home/<br />
	3、配置SSH<br />
	生成密钥</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
ssh-keygen -t dsa -P &#39;&#39; -f ~/.ssh/onecoder_dsa</pre>
<p>
	将公钥追加到key中</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
cat ~/.ssh/onecoder_rsa.pub &gt;&gt; ~/.ssh/authorized_keys
</pre>
<p>
	打开Mac OS的远程访问选项。系统设置 -》 共享 -》 远程登录</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CLgPDyHo/WtDn1.jpg" style="width: 585px; height: 480px;" /></p>
<p>
	4、配置namenode和datanode hdfs本地路径<br />
	在hdfs-site.xml中配置</p>
<pre class="brush:xml;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
&lt;property&gt;
 &lt;name&gt;dfs.name.dir&lt;/name&gt;
 &lt;value&gt;/Users/apple/Documents/hadoop/name/&lt;/value&gt;
&lt;/property&gt;
&lt;property&gt;
   &lt;name&gt;dfs.data.dir&lt;/name&gt;
  &lt;value&gt;/Users/apple/Documents/hadoop/data/&lt;/value&gt;
&lt;/property&gt;
 &lt;property&gt; 
    &lt;name&gt;dfs.replication&lt;/name&gt; 
    &lt;value&gt;1&lt;/value&gt; 
 &lt;/property&gt;

</pre>
<p>
	由于是验证环境，所以数据备份设为1。</p>
<p>
	5、格式化namenode</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
bin/Hadoop NameNode -format
</pre>
<p>
	6、启动hadoop</p>
<p>
	可通过bin下的start-all.sh直接全部启动，也可以通过</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
hadoop namenode (datanode、jobtracker、tasktracker)
</pre>
<p>
	，按照上述顺序依次启动。<br />
	使用后者可以比较方便的查看启动日志，方便查错。并且也可以在控制台日志中看到监控页面的访问地址和端口。如：<br />
	13/04/04 15:52:18 INFO http.HttpServer: Jetty bound to port 50070<br />
	当然，这些地址你可以已经烂熟于胸了。通过浏览器进入web监控页面查看。可以看到一切就绪。Hadoop环境部署完成。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CLgPE8yh/jBW5l.jpg" style="width: 640px; height: 376px;" /></p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CLgPEgoW/P4PgL.jpg" /></p>
<p>
	<br />
	其他。<br />
	关于警告：Unable to load realm info from SCDynamicStore<br />
	网上给出的解决方案是：在hadoop-env.sh中设置</p>
<blockquote>
	<p>
		export HADOOP_OPTS=&quot;-Djava.security.krb5.realm=OX.AC.UK -Djava.security.krb5.kdc=kdc0.ox.ac.uk:kdc1.ox.ac.uk&quot;</p>
</blockquote>
<p>
	不过在OneCoder这里无效，但是不影响Hadoop环境使用。</p>

