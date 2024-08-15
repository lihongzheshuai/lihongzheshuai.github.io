---
title: LeetCode Duplicate Emails
tags: [LeetCode,SQL]
date: 2017-12-21 09:43:24 +0800
comments: true
author: onecode
---
# Problem

Write a SQL query to find all duplicate emails in a table named Person.

```
+----+---------+
| Id | Email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
```
For example, your query should return the following for the above table:
```
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
```
找到重复的Email。
<!--break-->

# MySQL

``` sql

SELECT Email FROM Person GROUP BY Email HAVING COUNT(Email) > 1;

```

## 分析

无