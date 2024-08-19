---
title: LeetCode Rising Temperature
tags: [LeetCode,SQL]
date: 2018-1-5 13:41:24 +0800
comments: true
author: onecode
---
# Problem

Given a Weather table, write a SQL query to find all dates' Ids with higher temperature compared to its previous (yesterday's) dates.

```
+---------+------------+------------------+
| Id(INT) | Date(DATE) | Temperature(INT) |
+---------+------------+------------------+
|       1 | 2015-01-01 |               10 |
|       2 | 2015-01-02 |               25 |
|       3 | 2015-01-03 |               20 |
|       4 | 2015-01-04 |               30 |
+---------+------------+------------------+
```
For example, return the following Ids for the above Weather table:
```
+----+
| Id |
+----+
|  2 |
|  4 |
+----+
```

即找到与前一日相比温度升高的条目Id。

<!--break-->

# MySQL

``` sql
# Write your MySQL query statement below
SELECT w1.Id FROM Weather w1, Weather w2 WHERE w1.Temperature > w2.Temperature AND datediff(w1.date,w2.date) =1;

```

## 分析

主要是掌握MySQL的日期函数。