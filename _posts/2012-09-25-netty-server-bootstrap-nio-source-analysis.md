---
layout: post
title: Java NIO框架Netty教程(十六)-ServerBootStrap启动流程源码分析
date: 2012-09-25 13:42 +0800
author: onecoder
comments: true
tags: [Netty]
categories: [Java技术研究]
thread_key: 1150
---
有一段事件没有更新文章了，各种原因都有吧。搬家的琐事，搬家后的安逸呵呵。不过，<a href="http://www.coderli.com">OneCoder</a>明白，绝不能放松。对于Netty的学习，也该稍微深入一点了。

所以，这次<a href="http://www.coderli.com">OneCoder</a>花了几天时间，仔细梳理了一下**Netty**的源码，总结了一下**ServerBootStrap**的启动和任务处理流程，基本涵盖了Netty的关键架构。<a href="http://www.coderli.com">OneCoder</a>总结了一张流程图：

![](/images/oldposts/aGtVD.jpg)

该图是<a href="http://www.coderli.com">OneCoder</a>通过阅读Netty源码，逐渐记录下来的。基本可以说明**Netty**服务的启动流程。这里在具体讲解一下。

首先说明，我们这次顺利的流程是基于**NioSocketServer**的。也就是基于Java NIO Selector的实现方式。在第六讲<a href="http://www.coderli.com/netty-nio-selector">《Java NIO框架Netty教程(六)-Java NIO Selector模式》</a>中，我们已经知道使用Selector的几个关键点，所以这里我们也重点关注一下，这些点在Netty中是如何使用的。

很多看过**Netty**源码的人都说Netty源码写的很漂亮。可漂亮在哪呢？Netty通过一个**ChannelFactory**决定了你当前使用的协议类型(Nio/oio等)，比如，OneCoder这里使用的是**NioServerSocket**，那么需要声明的Factory即为**NioServerSocketChannelFactory**，声明了这个**Factory**，就决定了你使用的Channel，pipeline以及pipeline中，具体处理业务的sink的类型。这种使用方式十分简洁的，学习曲线很低，切换实现十分容易。

**Netty**采用的是基于事件的管道式架构设计，事件(Event)在管道(**Pipeline**)中流转，交由(通过pipelinesink)相应的处理器(**Handler**)。这些关键元素类型的匹配都是由开始声明的**ChannelFactory**决定的。

**Netty**框架内部的业务也遵循这个流程，**Server**端绑定端口的**binder**其实也是一个**Handler**，在构造完**Binder**后，便要声明一个**Pipeline**管道，并赋给新建一个**Channel**。**Netty**在**newChannel**的过程中，相应调用了Java中的**ServerSocketChannel.open**方法，打开一个**channel**。然后触发**fireChannelOpen**事件。这个事件的接受是可以复写的。**Binder**自身接收了这个事件。在事件的处理中，继续向下完成具体的端口的绑定。对应**Selector**中的 **socketChannel.socket().bind()**。然后触发**fireChannelBound**事件。默认情况下，该事件无人接受，继续向下开始构造**Boss**线程池。我们知道在**Netty**中**Boss**线程池是用来接受和分发请求的核心线程池。所以在**channel**绑定后，必然要启动**Boss**线城池，随时准备接受**client**发来的请求。在**Boss**构造函数中，第一次注册了**selector**感兴趣的事件类型,**SelectionKey.OP_ACCEPT**。至此，在第六讲中介绍的使用**Selector**的几个关键步骤都体现在**Netty**中了。在**Boss**中回启动一个死循环来查询是否有感兴趣的事件发生，对于第一次的客户端的注册事件，**Boss**会将**Channel**注册给**worker**保存。

这里补充一下，也是图中忽略的部分，就是关于**worker**线程池的初始化时机问题。**worker**池的构造，在最开始构造**ChannelFactory**的时候就已经准备好了。在**NioServerSocketChannelFactory**的构造函数里，会new一个**NioWorkerPool**。在**NioWorkerPool**的基类**AbstractNioWorkerPool**的构造函数中，会调用**OpenSelector**方法，其中也打开了一个**selector**，并且启动了**worker**线程池。<

```java
private void openSelector() {
        try {
            selector = Selector.open();
        } catch (Throwable t) {
            throw new ChannelException(&quot;Failed to create a selector.&quot;, t);
        }

        // Start the worker thread with the new Selector.
        boolean success = false;
        try {
            DeadLockProofWorker.start(executor, new ThreadRenamingRunnable(this, &quot;New I/O  worker #&quot; + id));
            success = true;
        } finally {
            if (!success) {
                // Release the Selector if the execution fails.
                try {
                    selector.close();
                } catch (Throwable t) {
                    logger.warn(&quot;Failed to close a selector.&quot;, t);
                }
                selector = null;
                // The method will return to the caller at this point.
            }
        }
        assert selector != null &amp;&amp; selector.isOpen();
    }
```

至此，会分线程启动AbstractNioWorker中run逻辑。同样是循环处理任务队列。

```java
processRegisterTaskQueue();
processEventQueue();
processWriteTaskQueue();
processSelectedKeys(selector.selectedKeys());
```

这样，设计使事件的接收和处理模块完全解耦。

由此可见，如果你想从nio切换到oio，只需要构造不同的ChannelFacotry即可。果然简洁优雅。