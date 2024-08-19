---
layout: post
title: Netty5.x中新增和值得注意的点
date: 2014-02-26 23:50 +0800
author: onecoder
comments: true
tags: [Netty]
categories: [Java技术研究]
thread_key: 1630
---
<div>
	最近事情多，OneCoder折腾了好几天，总算翻译完成了。</div>
<div>
	翻译自官方文档：<a href="http://netty.io/wiki/new-and-noteworthy-in-5.x.html">http://netty.io/wiki/new-and-noteworthy-in-5.x.html</a></div>
<div>
	&nbsp;</div>
<div>
	该文档会列出在Netty新版本中值得注意变化和新特性列表。帮助你的应用更好的适应新的版本。</div>
<div>
	&nbsp;</div>
<div>
	不像Netty3.x和4.x之间的变化，5.x没有那么大的变化，不过也取得了其简化设计中的一些突破性进展.。我们力求尽可能平滑的从4.x版本过度到5.x版本，如果你在迁移过程中遇到任何问题，请告知我们。</div>
<div>
	&nbsp;</div>
<div>
	核心变化</div>
<div>
	&nbsp;</div>
<div>
	&nbsp;</div>
<div>
	<strong>支持Android</strong></div>
<div>
	&nbsp;</div>
<div>
	提供了：</div>
<ul>
	<li>
		&nbsp;移动设备变成更加强大</li>
	<li>
		通过Ice Cream Sandwich解决了在ADK中最著名的与NIO和SSLEngine相关的问题，且</li>
	<li>
		用户显然想要重用他们应用中的的编解码和处理器代码。</li>
</ul>
<div>
	我们决定官方支持Android(4.0及以上版本)</div>
<div>
	&nbsp;</div>
<div>
	<strong>简化处理器层次</strong></div>
<div>
	&nbsp;</div>
<div>
	ChannelInboundHandler和ChannelOutboundHandler整合为ChannelHandler。ChannelHandler现在包含输入和输出的处理方法。</div>
<div>
	&nbsp;</div>
<div>
	ChannelInboundHandlerAdapter，ChannelOutboundHandlerAdapter和ChannelDuplexHandlerAdapter已被废弃，由 ChannelHandlerAdapter代替。</div>
<div>
	&nbsp;</div>
<div>
	由于现在无法区分处理器(handler) 是输入还是输出的处理器，CombinedChannelDuplexHandler现在由 ChannelHandlerAppender代替。</div>
<div>
	&nbsp;</div>
<div>
	更多相关变化，可参考<a href="https://github.com/netty/netty/pull/1999">https://github.com/netty/netty/pull/1999</a></div>
<div>
	&nbsp;</div>
<div>
	<em><strong>channelRead0() &rarr; messageReceived()</strong></em></div>
<div>
	&nbsp;</div>
<div>
	我知道。这是一个愚蠢的错误。如果你使用了SimpleChannelInboundHandler，你需要把channelRead0()重命名为messageReceived()。</div>
<div>
	&nbsp;</div>
<div>
	<strong>废弃中移除的</strong></div>
<div>
	&nbsp;</div>
<div>
	Channel.deregister()已被移除。不再生效和被使用。取而代之的，我们将允许Channel被充注册到不同的事件循环。</div>
<div>
	&nbsp;</div>
<div>
	<strong><em>ChannelHandlerContext.attr(..) == Channel.attr(..)</em></strong></div>
<div>
	&nbsp;</div>
<div>
	Channel和ChannelHandlerContext类都实现了AttributeMap接口，使用户可以在其上关联一个或多个属性。有时会让用户感到困惑的是Channel和ChannelHandlerContext都有其自己的存储用户定义属性的容器。例如，即使你通过Channel.attr(KEY_X).set(valueX)给属性&#39;KEY_X&rsquo;赋值，你却无法通过ChannelHandlerContext.attr(KEY_X).get()方法获取到值。反之亦是如此。这种行为不仅仅令人不解而且还浪费内存。</div>
<div>
	&nbsp;</div>
<div>
	为了解决这个问题，我们决定每个Channel内部仅保留一个map。AttributeMap总是用AttributeKey作为它的key。AttributeKey确保键的唯一性，因此每个Channel中如果存在一个以上的属性容易是多余的。只要用户把他自己的AttributeKey定义成ChannelHandler的private static final变量，就不会有出现重复key的风险。</div>
<div>
	&nbsp;</div>
<div>
	<strong>更简单更精确的缓冲区泄漏追踪</strong></div>
<div>
	&nbsp;</div>
<div>
	&nbsp;</div>
<div>
	之前，查找缓冲区泄漏是很困难的，并且泄漏的警告信息也不是很有帮助。现在我们有了增强的泄漏报告机制，该机制会在增长超过上限时触发。</div>
<div>
	&nbsp;</div>
<div>
	更多的信息可查看：http://netty.io/wiki/reference-counted-objects.html 。由于该特性十分重要，所以也移植入了4..0.14.Final版中。</div>
<div>
	&nbsp;</div>
<div>
	<strong>PooledByteBufAllocator成为默认的allocator</strong></div>
<div>
	&nbsp;</div>
<div>
	在4.x版本中，UnpooledByteBufAllocator是默认的allocator，尽管其存在某些限制。现在PooledByteBufAllocator已经广泛使用一段时间，并且我们有了增强的缓冲区泄漏追踪机制，所以是时候让PooledByteBufAllocator成为默认了。</div>
<div>
	&nbsp;</div>
<div>
	<strong>全局唯一的Channel ID</strong></div>
<div>
	&nbsp;</div>
<div>
	&nbsp;</div>
<div>
	每个Channel现在有了全局唯一的ID，其生成的依据是：</div>
<div>
	&nbsp;</div>
<div>
	&nbsp; &nbsp;* MAC地址(EUI-48或是EUI-64)，最好是全局唯一的，</div>
<div>
	&nbsp; &nbsp;* 当前进程的ID</div>
<div>
	&nbsp; &nbsp;* System#currentTimeMillis()</div>
<div>
	&nbsp; &nbsp;* System#nanoTime()</div>
<div>
	&nbsp; &nbsp;* 随机的32位整数，以及</div>
<div>
	&nbsp; &nbsp;* 系列递增的32位整数</div>
<div>
	&nbsp;</div>
<div>
	可通过Channel.id()方法获取Channel的ID。</div>
<div>
	&nbsp;</div>
<div>
	<strong>更灵活的线程模型</strong></div>
<div>
	&nbsp;</div>
<div>
	&nbsp;</div>
<div>
	增加了新的ChannelHandlerInvoker接口，用于使用户可以选择使用哪个线程调用事件处理方法。替代之前的在向ChannelPipeline添加 ChannelHandler时指定一个EventExecutor的方式，使用该特性需要指定一个用户自定义的 ChannelHandlerInvoker实现。</div>
<div>
	&nbsp;</div>
<div>
	关于该变化更多的信息，可参考:<a href="https://github.com/netty/netty/commit/132af3a485015ff912bd567a47881814d2ce1828">https://github.com/netty/netty/commit/132af3a485015ff912bd567a47881814d2ce1828</a></div>
<div>
	&nbsp;</div>
<div>
	<strong>EmbeddedChannel的易用性</strong></div>
<div>
	&nbsp;</div>
<div>
	EmbeddedChannel中的readInbound()和readOutbound()方法返回专门类型的参数，因此你不必在转换他们的返回值。这可以简化你的测试用例代码。</div>
<div>
	<pre class="brush:java;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
EmbeddedChannel ch = ...;

// BEFORE:
FullHttpRequest req = (FullHttpRequest) ch.readInbound();

// AFTER:
FullHttpRequest req = ch.readInbound();

</pre>
</div>
<div>
	&nbsp;</div>
<div>
	<strong>使用Executor代替ThreadFactory</strong></div>
<div>
	&nbsp;</div>
<div>
	&nbsp;</div>
<div>
	有些应用要求用户使用Executor运行他们的任务。4.x版本要求用户在创建事件循环(event loop)时指定ThreadFacotry，现在不再是这样了。</div>
<div>
	&nbsp;</div>
<div>
	关于该变化的更多信息，可参考：https://github.com/netty/netty/pull/1762</div>
<div>
	&nbsp;</div>
<div>
	<strong>Class loader友好化</strong></div>
<div>
	&nbsp;</div>
<div>
	一些类型，如AttributeKey对于在容器环境下运行的应用是不友好的，现在不是了。</div>
<div>
	&nbsp;</div>
<div>
	<strong>编解码和处理器(handlers)</strong></div>
<div>
	&nbsp;</div>
<div>
	&nbsp; &nbsp;* XmlFrameDecoder支持流式的XML文档</div>
<div>
	&nbsp;</div>
<div>
	&nbsp; &nbsp;* 二进制的memcache协议编解码</div>
<div>
	&nbsp; &nbsp;* 支持SPDY/3.1 (也移植到了4.x版本)</div>
<div>
	&nbsp; &nbsp;* 重构了HTTP多部分的编解码</div>
<div>
	&nbsp;</div>

