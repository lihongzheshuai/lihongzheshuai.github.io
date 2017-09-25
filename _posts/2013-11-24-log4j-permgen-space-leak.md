---
layout: post
title: log4j 和 java.lang.OutOfMemoryError PermGen space
date: 2013-11-24 23:09 +0800
author: onecoder
comments: true
tags: [Log4j]
thread_key: 1554
---
<p>
	还是<a href="http://www.coderli.com">OneCoder</a>在项目中沙箱的问题，用classloader隔离做的沙箱，反复运行用户的任务，出现永生区内存溢出：<br />
	java.lang.OutOfMemoryError: PermGen space</p>
<p>
	这个问题在tomcat重复热部署的时候其实比较常见。其道理也和我们沙箱的道理基本一致，就是每次任务运行的类没有卸载掉。而永生区正式存储加载入classloader中的类，反射的方法等的地方。如此只增不减，自然会产生溢出。</p>
<p>
	那么，什么情况下会产生沙箱中loader进来的类不会被回收的情况呢？简单说，就是当外部loader里加载的类，持有了沙箱loader中的加载的类的实例时。道理简单，但是实际项目中，寻找这种可能情况就复杂的多了。为了说明这个道理，我们做个简单的试验。</p>
<p>
	ClassLoader加载试验</p>
<p>
	试验思想，基本思想就是循环创建Classloader手动加载包，并通过反射调用包中的代码，考察在外部loader有无引用的情况下，PermGen区的变化情况。监控工具，即为JDK自带的Java VisualVM。</p>
<p>
	场景一、无引用</p>

```java
package com.coderli.permgen.leak;

import java.io.File;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * Classloader导致Permleak测试类
 * 
 * @author <a href="http://www.coderli.com">OneCoder</a>
 * @date 2013年11月21日 上午10:07:02
 * @website http://www.coderli.com
 */
public class ClassloaderPermGenLeakTest {

public static void main(String[] args) throws InterruptedException,
MalformedURLException, ClassNotFoundException {

     ExecutorService es = new ThreadPoolExecutor(1, 10, 5L,
     TimeUnit.SECONDS, new SynchronousQueue<Runnable>());
     ClassloaderPermGenLeakTest clpg = new ClassloaderPermGenLeakTest();

     for (int i = 0; i < 1; i++) {
          es.execute(clpg.new ExecutroRun());
     }
     Thread.sleep(2000000);
}

private class ExecutroRun implements Runnable {

@Override
public void run() {
     try {
          permLeak();
     } catch (Exception e) {
          e.printStackTrace();
     }
}

private void permLeak() throws Exception {
     Thread.sleep(5000);
     List<Object> insList = new ArrayList<Object>();
     ClassLoader _temp = Thread.currentThread().getContextClassLoader();
     for (int i = 0; i < 100; i++) {
          URL[] urls = getURLS();
          URLClassLoader urlClassloader = new URLClassLoader(urls, null);
          Class<?> logfClass = Class.forName("org.apache.commons.logging.LogFactory", true,
                urlClassloader);
          Method getLog = logfClass.getMethod("getLog", String.class);
          getLog.invoke(logfClass, "logName&rdquo;);        (100);
          System.out.println("print: " + i);
     }
}

private URL[] getURLS() throws MalformedURLException {
     File libDir = new File("src/main/java/com/coderli/permgen/leak/lib");
     File[] subFiles = libDir.listFiles();
     int count = subFiles.length;
     URL[] urls = new URL[count];
     for (int i = 0; i < count; i++) {
          urls[i] = subFiles[i].toURI().toURL();
     }
     return urls;
     }
}
```

<p>
	从代码可见，在自定义的100个Classloader里，我们只是通过反射调用了LogFactory里的getLog方法，对于该方法返回的实例，并没有保存。所以没有引用，可正常回收。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DkUewQvK/cmW9X.jpg" style="width: 640px; height: 444px;" /></p>
<p>
	通过内存dump查看，可以发现，内存中没有commmon logging相关的类，说明PermGen区正常回收了。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DkUevtC2/qnzyM.jpg" style="width: 640px; height: 444px;" /></p>
<p>
	场景二、持有引用</p>
<p>
	修改代码如下：</p>

```java
package com.coderli.permgen.leak;

import java.io.File;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * Classloader导致Permleak测试类
 * 
 * @author lihzh
 * @date 2013年11月21日 上午10:07:02
 */
public class ClassloaderPermGenLeakTest {


private List<Object> insList = new ArrayList<Object>();

public static void main(String[] args) throws InterruptedException,
MalformedURLException, ClassNotFoundException {

     ExecutorService es = new ThreadPoolExecutor(1, 10, 5L,
     TimeUnit.SECONDS, new SynchronousQueue<Runnable>());
     ClassloaderPermGenLeakTest clpg = new ClassloaderPermGenLeakTest();

     for (int i = 0; i < 1; i++) {
          es.execute(clpg.new ExecutroRun());
     }
     Thread.sleep(2000000);
     System.out.println(clpg.insList.size());
}

private class ExecutroRun implements Runnable {

     @Override
     public void run() {
          try {
               permLeak();
          } catch (Exception e) {
               e.printStackTrace();
          }
     }

private void permLeak() throws Exception {
     Thread.sleep(5000);
     for (int i = 0; i < 100; i++) {
          URL[] urls = getURLS();
          URLClassLoader urlClassloader = new URLClassLoader(urls, null);
          Class<?> logfClass = Class.forName(
               "org.apache.commons.logging.LogFactory", true,
               urlClassloader);
          Method getLog = logfClass.getMethod("getLog", String.class);
          Object result = getLog.invoke(logfClass, "logName");
          insList.add(result);
          System.out.println("print: " + i);
     }
}

private URL[] getURLS() throws MalformedURLException {
     File libDir = new File("src/main/java/com/coderli/permgen/leak/lib");
     File[] subFiles = libDir.listFiles();
     int count = subFiles.length;
     URL[] urls = new URL[count];
     for (int i = 0; i < count; i++) {
          urls[i] = subFiles[i].toURI().toURL();
     }
     return urls;
     }
}
```

<p>
	在外部增加一个list存放内部反射出来的对象，并保证list对象被引用。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DkUevfFG/efY2T.jpg" style="width: 640px; height: 444px;" /></p>
<p>
	这次可看到PermGen不会被释放，观察dump内存</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DkUewutG/X95mE.jpg" style="width: 640px; height: 444px;" /></p>
<p>
	<br />
	有大量的commons logging类没有释放。即出现内存泄漏。</p>
<p>
	这是最简单，最直观的PermGen Leak的场景。更多的时候，这种内存泄漏并不是那么的好察觉。 比如，我们经历的沙盒中的问题就是一个比较典型的问题，沙盒中使用log4j。</p>
<p>
	log4j导致永生区溢出的问题其实并不罕见，网上也有不少人讨论过这个问题。下面摘录的一段博文内容，给了我启示。</p>
<blockquote>
	<p>
		More sneaky problems</p>
	<p>
		I don't blame you if you didn't see the problem with the Level class: it's sneaky. Last year we had some undeployment problems in our application server. My team, in particular Edward Chou, spent some time to track them all down. Next to the problem withLevel, here are some other problems Edward and I encountered. For instance, if you happen to use some of the Apache Commons BeanHelper's code: there's a static cache in that code that refers to Method objects. The Method object holds a reference to the class the Method points to. Not a problem if the Apache Commons code is loaded in your application's classloader. However, you do have a problem if this code is also present in the classpath of the application server because those classes take precedence. As a result now you have references to classes in your application from the application server's classloader... a classloader leak!</p>
	<p>
		I did not mentiond yet the simplest recipe for disaster: a thread started by the application while the thread does not exit after the application is underplayed.</p>
</blockquote>
<p>
	在使用log4j的时候，不论你是直接使用log4j还是通过slf4j和commons-longging间接使用，当你通过LoggerFactory(LogFactory)获取一个实例的时候，log4j都会将该实例缓存起来。这就会导致你外部持有了一个沙箱内部的log对象，内部又持有了一个外部的对象，最终导致所有加载的log4j的相关类都无法释放。产生溢出。</p>
<p>
	而在我们的项目还不仅如此，我们还是使用了log4j的MDC类，log4j提供了线程相关的MDC类用于保存当前线程的日志上线文信息。如果内外loader的类公用一个线程，那么在线程没有终止的情况下，MDC信息会绑定在当前线程的ThreadLocal上，这也会造成类无法释放，最终产生溢出。</p>
<p>
	那么解决上述问题的比较常见的办法就是全局使用一份log4j，即将log4j置于更高层次的loader中进行加载，避免每个loader重复加载。而在我们的项目中，也采用了类似的做法，即在沙箱的一个公用的父类loader中加载了log4j类。从而避免溢出。</p>
<p>
	最后，推荐两篇相关博文，里面有关于永生区(PermGen)较为细致的分析和讲解</p>
<p>
	<a href="http://frankkieviet.blogspot.com/2006/10/classloader-leaks-dreaded-permgen-space.html">http://frankkieviet.blogspot.com/2006/10/classloader-leaks-dreaded-permgen-space.html</a></p>
<p>
	<a href="https://blogs.oracle.com/jonthecollector/entry/presenting_the_permanent_generation">https://blogs.oracle.com/jonthecollector/entry/presenting_the_permanent_generation</a></p>

