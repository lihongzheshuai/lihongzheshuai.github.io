---
layout: post
title: 导出Maven工程依赖的Jar包
date: 2012-11-22 19:16
author: onecoder
comments: true
tags: [Maven]
categories: [Java技术研究]
thread_key: 1249
---
其实这个本来没什么可写的，只是<a href="http://www.coderli.com">OneCoder</a>恰巧用到又不会，在网上查了一下找到了答案，所以记录一下，也做分享。

很简单，一句话，执行：

```bash
mvn dependency:copy-dependencies -DoutputDirectory=lib   -DincludeScope=compile
```

会将依赖的包拷贝到工程的lib目录下。