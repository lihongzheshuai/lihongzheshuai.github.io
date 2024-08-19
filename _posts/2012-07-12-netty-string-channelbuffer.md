---
layout: post
title: Java NIO框架Netty教程（三）- 字符串消息收发
date: 2012-07-12 21:18 +0800
author: onecoder
comments: true
tags: [Netty]
categories: [Java技术研究]
thread_key: 922
---

了解了Netty的<a href="http://www.coderli.com/netty-two-concepts/" target="\_blank">基本概念</a>，开发起来应该会顺手很多。在<a href="http://www.coderli.com/netty-course-hello-world/" target="\_blank">"Hello World"</a>代码中，我们只是在完成绑定的时候，在各自的本地打印了简单的信息，并没有客户端和服务端的消息传递。这个肯定是最基本的功能。在上代码之前，先补充一个Netty中重要的概念，ChannelBuffer。

### ChannelBuffer

![](/images/oldposts/CT0dH.jpg)

Netty中的消息传递，都必须以字节的形式，以**ChannelBuffer**为载体传递。简单的说，就是你想直接写个字符串过去，对不起，抛异常。虽然，**Netty**定义的**writer**的接口参数是**Object**的，这可能也是会给新上手的朋友容易造成误会的地方。**Netty**源码中，是这样判断的：

```java
SendBuffer acquire(Object message) {
        if (message instanceof ChannelBuffer) {
            return acquire((ChannelBuffer) message);
        } else if (message instanceof FileRegion) {
            return acquire((FileRegion) message);
        }

        throw new IllegalArgumentException(
                "unsupported message type: " + message.getClass());
    }
```

所以，我们要想传递字符串，那么就必须转换成**ChannelBuffer**。明确了这一点，接下来我们上代码：

```java
/**
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class MessageServer {

	public static void main(String args[]) {
		// Server服务启动器
		ServerBootstrap bootstrap = new ServerBootstrap(
				new NioServerSocketChannelFactory(
						Executors.newCachedThreadPool(),
						Executors.newCachedThreadPool()));
		// 设置一个处理客户端消息和各种消息事件的类(Handler)
		bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
			@Override
			public ChannelPipeline getPipeline() throws Exception {
				return Channels.pipeline(new MessageServerHandler());
			}
		});
		// 开放8000端口供客户端访问。
		bootstrap.bind(new InetSocketAddress(8000));
	}

	private static class MessageServerHandler extends SimpleChannelHandler {

		/**
		 * 用户接受客户端发来的消息，在有客户端消息到达时触发
		 * 
		 * @author lihzh
		 * @alia OneCoder
		 */
		@Override
		public void messageReceived(ChannelHandlerContext ctx, MessageEvent e) {
			ChannelBuffer buffer = (ChannelBuffer) e.getMessage();
			System.out.println(buffer.toString(Charset.defaultCharset()));
		}

	}
}
```

```java
/**
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class MessageClient {

	public static void main(String args[]) {
		// Client服务启动器
		ClientBootstrap bootstrap = new ClientBootstrap(
				new NioClientSocketChannelFactory(
						Executors.newCachedThreadPool(),
						Executors.newCachedThreadPool()));
		// 设置一个处理服务端消息和各种消息事件的类(Handler)
		bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
			@Override
			public ChannelPipeline getPipeline() throws Exception {
				return Channels.pipeline(new MessageClientHandler());
			}
		});
		// 连接到本地的8000端口的服务端
		bootstrap.connect(new InetSocketAddress("127.0.0.1", 8000));
	}

	private static class MessageClientHandler extends SimpleChannelHandler {

		/**
		 * 当绑定到服务端的时候触发，给服务端发消息。
		 * 
		 * @alia OneCoder
		 * @author lihzh
		 */
		@Override
		public void channelConnected(ChannelHandlerContext ctx,
				ChannelStateEvent e) {
			// 将字符串，构造成ChannelBuffer，传递给服务端
			String msg = "Hello, I'm client.";
			ChannelBuffer buffer = ChannelBuffers.buffer(msg.length());
			buffer.writeBytes(msg.getBytes());
			e.getChannel().write(buffer);
		}
	}

}
```
与<a href="http://www.coderli.com/netty-course-hello-world/" target="\_blank">"Hello World"</a>样例代码不同的是，客户端在**channel**连通后，不是在本地打印，而是将消息转换成**ChannelBuffer**传递给服务端，服务端接受到**ChannelBuffer**后，解码成字符串打印出来。同时，通过对比可以发现，变动的只是**Handler**里的代码，启动服务和绑定服务的代码没有变化，也就是我们在<a href="http://www.coderli.com/netty-two-concepts/" target="\_blank">概念介绍</a>里提到了，关注**Handler**，在**Handler**里处理我们自己的业务。所以，以后我们会只给出业务中关键代码，不会在上重复的代码：）

由于在Netty中消息的收发全依赖于**ChannelBuffer**，所以，下一章我们将会详细的介绍**ChannelBuffer**的使用。我们一起学习。