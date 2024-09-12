---
layout: post
title: 一起学Java(13)-[日志篇]教你分析SLF4J和Log4j2源码，掌握SLF4J与Log4j2无缝集成原理
date: 2024-09-04 08:00 +0800
author: onecoder
image: /images/post/java-go-13/log4j2-slf4j2-provider.png
comments: true
tags: [Java, Log, SLF4J, 一起学Java]
categories: [一起学Java系列,（2）引入日志篇]
---
研究完`SLF4J`和`Logback`这种无缝集成的方式([一起学Java(12)-[日志篇]教你分析SLF4J源码，掌握SLF4J如何与Logback无缝集成的原理](https://www.coderli.com/java-go-12-import-log-four-logback/))，继续研究`Log4j2`和`SLF4J`这种需要桥接集成的方式。

<!--more-->

## 一、Log4j2如何实现SLF4JServiceProvider接口

我们已经知道SLF4J利用`ServiceLoader`机制，去寻找和加载`SLF4JServiceProvider`接口的实现类，而`Log4j2`原生是没有实现这个接口的，因此需要借助桥接机制，将`Log4j2`集成到`SLF4J`中，这个桥接包就是`log4j2-slf4j2-provider`。

![log4j2-slf4j2-provider](/images/post/java-go-13/log4j2-slf4j2-provider.png)

在桥接包中，找到`META-INF/services`目录，可以看到`org.slf4j.spi.SLF4JServiceProvider`文件，内容如下：

```plaintext
org.apache.logging.slf4j.Log4jLoggerFactory
```

这就是`Log4j2`对`SLF4JServiceProvider`接口的实现。

在实现中，返回了`Log4jLoggerFactory`，这个类是`Log4j2`的工厂类，用于创建`Logger`对象。这个工厂类是桥接包中的类。
