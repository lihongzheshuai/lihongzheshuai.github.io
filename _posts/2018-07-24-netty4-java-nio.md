---
title: Netty4自学笔记 (2) - Java NIO
tags: [Netty,BIO]
date: 2018-07-24 13:28:24 +0800
comments: true
author: onecode
---
距离上一篇博文已经过去了半个多月。这期间有一周多的时间用在了准备单位举办的英语竞赛上。余下的时间沉迷于陪孩子玩耍和睡觉，日复一日。

当然，我也抽空学习了Java NIO(None-Blocking / New IO) 一些知识，现总结如下。

Java的非阻塞IO的原理是采用了操作系统的多路复用器机制，即在一个通道（channel）上，注册一个事件选择器（selector）及各种事件（读、写等），当有事件到达时，事件选择器返归对应的事件，然后可对事件进行处理，这样即可实现在单一线程上对来自不同客户的请求进行交替处理，服务端处理返回后即可处理下一事件，而不会受制于客户端的响应速度，提高了并发访问的效率。

<!--break-->

Java NIO的样例代码如下：

**服务端**

```java
package com.coderli.nettylab.nio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

/**
 * @author lihongzhe 2018/7/11 10:59
 */
public class NioServer {

    public static void main(String[] args) {
        try {
            ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
            serverSocketChannel.bind(new InetSocketAddress("127.0.0.1", 7090));
            serverSocketChannel.configureBlocking(false);
            Selector selector = Selector.open();
            serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
            for (; ; ) {
                selector.select();
                Iterator<SelectionKey> keysItor = selector.selectedKeys().iterator();
                while (keysItor.hasNext()) {
                    SelectionKey selectionKey = keysItor.next();
                    keysItor.remove();
                    if (selectionKey.isAcceptable()) {
                        ServerSocketChannel ssChannel = (ServerSocketChannel) selectionKey.channel();
                        SocketChannel socketChannel = ssChannel.accept();
                        socketChannel.configureBlocking(false);
                        ByteBuffer buffer = ByteBuffer.allocate(17);
                        socketChannel.read(buffer);
                        System.out.println("Receive msg from client:" + new String(buffer.array()));
                        socketChannel.write(ByteBuffer.wrap(new String("Server: op_accept").getBytes()));
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}

```

**客户端**

```java
package com.coderli.nettylab.nio;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

/**
 * @author lihongzhe 2018/7/12 15:54
 */
public class NioClient {

    public static void main(String[] args) {
        try {
            SocketChannel socketChannel = SocketChannel.open();
            socketChannel.configureBlocking(false);
            socketChannel.connect(new InetSocketAddress("127.0.0.1", 7090));
            Selector selector = Selector.open();
            socketChannel.register(selector, SelectionKey.OP_CONNECT);
            selector.select();
            Iterator<SelectionKey> itor = selector.selectedKeys().iterator();
            while (itor.hasNext()) {
                SelectionKey key = itor.next();
                if (key.isConnectable()) {
                    System.out.println("Connectable...");
                    while (socketChannel.isConnectionPending()) {
                        socketChannel.finishConnect();
                        socketChannel.register(selector, SelectionKey.OP_READ);
                    }
                    SocketChannel channel = (SocketChannel) key.channel();
                    channel.write(ByteBuffer.wrap("I am client".getBytes()));
                }
            }
            for (; ; ) {
                selector.select();
                Iterator<SelectionKey> keyIterator = selector.selectedKeys().iterator();
                while (keyIterator.hasNext()) {
                    SelectionKey key = keyIterator.next();
                    if (key.isConnectable()) {
                        System.out.println("Connectable...");
                    }
                    if (key.isReadable()) {
                        SocketChannel channel = (SocketChannel) key.channel();
                        ByteBuffer buffer = ByteBuffer.allocate(17);
                        channel.read(buffer);
                        System.out.println("Receive msg from server:" + new String(buffer.array()));
                        keyIterator.remove();
                    }
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}

```

上述代码谈不上合理与严谨，仅是我实验中的代码，但可表述出Java NIO中的channel、select、selectionKey（事件）等基本要素，仅供参考。

对代码做一简单说明：

1. 服务端将监听端口绑定在7090上，并在通道上注册了OP_ACCEPT事件；
2. 客户端通过connect方法连接到服务端的该端口上，同时服务端监听到该事件，selector.select方法返回；
3. 客户端首先监听了OP\_CONNECT事件，在开始与服务端建立连接后，客户端获取到该事件并处理该事件，由于是非阻塞异步连接，因此需要通过socketChannel.isConnectionPending()来判断是否连接完成，并手动通过socketChannel.finishConnect();方法完成连接，然后注册OP\_READ事件，用于监听服务端传输的信息；
4. 客户端和服务端之间通过ByteBuffer作为载体传输数据；
5. 客户端监听的OP\_READ事件后，当服务端向channel写入数据后，客户端select到该事件，并读取信息。

对比BIO(OIO)来看，如要实现并发，BIO模式下的每一个客户端请求需要用一个线程与之对应，显然无法实现大规模并发；而NIO模式下，因为是事件驱动，一个selector可以处理所有客户端的事件，只有当有事件到达时才会返回处理，只需要启动一定数量的事件处理线程去异步处理客户端事件即可。因此，NIO模式从理论上具备应对高并发的条件。

至此，我暂不再去深究操作系统层面epoll等技术细节，带着对Java BIO、NIO的初步认识，下一步打算去了解一下使用Netty如何去创建和访问一个BIO、NIO的服务以及Netty带给我们的封装和基本的设计思想。