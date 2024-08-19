---
layout: post
title: JVM运行时数据区详解-Stack栈(优化配置、代码样例)
date: 2012-08-03 12:58 +0800
author: onecoder
comments: true
tags: [JVM]
categories: [Java技术研究]
thread_key: 1027
---
最近有段时间没有更新**Netty**的教程了，却发了一些其他的东西。可能有的朋友会问，难道这就完事了？不会的。两方面原因。第一、笔者也是需要工作的人，自然要完成好工作中的任务，这里面也有很多东西需要学习和研究，这也是我分享的方向和源泉。第二、想要掌握好**Netty**，周边的知识也不能少，这也是笔者在恶补的东西。所以，你完全可以把我最近分享的东西理解为为学习**Netty**所做的准备。

**Java**虚拟机定义了若干种程序运行期间会使用到的运行时数据区，其中有一些会随着虚拟机启动而创建，随着虚拟机退出而销毁。另外一些则是与线程一一对应的，这些与线程对应的数据区域会随着线程开始和结束而创建和销毁。

# Stack栈
栈也叫栈内存，是Java程序的运行区，是在线程创建时创建，它的生命期是跟随线程的生命期，线程结束栈内存也就释放，对于栈来说不存在垃圾回收问题，只要线程一结束，该栈就Over。问题出来了：栈中存的是那些数据呢？又什么是格式呢？
栈中的数据都是以栈帧（**Stack Frame**）的格式存在，栈帧是一个内存区块，是一个数据集，是一个有关方法(**Method**)和运行期数据的数据集，当一个方法A被调用时就产生了一个栈帧F1，并被压入到栈中，A方法又调用了B方法，于是产生栈帧F2也被压入栈，执行完毕后，先弹出F2栈帧，再弹出F1栈帧，遵循“先进后出”原则。
那栈帧中到底存在着什么数据呢？栈帧中主要保存3类数据：本地变量（**Local Variables**），包括输入参数和输出参数以及方法内的变量；栈操作（**Operand Stack**），记录出栈、入栈的操作；栈帧数据（**Frame Data**），包括类文件、方法等等。光说比较枯燥，我们画个图来理解一下Java栈，如下图所示：

![](/images/oldposts/sXecH.jpg)

图示在一个栈中有两个栈帧，栈帧2是最先被调用的方法，先入栈，然后方法2又调用了方法1，栈帧1处于栈顶的位置，栈帧2处于栈底，执行完毕后，依次弹出栈帧1和栈帧2，线程结束，栈释放。

根据**Java**虚拟机规范，**Java**虚拟机规范允许**Java**虚拟机栈被实现成固定大小的或者是根据计算动态扩展和收缩的。如果采用固定大小的Java虚拟机栈设计，那每一条线程的**Java**虚拟机栈容量应当在线程创建的时候独立地选定。**Java**虚拟机实现应当提供给程序员或者最终用户调节虚拟机栈初始容量的手段，对于可以动态扩展和收缩Java虚拟机栈来说，则应当提供调节其最大、最小容量的手段。
如果线程请求分配的栈容量超过**Java**虚拟机栈允许的最大容量时，**Java**虚拟机将会抛出一个**StackOverflowError**异常。

根据上面的分析，我们来构造一个**StackOverflowError**来加深理解：

```java
/**
 * JVM参数配置
 * 
 * @author lihzh(OneCoder)
 * @alia OneCoder
 * @Blog http://www.coderli.com
 * @date 2012-7-31 下午9:04:26
 */
public class JVMParams {
	/**
	 * @author lihzh(OneCoder)
	 * @date 2012-7-31 下午9:04:27
	 */
	public static void main(String[] args) {
		getStackOverFlowError(0);
	}

	/**
	 * 通过递归调用，诱发StackOverFlowError
	 * 
	 * @author lihzh
	 * @alia OneCoder
	 */
	private static void getStackOverFlowError(int count) {
		if (count < 10000) {
			System.out.println("count:" + count);
			getStackOverFlowError(++count);
		}
	}
}
```

> 
> count:4388
Exception in thread "main" java.lang.StackOverflowError
at sun.nio.cs.UTF_8.updatePositions(UTF_8.java:77)
at sun.nio.cs.UTF_8$Encoder.encodeArrayLoop(UTF_8.java:564)
at sun.nio.cs.UTF_8$Encoder.encodeLoop(UTF_8.java:619)
at java.nio.charset.CharsetEncoder.encode(CharsetEncoder.java:561)
at sun.nio.cs.StreamEncoder.implWrite(StreamEncoder.java:271)

在递归调用4388遍时，出现**stackoverflow**异常。(该数据不稳定，大约在4300行左右)。

下面修改下虚拟机栈的大小再配置一下，根据我们之前的文章介绍。设置

```
-Xss1024k。
```

> 
count:13404
Exception in thread "main" java.lang.StackOverflowError
at sun.nio.cs.UTF_8.updatePositions(UTF_8.java:77)

发现确实有明显的变化。再增大一倍试试。

![](/images/oldposts/xIGTl.jpg)


> 
count:24618
count:24619
Exception in thread "main" java.lang.StackOverflowError

《**Java虚拟机规范**》中对于**Stack**还有一段描述：

> 
如果Java虚拟机栈可以动态扩展，并且扩展的动作已经尝试过，但是目前无法申请到足够的内存去完成扩展，或者在建立新的线程时没有足够的内存去创建对应的虚拟机栈，那Java虚拟机将会抛出一个**OutOfMemoryError**异常。

我们再来，构造一个 **OutOfMemoryError** 异常。设置

```
-Xss170m
```
（具体临界值取决与测试机的系统环境，和**JVM**配置）。再跑一次，果然抛出：

> Error occurred during initialization of VM
java.lang.OutOfMemoryError: unable to create new native thread

这里网上给出了计算可以创建出最大线程数的计算公式：

```
MaxProcessMemory - JVMMemory - ReservedOsMemory) / (ThreadStackSize) = 线程数
MaxProcessMemory 指的是一个进程的最大内存
JVMMemory         JVM内存
ReservedOsMemory  保留的操作系统内存
ThreadStackSize      线程栈的大小
```

**OneCoder**在这里猜测，是否是当计算出的线程数 <1 时，便会抛出这样的异常。这个公式涉及到4个值，不过有的可以有据可查的。在**32**位系统下，**MaxProcessMemory**一般认识为**2G**。**JVM**内存我们可以通过-Xmx指定。保留的操作系统内存，网上说一般是**120m**左右，**OneCoder**这里无据可查，暂不考虑。

不过可以看到，栈空间的分配是用的**JVM**之外的部分(如果错误，还请指正。)，我们可以控制的是**-Xmx**的大小，所以OneCoder这里把**-Xmx**设置成**10m**(改小。)，测试**-Xms180m**的情形，果然可以成功运行了。

到这里，**OneCoder**其实认为研究还远未结束，**OneCoder**根据上面的公式和**OneCoder**的猜测，**-Xss**的最大值怎么也不应该这么小，当然这很可能是我猜测错了，但是真像是什么呢？。无奈一时间也无法验证，暂且就当存疑吧，希望随着对**JVM**的了解，能逐渐揭开一团。

**OneCoder**提醒：由此可见**-Xss**参数的设置是需要非常消息的，太大，则可能会无法创建足够的线程，太小，则可能无法进行足够深层次的递归。需要你对的你程序有足够的了解和把握的基础上，合理的优化栈的大小。

希望高手不吝赐教。感激不尽。

参考：

- 《Java虚拟机规范》
- 《慢慢琢磨JVM》
