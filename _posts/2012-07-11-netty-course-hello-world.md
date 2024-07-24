---
layout: post
title: Java NIO框架Netty教程（一） - Hello Netty
date: 2012-07-11 12:34
author: onecoder
comments: true
categories: [Netty, Netty, 分布式, 教程]
tags: [Netty,NIO]
thread_key: 907
---
先啰嗦两句，如果你还不知道Netty是做什么的能做什么。那可以先简单的搜索了解一下。我只能说Netty是一个NIO的框架，可以用于开发分布式的Java程序。具体能做什么，各位可以尽量发挥想象。技术，是服务于人而不是局限住人的。

Netty的简介和下载可参考：[开源Java高性能NIO框架推荐](http://www.coderli.com/opensource-netty-intro/)。注意，此时的最新版已经为3.5.2.Final。
	
如果你已经万事具备，那么我们先从一段代码开始。程序员们习惯的上手第一步，自然是"Hello world";，不过Netty官网的例子却偏偏抛弃了"Hello world"。那我们就自己写一个最简单的"Hello world"的例子，作为上手。

```java
/**
 * Netty 服务端代码
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class HelloServer {

	public static void main(String args[]) {
		// Server服务启动器
		ServerBootstrap bootstrap = new ServerBootstrap(
				new NioServerSocketChannelFactory(
						Executors.newCachedThreadPool(),
						Executors.newCachedThreadPool()));
		// 设置一个处理客户端消息和各种消息事件的类(Handler)
		bootstrap
				.setPipelineFactory(new ChannelPipelineFactory() {
					@Override
					public ChannelPipeline getPipeline()
							throws Exception {
						return Channels
								.pipeline(new HelloServerHandler());
					}
				});
		// 开放8000端口供客户端访问。
		bootstrap.bind(new InetSocketAddress(8000));
	}

	private static class HelloServerHandler extends
			SimpleChannelHandler {

		/**
		 * 当有客户端绑定到服务端的时候触发，打印"Hello world, I am server."
		 * 
		 * @alia OneCoder
		 * @author lihzh
		 */
		@Override
		public void channelConnected(
				ChannelHandlerContext ctx,
				ChannelStateEvent e) {
			System.out.println("Hello world, I am server.");
		}
	}
}
```
```java
/**
 * Netty 客户端代码
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class HelloClient {

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
				return Channels.pipeline(new HelloClientHandler());
			}
		});
		// 连接到本地的8000端口的服务端
		bootstrap.connect(new InetSocketAddress(
				"127.0.0.1", 8000));
	}

	private static class HelloClientHandler extends SimpleChannelHandler {


		/**
		 * 当绑定到服务端的时候触发，打印"Hello world, I am client."
		 * 
		 * @alia OneCoder
		 * @author lihzh
		 */
		@Override
		public void channelConnected(ChannelHandlerContext ctx,
				ChannelStateEvent e) {
			System.out.println("Hello world, I am client.");
		}
	}
}
```

既然是分布式的，自然要分多个服务。Netty中，需要区分Server和Client服务。所有的Client都是绑定在Server上的，他们之间是不能通过Netty直接通信的。（自己采用的其他手段，不包括在内。）。白话一下这个通信过程，Server端开放端口，供Client连接，Client发起请求，连接到Server指定的端口，完成绑定。随后便可自由通信。其实就是普通Socket连接通信的过程。

Netty框架是基于事件机制的，简单说，就是发生什么事，就找相关处理方法。就跟着火了找119，抢劫了找110一个道理。所以，这里，我们处理的是当客户端和服务端完成连接以后的这个事件。什么时候完成的连接，Netty知道，他告诉我了，我就负责处理。这就是框架的作用。Netty，提供的事件还有很多，以后会慢慢的接触和介绍。

你应该已经可以上手了：）

