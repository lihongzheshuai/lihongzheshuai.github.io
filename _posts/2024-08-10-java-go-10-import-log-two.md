---
layout: post
title: 一起学Java(10)-为项目引入Log框架(Log篇二-引入SLF4J接口层框架)
date: 2024-08-10 22:04 +0800
author: onecoder
comments: true
tags: [Java,Log,SLF4J,一起学Java]
categories: [Java,Log,SLF4J,一起学Java]
---
在上一节[***一起学Java(9)-为项目引入Log框架(Log篇一-框架演进和设计逻辑***](https://www.coderli.com/java-go-9-import-log-one/)中，我们已经理清了Java日志框架的演进过程、设计思想和核心框架。从这节开始，进入实战研究环节。

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

按照[SLF4J官方文档](https://www.slf4j.org/manual.html)，编写代码如下:

```java
package com.coderli.one.log;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author OneCoder
 * @Blog https://www.coderli.com
 */
public class LogMain {
    public static void main(String[] args) {
        Logger logger = LoggerFactory.getLogger(LogMain.class);
        logger.info("Hello World");
    }
}
```

直接运行代码，提示错误：

```
SLF4J(W): No SLF4J providers were found.
SLF4J(W): Defaulting to no-operation (NOP) logger implementation
SLF4J(W): See https://www.slf4j.org/codes.html#noProviders for further details.
```

这个信息的意思是，`SLF4J` 没有找到实际的日志实现库，因此它将默认使用一个“无操作”的日志实现，即不会输出任何日志信息。因为，前面我们已经提到`SLF4J`只是一个日志接口层框架，想要运行它需要引入一个日志实现层框架来提供具体的日志实现。常见在上篇[一起学Java(9)-为项目引入Log框架](https://www.coderli.com/java-go-9-import-log-one/)已经分析过了，不再赘述，这里我们先直接选用同一个作者，无缝衔接`Logback`作为日志实现层，后续我们在体验`Log4j 2`的实现方式。当前`Logback`最新稳定版位d。

修改`build.gradle.kts`中的依赖引入部分

```kotlin
    dependencies {
        implementation("org.slf4j:slf4j-api:2.0.16")
        implementation("ch.qos.logback:logback-classic:1.5.6")
    }
```

重新执行代码，成功得到输出：

```
21:35:48.876 [main] INFO com.coderli.one.log.LogMain -- Hello World
```

至此，一个最简单SLF4J+Logback的项目日志框架方案就引入完成了。依赖只有两个接口层的slf4j-api和实现层的logback-classic，没有那一大堆乱七八糟的jar。

当然，实际项目中日志使用比这个样例复杂的多，需要根据项目需要进行日志框架的配置，这些是日志实现层框架提供的功能。Logback自然也支持更为复杂的应用配置，具体需要通过logback-test或logback文件配置实现，这个我们后续会慢慢研究。

对我而言，下一步，我更好奇的是，在没引入logback-classic时，程序怎么输出的那段错误信息，以及在引入了logback后，程序怎么自动找到的日志实现，正常输出。下一节，我会研究这部分内容。

项目的整体配置和上述代码以同步提交到Github上：[https://github.com/lihongzheshuai/java-all-in-one](https://github.com/lihongzheshuai/java-all-in-one)，可以同步更新。项目的整体结构也进行了调整，后续择机进行这部分的介绍。

最近很忙，更新慢了，见谅。

喝酒，走肾
写码，走心