---
layout: post
title: log4j自定义appender实现，处理异常堆栈
date: 2013-10-12 22:53 +0800
author: onecoder
comments: true
tags: [Log4j]
categories: [Java技术研究]
thread_key: 1524
---
在项目中需要自定义实现一个log4j的appender。根据log中MDC里的信息，构造日志存储的目录结构。自定义实现log4j appender的方法已经介绍过了。主要是覆盖AppenderSkeleton中的appender方法。

```java
@Override
      protected void append(LoggingEvent event) {
           this .logEvent = event;
     }
```

日志内容的获取和格式处理，通过Layout进行格式化

```java
this .getLayout().format(event).getBytes( DEFAULT_CS )
```

这里有个问题，一般情况下，我们常用的**org.apache.log4j.PatternLayout**是不会处理异常堆栈的。因为，其内部的方法，返回的是true。

```java
public  boolean ignoresThrowable () {
    return true ;
  }
```

在这种情况，如果你的日志里有异常对象，如**logger.error("错误信息。", e)** 那么e将会被忽略。这时候需要我们自己处理。处理方式如下：

```java
if (layout .ignoresThrowable()) {
      String[] s = event.getThrowableStrRep();
      if (s != null ) {
      int len = s. length;
      for( int i = 0; i < len; i++) {
           // 处理异常堆栈，比如记录到日志文件中
     }
```