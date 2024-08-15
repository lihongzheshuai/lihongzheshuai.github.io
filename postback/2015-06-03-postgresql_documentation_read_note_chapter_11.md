---
layout: post
title: "Postgresql 9.4 文档阅读笔记-第十一章 索引"
modified:
categories: 
excerpt: 记录阅读中在意的点, 给自己一点积累。
tags: [postgresql, documentation, index]
image:
  feature:
thread_key: 1866
date: 2015-06-03T22:28:45+08:00
---
**索引类型** - B-tree，Hash, GiST, SP-GiST, GIN。默认是B-tree

**B-tree** - 适合处理等值和范围查询。支持的操作符： <, <=, =, >=, >, in, between， is null, is not null。 like和~ 操作支持从前匹配，如：foo% 、^foo。 
B-tree也可用于获取排序后的数据，虽然效率上与一般情况无太大差异。

**hash** - 只适用于相等比较。不过，由于hash索引没有保存在WAL日志中，数据出错后需要重建，并且索引不支持流和文件复制，因此一般不推荐使用。

**GiST** （通用的搜索树（Generalized Search Tree））- 一般用于图形类型数据的索引。

**GIN** - 反向索引，可支持含有多个key的value情况。

**多字段索引** - B-tree， GiST，GIN支持。

Order by - B-tree的输出是排序好的。其他不是。扫描表中大量数据的时候，排序好于索引，因此需要较少的磁盘I/O。查询少量数据的时候可以用索引。不过，当结合limit n使用的时候，由于排序需要排序全部数据，而所以直接获得n条数据，因此此时索引更适合。

B-tree默认是升序的，可调整索引树的顺序以及null值的位置。

多索引联合 - Postgresql 可优化两个单独索引查询，然后针对查询结果做集合。

可针对某个特定条件或者函数建立索引。

局部索引 - 例如：
CREATE INDEX access_log_client_ip_ix ON access_log (client_ip) WHERE NOT (client_ip > inet ’192.168.100.0’ AND client_ip < inet ’192.168.100.255’);

检查索引使用 - explain，analyze。可通过参数强制使用索引与否。
