---
layout: post
title: log4j 控制台和文件输出乱码问题解决
date: 2012-07-05 23:10 +0800
author: onecoder
comments: true
tags: [Log4j]
categories: [Java技术研究]
thread_key: 843
---

一个小问题，却让我感觉到，现在真正动脑的人很少。。我来说说吧。

今天遇到一个小问题，log4j输出到文件乱码，控制台正常。显然是编码问题导致。Google一搜，几乎一水的说：

> 项目中**log4j**在英文版linux下输出中文日志为乱码。由于**log4j**配置文件中没有设置编码格式(encoding)，所以log4j就使用系统默认编码。导致乱码。解决方法是设置编码格式**UTF-8**,方法为：
> 
```properties
log4j.appender.syslog.encoding=UTF-8
```

这显然是转的，因为全网几乎一样。先不说这是**properties**配置的，还不是**xml**的。如果要xml的，配置如下：

```xml
<appender name="A1" class="org.apache.log4j.RollingFileAppender">
        <param name="Encoding" value="UTF-8" />
        <param name="File" value="all.log" />
        ......
</appender>
```

但是，我是已经设置成UTF-8，而乱码了。所以，上述答案是不严谨的。

先说说笔者的情况吧，其实笔者的问题很简单，两套log4j appender配置，一个输出的文件，一个控制台，文件的配置了utf-8编码，控制台没配置。现象，控制台正常，文件乱码。

把文件的改成**gbk**，不乱了。控制台改成**gbk**，乱码。控制台改成**utf-8**，正常。到这里你可能糊涂了。怎么这么乱？

其实道理很简单，乱码，自然是编码不匹配。什么匹配？**log4j**用**utf-8**输入，你文件是不是**utf-8**编码的呢？检查一下，果然不是，改成**utf-8**编码，解决。

你可能要问了，那控制台的匹配在哪里？Eclipse控制台也有是编码的，而且，不仅仅是有，你还可以为每个执行的程序，设置独立的编码。

![](/images/post/log4j-console/console-config.png)

自然，这里的编码匹配了，也就不会乱码了。