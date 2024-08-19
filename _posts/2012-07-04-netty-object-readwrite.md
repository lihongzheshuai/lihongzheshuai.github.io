---
layout: post
title: Netty Object传输问题解决
date: 2012-07-04 12:53 +0800
author: onecoder
comments: true
tags: [Netty]
categories: [Java技术研究,Netty]
thread_key: 838
---
使用Netty开发分布式框架，对象的传输是基本的需求。但是，在开发中却总遇到服务端接受不到客户端的对象发送数据。遂动手解决。

如果看到最后，你可能会发现，笔者的问题是那么的二，不适合你。。所以，你可以决定不看，或者只看样例代码。笔者记录的是，个人的解决过程。

先看一下官方提供的，对象传输的样例代码：(核心部分)

```java
    public void run() {
        // Configure the client.
        ClientBootstrap bootstrap = new ClientBootstrap(
                new NioClientSocketChannelFactory(
                        Executors.newCachedThreadPool(),
                        Executors.newCachedThreadPool()));

        // Set up the pipeline factory.
        bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
            public ChannelPipeline getPipeline() throws Exception {
                return Channels.pipeline(
                        new ObjectEncoder(),
                        new ObjectDecoder(
                                ClassResolvers.cacheDisabled(getClass().getClassLoader())),
                        new ObjectEchoClientHandler(firstMessageSize));
            }
        });

        // Start the connection attempt.
        bootstrap.connect(new InetSocketAddress(host, port));
    }
```

```java
    @Override
    public void handleUpstream(
            ChannelHandlerContext ctx, ChannelEvent e) throws Exception {
        if (e instanceof ChannelStateEvent &&
            ((ChannelStateEvent) e).getState() != ChannelState.INTEREST_OPS) {
            logger.info(e.toString());
        }
        super.handleUpstream(ctx, e);
    }

    @Override
    public void channelConnected(
            ChannelHandlerContext ctx, ChannelStateEvent e) {
        // Send the first message if this handler is a client-side handler.
        e.getChannel().write(firstMessage);
    }

    @Override
    public void messageReceived(
            ChannelHandlerContext ctx, MessageEvent e) {
        // Echo back the received object to the client.
        transferredMessages.incrementAndGet();
        e.getChannel().write(e.getMessage());
    }
```
	
```java
    public void run() {
        // Configure the server.
        ServerBootstrap bootstrap = new ServerBootstrap(
                new NioServerSocketChannelFactory(
                        Executors.newCachedThreadPool(),
                        Executors.newCachedThreadPool()));

        // Set up the pipeline factory.
        bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
            public ChannelPipeline getPipeline() throws Exception {
                return Channels.pipeline(
                        new ObjectEncoder(),
                        new ObjectDecoder(
                                ClassResolvers.cacheDisabled(getClass().getClassLoader())),
                        new ObjectEchoServerHandler());
            }
        });

        // Bind and start to accept incoming connections.
        bootstrap.bind(new InetSocketAddress(port));
    }
```

```java
    @Override
    public void handleUpstream(
            ChannelHandlerContext ctx, ChannelEvent e) throws Exception {
        if (e instanceof ChannelStateEvent &&
            ((ChannelStateEvent) e).getState() != ChannelState.INTEREST_OPS) {
            logger.info(e.toString());
        }
        super.handleUpstream(ctx, e);
    }

    @Override
    public void messageReceived(
            ChannelHandlerContext ctx, MessageEvent e) {
        // Echo back the received object to the client.
        transferredMessages.incrementAndGet();
        e.getChannel().write(e.getMessage());
    }
```

代码很简单，都是在服务端/客户端，绑定Object的编码和解码的Handler，再绑定处理自己业务的Handler。然后就是接收到消息以后的事情了。笔者，跑了一下样例，确实可以正常收发Object。

再看看我的代码：
	
```java
	public void run() {
		ServerBootstrap bootstrap = new ServerBootstrap(
				new NioServerSocketChannelFactory(
						Executors.newCachedThreadPool(),
						Executors.newCachedThreadPool()));
		bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
			public ChannelPipeline getPipeline() throws Exception {
				return Channels.pipeline(
						new ObjectEncoder(),
						new ObjectDecoder(ClassResolvers
								.cacheDisabled(getClass().getClassLoader())),
						new CommandServerHandler());
			}
		});
		bootstrap.bind(new InetSocketAddress(port));
		log.info("Netty server has been started.");
	}
```

```java
	@Override
	public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e) {
		log.info("Server has connected to client now.");
	}

	@Override
	public void messageReceived(ChannelHandlerContext ctx, MessageEvent e) {
		// Send back the received message to the remote peer.
		handleClientMsg(ctx, e);
	}
```

```java
	public void bindToServer() {
		// 配置NIO客户端启动
		ClientBootstrap bootstrap = new ClientBootstrap(
				new NioClientSocketChannelFactory(
						Executors.newCachedThreadPool(),
						Executors.newCachedThreadPool()));
		bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
			public ChannelPipeline getPipeline() throws Exception {
				return Channels.pipeline(
						new ObjectEncoder(),
						new ObjectDecoder(ClassResolvers
								.cacheDisabled(getClass().getClassLoader())),
						new CommandHandler());
			}
		});
		if (log.isDebugEnabled()) {
			log.debug("Start to connect to server at time: "
					+ TimeUtil.getCurrentTimeStr());
		}
		bootstrap.connect(new InetSocketAddress(serverIp, port));
	}
```

```java
	@Override
	public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e)
			throws Exception {
		log.info("Agent has connected to server at time: "
				+ TimeUtil.getCurrentTimeStr());
		sendAgentInfo(e.getChannel());
	}
```

方法内具体实现略掉，因为笔者的问题是，方法都压根没进入。也没有异常抛出。（后来反应过来，这也是笔者的失误。在异常处理的方法里，日志级别是debug。）

比较半天，比较不出所以然。幸好笔者习惯下载源码，遂决定开始**debug**。结果，果然有异常出现。说的是**ClassNotFound**。这就好办了。仔细一看，原来是笔者传输的模型没有找到。惊醒，原来笔者测试是在两个独立的工程，独立的进程里测试的。忘记了对模型的依赖。。靠。。2。。。。

笔者又试着将异常处理里的日志级别调高。唉。。神马都有

```text
...
Caused by: java.lang.ClassNotFoundException:
```

早打印，就省老了事了。日志，重要啊。此事，提醒自己，要仔细啊

PS：问题的解决可能对你没有帮助，但是如果你也想写Netty Object传入的代码，上面的样例代码是可以行得通的。