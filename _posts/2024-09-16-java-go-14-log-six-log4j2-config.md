---
layout: post
title: 一起学Java(14)-[日志篇]教你用透Log4j2，掌握Log4j2配置文件原理
date: 2024-09-26 19:00 +0800
author: onecoder
image: /images/post/java-go-13/log4j2-slf4j2-provider-relation.svg
comments: true
tags: [Java, Log, SLF4J, 一起学Java]
categories: [一起学Java系列,（2）引入日志篇]
---
掌握了Log4j2与SLF4J的集成原理([一起学Java(12)-[日志篇]教你分析SLF4J源码，掌握SLF4J如何与Logback无缝集成的原理](https://www.coderli.com/java-go-12-import-log-four-logback/))，继续研究`Log4j2`和`SLF4J`这种需要桥接集成的方式。

<!--more-->

`Log4j2` 的配置文件用于定义日志记录的行为，控制日志输出的位置、格式、级别等内容。常用的配置文件格式有 `XML`、`YAML` 和 `properties`，其中 `XML` 最为常用。下面将详细解析 `log4j2` 的 `XML` 配置文件结构及各个部分的功能。

### 1. `Log4j2` 配置文件的基本结构
一个完整的 `Log4j2 XML` 配置文件通常包含以下几个部分：
- `<Configuration>`: 顶层配置节点，包含所有日志配置信息。
- `<Properties>`: 定义日志配置中使用的常量。
- `<Appenders>`: 定义日志的输出目标。
- `<Loggers>`: 定义不同类别的日志器及其级别、输出方式等。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="warn">
    <Properties>
        <Property name="log.path">logs/app.log</Property>
    </Properties>

    <Appenders>
        <!-- 定义控制台输出 -->
        <Console name="ConsoleAppender" target="SYSTEM_OUT">
            <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
        </Console>

        <!-- 定义文件输出 -->
        <File name="FileAppender" fileName="${log.path}">
            <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
        </File>
    </Appenders>

    <Loggers>
        <!-- 根日志器 -->
        <Root level="info">
            <AppenderRef ref="ConsoleAppender"/>
            <AppenderRef ref="FileAppender"/>
        </Root>

        <!-- 自定义日志器 -->
        <Logger name="com.example.MyClass" level="debug" additivity="false">
            <AppenderRef ref="FileAppender"/>
        </Logger>
    </Loggers>
</Configuration>
```

### 2. `Configuration` 节点
- `status`: 配置 `log4j2` 自身日志的级别，如 `error`、`warn`、`info`，用于输出 `log4j2` 配置过程中的错误或警告。
- `monitorInterval`: （可选）用于指定监控文件变化的时间间隔，以秒为单位。配置文件更改后，`log4j2` 会自动重载配置文件。

### 3. `Properties` 节点
定义变量，便于配置复用。可以通过 `${propertyName}` 的形式在配置中使用。
```xml
<Properties>
    <Property name="log.path">logs/app.log</Property>
</Properties>
```

### 4. `Appenders` 节点
`Appenders` 节点用于定义日志的输出目标，如控制台、文件、数据库等。常见的 `Appender` 类型有：
- `Console`: 输出到控制台。
- `File`: 输出到文件。
- `RollingFile`: 滚动输出到多个文件。

#### 常用的 `Appender` 配置
1. **ConsoleAppender**: 输出日志到控制台。
```xml
<Console name="ConsoleAppender" target="SYSTEM_OUT">
    <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
</Console>
```
- `name`: `Appender` 的名称，用于在 `Loggers` 中引用。
- `target`: 可以是 `SYSTEM_OUT` 或 `SYSTEM_ERR`，表示输出到标准输出或错误输出。
- `PatternLayout`: 格式化输出日志内容，`%d` 表示日期，`%t` 表示线程名，`%-5p` 表示日志级别，`%c{1}` 表示类名，`%m` 表示日志信息，`%n` 表示换行。

2. **FileAppender**: 输出日志到文件。
```xml
<File name="FileAppender" fileName="${log.path}">
    <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
</File>
```
- `fileName`: 指定输出日志文件的路径。

3. **RollingFileAppender**: 滚动日志文件，按大小或时间分割日志文件。
```xml
<RollingFile name="RollingFileAppender" fileName="${log.path}" filePattern="logs/app-%d{MM-dd-yyyy}.log.gz">
    <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
    <Policies>
        <TimeBasedTriggeringPolicy />
    </Policies>
</RollingFile>
```
- `filePattern`: 指定日志滚动后文件的命名规则，`%d{MM-dd-yyyy}` 表示按日期滚动，`.gz` 表示日志文件压缩。

### 5. `Loggers` 节点
定义了日志器，`Loggers` 包含根日志器和自定义日志器。

1. **Root Logger (根日志器)**: 定义全局默认的日志级别和输出方式。
```xml
<Root level="info">
    <AppenderRef ref="ConsoleAppender"/>
    <AppenderRef ref="FileAppender"/>
</Root>
```
- `level`: 指定日志级别，如 `trace`、`debug`、`info`、`warn`、`error`、`fatal`，`log4j2` 只会输出不低于该级别的日志。
- `AppenderRef`: 引用 `Appenders` 中定义的 `Appender`，决定日志输出到哪里。

2. **Custom Logger (自定义日志器)**: 用于某些包或类的单独日志配置。
```xml
<Logger name="com.example.MyClass" level="debug" additivity="false">
    <AppenderRef ref="FileAppender"/>
</Logger>
```
- `name`: 指定日志器的名称，通常是包名或类名。
- `level`: 指定该日志器的日志级别。
- `additivity`: 如果为 `false`，表示该日志器不会继承上级日志器的 `Appender`，只使用自己定义的 `Appender`。

### 6. `Layouts` 节点
`Layout` 定义了日志输出的格式，最常用的是 `PatternLayout`。常见的格式化符号包括：
- `%d`: 日志时间。
- `%t`: 线程名。
- `%p`: 日志级别。
- `%c`: 日志记录器的类名。
- `%m`: 日志信息。
- `%n`: 换行符。

### 7. 常见场景的配置

#### 按时间滚动日志
```xml
<RollingFile name="RollingFileAppender" fileName="${log.path}" filePattern="logs/app-%d{MM-dd-yyyy}.log">
    <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
    <Policies>
        <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
    </Policies>
</RollingFile>
```
`TimeBasedTriggeringPolicy` 用于按时间间隔滚动日志文件。

#### 按大小滚动日志
```xml
<RollingFile name="RollingFileAppender" fileName="${log.path}" filePattern="logs/app-%i.log">
    <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
    <Policies>
        <SizeBasedTriggeringPolicy size="10MB"/>
    </Policies>
</RollingFile>
```
`SizeBasedTriggeringPolicy` 用于日志文件超过指定大小时滚动。

### 总结
`Log4j2` 的配置文件灵活性很强，允许对日志输出目标、格式、级别进行精细控制。通过配置 `Appender` 和 `Logger`，你可以将不同级别的日志发送到不同的目标位置，并为不同的模块设置不同的日志输出规则。