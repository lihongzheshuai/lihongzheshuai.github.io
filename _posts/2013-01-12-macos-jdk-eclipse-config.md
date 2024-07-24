---
layout: post
title: Mac OS 下 Java开发环境搭建
date: 2013-01-12 20:04 +0800
author: onecoder
comments: true
tags: [Java]
thread_key: 1280
---
<a href="http://www.coderli.com">OneCoder</a>最近入手一台Mac Pro。其实这个话题本来没什么可写的。但是考虑确实自己开始是不知道的，哪怕是一丁点的收获，也应该记录下来。

其实Java开发环境无非就是安装JDK，安装IDE，配置环境变量。JDK自然从官网下载Mac版的，IDE，<a href="http://www.coderli.com">OneCoder</a>也从Eclipse的官网下载了。安装也是一键安装和解压即可。而且发现JDK安装后，在命令行运行java -version和javac -version直接会识别出你刚才安装的版本是无需配置的。

![](/images/oldposts/11JWWn.jpg)

直接通过eclpse.app启动Eclipse Juno(4.2) 居然报错，寻找Java6版本。但是通过&ldquo;替身&rdquo;eclipse启动是可以启动的。虽然可用，不过OneCoder还是想解决这个问题。
<blockquote>
	<p>
		若要打开&ldquo;Eclipse&rdquo;，您需要 Java SE 6 运行时。您想现在安装一个吗？</p>
</blockquote>

<a href="http://www.coderli.com">OneCoder</a>点击安装后，即可正常使用了。不过网上有人说他点了安装后也无效。这个<a href="http://www.coderli.com">OneCoder</a>就不知道到底是什么原因了。至少那个没有图标样式的替身eclipse是可用的吧。也可以考虑尝试打开Eclipse.app这个项目，编辑里面的eclipse.ini文件，指定vm路径来解决这个问题，不过<a href="http://www.coderli.com">OneCoder</a>并没有亲自验证可行性。只是修改了里面的启动参数，增加了一些内存而已。

