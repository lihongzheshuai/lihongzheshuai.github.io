---
title: LeetCode Combine Two Tables
tags: [LeetCode,SQL]
date: 2017-12-20 17:01:24 +0800
comments: true
author: onecode
---
# Problem

Table: Person

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| PersonId    | int     |
| FirstName   | varchar |
| LastName    | varchar |
+-------------+---------+
PersonId is the primary key column for this table.
```
Table: Address
```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| AddressId   | int     |
| PersonId    | int     |
| City        | varchar |
| State       | varchar |
+-------------+---------+
AddressId is the primary key column for this table.
```
Write a SQL query for a report that provides the following information for each person in the Person table, regardless if there is an address for each of those people:
```
FirstName, LastName, City, State
```

意外进入SQL题了
<!--break-->

# MySQL

``` sql

Select FirstName, LastName, City, State FROM Person LEFT JOIN Address ON Person.PersonId = Address.PersonId;

```

## 分析

正好符合left join的语义。