---
layout: post
title: Flume(ng) 自定义sink实现和属性注入
date: 2013-10-29 11:14 +0800
author: onecoder
comments: true
tags: [Flume]
thread_key: 1533
---
最近需要利用flume来做收集远端日志，所以学习一些flume最基本的用法。这里仅作记录。

远端日志收集的整体思路是远端自定义实现log4j的appender把消息发送到flume端，flume端自定义实现一个sink来按照我们的规则保存日志。

自定义Sink代码：
	
```java
public class LocalFileLogSink extends AbstractSink implements Configurable {
     private static final Logger logger = LoggerFactory
              . getLogger(LocalFileLogSink .class );
            private static final String PROP_KEY_ROOTPATH = "rootPath";
      private String rootPath;
     @Override
     public void configure(Context context) {
          String rootPath = context.getString(PROP_KEY_ROOTPATH );
          setRootPath(rootPath);
     }
          
          @Override
          public Status process() throws EventDeliveryException {
           logger .debug("Do process" );
       ｝
}
```


实现Configurable接口，即可在初始化时，通过configure方法从context中获取配置的参数的值。这里，我们是想从flume的配置文件中获取rootPath的值，也就是日志保存的根路径。在flume-conf.properties中配置如下：

```
agent.sinks = loggerSink
agent.sinks.loggerSink.rootPath = ./logs
```

loggerSink是自定义sink的名称，我们取值时的key，只需要loggerSink后面的部分即可，即这里的rootPath。

实际业务逻辑的执行，是通过继承复写AbstractSink中的process方法实现。从基类的getChannel方法中获取信道，从中取出Event处理即可。

```java
 Channel ch = getChannel();
            Transaction txn = ch.getTransaction();
          txn.begin();
           try {
               logger .debug("Get event." );
              Event event = ch.take();
              txn.commit();
              status = Status. READY ;
              return status;
                    ｝finally {
              Log. info( "trx close.");
              txn.close();
          }
```