---
layout: post
title: Lombok与Java9兼容性问题
tags: [Java,Lombok]
categories: [Java技术研究]
date: 2017-09-23 17:00:35 +0800
comments: true
author: onecoder
thread_key: 1910
---
很久没更新博客，本想写篇关于Java9 集合工厂函数的博客，却没想到阴差阳错先遇到Lombok与Java9的兼容性问题。

<!--break-->

我在一个试验用的工程里，想做一些关于Java9新特性的试验，该工程原本是依赖lombok的。结果，编译时，原有的使用**@Slf4j**注解的的类报编译错误。

>
Error:(18, 1) java: 程序包 javax.annotation 不可见
  (程序包 javax.annotation 已在模块 java.xml.ws.annotation 中声明, 但该模块不在模块图中)

这首先就证明了，Java9对来老项目是不能轻易升级的。有很多的代码、依赖库需要更新、重写。

我尝试增加一个module-info.java根据提示，require相应的module试图解决该问题。

```
module httpserver {
    requires java.xml.ws.annotation;
    requires lombok;
}
```

结果，在IDE中没有错误提示，但是编译运行时，由Lombok生成的log会报错

>
Error:(32, 13) java: 找不到符号
  符号:   变量 log
  位置: 类 com.coderli.http.server.SimpleHttpServer

我查询了Lombok的ISSUE，发现如下讨论：

**Add jdk9 compiler support**  
[https://github.com/rzwitserloot/lombok/issues/985](https://github.com/rzwitserloot/lombok/issues/985)

并且，进一步测试我发现一个问题。就是，只要我声明了一个module，并且在Maven中声明依赖lombok，即使我没有使用任何lombok注解。都会报如下错误：

>
Error occurred during initialization of boot layer
java.lang.module.FindException: Unable to derive module descriptor for /Users/apple/.m2/repository/org/projectlombok/lombok/1.16.14/lombok-1.16.14.jar
Caused by: java.lang.module.InvalidModuleDescriptorException: Provider class lombok.eclipse.handlers.HandleAccessors not in module

官方也有对应issue#1361
work not good with java 9 #1361  
[https://github.com/rzwitserloot/lombok/issues/1361](https://github.com/rzwitserloot/lombok/issues/1361)

Lombok在Java9下，基本算是无法使用了。

补充：发现issue1361是关闭状态。我提交了一个new issue#1470
[https://github.com/rzwitserloot/lombok/issues/1470](https://github.com/rzwitserloot/lombok/issues/1470)