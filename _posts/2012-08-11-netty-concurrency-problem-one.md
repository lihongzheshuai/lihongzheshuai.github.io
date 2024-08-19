---
layout: post
title: Java NIO框架Netty教程(十一)-并发访问测试(上)
date: 2012-08-11 23:11 +0800
author: onecoder
comments: true
tags: [Netty]
categories: [Java技术研究]
thread_key: 1048
---
之前更新了几篇关于JVM研究的文章，其实也是在做本篇文章验证的时候，跑的有点远，呵呵。回归Netty教程，这次要讲的其实是针对一个问题的研究和验证结论。另外，最近工作比较忙，所以可能会分文章更新一些阶段性的成果，而不是全部汇总更新，以免间隔过久。

起因是一个朋友，通过微博私信给我一个问题，大意是说他在用**Netty**做并发测试的时候，会出现大量的**connection refuse**信息，问我如何解决。

没动手就没有发言权，所以OneCoder决定测试一下：

```java
/**
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class ConcurrencyNettyTestHandler extends SimpleChannelHandler {

	private static int count = 0;

	/**
	 * 当接受到消息的时候触发
	 */
	@Override
	public void channelConnected(ChannelHandlerContext ctx,
			final ChannelStateEvent e) throws Exception {
		for (int i = 0; i &lt; 100000; i++) {
			Thread t = new Thread(new Runnable() {
				@Override
				public void run() {
					sendObject(e.getChannel());
				}
			});
			System.out.println(&quot;Thread count: &quot; + i);
			t.start();
		}

	}

	/**
	 * 发送Object
	 * 
	 * @author lihzh
	 * @alia OneCoder
	 */
	private void sendObject(Channel channel) {
		count++;
		Command command = new Command();
		command.setActionName(&quot;Hello action.&quot;);
		System.out.println(&quot;Write: &quot; + count);
		channel.write(command);
	}
}
```

运行结果：

```
Hello action.: 99996
Hello action.: 99997
Hello action.: 99998
Hello action.: 99999
Hello action.: 100000
```

你可能会惊讶，**10w**个请求都能通过？呵呵，细心的同学，可能会发现，这其实并不是并发，而只是所谓**10w**个线程的，单channel的伪并发，或者说是一种持续的连续访问。并且，如果你跑一下测试用例，会发现，Server端开始接受处理消息，是在Client端10w个线程请求都结束之后再开始的。这是为什么？

其实，如果您看过OneCoder的<a href="http://www.coderli.com/netty-message-receive-count-mismatch-two/" target="\_blank">《Java NIO框架Netty教程(七)-再谈收发信息次数问题》</a>，应该会有所联想。不过坦白的说，**OneCoder**也是在经过一番周折，一番**Debug**以后，才发现了这个问题。当**OneCoder**在线程内断点以后，放过一个线程，接收端就会有一条信息出现，这其实是和之前文章里介绍的场景是一样的。所以，呵呵，可能对您来说，看了这篇文章，并没有更多的收获，但是对<a href="http://www.coderli.com">**OneCoder**</a>来说，确实是经历了不小的周折，绕了挺大的弯子，也算是对代码的再熟悉过程吧。

下篇我们会面对真正并发的问题：）

