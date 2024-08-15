---
layout: post
title: Gradle 使用Maven本地缓存库
date: 2013-10-08 21:20 +0800
author: onecoder
comments: true
tags: [Gradle]
thread_key: 1520
---
从Maven切换到Gradle，原有的几G的本地缓存库当然想继续使用。在用户手册中找到了答案。在50.6.3章节。

如果想使用Maven本地缓存，需要定义：

```groovy
repositories {
    mavenLocal()
}
```

Gradle使用与Maven相同的策略去定位本地Maven缓存的位置。如果在settings.xml中定义了本地Maven仓库的地址，则使用该地址。在USER_HOME/.m2下的settings.xml文件中的配置会覆盖存放在M2_HOME/conf下的settings.xml文件中的配置。如果没有settings.xml配置文件，Gradle会使用默认的USER_HOME/.m2/repository地址。

