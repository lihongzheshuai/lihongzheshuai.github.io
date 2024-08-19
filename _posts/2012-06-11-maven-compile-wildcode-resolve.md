---
layout: post
title: Maven编译报错乱码问题和编译问题解决
date: 2012-06-11 20:07 +0800
author: onecoder
comments: true
tags: [Maven]
categories: [Java技术研究,Maven]
thread_key: 412
---
最近需要用Maven打包工程，却不想遇到乱码问题。在Eclipse中通过Maven Plugin执行install 命令报错如下：	

> [ERROR] Failure executing javac, but could not parse the error:"一串乱码"

错误信息都是乱码，问题解决起来就头疼了。所以决定先解决乱码问题。经过一番搜索排查终于找到了办法：

在控制面板的，区域和语言中，将非Unicode语言改为英语美国即可。

![](/images/post/maven-compile-encode/language-setting.jpg)

(注：笔者系统为win7，xp听说没这个选项？如果没有，改位置的里的信息试试。同理，如果你已经是英语了但是还乱码，那就改成中文的，总之取决于你的Maven环境和你的系统语言的匹配。)

改后重启，再编译，错误信息出来了：

>[ERROR] Failure executing javac, &nbsp;but could not parse the error:The system cannot find the path specifie.

第一反映就是检查path里配置，用：	

```sh	
echo %path%
```

打印path里的结果，没什么问题。
	
猛然间，OneCoder想起，我们的Maven工程里，自定义了一个变量，用于工程编译的

>org.apache.maven.plugins maven-compiler-plugin 2.3.2 true true ${JAVA_1_6_HOME}/bin/javac 1.6 1.6 1.6 

这是强制大家用1.6版本JDK进行工程编译。这个变量是在各自Maven setting.xml文件中赋值的。

```sh
compiler C:/Program Files/Java/jdk1.6.0_30 
```

问题就在这，笔者最近升级了1.6版本的jdk到32，而这里还配置的30的路径，自己找不到了。将这里的值改为正确的路径。再次编译，成功！