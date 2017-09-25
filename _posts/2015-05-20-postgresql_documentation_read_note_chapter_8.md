---
layout: post
title: "Postgresql 9.4 文档阅读笔记-第八章 数据类型"
modified:
categories: 
excerpt: 记录阅读中在意的点, 给自己一点积累。
tags: [postgresql, documentation, note]
image:
  feature:
thread_key: 1865
date: 2015-05-20T14:35:02+08:00
---

**numeric** - 可以存储非常大数据，并且可存储高精度数据。numeric（precision, scale）例如：23.5141 precision=6, scale=4
可存储NaN值，代表not-a-number。在Postgresql中NaN和NaN数值是相等的，并且大于其他任何值。

**serial** - 用于自增字段。相当于：
CREATE SEQUENCE tablename_colname_seq; CREATE TABLE tablename (
colname integer NOT NULL DEFAULT nextval(’tablename_colname_seq’) );
ALTER SEQUENCE tablename_colname_seq OWNED BY tablename.colname;

**money** - 用于保存跟钱相关的数据。可支持如：$1,000.00 格式的数据。跟本地位置信息相关。取决于lc_monetary参数的配置。例如：

mydb=# select '12.34' ::money;
  money  
 ￥12.34
 
**character varying(n)**  - 有限可变长度字符串

**character（n)** - 有限定长字符串。空格补位。

**text** - 任意长度字符串。
短字符串（小于126byte）需要额外的1字节存储空间，长的字符串需要4字节的额外存储。最长的字符串大约1GB。
三种类型在效率上无明显差别，只在存储空间上不同。在Postgresql中charater反而会慢，因为需要额外的blank paded操作。

**binary** - 可变长二进制串。与character String有两点主要区别：1、binary可存储0值八位字节以及任何不可打印的字符，而charater不允许任何在数据库编码下无法解析的字符编码。2、binary直接操作字节，而strings依赖与本地化设置。
支持两种输入输出格式: escape和hex。默认是hex。

**date** - 日期类型，推荐的输入格式1999-01-08 ，支持输入为now，当前事务时间。

**interval** - 保存间隔。例如：
Style Specification Year-Month Interval Day-Time Interval Mixed Interval
sql_standard 1-2 3 4:05:06 -1-2 +3 -4:05:06

**网络地址类型** - 推荐使用网络地址类型保存相关数据，因为提供了额外的操作和函数支持。具体可参考：[http://francs3.blog.163.com/blog/static/405767272012584552165/
](http://francs3.blog.163.com/blog/static/405767272012584552165/)

**tsvector** - 排序去重列表。例如：
SELECT ’a fat cat sat on a mat and ate a fat rat’::tsvector;                              
输出：’a’ ’and’ ’ate’ ’cat’ ’fat’ ’mat’ ’on’ ’rat’ ’sat’

**tsquery** - 全文检索，具体可参考：
[http://francs3.blog.163.com/blog/static/405767272015065565069/](http://francs3.blog.163.com/blog/static/405767272015065565069/)

**json** -  存储json数据类型，分两种形式，json和jsonb，支持的输入格式几乎相同。

*json* - 完全拷贝输入数据存储，因此在处理时需要重新解析，耗时。并且，没有对空格，重复key等的处理，因为完全拷贝。
*jsonb* - 解析后存储，因此在存储时有额外耗时，但是后续处理时效率高，并且支持索引。
因此，通常使用jsonb。
jsonb 的索引 - GIN（Generalized Inverted Index）索引。可针对列整体创建索引，也可以针对jsonb字段中的某个子属性加索引。
例如：
CREATE INDEX idxgintags ON api USING gin ((jdoc -> ’tags’)); 



