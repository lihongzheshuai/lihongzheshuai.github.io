---
layout: post
title: Java NIO框架Netty教程（二） - 白话概念
date: 2012-07-11 22:38 +0800
author: onecoder
comments: true
tags: [Java,Netty,NIO]
thread_key: 913
---

<a href="http://www.coderli.com/netty-course-hello-world/" target="\_blank"> "Hello World"</a>的代码固然简单，不过其中的几个重要概念（类）和 Netty的工作原理还是需要简单明确一下，至少知道其是负责什。方便自己以后更灵活的使用和扩展。

声明，笔者一介码农，不会那么多专业的词汇和缩写，只能以最简单苍白的话来形容个人的感受和体会。如果您觉得这太不专业，笔者首先只能抱歉。

### ChannelEvent

![](/images/oldposts/FjuwT.jpg)

先说这个ChannelEvent，因为Netty是基于事件驱动的，就是我们<a href="http://www.coderli.com/netty-course-hello-world/" target="\_blank">上文</a>提到的，发生什么事，就通知"有关部门"。所以，不难理解，我们自己的业务代码中，一定有跟这些事件相关的处理。在<a href="http://www.coderli.com/netty-course-hello-world/" target="\_blank">样例代码</a>，我们处理的事件，就是**channelConnected**。以后，我们还会处理更多的事件。

### ChannelPipeline

![](/images/oldposts/y2XNy.jpg)

**Pipeline**，翻译成中文的意思是：管道，传输途径。也就是说，在这里他是控制**ChannelEvent**事件分发和传递的。事件在管道中流转，第一站到哪，第二站到哪，到哪是终点，就是用这个**ChannelPipeline**处理的。比如：开发事件。先给A设计，然后给B开发。一个流转图，希望能给你更直观的感觉。

![](/images/oldposts/3SIYH.jpg)

### ChannelHandler

刚说**Pipeline**负责把事件分发到相应的站点，那个这个站点在Netty里，就是指**ChannelHandler**。事件到了**ChannelHandler**这里，就要被具体的进行处理了，我们的<a href="http://www.coderli.com/netty-course-hello-world/" >样例代码</a>里，实现的就是这样一个处理事件的"站点"，也就是说，你自己的业务逻辑一般都是从这里开始的。

![](/images/oldposts/BuUyL.jpg)

有了个部门的协调处理，我们还需要一个从整体把握形势的，所谓"大局观"的部门，**channel**。

**channel**，能够告诉你当前通道的状态，是连同还是关闭。获取通道相关的配置信息。得到**Pipeline**等。是一些全局的信息。**Channel**自然是由**ChannelFactory**产生的。**Channel**的实现类型，决定了你这个通道是同步的还是异步的(nio)。例如，我们<a href="http://www.coderli.com/netty-course-hello-world/" target="\_blank">样例</a>里用的是**NioServerSocketChannel**。

这些基本的概念，你懂了吧。
