---
layout: post
title: 白话Java - Double.NaN
date: 2012-06-28 12:49 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究]
thread_key: 704
---
今天处理一个关于Double.NaN的异常。

	Unknown column 'NaN' in 'field list'

**NaN = Not a Number**。就是不是数字。我们用**0/0.0**打印出来的结果就是NaN。

```java
Double d = 0/0.0;
System.out.println(d);
```

JDK的**Double**类里，提供的**NaN**的实现是：

```java
public static final double NaN = 0.0d / 0.0;
```

如果是非零的数除以0.0，得出的是：**Infinity**。正数除以0.0，就是正Infinity，负数就是**-Infinity**。JDK里给出样例是：

```java
    /**
     * A constant holding the positive infinity of type
     * {@code double}. It is equal to the value returned by
     * {@code Double.longBitsToDouble(0x7ff0000000000000L)}.
     */
    public static final double POSITIVE_INFINITY = 1.0 / 0.0;

    /**
     * A constant holding the negative infinity of type
     * {@code double}. It is equal to the value returned by
     * {@code Double.longBitsToDouble(0xfff0000000000000L)}.
     */
    public static final double NEGATIVE_INFINITY = -1.0 / 0.0;
```

用控制台啊打印的结果是：

	Infinity/-Infinity


既然，NaN不是一个数，那他跟任何数比较都不相等，即使跟他自己比较。

```java
System.out.println(Double.NaN == Double.NaN);//输出:false
```

说点通俗的，什么情况下出现NaN？其实这就是数学老师教的那些，没有意义的计算的结果。比如0/0没有意义。老师还教过什么？对啊，负数的平方根啊。所以，用***Math.sqrt(-n)***，算出来的结果，也是**NaN**。

不过有一点，我也不能很好解释的就是***(int) Double.NaN = 0***。。这个，就先这样吧。