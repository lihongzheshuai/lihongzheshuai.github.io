---
layout: post
title: log4j2 与 log4j使用时的几点小区别 - log4j2上手说明
date: 2013-12-08 17:44 +0800
author: onecoder
comments: true
tags: [Log4j]
categories: [Java技术研究]
thread_key: 1567
---
<p>
	虽然log4j2 目前还是beta版，不过<a href="http://www.coderli.com">OneCoder</a>已经忍不住要尝试一下。跟使用log4j 比起来，上手上主要的区别有。<br />
	1、依赖的jar包。使用slf4j+log4j2 时，依赖的jar包如下：(gradle配置，Maven对照修改即可)</p>

```groovy
dependencies{
compile(
"org.apache.logging.log4j:log4j-api:$log4j_version",
"org.apache.logging.log4j:log4j-core:$log4j_version",
"org.apache.logging.log4j:log4j-slf4j-impl:$log4j_version"
)

}
```

<p>
	其中，log4j_version=2.0-beta9</p>
<p>
	<br />
	2、默认配置文件名字<br />
	默认搜索的配置文件名字变为log4j2或log4j-test开头的配置文件，这个变化，让<a href="http://www.coderli.com">OneCoder</a>吃了些苦头。没注意观察，还自以为配置文件还是log4j.xml，结果怎么都不管用。后来仔细阅读官方文档才发现问题。log4j2中，支持json和xml两个格式的配置文件，配置文件的搜索顺序为：</p>
<blockquote>
	<p>
		&nbsp; 1. Log4j will inspect the "log4j.configurationFile" system property and, if set, will attempt to load the configuration using the ConfigurationFactory that matches the file extension.<br />
		&nbsp; 2. If no system property is set the JSON ConfigurationFactory will look for log4j2-test.json or log4j2-test.jsn in the classpath.<br />
		&nbsp; 3. If no such file is found the XML ConfigurationFactory will look for log4j2-test.xml in the classpath.<br />
		&nbsp; 4. If a test file cannot be located the JSON ConfigurationFactory will look for log4j2.json or log4j2.jsn on the classpath.<br />
		&nbsp; 5. If a JSON file cannot be located the XML ConfigurationFactory will try to locate log4j2.xml on the classpath.<br />
		&nbsp; 6. If no configuration file could be located the DefaultConfiguration will be used. This will cause logging output to go to the console.</p>
</blockquote>
<p>
	环境变量log4j.configurationFile指定的文件->log4j2-test.json/log4j2-test.jsn -> log4j2-test.xml -> log4j2.json/log4j2.jsn -> log4j2.xml - > 默认配置DefaultConfiguration</p>
<p>
	3、配置文件格式</p>
<p>
	配置文件样例，跟1比起来有所简化。</p>
	
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
     <Appenders>
          <Console name="Console" target="SYSTEM_OUT">
               <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss} [%t] %-5level %l - %msg%n" />
          </Console>
     </Appenders>
     <Loggers>
          <Root level="debug">
               <AppenderRef ref="Console" />
          </Root>
     </Loggers>
</Configuration>
```

<p>
	其他的变化和优势，您可以在使用中慢慢体会了。</p>

