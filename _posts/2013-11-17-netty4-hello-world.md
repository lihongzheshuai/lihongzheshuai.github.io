---
layout: post
title: Java NIO框架Netty教程（十七） - Netty4 Hello world
date: 2013-11-17 21:51 +0800
author: onecoder
comments: true
tags: [Netty]
thread_key: 1540
---
最近很多人问我有没有Netty4的Hello World样例，很早之前知道Netty要出4，当时只知道4的包名完全边了，因为Netty从JBoss中独立出来了，并采用了新的netty.io的域名，但是没想到代码也有这么大的调整。

<!--break-->

既然答应了别人，就抽时间看一下Netty4，也顺便补充一下自己的知识。还是先从最简单的Hello world开始吧。下面代码基于最近版的Netty4，netty4.0.12-Final。由于Netty4最代码进行了分包，分了很多工程，有可能会对你的开发造成困扰，不过Netty4也提供了一个netty4-all的jar包，里面包含了所有的代码，方便你进行依赖开发。这里<a href="http://www.coderli.com">OneCoder</a>用的就是该jar包。

```java
/**
 * Netty4 服务端代码
 *
 * @author lihzh
 * @date 2013年11月15日 下午1:10:06
 * @website http://www.coderli.com
 */
public class HelloWorldServer {

      public static void main(String[] args) {
           // EventLoop 代替原来的 ChannelFactory
          EventLoopGroup bossGroup = new NioEventLoopGroup();
          EventLoopGroup workerGroup = new NioEventLoopGroup();
           try {
               ServerBootstrap serverBootstrap = new ServerBootstrap();
               // server端采用简洁的连写方式，client端才用分段普通写法。
              serverBootstrap.group(bossGroup, workerGroup)
                        .channel(NioServerSocketChannel. class )
                        .childHandler( new ChannelInitializer&lt;SocketChannel&gt;() {
                              @Override
                              public void initChannel(SocketChannel ch)
                                       throws Exception {
                                  ch.pipeline().addLast( new HelloServerHandler());
                             }
                        }).option(ChannelOption. SO_KEEPALIVE , true );

              ChannelFuture f = serverBootstrap.bind(8000).sync();
              f.channel().closeFuture().sync();
          } catch (InterruptedException e) {
          } finally {
              workerGroup.shutdownGracefully();
              bossGroup.shutdownGracefully();
          }
     }

      private static class HelloServerHandler extends
              ChannelInboundHandlerAdapter {

           /**
           * 当绑定到服务端的时候触发，打印"Hello world, I'm client."
           *
           * @alia OneCoder
           * @author lihzh
           * @date 2013年11月16日 上午12:50:47
           */
           @Override
           public void channelActive(ChannelHandlerContext ctx) throws Exception {
              System. out .println("Hello world, I'm server.");
          }
     }

}
```

```java
/**
 * Netty4 客户端代码
 * @author OneCoder
 * @date 2013年11月15日 下午1:28:21
 * @website http://www.coderli.com
 */
public class HelloWorldClient {

      public static void main(String args[]) {
           // Client服务启动器 3.x的ClientBootstrap 改为Bootstrap，且构造函数变化很大，这里用无参构造。
          Bootstrap bootstrap = new Bootstrap();
           // 指定channel类型
          bootstrap.channel(NioSocketChannel. class );
           // 指定Handler
          bootstrap.handler( new HelloClientHandler());
           // 指定EventLoopGroup
          bootstrap.group( new NioEventLoopGroup());
           // 连接到本地的8000端口的服务端
          bootstrap.connect( new InetSocketAddress("127.0.0.1" , 8000));
     }

      private static class HelloClientHandler extends
              ChannelInboundHandlerAdapter {

           /**
           * 当绑定到服务端的时候触发，打印"Hello world, I'm client."
           *
           * @alia OneCoder
           * @author lihzh
           * @date 2013年11月16日 上午12:50:47
           */
           @Override
           public void channelActive(ChannelHandlerContext ctx) throws Exception {
              System. out .println("Hello world, I'm client.");
          }
     }
}
```

一些主要的变化和对比注释在代码中。简单补充介绍几点：

NioEventLoopGroup 是一个处理I/O操作的多线程事件环。即为Netty4里的线程池，在3.x里，一个Channel是由ChannelFactory创建的，同时新创建的Channel会自动注册到一个隐藏的I/O线程。 4.0使用新的名为EventLoopGroup的接口来替换ChannelFactory，它由一个或多个EventLoop来构成。一个新的 Channel不会自动注册到EventLoopGroup，但用户可以显式调用EventLoopGroup.register（）来注册。在Server端的Bootstrap参数中，有两个EventLoopGroup，第一个通常称为'boss'，用于接收发来的连接请求。第二个称为'worker',，用于处理boss接受并且注册给worker的连接中的信息。

ChannelInitializer是一个特殊的handler，用于方便的配置用户自定义的handler实现，如代码中所示。在channelRegistered的生命周期中会触发用户复写的initChannel(C ch)方法，并且在调用后会讲自身从channelPipeline中移除。