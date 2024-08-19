---
layout: post
title: 未初始化的String相 "+" 为什么会打印出“nullnull"
date: 2012-06-14 21:13 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究]
thread_key: 474
---
今天在我的一个qq群里有人问了这样一个问题。

```java
private static String a;

private static String b;

public static void main(String[] args) {

    String c = a+b;

    System.out.println(c);

}
```

输出是**nullnull**。问为什么是这样。

其实问题并不复杂，很多同学也觉得自己知道原因，遂不予关注。但是我相信还是有初学Java的同学在这里是存在误会的。很典型的误会就是如一个群里的朋友说的String类型的变量如果没有显示初始化，默认的值就是"null"。支持的理由就是

```java
private static String a;

public static void main(String[] args) {

System.out.println(a);

}
```

输出是**null**。

这个现象确实很容易迷惑一些初学的人，包括我也忽略了挺久。其实呢证明这种想法错误很简单。如果默认值是**null**，那么就意味着，该变量不是空(**null**)。而是字符串的**"null"**。

```java
private static String a;

public static void main(String[] args) {

System.out.println(a==null);

System.out.println("null".equals(a));

}
```

上述代码输出分别是**true**,**false**。（呵呵，挺弱智的。）

说明String类型变量a，其实是空(**null**)，而并没有被赋值。那么打印出null是为什么呢？我们查看**PrintStream**的源码就很清晰的明白了，其实是Java在**println**的时候进行了处理。

```java
public void print(String s) {

if (s == null) {

s = "null";

}

write(s);

}
```

回到开头的问题，既然没有初始化赋值，那么输出为什么是"**nullnull**"，两个"**null**"连接的结果呢。这里略微细说一下，查看编译过的class文件，我们可以看到

```class
public static void main(java.lang.String[] args);

0 new java.lang.StringBuilder [19]

3 dup

4 getstatic cn.home.pratice.jdk.string.StringMain.a : java.lang.String [21]

7 invokestatic java.lang.String.valueOf(java.lang.Object) : java.lang.String [23]

10 invokespecial java.lang.StringBuilder(java.lang.String) [29]

13 getstatic cn.home.pratice.jdk.string.StringMain.b : java.lang.String [32]

16 invokevirtual java.lang.StringBuilder.append(java.lang.String) : java.lang.StringBuilder [34]

19 invokevirtual java.lang.StringBuilder.toString() : java.lang.String [38]

22 astore_1 [c][/c]

23 getstatic java.lang.System.out : java.io.PrintStream [42]

26 aload_1 [c][/c]

27 invokevirtual java.io.PrintStream.println(java.lang.String) : void [48]

30 return System.out.println(c);

}
```

String的相加实际在变异后被处理成了**StringBuilder**的**append**.(注：我的JDK是**1.6.0_u29**)。那么好，我们就应该查看**StringBuilder**的源码，发现是调用的父类里的方法，继续查看，道理就在这里。

```java
public StringBuilder append(String str) {

super.append(str);

return this;

}

public AbstractStringBuilder append(String str) {

if (str == null) str = "null";

int len = str.length();

if (len == 0) return this;

int newCount = count + len;

if (newCount &gt; value.length)

expandCapacity(newCount);

str.getChars(0, len, value, count);

count = newCount;

return this;

}
```

原来也是对空**null**，进行了特殊的处理，那么输出是"**nullnull**"，自然也就明白了。

这里我想说的是，很多问题，可能表面上很简单，或者我们可能会有很多想当然的想法，不过还是眼见为实，而且所有代码都放在那里，我们为什么不勤快的多翻开看看其中的实现，道理自然就在眼前。多动手，丰衣足食：）
