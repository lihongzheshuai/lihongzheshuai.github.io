---
layout: post
title: Eclipse4.2 Juno + Tomcat7.0.30启动Tomcat报APR版本错误问题解决
date: 2012-09-28 15:13 +0800
author: onecoder
comments: true
tags: [Tomcat]
categories: [知识扩展]
thread_key: 1158
---
本来<a href="http://www.coderli.com">OneCoder</a>是在一遍搭建一个J2EE的开发环境，一遍记录过程以跟大家分享。没想到这个过程中，遇到了很多细节的错误，考虑到如果和原来的主线任务文章混在一起，有点让人不知所措的感觉，所以<a href="http://www.coderli.com">OneCoder</a>决定把这些问题的解决过程单独记录下来，以跟大家分享。

在Eclipse中启动Tomcat，启动开始有如下信息提示。

> 九月 28, 2012 10:18:12 上午 org.apache.catalina.core.AprLifecycleListener init<br>
> SEVERE: An incompatible version 1.1.20 of the APR based Apache Tomcat Native library is installed, while Tomcat requires version 1.1.24

先是一堆这样的错误。意思很明显，APR的版本不够。去<a href="http://archive.apache.org/dist/tomcat/tomcat-connectors/native/1.1.24/binaries">http://archive.apache.org/dist/tomcat/tomcat-connectors/native/1.1.24/binaries</a>
	
下载 一个1.1.24版。网上有人说扔到Java的bin下就好用，那我想扔到System32下也一定可以了，呵呵，一试果然奏效。其实<a href="http://www.coderli.com">OneCoder</a>猜测，有这个问题主要还是因为Eclipse自带的wtp的插件没支持到最新的tomcat7导致的。貌似只支持到7.0.12。<a href="http://www.coderli.com">OneCoder</a>肯定不会满足于就这样不明不白的好用了，tomcat/bin下明明有个文件，并且已经是最新的，为什么还要在别的地方乱扔一个。</div>

看一下tomcat的源码，发现在原来是从

```java
String path = System.getProperty("java.library.path")
```

配置中读取dll文件的位置。这就简单了，给tomcat增加一个启动参数即可：

> -Djava.library.path="D:\Develop Software\apache-tomcat-7.0.30\bin"

再启动，果然好用了。