---
layout: post
title: MySQL主从配置-Amoeba读写分离验证
date: 2013-02-20 16:25 +0800
author: onecoder
comments: true
tags: [MySQL]
thread_key: 1337
---
<p>
	继续我们的验证工作，这次是搭建MySQL的主从配置，再利用Amoeba实现读写分离，搭建一个相对有实际意义的MySQL集群环境。</p>
<p>
	MySQL的主从配置比较简单，网上也有很多的文章，这里不多介绍。基于之前的介绍的环境考虑：</p>
<blockquote>
	<p>
		10.4.44.206 主-写<br />
		10.4.44.207 从-读1<br />
		10.4.44.208 从-读2</p>
</blockquote>
<p>
	MySQL的主从配置确实十分简单。主要就是配置好日志的监听。这里<a href="http://www.coderli.com">OneCoder</a>是参考：<a href="http://369369.blog.51cto.com/319630/790921">http://369369.blog.51cto.com/319630/790921</a> 的文章完成的配置。配置好后，验证一下主从环境是否可用。连接206插入一条数据，在207和208上可成功查询到该数据，证明我们的主从环境配置成功。接下来我们再来配置Amoeba，只要在amoeba.xml中配置好读写库就可以了。</p>
<p>
	然后连接205Amoeba服务端写入数据，分别直接206，207，208节点查询数据，均可查到，并且与通过Amoeba节点查询出的数据是相同的。可见数据是自动同步的。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/vG5R4.jpg" style="width: 473px; height: 160px;" /><br />
	&nbsp;&nbsp; 通过208查询效果，（205，206，207节点查询效果均相同）</p>
<p>
	&nbsp;</p>
<p>
	通过Amoeba查询数据，可以看到只有配置的读节点有网络传输，写节点的网络是风平浪静的。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/KyLOd.jpg" /><br />
	206写</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/e1ntA.jpg" /></p>
<p style="text-align: center;">
	<span style="text-align: center;">208 读节点</span></p>
<p>
	考虑的是，Amoeba是不支持事物的，所以我们可以考虑把写节点直接暴露出来，表引擎选择InnoDB, 其他读节点通过Amoeba进行负载均衡。不过这里就需要业务自己来控制读写的数据源选择了。</p>
<p>
	至此，对于MySQL的验证工作也基本告一段落了，对于形形色色的方案及其试用场景，<a href="http://www.coderli.com">OneCoder</a>也需要好好消化总结一下了。</p>

