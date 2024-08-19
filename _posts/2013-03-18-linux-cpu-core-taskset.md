---
layout: post
title: Linux 指定MySQL服务运行的CPU核心（数）
date: 2013-03-18 21:53 +0800
author: onecoder
comments: true
tags: [MySQL]
categories: [知识扩展]
thread_key: 1407
---
<p>
	最近在利用mysqlslap对MySQL进行性能测试，但是测得的TPS、QPS的benchmark数据，从趋势上就跟网上&ldquo;权威&rdquo;的测试数据不同。这让OneCoder十分怀疑测试数据的准确性。</p>
<p>
	在定位问题的过程中，在独立于MySQL Server的机器上执行mysqlslap测试，测得的数据趋势正常。即初始随着并发数增大（一定范围内），TPS和QPS成上升趋势。这让我怀疑我之前在同一台服务器进行的测试，可能mysqlslap和MySQL Server争夺了CPU资源。</p>
<p>
	在一篇MySQL的测试报告中看到这样的话：</p>
<blockquote>
	<p>
		此外测试的机器具有 16 核，其中 12 核运行 mysqld ，另外 4 核运行 sysbench。</p>
</blockquote>
<p>
	立马上网搜索指定方法。搜得Linux下的taskset命令</p>
<pre class="brush:bash;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
taskset -cp cpu序号 mysqld-pid  
</pre>
<p>
	即可指定mysqld服务使用的cpu核心。例如:</p>
<pre class="brush:bash;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
taskset -cp 0-47 12345
</pre>
<p>
	执行mysqlslap的时候，只需通过</p>
<pre class="brush:bash;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
taskset -c 48-63 mysqlslap xxxxxx
</pre>
<p>
	指定使用的cpu核心即可。准备给MySQL Server分配48核， mysqlslap 16核，测试看看效果。<br />
	&nbsp;</p>