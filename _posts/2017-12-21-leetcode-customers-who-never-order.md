---
title: LeetCode Customers Who Never Order
tags: [LeetCode,SQL]
date: 2017-12-21 09:55:24 +0800
comments: true
author: onecode
---
# Problem

Suppose that a website contains two tables, the Customers table and the Orders table. Write a SQL query to find all customers who never order anything.

Table: Customers.

```
+----+-------+
| Id | Name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+
```
Table: Orders.
```
+----+------------+
| Id | CustomerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+
```
Using the above tables as example, return the following:

```
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
```

即找到没有订单的客户

<!--break-->

# MySQL

## 解法一

``` sql

SELECT Name AS Customers FROM Customers c WHERE c.Id NOT IN (SELECT CustomerId FROM Orders);

```

## 解法二
``` sql

SELECT Customers FROM (SELECT c.Name AS Customers, o.Id AS oid FROM Customers c LEFT JOIN Orders o ON c.Id = o.CustomerId) AS r WHERE r.oid IS NULL;
```


## 分析

无