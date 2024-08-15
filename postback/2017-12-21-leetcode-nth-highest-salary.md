---
title: LeetCode Nth Highest Salary
tags: [LeetCode,SQL]
date: 2017-12-21 09:14:24 +0800
comments: true
author: onecode
---
# Problem

Write a SQL query to get the nth highest salary from the Employee table.

```
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
```
For example, given the above Employee table, the nth highest salary where n = 2 is 200. If there is no nth highest salary, then the query should return null.
```
+------------------------+
| getNthHighestSalary(2) |
+------------------------+
| 200                    |
+------------------------+
```
[上一个问题][1]的推广，找到第N大的元素
<!--break-->

# MySQL

``` sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  SET N = N - 1;
  RETURN (
      # Write your MySQL query statement below.
      SELECT DISTINCT Salary FROM Employee ORDER BY Salary DESC LIMIT 1 OFFSET N
  );
END

```

## 分析

解题思路一致，不过是改成个自定义函数而已。


  [1]: http://www.coderli.com/leetcode-second-highest-salary/