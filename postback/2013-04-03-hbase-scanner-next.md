---
layout: post
title: HBase“扫描器”scanner使用和优化
date: 2013-04-03 20:46 +0800
author: onecoder
comments: true
tags: [HBase]
thread_key: 1440
---
<p>
	HBase在扫描数据的时候，使用scanner表扫描器。HTable通过一个Scan实例，调用getScanner(scan)来获取扫描器。可以配置扫描起止位，以及其他的过滤条件。通过迭代器返回查询结果，使用起来虽然不是很方便，不过并不复杂。但是这里有一点可能被忽略的地方，就是返回的scanner迭代器，每次调用next的获取下一条记录的时候，默认配置下会访问一次RegionServer。这在网络不是很好的情况下，对性能的影响是很大的。测试中，未配置前，一个业务的消耗时间为：</p>
<blockquote>
	<p>
		Cost time: 159941</p>
</blockquote>
<p>
	通过：</p>
<pre class="brush:java;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
scan.setCaching(10000);
</pre>
<p>
	指定一次取出10000条记录后，该业务的消耗时间为：</p>
<blockquote>
	<p>
		Cost time: 64845</p>
</blockquote>
<p>
	因为该 业务访问数据次数很多，所以效果很明显。</p>
<p>
	也有说可通过修改配置项hbase.client.scanner.caching的值，来使该配置生效。不过，OneCoder这里在hbase-site.xml中增加了该配置却没有生效。</p>

