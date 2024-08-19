---
layout: post
title: 《HighPerformance MySQL》概译 事务
date: 2013-04-01 21:40 +0800
author: onecoder
comments: true
tags: [翻译,MySQL]
categories: [知识扩展]
thread_key: 1433
---
<p>
	<strong>事务</strong></p>
<p>
	事务是一组被看做一个整体的SQL请求。该组SQL被看成是原子的。如果所有的SQL都正常执行则数据确认请求，如果其中的任何一个失效，则所有的SQL都不生效。也就是说要么全成功，要么全失效。</p>
<p>
	本节并不是针对MySQL的，如果你已经事务的ACID特性了解，那么可以直接了解MySQL的事务特性。</p>
<p>
	银行系统是一个典型的需要事务特性的例子。假设系统有两张表支票账户和储蓄表。从Jane的支票账户转义200美元到她的储蓄账户需要至少三步：</p>
<blockquote>
	<p>
		1、校验支票账户有超过200的可用额。<br />
		2、从支票账户划掉200<br />
		3、给储蓄账户增加200</p>
</blockquote>
<p>
	所有操作需要封装到一个事务中，一旦其中一个步骤失败，整个操作可以回滚。</p>
<p>
	用START TRANSACTION开启事务。用COMMIT提交事务，或者用ROLLBACK回滚事务。因此，整个SQL形如：</p>
<pre class="brush:sql;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
START TRANSACTION;
SELECT balance FROM checking WHERE customer_id = 10233276;
UPDATE checking SET balance = balance - 200.00 WHERE customer_id = 10233276;
UPDATE savings SET balance = balance + 200.00 WHERE customer_id = 10233276;
COMMIT;
</pre>
<p>
	不过事务不是全部，试想一下，如果在执行第四行的时候数据崩溃了会怎样。很可能用户丢失了200元。</p>
<p>
	事务不是保证正确性的全部，系统必须满足ACID特性。ACID是指：原子性、一致性、隔离性、持久性。</p>
<p>
	<em><strong>原子性：</strong></em>事务必须作为一个不可分割的整体。整个事务全部生效或者回滚。不存在部分执行的事务。</p>
<p>
	<strong><em>一致性：</em></strong><br />
	数据库必须从一个一致性状态变为另一个。在我们例子中，一致性保证了发生在第三和第四行之间的数据库损坏不会造成账户中200元的丢失。因为，在事务提交前，事务中任何的修改都不会反应在数据库中。</p>
<p>
	<strong><em>隔离性：</em></strong>一个事务的结果对另外的事务通常是不可见的，直到该事务完成。这保证了银行的账户汇总程序运行在第三行和第四行之间的时候，仍然可以看到支票账户中的200元。当我们讨论隔离性的时候，你将会明白我们所说的&quot;通常不可见&quot;的含义。</p>
<p>
	<em><strong>持久性:</strong></em><br />
	一旦提交了事务，那么数据将会永久的改变。这意味着数据必须持久化起来，并且不会因为数据库的崩溃而丢失。持久性是一个有些模糊的概念，分很多等级。某些持久化的策略比其他的更有安全性保证，不过没有100%的安全。</p>
<p>
	ACID事务保证了银行系统不会弄丢你的钱。这在我们应用的逻辑中很难也几乎不可能保证的。一个满足ACID规则的数据库必须做很多复杂的工作以提供ACID特性。</p>
<p>
	跟提高锁的精确范围一样，更高的安全的的负面影响就是数据库要做更多的工作。提供ACID特性的数据库需要更多的CPU、内存利用率和磁盘空间。这是MySQL存储引擎架构提供的特性。你可以决定你的应用是否需要事务。如果你不需要，你可以选择性能更高的无事务的存储引擎。你可以选择锁表的策略在无事务的情况下提供你想要的保护。这都取决于你。</p>

