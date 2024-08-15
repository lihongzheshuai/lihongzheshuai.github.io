---
layout: post
title: "Postgresql 9.4 文档阅读笔记-第五章"
modified:
categories: 
excerpt: 记录阅读中在意的点, 给自己一点积累。
tags: [postgresql,documentation]
image:
  feature:
thread_key: 1864
date: 2015-05-15T20:38:20+08:00
---

记录阅读中在意的点

###字段约束：
check、notnull、unique、primary key、reference
外键必须关联primary key 或者unique字段。这两种字段都带索引。
exclude约束？？？

###系统列
oid、tableoid、xmin、cmin、xmax、cmax、ctid。都是32位的字段。

###schema（架构）
类似操作系统中的目录，每个目录中有独立的table，view，function等，不冲突。
show search_path; 查看查找路径。

###表继承(inheritance)
约束：继承check，not null。不继承：unique, primary key, foreign key
可以多继承。

###分区（partitioning）

把大表拆分成小的物理块，查询数据集中在某几个分区时可显著提升性能。
当查询或者更新的数据涉及到某个分区中的大部分数据的时候，用连续扫描代替索引和随机访问。
可通过添加或删除分区进行大数据量的导入和删除操作。效率更高。
不经常使用的数据可被转义至廉价的存储设备上。

一般来说，当表的大小超过物理内存的大小的时候，需要分区。

Postgresql通过子表的方式支持分区。主表为空。

**Postgresql支持两种分区模式**：

范围分区：通过连续不重叠的key范围定义分区。
列表分区：明确确定分区中包含哪些key。

**Postgresql分区实现方式：**

通过主表->继承主表->约束，触发器 实现。

**constraint exclusion**

有效的优化分区性能的手段。
set constraint_exclusion = on;
通过检查check来优化效率，所以建分区表要加check。索引只是用于单个分区内部。

**设置分区**

也可通过rule。不过rule的性能比trigger低。主要在于查询方面。插入还好。大多数情况，trigger的性能好于rule。copy命令可用于trigger但是不能用于rule。

**分区注意事项：**

vacuum和analyze命令不会自动作用于分区，需要手动操作。
不要素以修改分区key列。

**constraint exclusion注意事项：**

保持简单的分区规则。例如简单的比较和范围判断。最佳实践是，比较可用使用b-tree索引的分区列。
数据库会检查所以的分区校验，所以分区数不要过多。不要过百。上千不可。


