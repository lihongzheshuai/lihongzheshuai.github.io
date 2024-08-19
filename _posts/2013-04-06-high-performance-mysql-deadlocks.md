---
layout: post
title: 《HighPerformance MySQL》概译 死锁
date: 2013-04-06 22:31 +0800
author: onecoder
comments: true
tags: [翻译，MySQL]
categories: [知识扩展]
thread_key: 1447
---
<p>
	当多个事务同时持有和请求同一资源上的锁而产生循环依赖的时候就产生了死锁。死锁发生在事务试图以不同的顺序锁定资源。以StockPrice表上的两个事务为例：</p>
<blockquote>
	<p>
		事务1<br />
		START TRANSACTION;<br />
		UPDATE StockPrice SET close = 45.50 WHERE stock_id = 4 and date = &#39;2002-05-01&#39;;<br />
		UPDATE StockPrice SET close = 19.80 WHERE stock_id = 3 and date = &#39;2002-05-02&#39;;<br />
		COMMIT;<br />
		事务 #2<br />
		START TRANSACTION;<br />
		UPDATE StockPrice SET high = 20.12 WHERE stock_id = 3 and date = &#39;2002-05-02&#39;;<br />
		UPDATE StockPrice SET;<br />
		COMMIT;</p>
</blockquote>
<p>
	如果不走运的话，每个事务都可以执行完第一个语句，并在过程中锁住资源。然后每个事务都试图去执行第二行语句，当时却发现它被锁住了。两个事务将永远的等待对方完成，除非有其他原因打断死锁。</p>
<p>
	为了解决这个问题，数据库实现了各种死锁探查和超时机制。像InnoDB这样复杂的存储引擎会提示循环依赖并且立即返回错误。否则死锁将会导致查询非常缓慢。其他一些不好的做法是等待超时后放弃。当前InnoDB处理死锁的方式是回滚持有最少排他行级锁的事务。（几乎最简单的回滚的参考指标）</p>
<p>
	锁的行为是顺序是存储引擎决定的。因此，一些存储引擎可能会在特定的操作顺序下发生死锁，其他的可能没有。死锁有两种：一些是因为实际数据冲突而无法避免，一些是因为存储引擎的工作方式产生。</p>
<p>
	只有部分或者完全回滚其中的一个事务才可能打破死锁。死锁是事务系统中客观存在的事实，你的应该在设计上必须应该考虑处理死锁。一些业务系统可以从头重试事务。</p>

