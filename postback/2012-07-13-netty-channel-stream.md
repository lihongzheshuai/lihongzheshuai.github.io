---
layout: post
title: Java NIO框架Netty教程（四）- ChannelBuffer
date: 2012-07-13 22:10 +0800
author: onecoder
comments: true
tags: [Netty]
thread_key: 936
---
在<a href="http://www.coderli.com/netty-string-channelbuffer/" target="\_blank">字符串消息收发</a>中提到。**ChannelBuffer**是**Netty**中非常重要的概念。所有消息的收发都依赖于这个**Buffer**。我们通过**Netty**的官方的文档来了解一下，基于流的消息传递机制。
<blockquote>
	<div>
		In a stream-based transport such as TCP/IP, received data is stored into a socket receive buffer.</div>
	<div>
		<div>
			Unfortunately, the buffer of a stream-based transport is not a queue of packets but a queue of bytes. It</div>
		<div>
			means, even if you sent two messages as two independent packets, an operating system will not treat them</div>
		<div>
			as two messages but as just a bunch of bytes. Therefore, there is no guarantee that what you read is exactly</div>
		<div>
			what your remote peer wrote. For example, let us assume that the TCP/IP stack of an operating system has</div>
		<div>
			received three packets:</div>
		<div>
			+-----+-----+-----+</div>
		<div>
			| ABC | DEF | GHI |</div>
		<div>
			+-----+-----+-----+</div>
		<div>
						Because of this general property of a stream-based protocol, there' high chance of reading them in the</div>
			<div>
				following fragmented form in your application:</div>
			<div>
				+----+-------+---+---+</div>
			<div>
				| AB | CDEFG | H | I |</div>
			<div>
				+----+-------+---+---+</div>
			<div>
				Therefore, a receiving part, regardless it is server-side or client-side, should defrag the received data into one</div>
			<div>
				or more meaningful frames that could be easily understood by the application logic. In case of the example</div>
			<div>
				above, the received data should be framed like the following:</div>
			<div>
				+-----+-----+-----+</div>
			<div>
				| ABC | DEF | GHI |</div>
			<div>
				+-----+-----+-----+</div>
		</div>
	</div>
</blockquote>

您理解了没，简单翻译一下就是说。在**TCP/IP**这种基于流传递的协议中。他识别的不是你每一次发送来的消息，不是分包的。而是，只认识一个整体的流，即使分三次分别发送三段话：**ABC**、**DEF**、**GHI**。在传递的过程中，他就是一个具有整体长度的流。在读流的过程中，如果我一次读取的长度选择的不是三个，我可以收到类似**AB**、**CDEFG**、**H**、**I**这样的信息。这显然是我们不想看到的。所以说，在你写的消息收发的系统里，需要预先定义好这种解析机制，规定每帧(次)读取的长度。通过代码来理解一下:

```java
/**
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class ServerBufferHandler extends SimpleChannelHandler {
	
	/**
	 * 用户接受客户端发来的消息，在有客户端消息到达时触发
	 * 
	 * @author lihzh
	 * @alia OneCoder
	 */
	@Override
	public void messageReceived(ChannelHandlerContext ctx, MessageEvent e) {
		ChannelBuffer buffer = (ChannelBuffer) e.getMessage();
		// 五位读取
		while (buffer.readableBytes() >= 5) {
			ChannelBuffer tempBuffer = buffer.readBytes(5);
			System.out.println(tempBuffer.toString(Charset.defaultCharset()));
		}
		// 读取剩下的信息
		System.out.println(buffer.toString(Charset.defaultCharset()));
	}

}
```

```java
/**
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class ClientBufferHandler extends SimpleChannelHandler {

	/**
	 * 当绑定到服务端的时候触发，给服务端发消息。
	 * 
	 * @alia OneCoder
	 * @author lihzh
	 */
	@Override
	public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e) {
		// 分段发送信息
		sendMessageByFrame(e);
	}

	/**
	 * 将<b>"Hello, I'm client."</b>分成三份发送。 <br>
	 * Hello, <br>
	 * I'm<br>
	 * client.<br>
	 * 
	 * @param e
	 *            Netty事件
	 * @author lihzh
	 */
	private void sendMessageByFrame(ChannelStateEvent e) {
		String msgOne = "Hello, ";
		String msgTwo = "I'm ";
		String msgThree = "client.";
		e.getChannel().write(tranStr2Buffer(msgOne));
		e.getChannel().write(tranStr2Buffer(msgTwo));
		e.getChannel().write(tranStr2Buffer(msgThree));
	}

	/**
	 * 将字符串转换成{@link ChannelBuffer}，私有方法不进行字符串的非空判断。
	 * 
	 * @param str
	 *            待转换字符串，要求非null
	 * @return 转换后的ChannelBuffer
	 * @author lihzh
	 */
	private ChannelBuffer tranStr2Buffer(String str) {
		ChannelBuffer buffer = ChannelBuffers.buffer(str.length());
		buffer.writeBytes(str.getBytes());
		return buffer;
	}

}
```

服务端输出结果：

```
Hello
, I'm
 clie
nt.
```

这里其实，服务端是否分段发送并不会影响输出结果，也就是说，你一次性的把"Hi, I'm client."这段信息发送过来，输出的结果也是一样的。这就是开头说的，传输的是流，不分包。而只在于你如何分段读写。