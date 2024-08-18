---
title: LeetCode Delete Duplicate Emails
tags: [LeetCode,SQL]
date: 2017-12-29 13:42:24 +0800
comments: true
author: onecode
---
# Problem

Write a SQL query to delete all duplicate email entries in a table named Person, keeping only unique emails based on its smallest Id.

```
+----+------------------+
| Id | Email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
Id is the primary key column for this table.
```
For example, after running your query, the above Person table should have the following rows:
```
+----+------------------+
| Id | Email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
```

删除邮件重复的记录，保留Id最小的

<!--break-->

# MySQL

``` sql

DELETE p1 FROM Person p1, Person p2 WHERE p1.Email = p2.Email AND p1.Id > p2.Id;

```

## 分析

无