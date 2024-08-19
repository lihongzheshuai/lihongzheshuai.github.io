---
layout: post
title: slf4j+logback配置方式和logback.groovy配置文件
date: 2012-05-30 19:43 +0800
author: onecoder
comments: true
tags: [Logback, SLF4J]
categories: [Java技术研究,Log]
thread_key: 162
---
最近看到slf4j+logback的日志方案，并且介绍说，与log4j出自同一作者且做了不少优化，所以决定从commons-logging+log4j切换过来。

* logback官网：（该作者即为log4j的作者）[http://logback.qos.ch/](http://logback.qos.ch/)

切换方式非常简单，在原有基础上加入如下jar包即可。

* slf4j-api-1.6.2.jar
* jcl-over-slf4j-1.6.2.jar \\\用于桥接commons-logging 到 slf4j

如果直接使用slf4j+logback的方案则无需此jar logback目前最新版是1.0.3

* 下载链接： [http://logback.qos.ch/dist/logback-1.0.3.zip](http://logback.qos.ch/dist/logback-1.0.3.zip)

Maven依赖如下：

```xml
<dependency> 
    <groupId>org.slf4j</groupId> 
    <artifactId>slf4j-api</artifactId> 
    <version>1.6.2</version> 
</dependency> 
<dependency> 
    <groupId>org.slf4j</groupId> 
    <artifactId>jcl-over-slf4j</artifactId> 
    <version>1.6.2</version> 
</dependency> 
<dependency> 
    <groupId>ch.qos.logback</groupId> 
    <artifactId>logback-core</artifactId> 
    <version>0.9.29</version> 
</dependency> 
<dependency> 
    <groupId>ch.qos.logback</groupId> 
    <artifactId>logback-classic</artifactId> 
    <version>0.9.29</version> 
</dependency> 
```

logback会依次读取以下类型配置文件：

* logback.groovy
* logback-test.xml
* logback.xml
如果均不存在会采用默认配置 

logback.xml样例如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>   
<configuration>   
  <appender name="stdout" class="ch.qos.logback.core.ConsoleAppender">   
    <encoder  class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">   
      <pattern>%d{yyyy/MM/dd-HH:mm:ss.SSS} %level [%thread] %class:%line>>%msg%n</pattern>   
    </encoder >   
  </appender>   
   
  <root level="INFO">   
    <appender-ref ref="stdout" />   
  </root>   
</configuration>
```

其中pattern属性的意义跟log4j基本相同，具体可参考

* 官方文档：[http://logback.qos.ch/manual/layouts.html](http://logback.qos.ch/manual/layouts.html)

logback.groovy的样例代码如下：

```groovy
import static ch.qos.logback.classic.Level.DEBUG 
import ch.qos.logback.classic.encoder.PatternLayoutEncoder 
import ch.qos.logback.core.ConsoleAppender 
 
appender("CONSOLE", ConsoleAppender) { 
  encoder(PatternLayoutEncoder) { 
    pattern = "%d{yyyy/MM/dd-HH:mm:ss} %-5level [%thread] %class{5}:%line>>%msg%n" 
  } 
} 
root(DEBUG, ["CONSOLE"]) 
```

官方提供了logback.xml->logback.groovy的转换工具

* 地址：[http://logback.qos.ch/translator/asGroovy.html](http://logback.qos.ch/translator/asGroovy.html)

对于logback.groovy的使用，***需要注意：*** logback.groovy需要放在源码包的根目录下，否则会找不到。 在eclipse中，如果安装了groovy的插件，需要将放置logback.groovy的源码包位置设置为groovysrcipt的所在位置，即在编译的时候不将goorvy编译成class文件，而是直接将groovy脚本复制到output path下。否则仍无法生效。 