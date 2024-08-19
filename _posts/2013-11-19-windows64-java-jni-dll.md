---
layout: post
title: Java JNI Windows64位系统下 使用32位的dll
date: 2013-11-19 22:50 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究]
thread_key: 1544
---
<p>
	今天遇到在处理一个多classloader调用本地native方法报错的问题的时候，想要通过调用本地的一个dll进行测试。该dll是在32位环境下编译的。而<a href="http://www.coderli.com">OneCoder</a>的调试机器是64位的win7。自然调用会报如下错误：</p>
<blockquote>
	<p>
		Can&rsquo;t load IA 32-bit .dll on a AMD 64-bit</p>
</blockquote>
<p>
	错误信息很明显，于是替换了一个32位的JDK，重新测试，结果又报找不到dll的异常。加载dll的代码很简单：</p>
<pre class="brush:java;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
System.loadLibrary(&quot;hello&rdquo;);//dll的文件名为hello.dll
</pre>
<p>
	此时，我已经按照经验将dll扔到C:\windows\System32目录下了，感觉应该万无一失的，结果却不行。以前在做windows下libvirt接口开发的时候，就是这么做的，当时运行正常。这是为什么？</p>
<p>
	仔细回忆，想起当时的环境是win7 32位，而现在是64位的，难道windows的目录有变化？马上查看，果然在windows目录下又发现了一个SysWow64的文件夹，里面的文件几乎和System32内的文件一致。立马把hello.dll扔到里面再次运行。成功！</p>
<p>
	果然64位的win7的目录有变化，后来笔者也在网上搜索了一番，有几篇介绍windows32位和64位系统dll文件夹命名规则的文章，如果大家有兴趣可以去搜索一下。</p>
<p>
	由该问题，笔者也想起之前对于windows下libvirt开发的文章中介绍的操作方式可能不够严谨，当时也有很多朋友向<a href="http://www.coderli.com">OneCoder</a>询问为什么他们按照我介绍的扔到System32目录下，仍然不好用，但是我没能给出解答，如此看来，很可能是那些朋友的开发环境是64位的系统，如果是这样，那他们放到C:\Windows\SysWoW64下，应该会好用了。&nbsp;</p>