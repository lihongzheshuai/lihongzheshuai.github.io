---
layout: post
title: 一起学Java(13)-[日志篇]教你分析SLF4J和Log4j2源码，掌握SLF4J与Log4j2无缝集成原理
date: 2024-09-14 19:00 +0800
author: onecoder
image: /images/post/java-go-13/log4j2-slf4j2-provider-relation.svg
comments: true
tags: [Java, Log, SLF4J, 一起学Java]
categories: [一起学Java系列,（2）引入日志篇]
---
研究完`SLF4J`和`Logback`这种无缝集成的方式([一起学Java(12)-[日志篇]教你分析SLF4J源码，掌握SLF4J如何与Logback无缝集成的原理](https://www.coderli.com/java-go-12-import-log-four-logback/))，继续研究`Log4j2`和`SLF4J`这种需要桥接集成的方式。

<!--more-->

## 一、桥接包如何与SLF4J集成

我们已经知道SLF4J利用`ServiceLoader`机制，去寻找和加载`SLF4JServiceProvider`接口的实现类，而`Log4j2`原生是没有实现这个接口的，因此需要借助桥接机制，将`Log4j2`集成到`SLF4J`中，这个桥接包就是`log4j2-slf4j2-provider`。

![log4j2-slf4j2-provider](/images/post/java-go-13/log4j2-slf4j2-provider.png)

在桥接包中，找到`META-INF/services`目录，可以看到`org.slf4j.spi.SLF4JServiceProvider`文件，内容如下：

```plaintext
org.apache.logging.slf4j.Log4jLoggerFactory
```

这就是`Log4j2`对`SLF4JServiceProvider`接口的实现。

在实现中，返回了`Log4jLoggerFactory`，这个类是`Log4j2`的工厂类，用于创建`Logger`对象。这个工厂类是桥接包中的类。

## 二、桥接包如何与Log4j2集成

SLF4J的的LoggerFactory类中，在bind函数中，当获取到SLF4JServiceProvider后，会调用Provider的**initialize**方法，进行初始化。

```java
    private final static void bind() {
        try {
            List<SLF4JServiceProvider> providersList = findServiceProviders();
            reportMultipleBindingAmbiguity(providersList);
            if (providersList != null && !providersList.isEmpty()) {
                PROVIDER = providersList.get(0);
                // SLF4JServiceProvider.initialize() is intended to be called here and nowhere else.
                PROVIDER.initialize(); // by OneCoder 调用桥接包中Provider的initialize方法初始化
                INITIALIZATION_STATE = SUCCESSFUL_INITIALIZATION;
                reportActualBinding(providersList);
            } else {
                INITIALIZATION_STATE = NOP_FALLBACK_INITIALIZATION;
                Reporter.warn("No SLF4J providers were found.");
                Reporter.warn("Defaulting to no-operation (NOP) logger implementation");
                Reporter.warn("See " + NO_PROVIDERS_URL + " for further details.");

                Set<URL> staticLoggerBinderPathSet = findPossibleStaticLoggerBinderPathSet();
                reportIgnoredStaticLoggerBinders(staticLoggerBinderPathSet);
            }
            postBindCleanUp();
        } catch (Exception e) {
            failedBinding(e);
            throw new IllegalStateException("Unexpected initialization failure", e);
        }
    }
```

Log42j桥接包中，初始化的代码如下：

```java
    public void initialize() {
        markerFactory = new Log4jMarkerFactory();
        loggerFactory = new Log4jLoggerFactory(markerFactory);
        mdcAdapter = new Log4jMDCAdapter();
    }
```

即核心是构造了一个`Log4jLoggerFactory`对象返回给SLF4J，该类集成自`log4j-api`包中的`AbstractLoggerAdapter`抽象类，并实现了`SLF4J`中的`ILoggerFactory`接口，用于真正获取**Logger**实例。这样桥接包已经有呈上启下的关系了。

```java
public class Log4jLoggerFactory extends AbstractLoggerAdapter<Logger> implements ILoggerFactory
```

获取到`ILoggerFactory`实例后，SLF4J会调用`LoggerFactory`的`getLogger`方法，获取到`Logger`实例。

```java
    public Logger getLogger(String name) {
        return loggerFactory.getLogger(name);
    }
```

这时便会进入`AbstractLoggerAdapter`类中的`getLogger`方法:

```java
    public L getLogger(final String name) {
        final LoggerContext context = getContext();
        final ConcurrentMap<String, L> loggers = getLoggersInContext(context);
        final L logger = loggers.get(name);
        if (logger != null) {
            return logger;
        }
        // by OneCoder如果logger不存在，则创建一个新的logger，并将其添加到loggers中
        loggers.putIfAbsent(name, newLogger(name, context));
        return loggers.get(name);
    }
```

这里的LoggerContext是Log4j2中的概念，表示一个Logger的上下文，用于存储Logger的配置信息和获取Logger实例。桥接包中实现了getContext方法，返回Log4j2中(log4j-api包中)的LoggerContext对象。

```java
    protected LoggerContext getContext() {
        final Class<?> anchor = LogManager.getFactory().isClassLoaderDependent()
                ? StackLocatorUtil.getCallerClass(Log4jLoggerFactory.class, CALLER_PREDICATE)
                : null;
        LOGGER.trace("Log4jLoggerFactory.getContext() found anchor {}", anchor);
        return anchor == null ? LogManager.getContext(false) : getContext(anchor);
    }
```

获取到`LoggerContext`后，便可以在LogContext中获取真正的Logger实例，如果是第一次创建logger，从上下文中获取不到logger对象，则会调用`newLogger`方法，创建一个新的logger，并将其添加到loggers中。newLogger方法的实现在桥接包中。

```java
    protected Logger newLogger(final String name, final LoggerContext context) {
        final String key = Logger.ROOT_LOGGER_NAME.equals(name) ? LogManager.ROOT_LOGGER_NAME : name;
        return new Log4jLogger(markerFactory, validateContext(context).getLogger(key), name);
    }
```

LogContext中获取真正logger的代码：

```java
    public Logger getLogger(final String name, final MessageFactory messageFactory) {
        // Note: This is the only method where we add entries to the 'loggerRegistry' ivar.
        Logger logger = loggerRegistry.getLogger(name, messageFactory);
        if (logger != null) {
            AbstractLogger.checkMessageFactory(logger, messageFactory);
            return logger;
        }

        logger = newInstance(this, name, messageFactory);
        loggerRegistry.putIfAbsent(name, messageFactory, logger);
        return loggerRegistry.getLogger(name, messageFactory);
    }
```

这里通过LoggerContext的getLogger方法，获取到Log4j2中(`log4j-core`包中)的Logger对象，然后通过Log4j2中的Logger对象，创建一个`Log4jLogger`对象，该类是在桥接包中定义的类，因为应用需要返回的是SLF4J中的`Logger`接口，Log4j2中没有提供原生实现，因此需要在桥接包中包装一层。

```java
public class Log4jLogger implements LocationAwareLogger, Serializable
```

```java
public interface LocationAwareLogger extends Logger
```

```java
    public Log4jLogger(final Log4jMarkerFactory markerFactory, final ExtendedLogger logger, final String name) {
        this.markerFactory = markerFactory;
        this.logger = logger;
        this.name = name;
    }
```

至此，通过桥接层就实现了向上与SLF4J接口层对接，向下包装了Log4j2的Logger对象，用于真正的Log记录。

在Log4jLogger中，日志记录函数中都是使用真正的Logger实例，来执行日志记录。例如：

```java
    public void info(final String format, final Object... args) {
        logger.logIfEnabled(FQCN, Level.INFO, null, format, args);
    }
```

一张图总结一下桥接包的关系原理：

![log4j2-slf4j2-provider](/images/post/java-go-13/log4j2-slf4j2-provider-relation.svg)

## Log4j2原生API用法

作为扩展和对比，试验一下原生使用Log4j2 API的用法。

```java
package com.coderli.one.log;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * 本类用于研究Log4j2原生日志接口使用方式
 * @author OneCoder
 * @Blog https://www.coderli.com
 * @source https://github.com/lihongzheshuai/java-all-in-one
 */
public class Log4jLogMain {

    public static void main(String[] args) {
        Logger logger = LogManager.getLogger(Log4jLogMain.class);
        logger.info("This is a log from log4j-api.");
    }

}
```

即在通过log4j-api包中的`LogManager`获取到`Logger`实例进行日志记录。

> 原生使用log4j-api的代码也已上传至[github：https://github.com/lihongzheshuai/java-all-in-one](https://github.com/lihongzheshuai/java-all-in-one)，有兴趣的可以参考。考虑到未来可能使用Logback框架，因此这部分代码放在分支feature-log-log4j2中。
{: .prompt-warning }











