---
layout: post
title: 《HighPerformance MySQL》概译 隔离等级
date: 2013-04-02 20:03 +0800
author: onecoder
comments: true
tags: [MySQL]
thread_key: 1433
---
<p>
	<strong>隔离等级</strong></p>
<p class="p1">
	隔离其实比它看起来复杂。SQL标准定义了四种隔离级别，决定了数据变化在事务内外可见或不可见。低级别的隔离等级会有更好的并发支持和更低的资源消耗。</p>
<blockquote>
	<p class="p1">
		&nbsp; &nbsp; &nbsp;每种存储引擎都有其独特的隔离等级实现方式。你应该从你使用的存储引擎的手册中获取更详细的信息。</p>
</blockquote>
<p class="p1">
	下面让我们来看下四种隔离等级：</p>
<p class="p1">
	<strong>未提交读(READ UNCOMMITED)</strong></p>
<p class="p1">
	允许事物读取未提交的事物的结果。也就是允许脏读。这个级别在实际环境中很少使用，因为它可能会带来很多问题，并且性能比其他级别并没有好多少。未提交读，也被称为脏读。</p>
<p class="p1">
	<strong>提交读(READ COMMITED)</strong></p>
<p class="p1">
	大多数数据库的默认隔离级别（但不是MySQL的！）它满足之前提到的隔离定义：事物仅可以看到其它事务已经提交的数据。它自身的数据也只有在提交后才能被读到。也被成为不重复读（nonrepeatable read）。意味着，你运行同一个查询两次，可能读到不同的数据。</p>
<p class="p1">
	<strong>重复读(REPEATABLE READ)</strong></p>
<p class="p1">
	解决了不提交读的问题。事务读取到的行在同一事务内部其他查询读取的时候都是一样的。不过，这也带来其他问题：幻象读。(phantom reads)。当你正在读取一些行的时候，另外的事务插入了数据，你再次读取的时候，会读到新插入的行。就好像&ldquo;幻象&rdquo;行一样。InnoDB和XtraDB通过多版本并发管理解决了幻象读的问题，后续我们会介绍。</p>
<p class="p1">
	重复读是MySQL事务的默认隔离级别。</p>
<p class="p1">
	<strong>串行读(SERIALIZABLE)</strong></p>
<p class="p1">
	最高级别的隔离。串行读强制要求事务顺序执行，从而避免了冲突解决上述问题。从内部来看，串行读给每个读取的行加了锁。在该级别下，会发生很多的超时和锁竞争。很少见到有人使用该级别，不过这取决与你的业务需求是否苛刻。</p>
<p class="p1">
	下表列出不同隔离级别的概要和缺点</p>
<p class="p3">
	<i>Table 1-1. ANSI SQL 隔离级别</i></p>
<table cellpadding="0" cellspacing="0" class="t1" width="782.0">
	<tbody>
		<tr>
			<td class="td1" valign="top">
				<p class="p3">
					隔离级别</p>
			</td>
			<td class="td2" valign="top">
				<p class="p3">
					是否允许脏读</p>
			</td>
			<td class="td3" valign="top">
				<p class="p4">
					是否允许不重复读</p>
			</td>
			<td class="td4" valign="top">
				<p class="p5">
					是否允许幻象读</p>
			</td>
			<td class="td5" valign="top">
				<p class="p4">
					读锁</p>
			</td>
		</tr>
		<tr>
			<td class="td1" valign="top">
				<p class="p4">
					未提交读</p>
			</td>
			<td class="td2" valign="top">
				<p class="p4">
					是</p>
			</td>
			<td class="td3" valign="top">
				<p class="p4">
					是</p>
			</td>
			<td class="td4" valign="top">
				<p class="p4">
					是</p>
			</td>
			<td class="td5" valign="top">
				<p class="p4">
					否</p>
			</td>
		</tr>
		<tr>
			<td class="td1" valign="top">
				<p class="p4">
					提交读</p>
			</td>
			<td class="td2" valign="top">
				<p class="p4">
					否</p>
			</td>
			<td class="td3" valign="top">
				<p class="p4">
					是</p>
			</td>
			<td class="td4" valign="top">
				<p class="p4">
					是</p>
			</td>
			<td class="td5" valign="top">
				<p class="p4">
					否</p>
			</td>
		</tr>
		<tr>
			<td class="td1" valign="top">
				<p class="p4">
					重复读</p>
			</td>
			<td class="td2" valign="top">
				<p class="p4">
					否</p>
			</td>
			<td class="td3" valign="top">
				<p class="p4">
					否</p>
			</td>
			<td class="td4" valign="top">
				<p class="p4">
					是</p>
			</td>
			<td class="td5" valign="top">
				<p class="p4">
					否</p>
			</td>
		</tr>
		<tr>
			<td class="td1" valign="top">
				<p class="p4">
					串行读</p>
			</td>
			<td class="td2" valign="top">
				<p class="p4">
					否</p>
			</td>
			<td class="td3" valign="top">
				<p class="p4">
					否</p>
			</td>
			<td class="td4" valign="top">
				<p class="p4">
					否</p>
			</td>
			<td class="td5" valign="top">
				<p class="p4">
					是</p>
			</td>
		</tr>
	</tbody>
</table>
<p>
	&nbsp;</p>

