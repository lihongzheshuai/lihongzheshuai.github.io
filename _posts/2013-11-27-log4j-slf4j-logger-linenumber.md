---
layout: post
title: log4j日志封装说明—slf4j对于log4j的日志封装-正确获取调用堆栈
date: 2013-11-27 12:54 +0800
author: onecoder
comments: true
tags: [Log4j,SLF4J]
categories: [Java技术研究]
thread_key: 1558
---
<p>
	日志是项目中必用的东西，日志产品里最普及应该就是log4j了。(logback这里暂不讨论。) 先看一下常用的log4j的用法，一般来说log4j都会配合slf4j或者common-logging使用，这里已slf4j为例。添加gradle依赖：</p>

```groovy
dependencies {
compile('log4j:log4j:1.2.17',
'org.slf4j:slf4j-api:1.7.5',
'org.slf4j:slf4j-log4j12:1.7.5')
}
```

<p>
	最直接的用法就是在每个需要记录日志的类里，构造一个属于自己类的log实例，实际上很多著名的开源项目也是这么做的。如spring。</p>

```java
private static final Log logger = LogFactory.getLog(BeanUtils.class);
```

<p>
	那么我们也先从这种用法开始，先配置好最基本的log4j.xml配置文件。</p>

```xml
<?xml version= "1.0" encoding ="UTF-8"?>
<!DOCTYPE log4j:configuration SYSTEM "http://log4j.dtd">
<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/" >

     <appender name="Console" class="org.apache.log4j.ConsoleAppender" >
           <layout class= "org.apache.log4j.PatternLayout" >
               <param name= "ConversionPattern" value ="%d >> %-5p >> %t >> %l >> %m%n" />
           </layout>
     </appender >
     <root >
           <level value= "info" />
           <appender-ref ref= "Console" />
     </root >

</log4j:configuration>
```

<p>
	参数说明：</p>
<blockquote>
	<p>
		%p 输出优先级，即DEBUG，INFO，WARN，ERROR，FATAL<br />
		%r 输出自应用启动到输出该log信息耗费的毫秒数<br />
		%c 输出所属的类目，通常就是所在类的全名<br />
		%t 输出产生该日志事件的线程名<br />
		%n 输出一个回车换行符，Windows平台为&ldquo;\r\n&rdquo;，Unix平台为&ldquo;\n&rdquo;<br />
		%d 输出日志时间点的日期或时间，默认格式为ISO8601，也可以在其后指定格式，比如：%d{yyy MMM dd HH:mm:ss,SSS}，输出类似：2002年10月18日 22：10：28，921<br />
		%l 输出日志事件的发生位置，包括类目名、发生的线程，以及在代码中的行数。</p>
</blockquote>
<p>
	日志测试类：</p>

```java
package com.coderli.log4jpackage;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
/**
* log4j封装实验室中的用户模拟类
*
* @author OneCoder
* @date 2013年11月25日 下午4:39:19
*/
public class UserClass {

     private static final Logger logger = LoggerFactory
              . getLogger(UserClass.class);
     public static void main(String[] args) {
           logger.info("这是一个Info级别的log4j日志。" );
     }
}
```

<p>
	输出日志：</p>
<blockquote>
	<p>
		2013-11-26 11:09:21,305 >> INFO&nbsp; >> main >> com.coderli.log4jpackage.UserClass.main(UserClass.java:18) >> 这是一个Info级别的log4j日志。</p>
</blockquote>
<p>
	这里包含的日志发生时的类、线程、行号等信息。很完整。本身这么做没什么问题，只是可能有的项目考虑如果每个类里都写这样一个开头，有点麻烦，同时，如果每个类一个独立的声明，log4j内存会缓存很多的实例，占用内存，可能有时候也不便于统一配置管理。所以，有些项目里考虑了对log进行封装，提供统一的一个静态方法调用：</p>

```java
package com.coderli.log4jpackage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
* @author lihzh(OneCoder)
* @date 2013年11月25日 下午4:39:54
* @blog http://www.coderli.com
*/
public class MyLog4j {
     private static final Logger logger = LoggerFactory.getLogger("MyLog4j");

     public static void info(String msg) {
           logger.info(msg);
     }
}
```

<p>
	记录日志代码变为：</p>

```java
/**
 * log4j封装实验室中的用户模拟类
 *
 * @author OneCoder
 * @date 2013年11月25日 下午4:39:19
 */
public class UserClass {

     public static void main(String[] args) {
          MyLog4j. info("这是一个Info级别的log4j日志。" );
     }
}
```

<p>
	日志输出：</p>
<blockquote>
	<p>
		2013-11-26 11:23:29,936 >> INFO&nbsp; >> main >> com.coderli.log4jpackage.MyLog4j.info(MyLog4j.java:16 ) >> 这是一个Info级别的log4j日志。</p>
</blockquote>
<p>
	咋一看没什么问题，仔细分析就发现，对我们调试很有帮助的日志发生时的类名、行号都编程了封装类里面的类和行，这对于依靠日志进行错误调试来说是悲剧的。这种封装虽然解决了实例过多的问题，但是也是失败的，甚至是灾难性的。</p>
<p>
	也有人把发生日志的Class信息也传递进来一起打印。如：</p>

```java
public static void info(String className, String msg) {
           logger.info(className + ">> " + msg);
     }
```

<p>
	这种方式显然是治标不治本的。于是很多人想到了另外的封装方式，即提供一个统一获取logger实例的位置，然后在自己的类里进行嗲用：</p>

```java
public static Logger getLogger() {
           return logger;
     }
```

<p>
	调用代码：</p>

```java
public static void main(String[] args) {
          MyLog4j. getLogger().info("这是一个Info级别的log4j日志。" );
     }
```

<p>
	这种方法，日志虽然恢复了正常，但是对于开发者实际又增加了麻烦，打印一个日志需要两部操作了。当然你可以使用import static。或者每个类里还是全局声明一个logger实例。</p>
<p>
	那么有没有想过，slf4j内部是怎么对log4j封装的呢？我们通过slf4j调用为什么就可以之间获得你实际打印日志的行号，同时又不会把自己类给暴露出来呢？你可能还没明白我在说什么，细说一下，如果我们直接使用log4j的logger，打印出来的是我们调用类的行号这没什么问题，但是这里我们获得的是slf4j的logger实例，它底层调用的是log4j的logger实例，那么为什么不会打印出slf4j内部调用类的行号呢？这就是我关心的问题。知道了这个，也许我们就可以封装出更好用的全局log组件了。</p>
<p>
	其实，这个问题的关键就集中在log4j是如何获取你调用日志的代码的类和行号的，在Java中可以通过Throwable来获取调用堆栈, 例如我们将如下代码，放在MyLog4j类的info方法中：</p>

```java
   public static void info(String msg) {
      Throwable throwable = new Throwable();
      StackTraceElement[] ste = throwable.getStackTrace();
      for (StackTraceElement stackTraceElement : ste) {
         System.out
               .println("ClassName: " + stackTraceElement.getClassName());
         System.out.println("Method Name: "
               + stackTraceElement.getMethodName());
         System.out.println("Line number: "
               + stackTraceElement.getLineNumber());
      }
      logger.info(msg);
   }
```

<p>
	再次通过UserClass调用，就可获得如下输出：</p>
<blockquote>
	<p>
		ClassName: com.coderli.log4jpackage.MyLog4j<br />
		Method Name: info<br />
		Line number: 28<br />
		ClassName: com.coderli.log4jpackage.UserClass<br />
		Method Name: main<br />
		Line number: 12</p>
</blockquote>
<p>
	由此可见只要在调用堆栈里找到用户的类，就可以获得所有我们需要的信息。有了这个基础，我们再来看看slf4j和log4j是怎么做的。</p>
<p>
	在log4j的Logger中，实际对外提供了用于封装的统一的log方法。</p>

```java
 /**

     This is the most generic printing method. It is intended to be
     invoked by <b>wrapper</b> classes.

     @param callerFQCN The wrapper class' fully qualified class name.
     @param level The level of the logging request.
     @param message The message of the logging request.
     @param t The throwable of the logging request, may be null.  */
  public
  void log(String callerFQCN, Priority level, Object message, Throwable t）
```

<p>
	而第一个参数callerFQCN，就是关键的决定调用者位置的参数。在LocationInfo中，可看到对该参数的使用方式为：</p>

```java
public LocationInfo(Throwable t, String fqnOfCallingClass) {
      if(t == null || fqnOfCallingClass == null)
return;
      if (getLineNumberMethod != null) {
          try {
              Object[] noArgs = null;
              Object[] elements =  (Object[]) getStackTraceMethod.invoke(t, noArgs);
              String prevClass = NA;
              for(int i = elements.length - 1; i >= 0; i--) {
                  String thisClass = (String) getClassNameMethod.invoke(elements[i], noArgs);
                  if(fqnOfCallingClass.equals(thisClass)) {
                      int caller = i + 1;
                      if (caller < elements.length) {
                          className = prevClass;
                          methodName = (String) getMethodNameMethod.invoke(elements[caller], noArgs);
                          fileName = (String) getFileNameMethod.invoke(elements[caller], noArgs);
                          if (fileName == null) {
                              fileName = NA;
                          }
                          int line = ((Integer) getLineNumberMethod.invoke(elements[caller], noArgs)).intValue();
                          if (line < 0) {
                              lineNumber = NA;
                          } else {
                              lineNumber = String.valueOf(line);
                          }
                          StringBuffer buf = new StringBuffer();
                          buf.append(className);
                          buf.append(".");
                          buf.append(methodName);
                          buf.append("(");
                          buf.append(fileName);
                          buf.append(":");
                          buf.append(lineNumber);
                          buf.append(")");
                          this.fullInfo = buf.toString();
                      }
                      return;
                  }
                  prevClass = thisClass;
              }
              return;
…….//省略若干

```

<p>
	可见，log4j把传递进来的callerFQCN在堆栈中一一比较，相等后，再往上一层即认为是用户的调用类。所以，在slf4j封装的logger中是这样封装的：</p>

```java
final static String FQCN = Log4jLoggerAdapter.class .getName();
public void info(String msg) {
    logger.log(FQCN, Level. INFO, msg, null );
  }
```

<p>
	用户的代码调用的正是调用的这个info，所以就会正常的显示用户代码的行号了。那么对于封装来说，你只需要注意调用log4j的log方法，并传递进去正确的FQCN即可。</p>

```java
final static String FQCN = Log4jLoggerAdapter.class .getName();
public void info(String msg) {
    logger.log(FQCN, Level. INFO, msg, null );
  }
```