---
title: LeetCode Employees Earning More Than Their Managers
tags: [LeetCode,SQL]
date: 2017-12-21 09:33:24 +0800
comments: true
author: onecode
---
# Problem

The Employee table holds all employees including their managers. Every employee has an Id, and there is also a column for the manager Id.

```
+----+-------+--------+-----------+
| Id | Name  | Salary | ManagerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | NULL      |
| 4  | Max   | 90000  | NULL      |
+----+-------+--------+-----------+
```
Given the Employee table, write a SQL query that finds out employees who earn more than their managers. For the above table, Joe is the only employee who earns more than his manager.
```
+----------+
| Employee |
+----------+
| Joe      |
+----------+
```
找到比Manager薪水高的雇员
<!--break-->

# MySQL

``` sql

SELECT e1.Name AS Employee FROM Employee e1 INNER JOIN Employee e2 ON e1.ManagerId = e2.Id WHERE e1.Salary > e2.Salary;

```

## 分析

通过Join解决问题