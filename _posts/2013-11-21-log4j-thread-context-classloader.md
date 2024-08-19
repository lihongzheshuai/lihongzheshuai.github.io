---
layout: post
title: log4j 多classloader重复加载配置问题解决
date: 2013-11-21 00:45 +0800
author: onecoder
comments: true
tags: [Log4j]
categories: [Java技术研究]
thread_key: 1551
---
<p>
	最近<a href="http://www.coderli.com">OneCoder</a>在开发隔离任务运行的沙箱，用于隔离用户不同任务间以及任务和框架本身运行代码的隔离和解决潜在的jar包冲突问题。<br />
	
<!--break-->

运行发现，隔离的任务正常运行，但是却没有任何日志记录。从控制台可看到如下错误信息：</p>
<blockquote>
	<p>
		log4j:ERROR A &quot;org.apache.log4j.xml.DOMConfigurator&quot; object is not assignable to a &quot;org.apache.log4j.spi.Configurator&quot; variable.<br />
		log4j:ERROR The class &quot;org.apache.log4j.spi.Configurator&quot; was loaded by<br />
		log4j:ERROR [java.net.URLClassLoader@5b0a69d3] whereas object of type<br />
		log4j:ERROR &quot;org.apache.log4j.xml.DOMConfigurator&quot; was loaded by [WebappClassLoader<br />
		&nbsp; context:<br />
		&nbsp; delegate: false<br />
		&nbsp; repositories:<br />
		&nbsp;&nbsp;&nbsp; /WEB-INF/classes/<br />
		----------&gt; Parent Classloader:<br />
		org.apache.catalina.loader.StandardClassLoader@4d405ef7<br />
		].<br />
		log4j:ERROR Could not instantiate configurator [org.apache.log4j.xml.DOMConfigurator].<br />
		log4j:WARN No appenders could be found for logger (com.xxx.xxx.xxx).<br />
		log4j:WARN Please initialize the log4j system properly.</p>
</blockquote>
<p>
	错误信息很明显，log4j被两个不同的classloader初始化了两遍结果包错。这个问题不难解决，主要有两种手段：<br />
	第一、增加配置，让log4j忽略由不同的classloader的初始化这个问题。在log4j的配置文件中增加</p>

```
log4j.ignoreTCL=true
```

<p>
	即可。在某些版本的log4j的错误信息中，还会提到下面的网址：<br />
	http://logging.apache.org/log4j/1.2/faq.html，里面有关注上面属性的介绍。<br />
	第二、修改初始化log4j线程的classloader。由于log4j会用当前线程上下文中的classloader去初始化配置，所以在我的沙箱应用中，虽然log4j的jar是由URLClassLoader加载进来的，但是加载的线程还是在WebApp中的，还是WebApp的ClassLoader，所以会出现上面的提示信息。因此，我们至要通过下面代码：</p>

```java
Thread.currentThread().setContextClassLoader(urlclassLoader);
```

<p>
	将当前线程的上下文loader改为沙箱的ClassLoader即可。</p>
<p>
	两种解决方式，你可以按需选择了。</p>

