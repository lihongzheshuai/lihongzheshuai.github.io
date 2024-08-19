---
layout: post
title: Logback控制台输出类名行号带链接的Pattern配置
date: 2012-06-14 23:28 +0800
author: onecoder
comments: true
tags: [Logback]
categories: [Java技术研究,Log]
thread_key: 476
---
从**log4j**切换到**logback**会发现，原来在log4j使用的日志格式 ***%l*** 的功能不见了。Eclipse控制台的输出，不再带有可快速进入的链接了。

在**logback**里，需要使用***%c%L***才能打印出完整的类路径和行号。但是却没有链接。查阅了一下，发现了**caller**这个Pattern。配置好***caller：%caller{1}***后，链接终于又出现了。效果如下：

![](/images/post/logback-console-link/console.jpg)

虽然感觉上，没原来的好看了，不过好歹，这个功能是有了。如果你想去掉烦人的**Caller+0**字样，还可以继续使用**replace**进行替换。

附上笔者使用的**logback pattern**配置：

```xml
%d{yyyy/MM/dd-HH:mm:ss} %level [%thread] %caller{1} - %msg%n
```

关于***logback pattern*** 转换符的说明，我找到了这个帖子，说的还是比较详细的

- <a href="http://aub.iteye.com/blog/1103685" target="_blank">http://aub.iteye.com/blog/1103685</a>