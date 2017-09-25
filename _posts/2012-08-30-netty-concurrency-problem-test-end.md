---
layout: post
title: Java NIO框架Netty教程(十三)-并发访问测试(下)
date: 2012-08-30 21:47 +0800
author: onecoder
comments: true
tags: [Netty]
thread_key: 1116
---
在上节(<a href="http://www.coderli.com/netty-concurrency-problem-test-two" target="\_blank">《Java NIO框架Netty教程(十二)-并发访问测试(中)》</a>)，我们从各个角度对**Netty**并发的场景进行了测试。这节，我们将重点关注上节最后提到的问题。在多线程并发访问的情况下，会出现
<blockquote>
<div>警告: EXCEPTION, please implement one.coder.netty.chapter.eight.ObjectClientHandler.exceptionCaught() for proper handling.</div>
<div>java.net.ConnectException: Connection refused: no further information</div></blockquote>
<div>
<div>的错误警告。</div>
<div></div>
<div>之前<a href="http://www.coderli.com/">OneCoder</a>层怀疑过是端口数不够的问题，所以还准备了一套修改操作系统端口数限制的配置。</div>
</div>
<div>
<blockquote>
<div>a) windows --</div>
<div>1、打开注册表：regedit</div>
<div>2、HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\ Services\TCPIP\Parameters</div>
<div>3、新建 DWORD值，name：TcpTimedWaitDelay，value：0（十进制） –&gt; 设置为0</div>
<div>4、新建 DWORD值，name：MaxUserPort，value：65534（十进制） –&gt; 设置最大连接数65534</div>
<div>5、重启系统</div>
<div></div>
<div>b) linux --</div>
<div>1、查看有关的选项 /sbin/sysctl -a|grep net.ipv4.tcp_tw</div>
<div>   net.ipv4.tcp_tw_reuse = 0</div>
<div>   #表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；</div>
<div>   net.ipv4.tcp_tw_recycle = 0</div>
<div>   #表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭</div>
<div>2、修改 vi /etc/sysctl.conf</div>
<div>   net.ipv4.tcp_tw_reuse = 1</div>
<div>   net.ipv4.tcp_tw_recycle = 1</div>
<div>3、使内核参数生效sysctl -p</div></blockquote>
</div>
这套配置在测试Restlet框架并发的时候，起到了明显的效果。
<div></div>
<div>然后，这次即使 <a href="http://www.coderli.com/">OneCoder</a> 修改配置，并发连接也没有明显的上升。 <a href="http://www.coderli.com/">OneCoder</a> 决定换个思路，启动多个进程对同一个服务进行持续访问，以证明之前的连接拒绝就是因为客户端多线程并发自身的问题(其实 <a href="http://www.coderli.com/">OneCoder</a> 一直非常怀疑是这个问题)还是服务端连接处理的问题。</div>
<div>修改了一下客户端发动消息的代码，使其在其线程内部，不停的给服务端发送信息。</div>

```java
	**
	 * 发送Object
	 * 
	 * @param channel
	 * @author lihzh
	 * @alia OneCoder
         * @blog http://www.coderli.com
	 */
	private void sendObject(final Channel channel) {
		new Thread(new Runnable() {

			@Override
			public void run() {
				// TODO Auto-generated method stub
				for (;;) {
					Command command = new Command();
					command.setActionName("Hello action.");
					channel.write(command);
					try {
						Thread.sleep(1000);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
			}
		}).start();
	}
```

启动多个客户端，效果如图：

![](http://onecoder.qiniudn.com/8wuliao/CehmeXcf/4hFcy.jpg)

<div>果然，在单个进程数量控制合理的情况下，服务端可以处理所有请求，不会出现链接拒绝的情况。总连接数轻松达到4，5k。（ <a href="http://www.coderli.com/">OneCoder</a> 注：以前超过1000都容易出错。这里只是测试到以前完全没有办法支持的情形，并没有测试最大压力值。）</div>
<div></div>
<div>对于测试Netty服务端压力来说，这样的测试， <a href="http://www.coderli.com/">OneCoder</a> 认为完全可以起到效果，有参考价值。因为即使单进程网络连接方面无上限，单进程能启动的线程数也是有限制的，效率也一定会受到影响。所以，对于并发测试来说， <a href="http://www.coderli.com/">OneCoder</a> 认为可以采用上面的方式。</div>
<div></div>
<div>对于，单进程多线程的时，拒绝连接的问题。是在sun.nio.ch.SocketChannelImple 中的native方法checkConnect中抛出的。这应该是跟操作系统密切相关的。 <a href="http://www.coderli.com/">OneCoder</a> 没有在linux下进行测试，但是猜测在linux下，上面的设置参数是可以起到作用的，也就是会比windows下可以开启的并发线程数多。当然这只是猜测。</div>
<div></div>
<div>对于windows来说，揪净能开启多个线程的并发，这个数据在 <a href="http://www.coderli.com/">OneCoder</a> 的环境下也是非常不稳定的。最开始的时候是，起1000个线程，成功的350个线程左右。后来， <a href="http://www.coderli.com/">OneCoder</a> 怀疑启动的程序过多，尤其是跟网络相关的程序会影响测试结果，关闭了很多程序。结果，多次1000线程都成功连接。</div>
<div></div>
<div><a href="http://www.coderli.com/">OneCoder</a>仔细排查了一下，猛然发现 <a href="http://www.coderli.com/">OneCoder</a> 使用了Proxifier这个代理。在代理打开的情况下，一般只能跑到300左右。关闭有1000个线程基本稳定通过。最多可以跑到1500左右。目前被列为最大“嫌疑人”</div>
<div></div>
<div>以 <a href="http://www.coderli.com/">OneCoder</a> 目前的知识构成来说，Netty并发的测试基本可以告一段落了。再简单的总结唠到几句：</div>
<div>
<ol>
	<li>如果需要测试并发，可以考虑多进程，进程内多线程的方式测试服务端压力。</li>
	<li><a href="http://www.coderli.com/">OneCoder</a> 没有测试Netty最大可以支持多少并发，因为从目前测试的效果来看。（5个进程，每个进程1000线程，持续访问同一个服务），已经完全可以满足 <a href="http://www.coderli.com/">OneCoder</a> 的要求了。您也可以继续测试下去。</li>
	<li><a href="http://www.coderli.com/">OneCoder</a> 使用的是windows7 32位操作系统，在测试过程其实也修改了注册表中的若干参数，包括上面提到的两个。不知道是否起到了一定的作用，也就是是否使单进程可以支持的多线程数增加，或者服务端可以支持的连接数增加，您在测试的过程中，可以配合考虑这些参数。</li>
	<li>对于，connection refuse的具体原因， <a href="http://www.coderli.com/">OneCoder</a> 希望能随着自己知识的慢慢积累，找到其真正的答案。</li>
</ol>
</div>
