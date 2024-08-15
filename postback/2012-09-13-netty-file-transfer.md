---
layout: post
title: Java NIO框架Netty教程(十五)-利用Netty进行文件传输
date: 2012-09-13 12:53 +0800
author: onecoder
comments: true
tags: [Netty]
thread_key: 1140
---
如果您持续关注<a href="http://www.coderli.com">OneCoder</a>，您可能会问，在<a href="http://www.coderli.com/netty-oio-nio">《Java NIO框架Netty教程(十四)- Netty中OIO模型(对比NIO)》</a>中不是说下节介绍的是，**NIO**和**OIO**中的**worker**处理方式吗。这个一定会有的，只是在研究的过程中，<a href="http://www.coderli.com">OneCoder</a>发现了之前遗留的文件传输的代码，所以决定先完成它。

其实，Netty的样例代码中也提供了文件上传下载的代码样例，不过太过复杂，还包括了Http请求的解析等，对<a href="http://www.coderli.com">OneCoder</a>来说，容易迷惑那些才是文件传输的关键部分。所以<a href="http://www.coderli.com">OneCoder</a>决定根据自己去写一个样例，这个理解就是在最开始提到的，Netty的传输是基于流的，我们把文件流化应该就可以传递了。于是有了以下的代码：

```java
/**
 * 文件传输接收端，没有处理文件发送结束关闭流的情景
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class FileServerHandler extends SimpleChannelHandler {

	private File file = new File(&quot;F:/2.txt&quot;);
	private FileOutputStream fos;

	public FileServerHandler() {
		try {
			if (!file.exists()) {
				file.createNewFile();
			} else {
				file.delete();
				file.createNewFile();
			}
			fos = new FileOutputStream(file);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void messageReceived(ChannelHandlerContext ctx, MessageEvent e)
			throws Exception {
		ChannelBuffer buffer = (ChannelBuffer) e.getMessage();
		int length = buffer.readableBytes();
		buffer.readBytes(fos, length);
		fos.flush();
		buffer.clear();
	}

}
```

```java
/**
 * 文件发送客户端，通过字节流来发送文件，仅实现文件传输部分，<br>
 * 没有对文件传输结束进行处理<br>
 * 应该发送文件发送结束标识，供接受端关闭流。
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class FileClientHandler extends SimpleChannelHandler {

        // 每次处理的字节数
	private int readLength = 8;

	@Override
	public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e)
			throws Exception {
		// 发送文件
		sendFile(e.getChannel());
	}

	private void sendFile(Channel channel) throws IOException {
		File file = new File(&quot;E:/1.txt&quot;);
		FileInputStream fis = new FileInputStream(file);
		int count = 0;
                BufferedInputStream bis = new BufferedInputStream(fis);
		for (;;) {
			byte[] bytes = new byte[readLength];
			int readNum = bis.read(bytes, 0, readLength);
			if (readNum == -1) {
				return;
			}
			sendToServer(bytes, channel, readNum);
			System.out.println(&quot;Send count: &quot; + ++count);
		}

	}

	private void sendToServer(byte[] bytes, Channel channel, int length)
			throws IOException {
		ChannelBuffer buffer = ChannelBuffers.copiedBuffer(bytes, 0, length);
		channel.write(buffer);
	}

}
```

待发送的文件1.txt内容如下：

<img alt="" src="/images/oldposts/2OWBx.jpg" style="height: 401px; width: 630px; " />

运行上述代码，接受到的文件2.txt结果：

<img alt="" src="/images/oldposts/L4ywi.jpg" style="width: 630px; " />

完全一模一样。成功！

这只是一个简单的文件传输的例子，可以做为样例借鉴。对于大文件传输的情景，本样例并不支持，会出现内存溢出的情景，OneCoder准备另外单独介绍一下。

