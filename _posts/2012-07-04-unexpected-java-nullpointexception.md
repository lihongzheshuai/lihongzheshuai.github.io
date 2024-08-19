---
layout: post
title: 一个容易忽略的Java空指针问题
date: 2012-07-04 11:37 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究]
thread_key: 835
---
今天有人提出了代码中一个的**NullPointException**问题。这类问题，很好解决，找到所在行，一看便知。

但是这次，有点意外。抛异常的行，只是一个简单的**Pojo**的**get**、**set**方法。出错的行在

```java
a.setSize(b.getSize());
```

很自然的想到**b**会为**null**。但是前面的代码已经用过**b**了，也就是说，如果**b**是**null**。早就抛出空指针了。**a**是新**new**的。不会是**null**。se****t方法内部也只是赋值。

```java
this.size = size
```
	
一时间，我迷惑了。再仔细看代码，发现b**.getSize**获取的类型是**Long**。而**a.setSize**，传入的类型是**long**。

这种包装类到基本类型的转换，是会导致空指针的发生的。到此，bug是定位了。但是，你不想知道为什么这种强转会抛空指针吗？首先，应该想到的是，通俗的说，**NullPointException**的一般情况，就是用null对象调用方法。那么自然联想到，这里究竟是调用了什么方法？很简单，看编译过的字节码便知：

```class
  1  astore_1 [l]
     2  aload_1 [l]
     3  invokevirtual java.lang.Long.longValue() : long [16]
     6  lstore_2 [m]
```

原来这种强转是调用了**Long**中的**longValue()**方法。自然符合用null对象调用方法，抛出空指针异常，也就不奇怪了。