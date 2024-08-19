---
title: LeetCode Second Highest Salary
tags: [LeetCode,SQL]
categories: [算法学习]
date: 2017-12-20 22:19:24 +0800
comments: true
author: onecode
---
# Problem

Write a SQL query to get the second highest salary from the Employee table.

```
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
```
For example, given the above Employee table, the query should return 200 as the second highest salary. If there is no second highest salary, then the query should return null.
```
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
```

即找到第二大的元素。没有返回null。
<!--break-->

# MySQL

``` sql
# Write your MySQL query statement below
SELECT (SELECT DISTINCT Salary FROM Employee ORDER BY Salary DESC LIMIT 1 OFFSET 1) AS SecondHighestSalary;

```

## 分析

通过LIMIT OFFSET找到第二个元素。DISTINCT是为了排除两个最大值的情况。嵌套是为了解返回null的情况。另一种办法是使用IFNULL函数。