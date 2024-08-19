---
layout: post
title: Restlet 客户端连接超时问题解决
date: 2013-12-16 13:05 +0800
author: onecoder
comments: true
tags: [Restlet]
categories: [Java技术研究]
thread_key: 1581
---
<p>
	使用Restlet进行同步请求，有时可能处理的时间会很长所以需要客户端进行较长时间的等待。从API中查得客户端的设置方式如下：</p>
	
<!--break-->
	
```java
ClientResource client = new ClientResource(new Context(), uri);
client.setRetryAttempts(0);
client.setProtocol(protocol);
client.getContext().getParameters().add("socketTimeout", "60000");
```

不过，设置后，OneCoder经测试却发现无效。无论socketTimeout设置为多少。均会在1分钟左右超时。

这好像是由于Restlet默认使用的是一个简单的http服务，而在现在版本中，Restlet提供了很多增强的扩展。其中一个是ext.jetty扩展。即以jetty服务器做服务，启动Rest服务。使用方式很简单，无需修改原有代码，只需增加ext.jetty的依赖即可。
{% highlight xml %}
 <dependency>
  <groupId>org.restlet.jse</groupId>
  <artifactId>org.restlet.ext.jetty</artifactId>
  <version>2.1.2</version>
</dependency>
{% endhighlight %}
再次测试，有效。
	
值得一提的是，Restlet提供了很多扩展包。会对默认的Restlet服务进行很多增强。

