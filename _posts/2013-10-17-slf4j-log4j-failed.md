---
layout: post
title: slf4j+log4j2 控制台输出错误解决
date: 2013-10-17 20:12 +0800
author: onecoder
comments: true
tags: [Log4j,SLF4J]
categories: [Java技术研究]
thread_key: 1530
---
<blockquote>
	<p>
		SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
		SLF4J: Defaulting to no-operation (NOP) logger implementation
		SLF4J: See <u>http://www.slf4j.org/codes.html#StaticLoggerBinder</u> for further details.</p>
</blockquote>

在使用log4j2+slf4j的时候遇到这个错误提示，这不到类。在slf4j的官网有正好有相应的说明。需要添加依赖包

<blockquote>
	<p>
		slf4j-api-1.7.5.jar
		slf4j-simple-1.7.5.jar
	</p>
</blockquote>

在Gradle的build.gradle配置文件种添加依赖

```groovy
dependencies{
compile(
"org.apache.logging.log4j:log4j-api:$log4j_version",
"org.apache.logging.log4j:log4j-core:$log4j_version",
"org.slf4j:slf4j-api:$slf4j_version",
"org.slf4j:slf4j-simple:$slf4j_version"
)}
```

刷新工程。再次输出，问题解决。

