---
layout: post
title: High Performance MySQL 翻译 第一章 MySQL架构和历史 - 逻辑架构
date: 2013-03-25 23:11 +0800
author: onecoder
comments: true
tags: [High performance mysql]
thread_key: 1418
---
<p>
	《High Performance MySQL》是OneCoder正在阅读的书，利用茶余饭后时间进行的阅读和翻译，日积月累。</p>
<p>
	MySQL与其他数据库服务有很大的不同，它的架构特性使得它在广泛领域内成为一种实用而&ldquo;廉价&rdquo;的选择。MySQL并不是完美的，但是他足够灵活以适应特定的需求环境，如网络应用。同时，MySQL也可以支持嵌入式应用，数据仓库，内容索引和软件分发，高可用系统，联机事务处理等等。</p>
<p>
	为了充分的利用MySQL，你需要理解其设计，从而利用而不是抗拒它。MySQL在很多方面是灵活的。例如，它支持的硬件范围很广，你可以在各种硬件环境下配置和运行它，并且，它支持多种数据类型。然而，MySQL最不寻常和重要的特性是它的存储引擎，它在设计上将查询进程和其他服务任务与数据存储和检索分离。这种分离的特性让你可以据需选择数据的存储方式以及想要怎样的性能，特性和其他特征。</p>
<p>
	本章概要介绍MySQL的架构，存储引擎的主要区别及其重要性。最后将介绍一些历史背景和基准数据。我们视图通过简化细节和展示样例的方式介绍了MySQL。这个讨论对于数据库新手和其他数据库的专家都非常有帮助。</p>
<p>
	MySQL 逻辑架构</p>
<p>
	一个好的展现MySQL各个组件如何协同工作的图会帮助你更好的理解MySQL。图1-1展示了MySQL的逻辑架构。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CJNaSO8g/8IgJ7.jpg" style="width: 227px; height: 346px;" /></p>
<p style="text-align: center;">
	图1-1</p>
<p>
	最上层是业务层，不局限于MySQL。他们大多是基于网络的客服端/服务端工具或者服务，需要进行连接管理，权限认证，安全等等。</p>
<p>
	第二层开始变得&ldquo;有趣&rdquo;。MySQL大部分的&ldquo;大脑&rdquo;都在这层，包括查询解析代码，分析，优化，缓存以及所有内嵌函数（如，dates, times, math 和 encryption）。提供的所有访问存储引擎的函数都在该层，例如：存储过程， 触发器和视图。</p>
<p>
	第三层包括存储引擎。他们负责存储和检索存储在MySQL中的所有数据。就跟GNU/Linue的各种可用的文件系统一样，不同存储引擎也有其优缺点。服务端通过存储引擎接口（API）与其通信。该API屏蔽了不同存储引擎的区别，使他们对查询层是透明的。该API包含了大量的底层函数，执行诸如&quot;开始一个事务&quot;或者&quot;查询包含该主键的行&quot;等操作。存储引擎不解析SQL（注1）或者与彼此通信；他们只负责响应来自服务端的请求。</p>
<p>
	注1：一个例外是在InnoDB引擎解析外键定义，因为MySQL服务本身并没有实现该功能。</p>

