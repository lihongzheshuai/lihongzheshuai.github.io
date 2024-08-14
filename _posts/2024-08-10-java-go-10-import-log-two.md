---
layout: post
title: 一起学Java(10)-为项目引入Log框架(Log篇二-引入SLF4J接口层框架)
date: 2024-08-10 22:04 +0800
author: onecoder
comments: true
tags: [Java,Log,SLF4J,一起学Java]
categories: [Java,Log,SLF4J,一起学Java]
---
在上一节[***一起学Java(9)-为项目引入Log框架(Log篇一-框架演进和设计逻辑)]***(https://www.coderli.com/java-go-9-import-log-one/)中，我们已经理清了Java日志框架的演进过程、设计思想和核心框架。从这节开始，进入实战研究环节。

<!--more-->

回顾下Java日志框架的设计结构。

![Java日志设计](/images/post/java-go-9/java-log-bridge.svg)

先研究接口层框架`SLF4J`。

## 一、引入***SLF4J***

在[***一起学Java(9)-为项目引入Log框架***](https://www.coderli.com/java-go-9-import-log-one/)中，我们已经分析过了，对于Java接口层来说，`SLF4J`几乎已经是实时的标准和唯一选择。目前官方(官网地址:[https://www.slf4j.org/](https://www.slf4j.org/))最新稳定版是**2.0.16**，发布于2024年8月10日。

**通过Gradle引入最新版`SLF4J`**，修改`build.gradle.kts`文件：

```kotlin
dependencies {
    implementation("org.slf4j:slf4j-api:2.0.16")
}
```