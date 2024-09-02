---
layout: post
title: 一起学Java(12)-[日志篇]教你分析SLF4J源码，掌握SLF4J如何与Logback无缝集成的原理
date: 2024-09-02 08:00 +0800
author: onecoder
image: /images/post/java-go-12/logback-provider.png
comments: true
tags: [Java,Log, SLF4J, Logback, 一起学Java]
categories: [一起学Java系列,（2）引入日志篇]
---
继续完成上篇([一起学Java(11)-[日志篇]教你分析SLF4J源码，掌握Logger接口实现类加载原理](https://www.coderli.com/java-go-11-import-log-three/))留给自己的任务，研究Logback是如何和SLF4J无缝集成的。

<!--more-->

在之前的`SLF4J`源码研究中([教你分析SLF4J源码，掌握Logger接口实现类加载原理](https://www.coderli.com/java-go-11-import-log-three/))我们已经知道`SLF4J`中利用`java.util.ServiceLoader` 机制寻找SLF4JServiceProvider的实现类，从而得到构造Logger实例的工厂类。那么我们就先看看`java.util.ServiceLoader`是个什么东西。

## 一、java.util.ServiceLoader定位和原理

`java.util.ServiceLoader` 是 Java 提供的一个服务发现机制，它允许程序在运行时动态地加载和使用实现了某个接口或抽象类的服务实现。这个机制在 Java 的模块化系统和插件系统中非常有用。正好符合Log框架的场景定位。

`ServiceLoader` 通过一种称为***服务提供者接口（SPI, Service Provider Interface***的机制工作。服务提供者接口是一个接口或抽象类，而服务实现类是该接口或抽象类的具体实现。

### 1. **服务声明**

服务提供者接口在 JAR 包中的 `META-INF/services` 目录下声明。该目录下的每个文件名对应一个服务接口，全路径名，文件内容是该接口的一个或多个实现类的全路径名。

例如，假设你有一个接口 `com.example.MyService`，那么你需要在 `META-INF/services` 目录下创建一个名为 `com.example.MyService` 的文件，文件内容如下：

```java
com.example.impl.MyServiceImpl1
com.example.impl.MyServiceImpl2
```

这表示 `MyService` 有两个实现类：`MyServiceImpl1` 和 `MyServiceImpl2`。

### 2. **加载服务**

使用 `ServiceLoader` 加载服务的代码通常如下：

```java
ServiceLoader<MyService> serviceLoader = ServiceLoader.load(MyService.class);
for (MyService service : serviceLoader) {
    service.doSomething(); // doSomething是MyService接口中定义的方法
}
```

`ServiceLoader.load()` 方法会查找并实例化所有在 `META-INF/services/com.example.MyService` 文件中列出的服务实现类，后面就是实现类的使用了，也就不难理解了。

以上述理论为基础，来看看Logback中的实现。

## 二、Logback代码解析，如何实现SLF4JServiceProvider接口

{% include custom/custom-post-content-inner.html %}

展开logback-classic源码包，找到`META-INF/services`文件夹，果然有名为`org.slf4j.spi.SLF4JServiceProvider`的文件

![logback-classic中META-INF/services目录下的文件](/images/post/java-go-12/logback-provider.png)

内容如下：

```plaintext
ch.qos.logback.classic.spi.LogbackServiceProvider
```

即Logback提供的`SLF4JServiceProvider`接口的实现类。这样，根据上文的分析([教你分析SLF4J源码，掌握Logger接口实现类加载原理](https://www.coderli.com/java-go-11-import-log-three/)),在`SLF4J`的***LoggerFactory***中便可以通过`java.util.ServiceLoader`获取到Logback的***SLF4JServiceProvider***实现，并在bind函数中执行后续的Logger初始化操作。

```java
private final static void bind() {
        try {
            List<SLF4JServiceProvider> providersList = findServiceProviders();
            reportMultipleBindingAmbiguity(providersList);
            if (providersList != null && !providersList.isEmpty()) {
                PROVIDER = providersList.get(0);
                // SLF4JServiceProvider.initialize() is intended to be called here and nowhere else.
                PROVIDER.initialize();
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

> 在bind函数源码中可以看到，如果项目中发现了多个`SLF4JServiceProvider`的实现类，SLF4J只会取第一个进行初始化。
{: .prompt-tip }

至此，SLF4J如何与Logback无缝集成的原理也就大致了解清楚了。对于Logback而言，原生实现了`SLF4JServiceProvider`接口，自然也就不需要桥接层了。对于像Log4j 2这种没有原生实现`SLF4JServiceProvider`的框架，其实我们也能大致猜到其桥阶层的实现原理：按照`java.util.ServiceLoader`原理向上实现SLF4J的`SLF4JServiceProvider`接口，向下调用对应的日志实现层框架，下一步我们就看一下Log4j 2的桥接方式，来印证一下我们的猜想。
