---
layout: post
title: log4j 同一线程隔离classloader下MDC信息不同问题解决 ThreadLocal问题分析
date: 2014-05-06 22:25 +0800
author: onecoder
comments: true
tags: [Log4j]
categories: [Java技术研究]
thread_key: 1641
---
<p>
	最近遇到日志文件记录错误的问题。一个任务的日志信息会被莫名的拆分到两个不同目录中。且有一个目录还是曾经执行过的任务的目录。经过分析，首先怀疑的是MDC没有清理的问题，这也是最直观的问题。因为任务是在线程池(fixedThreadPool)中运行的。由于线程会被重用，而MDC是绑定在Threadlocal上的，所以如果没有清理，是会造成上述问题。但是在代码检查中发现在线程的开始，是重新设置过MDC信息的。所以，怀疑的对象转移到了多classloader上。由于不能肯定，所以进行测试如下：</p>


```java
package com.coderli.log4j.mdc;


import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;


import org.apache.log4j.MDC;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
* 单线程多 classloader模式下，log4jMDC信息传递测试。
*
* @author OneCoder
* @blog http://www.coderli.com
* @date 2014年5月6日 上午10:55:34
*/
public class SingleThreadMultiLoader {


     private static final Logger logger = LoggerFactory
              . getLogger(SingleThreadMultiLoader.class);
     private static String key = "loaderName";
     static ThreadLocal<String> tl = new ThreadLocal<String>();


     public static void main(String[] args) throws MalformedURLException,
              ClassNotFoundException, InstantiationException,
              IllegalAccessException, NoSuchMethodException, SecurityException,
              IllegalArgumentException, InvocationTargetException {
          MDC. put(key, "in main loader" );
           logger.info( "线程名: {}; 日志MDC信息：{}。" , Thread.currentThread().getName(),
                   MDC. get(key));
           tl.set( "huanyige");
          ClassLoader cLoader = Thread.currentThread().getContextClassLoader();
          URL[] urls = new URL[] {
                    new URL("file:\\D:\\acap\\workspace\\shurnim-lab\\lib\\mdc.jar" ),
                    new URL(
                              "file:\\D:\\acap\\workspace\\shurnim-lab\\lib\\log4j-1.2.17.jar" ),
                    new URL(
                              "file:\\D:\\acap\\workspace\\shurnim-lab\\lib\\slf4j-api-1.7.5.jar" ),
                    new URL(
                              "file:\\D:\\acap\\workspace\\shurnim-lab\\lib\\slf4j-log4j12-1.7.5.jar" ) };
          ClassLoader loader = new URLClassLoader(urls, null);
          Thread. currentThread().setContextClassLoader(loader);
          String className = SingleThreadMultiLoader.class.getName();
           Class clz = loader.loadClass(className);
          Method main = clz.getMethod("logMethod");
          main.invoke( null);
           logger.info( "线程名: {}; 日志MDC信息：{}。" , Thread.currentThread().getName(),
                   MDC. get(key));
     }


     public static void logMethod() {
           logger.info( "线程名: {}; 日志MDC信息：{}。" , Thread.currentThread().getName(),
                   MDC. get(key));
          MDC. put(key, "hahahahhaha" );
          System. out.println( tl.get());
     }
}
```

<p>
	执行结果如下：</p>
<blockquote>
	<p>
		2014-05-06 16:02:53,802 >> INFO&nbsp; >> main >> com.coderli.log4j.mdc.SingleThreadMultiLoader.main(SingleThreadMultiLoader.java:32) >> 线程名: main; 日志MDC信息：in main loader。<br />
		2014-05-06 16:02:53,869 >> INFO&nbsp; >> main >> com.coderli.log4j.mdc.SingleThreadMultiLoader.logMethod(SingleThreadMultiLoader.java:62) >> 线程名: main; 日志MDC信息：null。<br />
		null<br />
		2014-05-06 16:02:53,870 >> INFO&nbsp; >> main >> com.coderli.log4j.mdc.SingleThreadMultiLoader.main(SingleThreadMultiLoader.java:50) >> 线程名: main; 日志MDC信息：in main loader。</p>
</blockquote>
<p>
	<br />
	可以看到，在全隔离的两个Classloader下，MDC信息也是隔离的，不互通的。OneCoder遇到的bug也由此而来，在沙箱内部，虽然是同一个线程，但是MDC内的信息是上一个任务的，自然会出错了。</p>
<p>
	为了更直观的说明问题，OneCoder还验证了ThreadLocal的情况，结果一样也是隔离的。这就跟ThreadLocal的实现机制有关了。</p>

```java
public T get() {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            ThreadLocalMap.Entry e = map.getEntry(this);
            if (e != null)
                return (T)e.value;
        }
        return setInitialValue();
    }
```

<p>
	从ThreadLocal的get()方法便可理解。在取值的时候，首先通过当前线程对象作为key。获取到当前线程的ThreadLocalMap，再用ThreadLocal对象作为key从Map中获取值。而在隔离的Classloader中，这个ThreadLocal对象是不同的。自然取到的值也就不同了。</p>
<p>
	<br />
	当然，如果你的Classloader不是完全隔离的。在ThreadLocal层是有共同的父loader话，ThreadLocal中的值还是可以互通的。</p>

