---
layout: post
title: 一起学Java(13)-[日志篇]教你分析SLF4J和Log4j2源码，掌握SLF4J与Log4j2无缝集成原理
date: 2024-09-04 08:00 +0800
author: onecoder
image: /images/post/java-go-13/log4j2-slf4j2-provider.png
comments: true
tags: [Java, Log, SLF4J, Log4j, 一起学Java]
categories: [一起学Java系列,（2）引入日志篇]
---
研究完`SLF4J`和`Logback`这种无缝集成的方式([一起学Java(12)-[日志篇]教你分析SLF4J源码，掌握SLF4J如何与Logback无缝集成的原理](https://www.coderli.com/java-go-12-import-log-four-logback/))，继续研究`Log4j2`和`SLF4J`这种需要桥接集成的方式。

<!--more-->

