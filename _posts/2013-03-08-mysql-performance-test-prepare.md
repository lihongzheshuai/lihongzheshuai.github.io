---
layout: post
title: MySQL性能测试—前期知识储备
date: 2013-03-08 21:04 +0800
author: onecoder
comments: true
tags: [MySQL]
thread_key: 1382
---
<p>
	今天是妇女节，先祝所有过节的女同胞们节日快乐：）</p>
<p>
	即将对MySQL进行性能测试。所以事先对MySQL的测试工作进行一番了解。主要考察性能测试的工具，MySQL的关键指标，以及一些基础的Benchmark数据，为测试用例和场景的规划做些准备。</p>
<p>
	先说说考量的指标（转载，网址找不到了，抱歉）</p>
<blockquote>
	<p>
		<span style="color:#ff0000;">(1)QPS(每秒Query量)</span><br />
		QPS = Questions(or Queries) / seconds<br />
		mysql &gt; show /*50000 global */ status like &#39;Question&#39;;<br />
		<span style="color:#ff0000;">(2)TPS(每秒事务量)</span><br />
		TPS = (Com_commit + Com_rollback) / seconds<br />
		mysql &gt; show status like &#39;Com_commit&#39;;<br />
		mysql &gt; show status like &#39;Com_rollback&#39;;<br />
		(3)key Buffer 命中率<br />
		key_buffer_read_hits = (1-key_reads / key_read_requests) * 100%<br />
		key_buffer_write_hits = (1-key_writes / key_write_requests) * 100%<br />
		mysql&gt; show status like &#39;Key%&#39;;<br />
		(4)InnoDB Buffer命中率<br />
		innodb_buffer_read_hits = (1 - innodb_buffer_pool_reads / innodb_buffer_pool_read_requests) * 100%<br />
		mysql&gt; show status like &#39;innodb_buffer_pool_read%&#39;;<br />
		(5)Query Cache命中率<br />
		Query_cache_hits = (Qcahce_hits / (Qcache_hits + Qcache_inserts )) * 100%;<br />
		mysql&gt; show status like &#39;Qcache%&#39;;<br />
		(6)Table Cache状态量<br />
		mysql&gt; show status like &#39;open%&#39;;<br />
		(7)Thread Cache 命中率<br />
		Thread_cache_hits = (1 - Threads_created / connections ) * 100%<br />
		mysql&gt; show status like &#39;Thread%&#39;;<br />
		mysql&gt; show status like &#39;Connections&#39;;<br />
		(8)锁定状态<br />
		mysql&gt; show status like &#39;%lock%&#39;;<br />
		(9)复制延时量<br />
		mysql &gt; show slave status<br />
		(10) Tmp Table 状况(临时表状况)<br />
		mysql &gt; show status like &#39;Create_tmp%&#39;;<br />
		(11) Binlog Cache 使用状况<br />
		mysql &gt; show status like &#39;Binlog_cache%&#39;;<br />
		(12) Innodb_log_waits 量<br />
		mysql &gt; show status like &#39;innodb_log_waits&#39;;</p>
</blockquote>
<p>
	其中QPS和TPS自然是重点考察的性能指标。其他指标可以作为每次测试数据的参考数据列出。如果遇到瓶颈，可能还需要考量当时系统的cpu，网络，磁盘的利用率情况。这个遇到具体问题再具体分析。</p>
<p>
	工具方面，首选考察的自然是MySQL自带的测试工具mysqlslap。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/GwZBc.jpg" style="width: 640px; height: 536px;" /></p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
./mysqlslap -a --concurrency=50,100 --number-of-queries 1000 --iterations=5 --engine=myisam,innodb --debug-info -uroot -proot

</pre>
<p>
	一个简单的示例即可说明工具的使用情况，</p>
<blockquote>
	<p>
		-a 自动生成sql<br />
		--concurrency=50,100分别执行50，100并发，<br />
		--iterations=5 执行5次，引擎分别选用myisam和innodb引擎测试。</p>
	<p>
		--number-of-queries&nbsp;&nbsp;&nbsp; Limit each client to this number of queries (this is not<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; exact).（一个客户端执行的测试SQL数量上限，通过--only-print观察自动生成的sql的执行情况来看，该条数限制的是准备数据以外的SQL语句的条数）<br />
		--engine=myisam,innodb 分别用myisam和innodb引擎进行测试。</p>
</blockquote>
<p>
	当然你也可以通过-q指定你想要测试的sql脚本，测试结束后，mysqlslap会给出你测试的相关数据。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/jSd7F.jpg" style="width: 640px; height: 126px;" /></p>
<p>
	关于mysqlslap的更多参数可参考：<a href="http://dev.mysql.com/doc/refman/5.1/en/mysqlslap.html">http://dev.mysql.com/doc/refman/5.1/en/mysqlslap.html</a><br />
	从目前来看上手还是比较容易的。通过执行的query数量和时间，很容易计算出tps和qps等指标。</p>
<p>
	<em>SysBench</em></p>
<p>
	也是MySQL官网提到的一个benchmark工具。只是在64位系统下安装困难，限于网络环境和考虑到其功能和我们即将进行的测试场景，暂时放弃。</p>
<p>
	性能测试基础准备其他话题</p>
<p>
	在思考和验证怎样使用mysqlslap规划测试场景的过程中，收获到一些离散的细节问题，也在此一并记录一下。也许哪天，哪一条就会有所帮助。</p>
<p>
	<span style="color:#ff8c00;"><strong>打开MySQL general_log 记录执行的sql情况</strong></span></p>
<p>
	默认情况下该属性是关闭的，通过set global general_log=ON 打开后，可在log文件中查看数据库执行的sql记录。该需求是OneCoder想要考察JDBC的batch insert的提交方式，究竟是数据库中是执行的多条insert然后commit还是一个insert values大列表的时候产生的。</p>
<p>
	<strong><span style="color:#ff8c00;">对比批量插入数据 多条insert和一条insert 大values列表(values(),(),())方式，性能差别</span></strong></p>
<p>
	从目前通过mysqlslap执行测试的效果来看，后者明显优于前者。前者1000条平均时间大约是0.2ms，而后者在0.1ms左右。该测试想法是在通过mysqldump到处已有数据的时候发现其sql文件的生成方式的时候以及联想到oracle到mysql的数据迁移工具的处理方式的时候想到的。</p>
<p>
	<strong><span style="color:#ff8c00;">写入性能瓶颈的一个大误解</span></strong></p>
<p>
	曾经极大的错误的认为单线程下mysql可处理的批量插入数据量就是该节点的瓶颈，所以只认为多线程并发写入优化只在NDB的环境下才有效。今天在看MySQL的一些benchmark图表曲线的时候，猛然惊醒，并发数和tps的曲线是类抛物线的就说明在一定并发数的范围内，TPS是有明显提高的。于是用以前的JDBC的代码，增加了几个线程，对同一个mysql并发写入，果然TPS成倍提升。</p>
<p>
	今天总结的大概就这么多，由于是事后回忆总结，不免有所遗漏，想起来再补充把。热烈欢迎指导。</p>

