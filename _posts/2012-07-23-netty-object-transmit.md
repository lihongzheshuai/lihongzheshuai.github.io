---
layout: post
title: Java NIO框架Netty教程(八)-Object对象传递
date: 2012-07-23 16:43 +0800
author: onecoder
comments: true
tags: [Netty]
categories: [Java技术研究,Netty]
thread_key: 982
---
说了这么多废话，才提到对象的传输，不知道您是不是已经不耐烦了。一个系统内部的消息传递，没有对象传递是不太现实的。下面就来说说，怎么传递对象。

如果，您看过前面的介绍，如果您善于专注本质，勤于思考。您应该也会想到，我们说过，**Netty**的消息传递都是基于流，通过**ChannelBuffer**传递的，那么自然，**Object**也需要转换成**ChannelBuffer**来传递。好在**Netty**本身已经给我们写好了这样的转换工具。**ObjectEncoder**和**ObjectDecoder**。

工具怎么用？再一次说说所谓的本质，我们之前也说过，**Netty**给我们处理自己业务的空间是在灵活的可子定义的**Handler**上的，也就是说，如果我们自己去做这个转换工作，那么也应该在**Handler**里去做。而**Netty**，提供给我们的**ObjectEncoder**和**Decoder**也恰恰是一组**Handler**。于是，修改**Server**和**Client**的启动代码：

```java
// 设置一个处理客户端消息和各种消息事件的类(Handler)
bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
    @Override
    public ChannelPipeline getPipeline() throws Exception {
        return Channels.pipeline(
		new ObjectDecoder(ClassResolvers.cacheDisabled(this
				.getClass().getClassLoader())),
		new ObjectServerHandler());
    }
});
```

```java
// 设置一个处理服务端消息和各种消息事件的类(Handler)
bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
	@Override
	public ChannelPipeline getPipeline() throws Exception {
		return Channels.pipeline(new ObjectEncoder(),
				new ObjectClientHandler());
	}
});
```

要传递对象，自然要有一个被传递模型，一个简单的**Pojo**，当然，实现序列化接口是必须的。

```java
/**
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class Command implements Serializable {

	private static final long serialVersionUID = 7590999461767050471L;

	private String actionName;

	public String getActionName() {
		return actionName;
	}

	public void setActionName(String actionName) {
		this.actionName = actionName;
	}
}
```

服务端和客户端里，我们自定义的Handler实现如下：

```java
/**
 * 对象传递服务端代码
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class ObjectServerHandler extends SimpleChannelHandler {

	/**
	 * 当接受到消息的时候触发
	 */
	@Override
	public void messageReceived(ChannelHandlerContext ctx, MessageEvent e)
			throws Exception {
		Command command = (Command) e.getMessage();
		// 打印看看是不是我们刚才传过来的那个
		System.out.println(command.getActionName());
	}
}
```

```java
/**
 * 对象传递，客户端代码
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class ObjectClientHandler extends SimpleChannelHandler {

	/**
	 * 当绑定到服务端的时候触发，给服务端发消息。
	 * 
	 * @author lihzh
	 * @alia OneCoder
	 */
	@Override
	public void channelConnected(ChannelHandlerContext ctx, ChannelStateEvent e) {
		// 向服务端发送Object信息
		sendObject(e.getChannel());
	}

	/**
	 * 发送Object
	 * 
	 * @param channel
	 * @author lihzh
	 * @alia OneCoder
	 */
	private void sendObject(Channel channel) {
		Command command = new Command();
		command.setActionName(&quot;Hello action.&quot;);
		channel.write(command);
	}

}
```

启动后，服务端正常打印结果：**Hello action**.

简单梳理一下思路：
			
1. 通过**Netty**传递，都需要基于流，以**ChannelBuffer**的形式传递。所以，**Object** -> **ChannelBuffer**.
2. Netty提供了转换工具，需要我们配置到Handler。
3. 样例从客户端 -> 服务端，单向发消息，所以在客户端配置了编码，服务端解码。如果双向收发，则需要全部配置**Encoder**和**Decoder**。

这里需要注意，注册到**Server**的**Handler**是有顺序的，如果你颠倒一下注册顺序：

```java
bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
	@Override
	public ChannelPipeline getPipeline() throws Exception {
		return Channels.pipeline(new ObjectServerHandler(),
				new ObjectDecoder(ClassResolvers.cacheDisabled(this
						.getClass().getClassLoader()))
				);
	}
});
```

结果就是，会先进入我们自己的业务，再进行解码。这自然是不行的，会强转失败。至此，你应该会用**Netty**传递对象了吧。

