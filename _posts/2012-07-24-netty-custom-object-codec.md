---
layout: post
title: Java NIO框架Netty教程(九)-Object对象编/解码
date: 2012-07-24 22:48 +0800
author: onecoder
comments: true
tags: [Netty]
categories: [Java技术研究]
thread_key: 990
---
看到题目，有的同学可能会想，上回不是说过<a href="http://www.coderli.com/netty-object-transmit/" target="\_blank">对象传递</a>了吗？是的，只是在<a href="http://www.coderli.com/netty-object-transmit/" target="\_blank">《Java NIO框架Netty教程(八)-Object对象传递》</a>中，我们只是介绍如何使用**Netty**提供的编/解码工具，完成对象的序列化。这节是想告诉你**Netty**具体是怎么做的，也许有的同学想自己完成序列化呢？况且，对象的序列化，随处可用：）
先看怎么编码。

```java
@Override
    protected Object encode(ChannelHandlerContext ctx, Channel channel, Object msg) throws Exception {
        ChannelBufferOutputStream bout =
            new ChannelBufferOutputStream(dynamicBuffer(
                    estimatedLength, ctx.getChannel().getConfig().getBufferFactory()));
        bout.write(LENGTH_PLACEHOLDER);
        ObjectOutputStream oout = new CompactObjectOutputStream(bout);
        oout.writeObject(msg);
        oout.flush();
        oout.close();

        ChannelBuffer encoded = bout.buffer();
        encoded.setInt(0, encoded.writerIndex() - 4);
        return encoded;
    }
```

其实你早已经应该想到了，在**Java**中对对象的序列化自然跑不出**ObjectOutputStream**了。**Netty**这里只是又做了一层包装，在流的开头增加了一个4字节的标志位。所以，**Netty**声明，该编码和解码的类必须配套使用，与单纯的**ObjectIntputStream**不兼容。

```java
		* An encoder which serializes a Java object into a {@link ChannelBuffer}.<br />
		* <p><br />
		* Please note that the serialized form this encoder produces is not<br />
		* compatible with the standard {@link ObjectInputStream}.&nbsp; Please use<br />
		* {@link ObjectDecoder} or {@link ObjectDecoderInputStream} to ensure the<br />
		* interoperability with this encoder.</p>
```

那么解码，自然是先解析出多余的4位，然后再通过**ObjectInputStream**解析。

关于Java对象序列化的细节问题，不在文本讨论的范围内，不过不知您是否感兴趣试试自己写一个呢？所谓，多动手嘛。

```java
/**
 * Object编码类
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class MyObjEncoder implements ChannelDownstreamHandler {

	@Override
	public void handleDownstream(ChannelHandlerContext ctx, ChannelEvent e)
			throws Exception {
		// 处理收发信息的情形
		if (e instanceof MessageEvent) {
			MessageEvent mEvent = (MessageEvent) e;
			Object obj = mEvent.getMessage();
			if (!(obj instanceof Command)) {
				ctx.sendDownstream(e);
				return;
			}
			ByteArrayOutputStream out = new ByteArrayOutputStream();
			ObjectOutputStream oos = new ObjectOutputStream(out);
			oos.writeObject(obj);
			oos.flush();
			oos.close();
			ChannelBuffer buffer = ChannelBuffers.dynamicBuffer();
			buffer.writeBytes(out.toByteArray());
			e.getChannel().write(buffer);
		} else {
			// 其他事件，自动流转。比如，bind，connected
			ctx.sendDownstream(e);
		}
	}
}
```

```java
/**
 * Object解码类
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class MyObjDecoder implements ChannelUpstreamHandler {

	@Override
	public void handleUpstream(ChannelHandlerContext ctx, ChannelEvent e)
			throws Exception {
		if (e instanceof MessageEvent) {
			MessageEvent mEvent = (MessageEvent) e;
			if (!(mEvent.getMessage() instanceof ChannelBuffer)) {
				ctx.sendUpstream(mEvent);
				return;
			}
			ChannelBuffer buffer = (ChannelBuffer) mEvent.getMessage();
			ByteArrayInputStream input = new ByteArrayInputStream(buffer.array());
			ObjectInputStream ois = new ObjectInputStream(input);
			Object obj = ois.readObject();
			Channels.fireMessageReceived(e.getChannel(), obj);
		}
	}
}
```

怎么样，是不是也好用？所谓，模仿，学以致用。

不过，提醒一下大家，这个实现里有很多硬编码的东西，切勿模仿，只是为了展示**Object**，编解码的处理方式和在**Netty**中的应用而已。
