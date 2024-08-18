---
layout: post
title: 教你打包Java程序，jar转exe随处可跑
date: 2012-06-16 11:51 +0800
author: onecoder
comments: true
tags: [Java]
thread_key: 499
---
发现很多人问如何把Jar转成exe程序。可能是想双击运行和随处运行。其实这个并不难，我就简单总结几种方法，供大家参考，关键还是要知其所以然。

Java程序的运行不可能脱离JRE，不管你是Jar包还是exe程序。这点你必须了解。那么在没有JRE的机器上你的程序怎么跑？很简单，在你程序里带一份JRE就行了。

先介绍集中打包的方法。以**Eclipse**为例，最简单直接的方法，选择你想打包的程序，右键**export...**

![](/images/post/jar-to-exe/export.jpg)

选择**Runnable Jar file**。（即可执行的Jar包）	

![](/images/post/jar-to-exe/runnable-jar.jpg)

选择你程序的主类，就是还有**Main**函数的类。点Finish即可。

在你的机器上，设置好Jar文件的打开方式（别默认用解压缩的工具打开就行），双击即可运行。

![](/images/post/jar-to-exe/4fun.jpg)

这个跟在命令行执行命令的效果是一样的。

```sh
java -jar forfun.jar
```

其实一个Jar能运行，关键还是配置Jar内部的**MANIFEST.MF**文件。该文件存在于Jar包根目录的**META-INF**文件夹内。主要由于指定**主类(Main)**的位置：

```properties
Manifest-Version: 1.0
Main-Class: one.coder.jdk.JDKMain
```

版本可以自己指定，默认生成是1.0。主类位置需要指定。

> 注意:Main-Class的冒号后，要跟一个空格。

如果你还有要依赖的Jar包，则可以配置**Class-Path**来指定。

```properties
Class-Path: ./ logback-core-0.9.29.jar junit-4.9.jar slf4j-api-1.6.1.jar logback-classic-0.9.29.jar hamcrest-core-1.1.jar
```

知道了这些，我们再打开刚才生成的Jar文件，你可能发现多了一些Eclipse的东西，并且主类变成了

```properties
Main-Class: org.eclipse.jdt.internal.jarinjarloader.JarRsrcLoader
```

也就是通过**Eclipse**提供的这个主类来加载的你程序。如果你不喜欢这样，将其去掉。自己进行配置。笔者通过一个不依赖任何Jar包的小程序进行说明。

![](/images/post/jar-to-exe/run-haoyajar.jpg)

这是笔者打出Jar的内部截图，去掉所有跟我的程序不相关的东西。**MANIFEST.MF**的配置也很简单。

```properties
Manifest-Version: 1.0
Main-Class: one.coder.jdk.JDKMain
```
	
在有**JRE**的机器上，双击一样可以运行。

> 注：这里需要提一下，尽量不用用解压软件自带的编辑器进行编辑，如果你编辑后发现不能运行，提示打开jar错误等信息，很可能是由于你编辑的**MANIFEST.MF**文件的编码错误。导致无法解析。默认是采用ANSI编码格式的。不要改成UTF-8等。笔者被这个问题，困扰了近半个小时。
	
接下来说说在没有JRE的机器上怎么办？最简单的手动的办法就是写一个**bat**脚本。并且带一份**jre**在你的程序里。

![](/images/post/jar-to-exe/bat-jar.jpg)

把图中的三个文件，放入同一个文件夹中。**start.bat**内容如下:

```sh
.\jre7\bin\java -jar .\run.jar
```	

说白了就是调用**jre**中的**java**命令，执行指定的jar程序。 双击**start.bat**，执行成功。

如果你非要打成**exe**程序，笔者推荐一个工具**JSmooth**。简单好用。同样这也肯定是需要JRE指定的。关于JSmooth的教程，笔者找到了一个不错的教学贴：<a href="http://yisufuyou.iteye.com/blog/403556" target="_blank">http://yisufuyou.iteye.com/blog/403556</a> 按照里面的步骤，你一定可以成功。		

![](/images/post/jar-to-exe/jsmooth.jpg)

说了这么多，如果还有什么不明白的，可以给我留言，一起讨论研究。 

- ***PS1***：默认的**JRE**体积实在太大，你可以考虑精简JRE还节约空间，这部分内容，不在本文讨论。另外，如果你想把你的软件做成安装包的形势，可考虑<a href="http://www.flexerasoftware.com/products/installanywhere.htm" target="_blank">**InstallAnyWhere**</a>这个工具。
	
- ***PS2：***笔者研究的过程中，为了模拟没有JRE的环境，真是百般折腾，因为笔者把所有环境变量都删掉，还有可以运行。不知道是不是从**JDK7**开始，Java居然在我的**System32**路径下，也放置**Java.exe**等程序，也就是说，不用配置Path了。jre路径的指定，貌似也写入了注册表，不过这点，笔者没有亲自证实，只是在注册表中简单的搜索了一下，仅发现了JavaFX的配置和一些其他的Java配置，没有深入研究，不好定论。有兴趣可以研究下，也麻烦告诉我一声。