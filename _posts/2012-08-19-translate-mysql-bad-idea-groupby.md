---
layout: post
title: OneCoder翻译-MySQL 的不良用法 Group By
date: 2012-08-19 22:37 +0800
author: onecoder
comments: true
tags: [MySQL]
categories: [翻译, 知识扩展]
thread_key: 1084
---
<a href="http://www.coderli.com">**OneCoder**</a>最近打算坚持每周左右至少翻译一篇技术文章，不管是从学习技术和学习英语的角度，对自己都会是一个提高。水平有限，如果您觉得翻译太过粗糙，甚至错误，还望不吝指出，<a href="http://www.coderli.com">**OneCoder**</a>必将虚心接受，努力学习改进。

**MySQL**是一个"容错性"很强的数据库。这种"容错性"体现在既能作为生产环境中的关系型数据库，又深受那些并不真正回写**SQL**的各色**hacker**欢迎。也正式因为他们不是真正会写**SQL**，所以他们选择了**MySQL**，因为**MySQL**容错性高。这种容错性，就跟在他们最喜欢的**PHP**语言中的"magic quotes"特性一样。**MySQL**可以允许你写"错误"的SQL语言，仍可以运行它。我所说的"错误的"**SQL**是这样的：

```sql
SELECT o.custid, c.name, MAX(o.payment)
  FROM orders AS o, customers AS c
  WHERE o.custid = c.custid
  GROUP BY o.custid;
```

这条语句是出在MySQL的官方文档：

- <a href="http://dev.mysql.com/doc/refman/5.6/en/group-by-hidden-columns.html">http://dev.mysql.com/doc/refman/5.6/en/group-by-hidden-columns.html</a>

> （<a href="http://www.coderli.com">OneCoder</a>
注：应该看看这个文档的介绍，能更清楚的明白该文的作者想表达的意思。）

那么，这条语句的含义是怎样呢。**c.name**这个映射的返回结果是什么？最大的(**c.name**)？任意的(**c.name**)？还是第一个(**c.name**)？还是**NULL**？还是42？根据文档，任意的**c.name(ANY(c.name))**，应该是最合理的可能。这种特殊的语法大概对那些少数的真正了解这种语法什么时候是有用的人是非常的智能的一种方式。也就是当他们确切的知道，**o.custid**和**c.name**需要是1对1的关系是，他们可以省略掉一些没有必要的语句，例如**Max(c.name)**或者在**Group by** 子句中加上**c.name**。（是的，节省了8个字符。）

但是，对大部分**MySQL**的初学者来说，会对此感到迷惑：

- 首先，他们会迷惑于并没有得到预期的c.name值。
- 其次，当他们最终将要迁移到另一个数据库的时候，会再次遇到困境。会报一些有趣的语法错误，如：**ORA-00979 not a GROUP BY expression**。

所以:

- MySQL的用户，停止使用这个特性。他直接带来痛苦和折磨，尽管你知道他是如何工作的。SQL语句中的GROUP BY不是被设计用于这种工作方式的。
- MySQL数据库：废弃这个特性。

原文地址： <a href="http://java.dzone.com/articles/mysql-bad-idea-384" target="\_blank">http://java.dzone.com/articles/mysql-bad-idea-384</a></div>

