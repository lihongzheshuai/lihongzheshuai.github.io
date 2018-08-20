---
title: Netty4自学笔记 (3) - Netty NIO Server & Client 样例说明
tags: [Netty,NIO]
date: 2018-08-13 16:41:24 +0800
comments: true
author: onecode
---
更新节奏缓慢，因为每晚学习注意力不够集中，学习进展缓慢。本还给自己找了一大堆其他理由，但摸着良心问自己，似乎只有这个理由说的通。

想搞懂的太多，却始终没搞明白。先看一个用Netty编写的NIO Server的样例。

<!--break-->

```java
package com.coderli.nettylab.guide;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;

/**
 * @author lihongzhe 2018/7/24 23:19
 */
public class NettyNioServer {

    public static void main(String[] args) throws InterruptedException {
        EventLoopGroup bossGroup = new NioEventLoopGroup(); // (1)
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        try {
            ServerBootstrap b = new ServerBootstrap(); // (2)
            b.group(bossGroup, workerGroup)
                    .channel(NioServerSocketChannel.class) // (3)
                    .childHandler(new ChannelInitializer<SocketChannel>() { // (4)
                        @Override
                        public void initChannel(SocketChannel ch) throws Exception {
                            ch.pipeline().addLast(new ServerHandler());
                        }
                    })
                    .option(ChannelOption.SO_BACKLOG, 128)
                    .childOption(ChannelOption.SO_KEEPALIVE, true);

            ChannelFuture f = b.bind(7060).sync(); // (5)
            f.channel().closeFuture().sync();
        } finally {
            workerGroup.shutdownGracefully();
            bossGroup.shutdownGracefully();
        }
    }

}

```

ServerHanler代码

```java
package com.coderli.nettylab.guide;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;

/**
 * @author lihongzhe 2018/7/24 23:58
 */
public class ServerHandler extends ChannelInboundHandlerAdapter {

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        System.out.println("Receive Msg.");
        ((ByteBuf) msg).release(); 
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
```

上述代码改自Netty官方手册。**NettyNioServer**代码中做了几处标记，分别对应我们在[Netty4 自学笔记（2）](http://www.coderli.com/netty4-java-nio/)中讨论的关键点，简析如下：

1. **标记1**是构建了两个线程池，我们在Java NIO学习中提到的，针对Select的实现方式，如果想要实现并发，只需要在事件处理时，启用多线程处理即可，此处的**workerGroup**正是为此服务。而在Netty中，不仅仅对于事件到达后的处理启用了线程池，为了实现高并发，Netty开启多个线程注册多个Selector同时处理事件。Netty中，默认线程池数量为，cpu核心数 * 2（**NettyRuntime.availableProcessors() * 2**），个人认为Selector线程数过多意义也不大，关键还是在于事件分发后的后续处理，即work线程。同样，这里worker线程池的默认数量与boss一致，因此在业务实现中应注意异步处理worker中的回调，以免堵塞worker，影响并发。
2. **标记2**的**ServerBootstrap**是Netty封装的统一配置并启动Server的启动器，在[Java NIO学习](http://www.coderli.com/netty4-java-nio/)中提到的Channel（**标记3**）和事件处理器Handler（**标记4**），都统一配置在此。**标记3**处指定不同类型的Channel（例如：Nio、Oio），底层便可方便的在不同的通信模式下进行切换，上层无感知。
3. **标记5**，一切配置好后，启动器绑定到指定端口。

从样例代码的直观感觉来说，Netty提供了良好的封装，无论是Server还是事件处理的Handler，Netty几乎帮我们做好了一切。对于开发人员来说，**只需要关注于Netty提供的Handler的回调时机**，开发自己的业务逻辑，比直接使用Java NIO的API节约了很多的开工作量，而且保证了代码的健壮性和多线程支持。

因此，**我下一步的思路就是去研究一下Netty中Handler的回调机制**，真正掌握才可开发逻辑正确的代码。

本文的最后，把Client端的代码补充完整，以便调试，

**NettyNioClient**

```java
package com.coderli.nettylab.guide;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;

/**
 * @author lihongzhe 2018/8/6 22:55
 */
public class NettyNioClient {

    public static void main(String[] args) throws InterruptedException {
        EventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            Bootstrap b = new Bootstrap();
            b.group(workerGroup);
            b.channel(NioSocketChannel.class);
            b.option(ChannelOption.SO_KEEPALIVE, true);
            b.handler(new ChannelInitializer<SocketChannel>() {
                @Override
                public void initChannel(SocketChannel ch) throws Exception {
                    ch.pipeline().addLast(new ClientHandler());
                }
            });

            ChannelFuture f = b.connect("127.0.0.1", 7060).sync(); 

            // Wait until the connection is closed.
            f.channel().closeFuture().sync();
        } finally {
            workerGroup.shutdownGracefully();
        }
    }

}
```

**ClientHandler**

```java
package com.coderli.nettylab.guide;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;

import java.util.Date;

/**
 * @author lihongzhe 2018/8/6 23:13
 */
public class ClientHandler extends ChannelInboundHandlerAdapter {
    private ByteBuf buf;

    @Override
    public void channelRegistered(ChannelHandlerContext ctx) throws Exception {
        System.out.println("Channel Registered, Client.");
        ctx.fireChannelRegistered();
    }

    @Override
    public void handlerAdded(ChannelHandlerContext ctx) {
        System.out.println("Handler added.");
        buf = ctx.alloc().buffer(4);
    }

    @Override
    public void handlerRemoved(ChannelHandlerContext ctx) {
        buf.release();
        buf = null;
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        ByteBuf m = (ByteBuf) msg;
        buf.writeBytes(m);
        m.release();

        if (buf.readableBytes() >= 4) { 
            long currentTimeMillis = (buf.readUnsignedInt() - 2208988800L) * 1000L;
            System.out.println(new Date(currentTimeMillis));
            ctx.close();
        }
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
```

后续的研究，我也会基于上述代码加以改造和调试。