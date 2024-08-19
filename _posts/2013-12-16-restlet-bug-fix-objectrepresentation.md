---
layout: post
title: Restlet2.1.6发布，修正ObjectRepresentation的构造函数问题
date: 2013-12-16 13:28 +0800
author: onecoder
comments: true
tags: [Restlet]
categories: [Java技术研究]
thread_key: 1583
---
<p>
	<a href="http://www.coderli.com\">OneCoder</a>在Restlet 2.1.4中 匪夷所思的ObjectRepresentation的构造函数中，提到过在使用2.1.4的时候遇到的异常</p>
<blockquote>
	<p>
		Exception in thread &quot;main&quot; java.lang.IllegalArgumentException : The serialized representation must have this media type: application/x-java-serialized-object or this one: application/x-java-serialized-object+xml<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; at org.restlet.representation.ObjectRepresentation.&lt;init&gt;(ObjectRepresentation.java:203)<br />
		&nbsp;&nbsp;&nbsp;&nbsp; at org.restlet.representation.ObjectRepresentation.&lt;init&gt;(ObjectRepresentation.java:114)</p>
</blockquote>
<p>
	当时结果阅读代码，认为是Restlet的一个bug，并提交给Restlet。得到回复确认，称将在2.1.6版本中修复：</p>
<blockquote>
	<p>
		Hello,<br />
		<br />
		thansk a lot for reporting this issue which is clearly a regression. I&#39;ve added a ticket for that point: <a href="https://github.com/restlet/restlet-framework-java/issues/809">https://github.com/restlet/restlet-framework-java/issues/809</a><br />
		The fix will be part of the 2.1.6 release, available in a few minutes.<br />
		<br />
		Best regards,<br />
		Thierry Boileau<br />
		&nbsp;</p>
</blockquote>
<p>
	今天想起，登录了一下Restlet的官方，发现最新版已经是2.1.6了。查看了一些change log，发现该问题确实已经解决。</p>
<blockquote>
	<p>
		===========<br />
		Changes log &nbsp;<br />
		===========<br />
		<br />
		- 2.1.6 (12/05/2013)<br />
		&nbsp;&nbsp;&nbsp; - Bug fixed<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - Fixed issue #809 regression introduced when handling issues #774 and #778.</p>
</blockquote>
<p>
	不过OneCoder还没有升级测试。大家可以测试一下。<br />
	<br />
	&nbsp;</p>

