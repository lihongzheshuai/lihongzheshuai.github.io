---
title: Netty4自学笔记 (1) - Java BIO
tags: [Netty,BIO]
date: 2018-07-06 21:41:24 +0800
comments: true
author: onecode
---
2012年，由于项目的需要我第一次接触到了Netty，当时Netty还处于3.x版本。我用十几篇博文记录了自己自学Netty的过程，虽然内容浅薄，但没想到被各处转载，我想主要是因为当时Netty的资料确实较少的缘故。

五六年过去了，Netty早已发展了4.x系列，好奇也好，求知也罢，我打算重学Netty，虽然严格来说，我已不是IT从业人员，但我仍希望保留对技术的热爱与追求。

学习Netty，就免不了先去了解Java中的几种通信模型。我不想先去学习很多概念，单刀直入，就先从最容易理解的BIO（阻塞I/O）学起。

<!--break-->

阻塞I/O，顾名思义，就是服务端在接受到客户端的请求时，在当前线程下是阻塞执行的。只有当一个客户端请求关闭后，才能接受其他客户端的请求。阻塞I/O的JDK原生实现代码如下：

**服务端**
```java?linenums
package com.coderli.nettylab.bio;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * @author lihongzhe 2018-06-19 11:06
 */
public class BioServer {

    public static void main(String[] args) throws IOException {
        ServerSocket socketServer = new ServerSocket();
        socketServer.bind(new InetSocketAddress("127.0.0.1", 7080)); 
        for (; ; ) {
            Socket socket = socketServer.accept();
            System.out.println("接收到新的连接请求。");
            InputStream is = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(is));
            String line = reader.readLine();
            System.out.println(line);
            socket.getOutputStream().write("Hello, I'm server.".getBytes());
            socket.shutdownOutput();
        }
    }

}
```

**客户端**

```java?linenums
package com.coderli.nettylab.bio;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketImpl;

/**
 * @author lihongzhe 2018-06-21 23:24
 */
public class BioClient {

    public static void main(String[] args) throws IOException {
        Socket socket = new Socket();
        socket.connect(new InetSocketAddress("127.0.0.1", 7080));
        OutputStream os = socket.getOutputStream();
        InputStream is = socket.getInputStream();
        os.write("Hello, I'm client.".getBytes());
        socket.shutdownOutput();
        BufferedReader br = new BufferedReader(new InputStreamReader(is));
        System.out.println(br.readLine());
        socket.close();
    }

}

```

简单解释一下上述代码：

 1. 服务端，通过 socketServer.bind() 绑定到指定的端口；
 2. 服务端，通过 socketServer.accept() 开启监听，等待客户端连接。当没有客户端连接时，代码阻塞在此处；
 3. 客户端，先构造一个Socket实例，然后通过socket.connect(）函数连接到刚服务端绑定的端口上。此时，若成果连接，则服务端代码继续执行；
 4. 服务端，socketServer.accept() 函数返回一个Socket实例，在实例中可以得倒输入(InputStream)/输出(OutputStream)流，用于与客户端之间读取/写入数据；
 5. 由于底层依赖的协议并没有要求数据流必须一次传输完成，实际上对于要传输的数据，可多次调用 socket.getOutputStream().write()函数写入数据。因此，必须有明确的手段标明一次数据传输的结束， socket.shutdownOutput()函数的作用正是如此。

由此可见，服务端同一时刻、同一线程只能处理来自一个客户端的请求，显然这种连接模式的并发效率并不能令人满意。

我暂不深究更多的细节，接下来先去了解一下Java NIO模式的特点和开发方式。

