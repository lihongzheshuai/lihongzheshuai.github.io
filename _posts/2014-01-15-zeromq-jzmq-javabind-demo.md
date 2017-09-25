---
layout: post
title: ZeroMQ 初学 Java Binding验证代码
date: 2014-01-15 21:20 +0800
author: onecoder
comments: true
tags: [ZeroMQ]
thread_key: 1622
---
<div>
	学习ZeroMQ使用，根据官方文档介绍，写了如下Java验证代码。仅供参考。需要依赖jzmq的jar包和本地库。</div>
<div>
	&nbsp;</div>
<div>
	1、请求-响应模式</div>
<div style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DsNVlVf9/u01Cb.jpg" /></div>


```java
package com.coderli.zeromq.requestreplay;


import org.zeromq.ZMQ;
import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ 请求响应模式验证代码 <br>
 * 此为服务端
 *
 * @author OneCoder
 * @date 2014年1月13日 下午11:28:47
 * @website http://www.coderli.com
 */
public class ReplayServer extends JZMQBase {


     public static void main(String[] args) {
           // 参数代表使用多少线程，大多数情况下，1个线程已经足够。
          ZMQ.Context context = ZMQ. context(1);
           // 指定模式为响应模式
          ZMQ.Socket socket = context.socket(ZMQ. REP);
          socket.bind( LOCAL_ADDRESS); // 绑定服务地址及端口
           for (;;) {
              System. out.println( "Server start.");
              socket.recv();
              String str = "Ok, I'm server";
              socket.send(str);
          }
     }
}
```


```java
package com.coderli.zeromq.requestreplay;


import org.zeromq.ZMQ;
import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ 请求响应模式验证代码 <br>
 * 此为客户端
 *
 * @author OneCoder
 * @date 2014年1月11日 上午10:34:18
 * @website http://www.coderli.com
 */
public class RequestClient extends JZMQBase {


     /**
      * @param args
      * @author OneCoder
      * @date 2014年1月11日 上午10:34:18
      */
     public static void main(String[] args) {


          ZMQ.Context context = ZMQ. context(1);
           // 指定模式为请求模式
          ZMQ.Socket socket = context.socket(ZMQ. REQ);
           // 创建链接
          socket.connect( LOCAL_ADDRESS);
           int count = 1;
           for (;;) {
               try {
                    long time = System. nanoTime();
                   socket.send( "Hello, currentTime: " + count);
                    byte[] recs = socket.recv();
                    long end = System. nanoTime();
                   System. out.println( new String(recs) + " Cost time: "
                             + (end - time));
                   count++;
                   Thread. sleep(1000);
              } catch (Exception e) {
                   e.printStackTrace();
              }
          }
     }
}
```

<div>
	测试结果，单线程请求-相应一次的耗时大概在450us。</div>

<div>
	2、Publish-subscribe</div>

<div style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DsNVlspt/Sg75e.jpg" /></div>

```java
package com.coderli.zeromq.pubsub;


import java.util.Random;


import org.zeromq.ZMQ;


import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ 发布订阅模式Java验证代码 <br>
 * 此为发布者
 *
 * @author OneCoder
 * @date 2014年1月14日 上午11:16:03
 * @blog http://www.coderli.com
 */
public class Publisher extends JZMQBase {


     public static void main(String[] args) throws InterruptedException {
           // 参数代表使用多少线程，大多数情况下，1个线程已经足够。
          ZMQ.Context context = ZMQ. context(1);
           // 指定模式为发布者
          ZMQ.Socket socket = context.socket(ZMQ. PUB);
          socket.bind( LOCAL_ADDRESS); // 绑定服务地址及端口
           for (;;) {
               int i = ( int) ( new Random().nextDouble() * 2 + 1);
              String s = String. valueOf(i);
               long time = System. nanoTime();
              socket.send(s + String. valueOf(time));
              System. out.println( "发布了新消息，时间：" + time + " 类型：" + s);
              Thread. sleep(2000);
          }
     }
}
```

```java
package com.coderli.zeromq.pubsub;


import org.zeromq.ZMQ;


import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ 发布订阅模式Java验证代码 <br>
 * 此为订阅者1号
 *
 * @author OneCoder
 * @date 2014年1月14日 上午11:16:03
 * @blog http://www.coderli.com
 */
public class SubscriberOne extends JZMQBase {


     public static void main(String[] args) throws InterruptedException {
          ZMQ.Context context = ZMQ. context(1);
           // 指定模式为请求模式
          ZMQ.Socket socket = context.socket(ZMQ. SUB);
           // 创建订阅者，必须要过主题过滤器
           byte[] filter = "1".getBytes();
          socket.subscribe(filter);
          socket.connect( LOCAL_ADDRESS);
           for (;;) {
               byte[] recs = socket.recv();
               long receiveTime = System. nanoTime();
              String oriMsg = new String(recs);
              String msg = new String(recs,1,recs.length-1);
               long pubTime = Long. valueOf(msg);
               long costTime = receiveTime - pubTime;
              System. out.println( "Receive: " + oriMsg + " Cost time: " + costTime);
          }
     }
}
```

```java
package com.coderli.zeromq.pubsub;


import org.zeromq.ZMQ;


import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ 发布订阅模式Java验证代码 <br>
 * 此为订阅者2号
 *
 * @author OneCoder
 * @date 2014年1月14日 上午11:16:03
 * @blog http://www.coderli.com
 */
public class SubscriberTwo extends JZMQBase{


     public static void main(String[] args) throws InterruptedException {
          ZMQ.Context context = ZMQ. context(1);
           // 指定模式为请求模式
          ZMQ.Socket socket = context.socket(ZMQ. SUB);
           // 创建订阅者，必须要过主题过滤器
           byte[] filter = "2".getBytes();
          socket.subscribe(filter);
          socket.connect( LOCAL_ADDRESS);
           for (;;) {
               byte[] recs = socket.recv();
               long receiveTime = System. nanoTime();
              String oriMsg = new String(recs);
              String msg = new String(recs,1,recs.length-1);
               long pubTime = Long. valueOf(msg);
               long costTime = receiveTime - pubTime;
              System. out.println( "Receive: " + oriMsg + " Cost time: " + costTime);
          }
     }
}
```


<div>
	&nbsp; &nbsp;* 发布者中随机发布开头为1或者2的消息。</div>
<div>
	&nbsp; &nbsp;* 订阅者中必须有过滤器，从前向后匹配发布者发送的消息，完全匹配则接收消息。这里1/2号订阅者分别过滤消息开头是1/2的数据。</div>
<div>
	&nbsp; &nbsp;* 如果没有发布者，则订阅者阻塞，直到有发布者发送消息。如果订阅者掉线，消息会丢失。</div>
<div>
	&nbsp; &nbsp;* 如果要订阅多个filter只需多次调用subscribe方法即可。</div>
<div>
	&nbsp; &nbsp;* 从发布到订阅收到消息，大约耗时300us。</div>
<div>
	&nbsp;</div>
<div>
	3、PipeLine模式</div>
<div>
	&nbsp;</div>
<div>
	想象一下这样的场景，如果需要统计各个机器的日志，我们需要将统计任务分发到各个节点机器上，最后收集统计结果，做一个汇总。PipeLine比较适合于这种场景，他的结构图，如图3所示。</div>
<div style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DsNVl5to/WRcmX.jpg" /></div>

```java
package com.coderli.zeromq.pipeline;

import org.zeromq.ZMQ;
import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Pipeline模式Java验证代码 <br>
 * 此为主Pusher
 *
 * @author OneCoder
 * @date 2014年1月14日 上午11:16:03
 * @blog http://www.coderli.com
 */
public class MainPusher extends JZMQBase {


     public static void main(String[] args) throws InterruptedException {
           // 参数代表使用多少线程，大多数情况下，1个线程已经足够。
          ZMQ.Context context = ZMQ. context(1);
           // 指定模式为Pusher
          ZMQ.Socket socket = context.socket(ZMQ. PUSH);
          socket.bind( LOCAL_ADDRESS); // 绑定服务地址及端口
           for (;;) {
               long time = System. nanoTime();
              socket.send(String. valueOf(time));
              System. out.println( "发布了新消息，时间：" + time);
              Thread. sleep(2000);
          }
     }


}
```

```java
package com.coderli.zeromq.pipeline;

import org.zeromq.ZMQ;
import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Pipeline模式Java验证代码 <br>
 * 此为中转worker
 *
 * @author OneCoder
 * @date 2014年1月14日 上午11:16:03
 * @blog http://www.coderli.com
 */
public class WorkerOne extends JZMQBase {


     public static void main(String[] args) {
           // 指定模式为pull模式
          ZMQ.Socket receiver = ZMQ.context(1).socket(ZMQ.PULL);
          receiver.connect( LOCAL_ADDRESS);
           // 指定模式为push模式
          ZMQ.Socket sender = ZMQ.context(1).socket(ZMQ.PUSH);
          sender.connect( LOCAL_ADDRESS_PUSHER);
           for (;;) {
               byte[] recs = receiver.recv();
               long receiveTime = System. nanoTime();
              String oriMsg = new String(recs);
               long pubTime = Long. valueOf(oriMsg);
               long costTime = receiveTime - pubTime;
              System. out.println( "Receive: " + oriMsg + " Cost time: " + costTime);
              sender.send( "1" + oriMsg);
              System. out.println( "Send to sinker.");
          }
     }
}
```

```java
package com.coderli.zeromq.pipeline;

import org.zeromq.ZMQ;
import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Pipeline模式Java验证代码 <br>
 * 此为中转worker
 *
 * @author OneCoder
 * @date 2014年1月14日 上午11:16:03
 * @blog http://www.coderli.com
 */
public class WorkerTwo extends JZMQBase {


     public static void main(String[] args) {
           // 指定模式为pull模式
          ZMQ.Socket receiver = ZMQ.context(1).socket(ZMQ.PULL);
          receiver. connect(LOCAL_ADDRESS);
           // 指定模式为push模式
          ZMQ.Socket sender = ZMQ.context(1).socket(ZMQ.PUSH);
          sender. connect(LOCAL_ADDRESS_PUSHER);
           for (;;) {
               byte[] recs = receiver.recv();
               long receiveTime = System. nanoTime();
              String oriMsg = new String(recs);
               long pubTime = Long. valueOf(oriMsg);
               long costTime = receiveTime - pubTime;
              System. out
                        .println( "Receive: " + oriMsg + " Cost time: " + costTime);
              sender.send( "2" + oriMsg);
              System. out.println( "Send to sinker.");
          }
     }
}
```

```java
package com.coderli.zeromq.pipeline;

import org.zeromq.ZMQ;
import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Pipeline模式Java验证代码 <br>
 * 此为最终sinker
 *
 * @author OneCoder
 * @date 2014年1月14日 上午11:16:03
 * @blog http://www.coderli.com
 */
public class Sinker extends JZMQBase {


     public static void main(String[] args) {
          ZMQ.Context context = ZMQ. context(1);
           // 指定模式为pull模式
          ZMQ.Socket receiver = context.socket(ZMQ. PULL);
          receiver. bind(LOCAL_ADDRESS_PUSHER);
           for (;;) {
               byte[] recs = receiver.recv();
               long receiveTime = System. nanoTime();
              String oriMsg = new String(recs);
              String msg = new String(recs,1,recs.length-1);
               long pubTime = Long. valueOf(msg);
               long costTime = receiveTime - pubTime;
              System. out.println( "Receive: " + oriMsg + " Cost time: " + costTime);
          }
     }
}
```

<div>
	以上只是一些初级结构的初步使用，对于我来说重点还是研究router模式，实现N对M集群的定向通信。随后会公布研究代码</div>

