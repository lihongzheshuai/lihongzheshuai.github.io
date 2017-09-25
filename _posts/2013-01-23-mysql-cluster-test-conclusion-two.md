---
layout: post
title: MySQL Cluster 使用小测小结(2)
date: 2013-01-23 17:27 +0800
author: onecoder
comments: true
tags: [MySQL]
thread_key: 1302
---
<p>
	承接之前的初测，题目本来想叫深入测试的，不过想想太大了，就还叫使用的一个小结吧。</p>
<p>
	在扩充数据节点之前，<a href="http://www.coderli.com">OneCoder</a>向数据库中又写入900w的数据，总量达到1kw。每批次写入20w的数据，写入时间大致如下：</p>
<blockquote>
	<p>
		&hellip;&hellip;<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 202634<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 168834<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 181764<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 156975<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 184845<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 202010<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 177443<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 203957<br />
		It&#39;s up to batch count: 200000<br />
		Batch data commit finished. Time cost: 159565<br />
		All data insert finished. Total time cost: 10476439</p>
</blockquote>
<p>
	1kw数据执行Select，查询10条结果效率如下：</p>
<blockquote>
	<p>
		Query ten rows from table [data_house] cost time: 27</p>
</blockquote>
<p>
	可见效率还是很快。当前数据分布情况如下：</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CAtAHU1A/bilwC.jpg" style="width: 620px; height: 90px;" /></p>
<p>
	现在，再添加一个数据节点。步骤略，主要就是修改配置文件，按顺序重启即可。不过在重启Data Node时候需要耐心等待成功。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CAtAIi6Q/q7QBH.jpg" style="width: 656px; height: 252px;" /></p>
<p>
	通过</p>

```bash
ndb_mgm>all report memory
```

<p>
	查看内存占用：</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CAtAHHFC/RnNDp.jpg" style="width: 630px; height: 123px;" /></p>
<p>
	发现数据并没有均匀分配。此时再通过代码查询记录，看看耗时情况。耗时还是24ms左右。没有明显变化。不过，这里我们还是想让数据均匀分配的。先测试再写入100w数据。会不会分别存储。测试显示，数据还是集中在原来的节点保存。插入效率基本与原来一致。</p>
<p>
	将NoOfReplicas的值从1改为2， 重新启动，发现一直报错：</p>
<blockquote>
	<p>
		Node 2: Forced node shutdown completed. Occured during startphase 1. Caused by error 2350: &#39;Invalid configuration received from Management Server(Configuration error). Permanent error, external action needed&#39;</p>
</blockquote>
<p>
	这个问题确实有由于修改了值引起的，但是找了半天一直没有正常的解决。考虑到现在data存储都是测试数据，所以考虑在data节点采用：</p>

```bash
shell>ndbd --initial-start --foreground
```

<p>
	的方式重启节点，并通过foreground的方式查看启动日志。最后，倒是正常启动成功了，只是数据确实被&quot;initial&quot;干净了。重新灌数据吧。还拿100w试验。数据灌入效率差不多，只是数据在两个节点上被复制两份了</p>
<p>
	查询效率还是20ms左右。</p>
<p>
	继续测试，在执行之前的1kw数据，20w一组批量写入数据灌入测试中，却出现：</p>
<blockquote>
	<p>
		Lock wait timeout exceeded; try restarting transaction</p>
</blockquote>
<p>
	的错误。有人说需要调整</p>
<blockquote>
	<p>
		TransactionDeadLockDetectionTimeOut=10000</p>
</blockquote>
<p>
	参数的值，默认是1200。不过我并没有采用，因为重启挺坎坷，根据网上的一些讨论分析，减少了每次写入的数量，到10w。目前来看，稳定许多，尚未出现错误。<br />
	关闭一个节点，验证集群的高可用性。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CAtAIQuE/10h06U.jpg" style="width: 630px; height: 215px;" /></p>
<p>
	再次调用查询接口。正常返回数据。</p>
<p>
	目前为止，我们还差最关心的数据自动分片，分节点保存的问题没有验证清楚。随后，我们将针对此问题再进行进一步的验证。</p>