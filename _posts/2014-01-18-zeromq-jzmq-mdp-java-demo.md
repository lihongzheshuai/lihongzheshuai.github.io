---
layout: post
title: ZeroMQ研究 Majordomo Protocol， Java样例实现
date: 2014-01-18 11:32 +0800
author: onecoder
comments: true
tags: [ZeroMQ]
thread_key: 1624
---
<div>
	最近研究利用zeromq实现多对多的双向自由收发。在官方上发现了MDP协议，经过验证貌似可行。正在开发中，将验证代码分享如下。</div>
<div>
	&nbsp;</div>
<div style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DtceMQG4/Gdysx.jpg" /></div>
<div>
	&nbsp;</div>
<div>
	交互协议栈：</div>
<div>
	&nbsp;</div>
<div>
	Worker端：</div>
<blockquote>
	<div>
		A READY command consists of a multipart message of 4 frames, formatted on the wire as follows:</div>
	<div>
		&nbsp;</div>
	<div>
		&nbsp; &nbsp;* Frame 0: Empty frame</div>
	<div>
		&nbsp; &nbsp;* Frame 1: "MDPW01" (six bytes, representing MDP/Worker v0.1)</div>
	<div>
		&nbsp; &nbsp;* Frame 2: 0x01 (one byte, representing READY)</div>
	<div>
		&nbsp; &nbsp;* Frame 3: Service name (printable string)</div>
	<div>
		&nbsp;</div>
	<div>
		A REQUEST command consists of a multipart message of 6 or more frames, formatted on the wire as follows:</div>
	<div>
		&nbsp;</div>
	<div>
		&nbsp; &nbsp;* Frame 0: Empty frame</div>
	<div>
		&nbsp; &nbsp;* Frame 1: "MDPW01" (six bytes, representing MDP/Worker v0.1)</div>
	<div>
		&nbsp; &nbsp;* Frame 2: 0x02 (one byte, representing REQUEST)</div>
	<div>
		&nbsp; &nbsp;* Frame 3: Client address (envelope stack)</div>
	<div>
		&nbsp; &nbsp;* Frame 4: Empty (zero bytes, envelope delimiter)</div>
	<div>
		&nbsp; &nbsp;* Frames 5+: Request body (opaque binary)</div>
	<div>
		&nbsp;</div>
	<div>
		A REPLY command consists of a multipart message of 6 or more frames, formatted on the wire as follows:</div>
	<div>
		&nbsp;</div>
	<div>
		&nbsp; &nbsp;* Frame 0: Empty frame</div>
	<div>
		&nbsp; &nbsp;* Frame 1: "MDPW01" (six bytes, representing MDP/Worker v0.1)</div>
	<div>
		&nbsp; &nbsp;* Frame 2: 0x03 (one byte, representing REPLY)</div>
	<div>
		&nbsp; &nbsp;* Frame 3: Client address (envelope stack)</div>
	<div>
		&nbsp; &nbsp;* Frame 4: Empty (zero bytes, envelope delimiter)</div>
	<div>
		&nbsp; &nbsp;* Frames 5+: Reply body (opaque binary)</div>
	<div>
		&nbsp;</div>
	<div>
		A HEARTBEAT command consists of a multipart message of 3 frames, formatted on the wire as follows:</div>
	<div>
		&nbsp;</div>
	<div>
		&nbsp; &nbsp;* Frame 0: Empty frame</div>
	<div>
		&nbsp; &nbsp;* Frame 1: "MDPW01" (six bytes, representing MDP/Worker v0.1)</div>
	<div>
		&nbsp; &nbsp;* Frame 2: 0x04 (one byte, representing HEARTBEAT)</div>
	<div>
		&nbsp;</div>
	<div>
		A DISCONNECT command consists of a multipart message of 3 frames, formatted on the wire as follows:</div>
	<div>
		&nbsp;</div>
	<div>
		&nbsp; &nbsp;* Frame 0: Empty frame</div>
	<div>
		&nbsp; &nbsp;* Frame 1: "MDPW01" (six bytes, representing MDP/Worker v0.1)</div>
	<div>
		&nbsp; &nbsp;* Frame 2: 0x05 (one byte, representing DISCONNECT)</div>
</blockquote>
<div>
	&nbsp;</div>
<div>
	Client端：</div>
<div>
	&nbsp;</div>
<blockquote>
	<div>
		A REQUEST command consists of a multipart message of 4 or more frames, formatted on the wire as follows:</div>
	<div>
		&nbsp;</div>
	<div>
		&nbsp; &nbsp;* Frame 0: Empty (zero bytes, invisible to REQ application)</div>
	<div>
		&nbsp; &nbsp;* Frame 1: "MDPC01" (six bytes, representing MDP/Client v0.1)</div>
	<div>
		&nbsp; &nbsp;* Frame 2: Service name (printable string)</div>
	<div>
		&nbsp; &nbsp;* Frames 3+: Request body (opaque binary)</div>
	<div>
		&nbsp;</div>
	<div>
		A REPLY command consists of a multipart message of 4 or more frames, formatted on the wire as follows:</div>
	<div>
		&nbsp;</div>
	<div>
		&nbsp; &nbsp;* Frame 0: Empty (zero bytes, invisible to REQ application)</div>
	<div>
		&nbsp; &nbsp;* Frame 1: "MDPC01" (six bytes, representing MDP/Client v0.1)</div>
	<div>
		&nbsp; &nbsp;* Frame 2: Service name (printable string)</div>
	<div>
		&nbsp; &nbsp;* Frames 3+: Reply body (opaque binary)</div>
</blockquote>
<div>
	&nbsp;</div>
<div>
	下面是示例代码，基于官方的代码精简改造，去掉了heartbeat机制。便于理解功能。</div>
<div>
	&nbsp;</div>
<div>
	Broker：</div>

```java
package com.coderli.zeromq.majordomoprotocol;


import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;


import org.zeromq.ZContext;
import org.zeromq.ZFrame;
import org.zeromq.ZMQ;
import org.zeromq.ZMsg;


import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Majordomo Protocol协议验证<br>
 * 用于实现多client、多worker实现双向指定目标数据收发 <br>
 * 此为核心Broker模块
 *
 */
public class Broker extends JZMQBase {


     private static class Service {
           // 服务名
           public final String name;
           // 请求信息队列
          Deque<ZMsg> requests;
           // 待用worker队列
          Deque<Worker> waiting; // List of waiting workers


           public Service(String name) {
               this. name = name;
               this. requests = new ArrayDeque<ZMsg>();
               this. waiting = new ArrayDeque<Worker>();
          }
     }


     private static class Worker {
           // worker的唯一标识
           @SuppressWarnings( "unused")
          String identity; // Identity of worker
           // 目标worker地址
          ZFrame address; // Address frame to route to
           // 包含的service名称，如果存在
          Service service;


           public Worker(String identity, ZFrame address) {
               this. address = address;
               this. identity = identity;
          }
     }


     private ZContext ctx;
     private ZMQ.Socket socket;
     private Map<String, Service> services;
     private Map<String, Worker> workers;
     private Deque<Worker> waiting;


     public static void main(String[] args) {
          Broker broker = new Broker();
          broker.bind( BROKER_FRONT_END);
          broker.mediate();
     }


     public Broker() {
           this. services = new HashMap<String, Service>();
           this. workers = new HashMap<String, Worker>();
           this. waiting = new ArrayDeque<Worker>();
           this. ctx = new ZContext();
           this. socket = ctx.createSocket(ZMQ. ROUTER);
     }


     public void mediate() {
           while (!Thread. currentThread().isInterrupted()) {
              ZMQ.Poller items = new ZMQ.Poller(1);
              items.register( socket, ZMQ.Poller. POLLIN);
              items.poll();
               if (items.pollin(0)) {
                   ZMsg msg = ZMsg. recvMsg(socket);
                    if (msg == null) {
                        System. out.println( "接收到的消息为null。" );
                         break; // Interrupted
                   }
                   System. out.println( "I: received message:\n");
                   msg.dump(System. out);
                    // 根据协议栈规则读取数据，此处需要注意broker接受到的协议栈格式
                   ZFrame sender = msg.pop();
                   ZFrame empty = msg.pop();
                   ZFrame header = msg.pop();
                    if (MDP. C_CLIENT.frameEquals(header)) {
                        processClient(sender, msg);
                   } else if (MDP.W_WORKER.frameEquals(header))
                        processWorker(sender, msg);
                    else {
                        System. out.println( "E: invalid message:\n");
                        msg.dump(System. out);
                        msg.destroy();
                   }
                   sender.destroy();
                   empty.destroy();
                   header.destroy();
              }
          }
          destroy();
     }


     private void destroy() {
          Worker[] deleteList = workers.entrySet().toArray( new Worker[0]);
           for (Worker worker : deleteList) {
              deleteWorker(worker, true);
          }
           ctx.destroy();
     }


     /**
      * 处理客户端请求的，用于分发给指定的worker.
      */
     private void processClient(ZFrame sender, ZMsg msg) {
           if (msg.size() < 2) {
              System. out.println( "消息栈不完整，不能发送" );
               return;
          }
          ZFrame serviceFrame = msg.pop();
          msg.wrap(sender);
          dispatch(requireService(serviceFrame), msg);
          serviceFrame.destroy();
     }


     private void processWorker(ZFrame sender, ZMsg msg) {
           if (msg.size() < 1) {
              System. out.println( "回复给客户端的消息不完整，不能发送。" );
          }
          ZFrame command = msg.pop();
           boolean workerReady = workers.containsKey(sender.strhex());
          Worker worker = requireWorker(sender);
           if (MDP. W_READY.frameEquals(command)) {
               if (workerReady) {
                   System. out.println( "删除worker：" + sender.strhex());
                   deleteWorker(worker, true);
              } else {
                   ZFrame serviceFrame = msg.pop();
                   worker. service = requireService(serviceFrame);
                   workerWaiting(worker);
                   serviceFrame.destroy();
              }
          } else if (MDP. W_REPLY.frameEquals(command)) {
               if (workerReady) {
                   System. out.println( "开始给客户端相应" );
                   ZFrame client = msg.unwrap();
                   msg.addFirst(worker. service. name);
                   msg.addFirst(MDP. C_CLIENT.newFrame());
                   msg.wrap(client);
                   msg.send( socket);
                   workerWaiting(worker);
              } else {
                   deleteWorker(worker, true);
              }
          } else {
              System. out.print( "不合法的消息结构" );
              msg.dump(System. out);
          }
          msg.destroy();
     }


     private void deleteWorker(Worker worker, boolean disconnect) {
          System. out.println( "删除worker");
           if (disconnect) {
              sendToWorker(worker, MDP. W_DISCONNECT, null, null);
          }
           if (worker. service != null)
              worker. service. waiting.remove(worker);
           workers.remove(worker);
          worker. address.destroy();
     }


     private Worker requireWorker(ZFrame address) {
           assert (address != null);
          String identity = address.strhex();
          Worker worker = workers.get(identity);
           if (worker == null) {
              worker = new Worker(identity, address.duplicate());
               workers.put(identity, worker);
              System. out.println( "注册了新的worker：" + identity);
          }
           return worker;
     }


     private Service requireService(ZFrame serviceFrame) {
           assert (serviceFrame != null);
          String name = serviceFrame.toString();
          Service service = services.get(name);
           if (service == null) {
              service = new Service(name);
               services.put(name, service);
          }
           return service;
     }


     private void bind(String endpoint) {
           socket.bind(endpoint);
          System. out.println( "Broker版定在端口： " + endpoint);
     }


     public synchronized void workerWaiting(Worker worker) {
           waiting.addLast(worker);
          worker. service. waiting.addLast(worker);
          dispatch(worker. service, null);
     }


     private void dispatch(Service service, ZMsg msg) {
           assert (service != null);
           if (msg != null) {
              service. requests.offerLast(msg);
          }
           while (!service. waiting.isEmpty() &amp;&amp; !service.requests.isEmpty()) {
              msg = service. requests.pop();
              Worker worker = service. waiting.pop();
               waiting.remove(worker);
              sendToWorker(worker, MDP. W_REQUEST, null, msg);
              msg.destroy();
          }
     }


     public void sendToWorker(Worker worker, MDP command, String option,
              ZMsg msgp) {
          ZMsg msg = msgp == null ? new ZMsg() : msgp.duplicate();
           if (option != null)
              msg.addFirst( new ZFrame(option));
          msg.addFirst(command.newFrame());
          msg.addFirst(MDP. W_WORKER.newFrame());
          msg.wrap(worker. address.duplicate());
          System. out.println( "给worker发送命令： [" + command + "]。");
          msg.dump(System. out);
          msg.send( socket);
     }
}
```

<div>
	ClientAPI:</div>

```java
package com.coderli.zeromq.majordomoprotocol;


import org.zeromq.ZContext;
import org.zeromq.ZFrame;
import org.zeromq.ZMQ;
import org.zeromq.ZMsg;


/**
 * ZeroMQ Majordomo Protocol协议验证<br>
 * 用于实现多client、多worker实现双向指定目标数据收发 <br>
 * 此为Client端依赖的API。
 *
 */
public class ClientAPI {


     private String broker;
     private ZContext ctx;
     private ZMQ.Socket client;
     private long timeout = 2500;
     private int retries = 3;


     public long getTimeout() {
           return timeout;
     }


     public void setTimeout( long timeout) {
           this. timeout = timeout;
     }


     public int getRetries() {
           return retries;
     }


     public void setRetries( int retries) {
           this. retries = retries;
     }


     public ClientAPI(String broker) {
           this. broker = broker;
           ctx = new ZContext();
          reconnectToBroker();
     }


     void reconnectToBroker() {
           if ( client != null) {
               ctx.destroySocket( client);
          }
           client = ctx.createSocket(ZMQ. REQ);
           client.connect( broker);
          System. out.println( "连接到Broker：" + broker );
     }


     /**
      * 给broker发送消息
      *
      * @param service
      * @param request
      * @return
      */
     public ZMsg send(String service, ZMsg request) {


          request.push( new ZFrame(service));
          request.push(MDP. C_CLIENT.newFrame());
          System. out.println( "发送消息给worker：" + service);
          request.dump(System. out);
          ZMsg reply = null;


           int retriesLeft = retries;
           while (retriesLeft > 0 &amp;&amp; !Thread.currentThread().isInterrupted()) {
              request.duplicate().send( client);
              ZMQ.Poller items = new ZMQ.Poller(1);
              items.register( client, ZMQ.Poller. POLLIN);
               if (items.poll( timeout) == -1)
                    break; // 超时退出
               if (items.pollin(0)) {
                   ZMsg msg = ZMsg. recvMsg(client);
                   System. out.println( "接收到消息。" );
                   msg.dump(System. out);
                   ZFrame header = msg.pop();
                   header.destroy();
                   ZFrame replyService = msg.pop();
                   replyService.destroy();
                   reply = msg;
                    break;
              } else {
                   items.unregister( client);
                    if (--retriesLeft == 0) {
                        System. out.println( "超过重试次数，错误。退出。" );
                         break;
                   }
                   System. out.println( "没有收到回应，重试。" );
                   reconnectToBroker();
              }
          }
          request.destroy();
           return reply;
     }


     public void destroy() {
           ctx.destroy();
     }
}
```

<div>
	ClientOne:</div>

```java
package com.coderli.zeromq.majordomoprotocol;


import org.zeromq.ZMsg;


import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Majordomo Protocol协议验证<br>
 * 用于实现多client、多worker实现双向指定目标数据收发 <br>
 * 此为Client端一号，定向发给1、2号worker
 *
 */
public class ClientOne extends JZMQBase {


     public static void main(String[] args) throws InterruptedException {
          ClientAPI clientSession = new ClientAPI(BROKER_FRONT_END);


           int count;
           for (count = 0; count < 1; count++) {
              ZMsg request = new ZMsg();
              ZMsg reply = null;
               long start = System. nanoTime();
              request.addString(String. valueOf(start));
               if (count % 2 == 1) {
                   reply = clientSession.send( "one", request);
              } else {
                   reply = clientSession.send( "two", request);
              }
               if (reply != null)
                   reply.destroy();
               else
                    break; // Interrupt or failure
              Thread. sleep(1000000L);
          }


          System. out.printf( "%d requests/replies processed\n", count);
          clientSession.destroy();
     }
}
```

<div>
	&nbsp;</div>
<div>
	WorkerAPI:</div>

```java
package com.coderli.zeromq.majordomoprotocol;


import org.zeromq.ZContext;
import org.zeromq.ZFrame;
import org.zeromq.ZMQ;
import org.zeromq.ZMsg;


/**
 * ZeroMQ验证 workerAPI封装
 *
 * @author lihzh
 * @date 2014年1月15日 下午2:23:14
 */
public class WorkerAPI {


     private String broker;
     private ZContext ctx;
     private String service;
     private ZMQ.Socket worker;


     private long timeout = 2500;


     private ZFrame replyTo;


     public WorkerAPI(String broker, String service) {
           assert (broker != null);
           assert (service != null);
           this. broker = broker;
           this. service = service;
           ctx = new ZContext();
          reconnectToBroker();
     }


     /**
      * 给Broker发送消息
      *
      * @param command
      * @param option
      * @param msg
      */
     void sendToBroker(MDP command, String option, ZMsg msg) {
          msg = msg != null ? msg.duplicate() : new ZMsg();


           if (option != null)
              msg.addFirst( new ZFrame(option));
          msg.addFirst(command.newFrame());
          msg.addFirst(MDP. W_WORKER.newFrame());
          msg.addFirst( new ZFrame( new byte[0]));
          msg.send( worker);
     }


     void reconnectToBroker() {
           if ( worker != null) {
               ctx.destroySocket( worker);
          }
           worker = ctx.createSocket(ZMQ. DEALER);
           worker.connect( broker);
          sendToBroker(MDP. W_READY, service, null);
     }


     /**
      * 接收数据
      *
      * @param reply
      * @return
      * @author lihzh
      * @date 2014年1月15日 下午2:24:23
      */
     public ZMsg receive(ZMsg reply) {
           if (reply != null) {
              reply.wrap( replyTo);
              sendToBroker(MDP. W_REPLY, null, reply);
              reply.destroy();
          }
           while (!Thread. currentThread().isInterrupted()) {
              ZMQ.Poller items = new ZMQ.Poller(1);
              items.register( worker, ZMQ.Poller. POLLIN);
               if (items.poll( timeout) == -1)
                    break; // Interrupted
               if (items.pollin(0)) {
                   ZMsg msg = ZMsg. recvMsg(worker);
                    if (msg == null)
                         break; // Interrupted
                   System. out.print( "接收到数据：" );
                    long time = System. nanoTime();
                    long endTime = Long
                             . valueOf(new String(msg.getLast().getData()));
                   System. out.println( "消耗时间：" + (time - endTime));
                   msg.dump(System. out);
                   ZFrame empty = msg.pop();
                   empty.destroy();
                   ZFrame header = msg.pop();
                   header.destroy();
                   ZFrame command = msg.pop();
                    if (MDP.W_REQUEST.frameEquals(command)) {
                         replyTo = msg.unwrap();
                        command.destroy();
                         return msg;
                   } else {
                        System. out.println( "不合法的消息结构。" );
                        msg.dump(System. out);
                   }
                   command.destroy();
                   msg.destroy();
              }


          }
           return null;
     }


     public void destroy() {
           ctx.destroy();
     }
}
```

<div>
	&nbsp;</div>
<div>
	WorkerOne:</div>

```java
package com.coderli.zeromq.majordomoprotocol;


import org.zeromq.ZMsg;


import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Majordomo Protocol协议验证<br>
 * 用于实现多client、多worker实现双向指定目标数据收发 <br>
 * 此为Worker端，定向回复给调用的client
 *
 */
public class WorkerOne extends JZMQBase {


     /**
      * @param args
      */
     public static void main(String[] args) {
          WorkerAPI workerSession = new WorkerAPI(BROKER_FRONT_END, "one" );


          ZMsg reply = null;
           while (!Thread. currentThread().isInterrupted()) {
              ZMsg request = workerSession.receive(reply);
               if (request == null)
                    break;
              reply = request;
          }
          workerSession.destroy();
     }
}
```

<div>
	&nbsp;</div>
<div>
	WorkerTwo：</div>

```java
package com.coderli.zeromq.majordomoprotocol;


import org.zeromq.ZMsg;


import com.coderli.zeromq.JZMQBase;


/**
 * ZeroMQ Majordomo Protocol协议验证<br>
 * 用于实现多client、多worker实现双向指定目标数据收发 <br>
 * 此为Worker端，定向回复给调用的client
 *
 */
public class WorkerTwo extends JZMQBase {


     /**
      * @param args
      */
     public static void main(String[] args) {
          WorkerAPI workerSession = new WorkerAPI(BROKER_FRONT_END, "two" );


          ZMsg reply = null;
           while (!Thread. currentThread().isInterrupted()) {
              ZMsg request = workerSession.receive(reply);
               if (request == null)
                    break;
              reply = request;
          }
          workerSession.destroy();
     }
}
```

<div>
	&nbsp;</div>
<div>
	MDP常量类：</div>

```java
package com.coderli.zeromq.majordomoprotocol;


import java.util.Arrays;


import org.zeromq.ZFrame;


/**
 * ZeroMQ Majordomo Protocol协议验证<br>
 * 用于实现多client、多worker实现双向指定目标数据收发 <br>
 * 此为常量类
 *
 */
public enum MDP {


     C_CLIENT("MDPC01"), W_WORKER("MDPW01"),


     W_READY(1), W_REQUEST(2), W_REPLY(3), W_HEARTBEAT(4), W_DISCONNECT (5);


     private final byte[] data;


     MDP(String value) {
           this. data = value.getBytes();
     }


     MDP(int value) { // watch for ints>255, will be truncated
           byte b = ( byte) (value &amp; 0xFF);
           this. data = new byte[] { b };
     }


     public ZFrame newFrame() {
           return new ZFrame( data);
     }


     public boolean frameEquals(ZFrame frame) {
           return Arrays. equals(data, frame.getData());
     }
}
```

<div>
	&nbsp;</div>
<div>
	附，基类代码</div>

```java
/**
 * @author lihzh
 * @date 2014年1月14日 上午9:32:01
 */
public abstract class JZMQBase {


     protected static String LOCAL_ADDRESS = "tcp://127.0.0.1:1234";
     protected static String LOCAL_ADDRESS_PUSHER = "tcp://127.0.0.1:2345";
     protected static String LOCAL_ADDRESS_ROUTER = "tcp://127.0.0.1:3456";
     protected static String LOCAL_ADDRESS_DECLARER = "tcp://127.0.0.1:4567";


     protected static String BROKER_FRONT_END = "tcp://127.0.0.1:4000";
     protected static String BROKER_BACK_END = "tcp://127.0.0.1:4001";
}
```

代码介绍：

其实原理很简单，主要利用ZeroMQ底层封装好的发送接受协议，来事先给指定的客户端发送消息。由于zeromq是基于socket的，所以本质上只能点对点通信。所以要事先多对多中心，就需要中间的一个转发器。即Broker。在Broker中记录了目标地址，这个地址ZeroMQ底层提供的，必须使用保存起来，用于下次发送时使用。


