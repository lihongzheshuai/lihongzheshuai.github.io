---
layout: post
title: 自定义实现log4j的appender
date: 2013-09-17 20:17 +0800
author: onecoder
comments: true
tags: [Log4j]
categories: [Java技术研究,Log]
thread_key: 1497
---

log4j，应用最广泛的日志框架。其作者后来推出logback，也是好选择。不多说废话。

log4j组件介绍  
Log4j主要有三个组件：
	Logger：负责供客户端代码调用，执行debug(Object msg)、info(Object msg)、warn(Object msg)、error(Object msg)等方法。  
	Appender：负责日志的输出，Log4j已经实现了多种不同目标的输出方式，可以向文件输出日志、向控制台输出日志、向Socket输出日志等。  	Layout：负责日志信息的格式化。

log4j默认提供了很多Appender，如org.apache.log4j.ConsoleAppender，FileAppender等。不过，如果有特殊的需求，就需要自定义实现，比如把日志发送到Flume中。我们的需求正是如此。

自定义一个Appender很简单，只需继承AppenderSkeleton类，并实现几个方法即可。

```java
@Override
     protected void append(LoggingEvent event) {
         System.out.println("OneCoder: " + event.getMessage());
     }

     @Override
     public void close() {
           // TODO Auto-generated method stub
     }

     @Override
     public boolean requiresLayout() {
           // TODO Auto-generated method stub
           return false ;
     }
```

上述代码的效果就是将原信息再开头加上"OneCoder"。我们想要发送到Flume里，也只需在该方法里添加Flume客户端的相关实现即可。这样你的系统日志就灵活多了。

当然，想要生效你需要修改log4j的配置文件，将appender改为你自己实现的appender即可。

