---
layout: post
title: 一起学Java(14)-[日志篇]教你用透Log4j2，掌握Log4j2配置原理和实际应用
date: 2024-09-28 14:00 +0800
author: onecoder
image: /images/post/java-go/log4j2-config.png
comments: true
tags: [Java, Log, 一起学Java]
categories: [一起学Java系列,（2）引入日志篇]
---
研究完Log4j2与SLF4J集成的原理([一起学Java(13)-[日志篇]教你分析SLF4J和Log4j2源码，掌握SLF4J与Log4j2桥接集成原理](https://www.coderli.com/java-go-13-import-log-five-log4j2-slf4j2/))，学习如何真正应用Log4j2。

<!--more-->

当你单纯引入`Log4j2`的包并编写完样例代码，运行后你可能会发现没有任何日志输出，这是因为`Log4j2`真正运行起来是需要首先完成日志的基本配置的，也就是告诉`Log4j2`，我要对哪些类进行日志记录，记录到哪里，日志记录成什么格式等等。然后`Log4j2`才能运行起来。这就是今天研究的重点。

## 一、理论篇Log4j2配置文件介绍

根据官方描述([Log4j2官方手册](https://logging.apache.org/log4j/2.12.x/manual/configuration.html))，Log4j2支持的配置文件类型和查找顺序如下：

### （一）配置文件类型

Log4j2 支持以下几种类型的配置文件：

1. **XML 文件** (`log4j2.xml`)
2. **YAML 文件** (`log4j2.yaml` 或 `log4j2.yml`)
3. **JSON 文件** (`log4j2.json`)
4. **Properties 文件** (`log4j2.properties`)

### （二）配置文件查找顺序

Log4j2 在启动时会按照以下顺序查找配置文件：

1. **通过系统属性 `log4j.configurationFile` 指定的配置文件**：如果设置了此系统属性，Log4j2 会首先使用该属性指定的配置文件路径。
   - 例如：`-Dlog4j.configurationFile=/path/to/log4j2.xml`

2. **类路径下的默认配置文件**：如果没有指定配置文件，Log4j2 会在类路径中按顺序查找以下名称的文件：
   1. `log4j2-test.xml`
   2. `log4j2-test.yaml` 或 `log4j2-test.yml`
   3. `log4j2-test.json`
   4. `log4j2-test.properties`
   5. `log4j2.xml`
   6. `log4j2.yaml` 或 `log4j2.yml`
   7. `log4j2.json`
   8. `log4j2.properties`

3. **默认配置**：如果找不到任何有效的配置文件，Log4j2 会使用一个默认配置，它会将日志输出到控制台，并且日志级别为 `ERROR`。

### (三) 配置文件内容介绍

下面将详细解析 `log4j2` 的 `XML` 配置文件结构及各个部分的功能。

#### 1. `Log4j2` 配置文件的基本结构

一个完整的 `Log4j2 XML` 配置文件通常包含以下几个部分：

- `<Configuration>`: 顶层配置节点，包含所有日志配置信息。
- `<Properties>`: 定义日志配置中使用的常量。
- `<Appenders>`: 定义日志的输出目标。
- `<Loggers>`: 定义不同类别的日志器及其级别、输出方式等。

**配置文件样例如下**：

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

#### 2. `Configuration` 节点

- `status`: 配置 `log4j2` 自身日志的级别，如 `error`、`warn`、`info`，用于输出 `log4j2` 配置过程中的错误或警告。
- `monitorInterval`: （可选）用于指定监控文件变化的时间间隔，以秒为单位。配置文件更改后，`log4j2` 会自动重载配置文件。

#### 3. `Properties` 节点

定义变量，便于配置复用。可以通过 `${propertyName}` 的形式在配置中使用。例如：

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

常用的 `Appender` 类型有：

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

#### 5. `Loggers` 节点

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

2. **Custom Logger (自定义日志器)**: 用于某些包或类的单独日志配置。这是我们后续应用实验的重点。

    ```xml
    <Logger name="com.example.MyClass" level="debug" additivity="false">
        <AppenderRef ref="FileAppender"/>
    </Logger>
    ```

    - `name`: 指定日志器的名称，通常是包名或类名。
    - `level`: 指定该日志器的日志级别。
    - `additivity`: 如果为 `false`，表示该日志器不会继承上级日志器的 `Appender`，只使用自己定义的 `Appender`。。例如，假设有以下层次结构的日志器：
      - 父日志器：`com.example`
        - 定义了一个控制台输出 `Appender`
      - 子日志器：`com.example.service`
        - 定义了一个文件输出 `Appender`

        如果 `com.example.service` 的 `additivity` 为 `true`，当你使用 `com.example.service` 记录日志时，日志将会被发送到两个地方：
        1. 使用子日志器的文件输出 `Appender`。
        2. 传播到父日志器 `com.example`，并通过父日志器的控制台输出 `Appender`。如果为`false`，则不会传播到父日志器。

#### 6. `Layouts` 节点

`Layout` 定义了日志输出的格式，最常用的是 `PatternLayout`。常见的格式化符号包括：

- `%d`: 日志时间。
- `%t`: 线程名。
- `%p`: 日志级别。
- `%c`: 日志记录器的类名。
- `%m`: 日志信息。
- `%n`: 换行符。

#### 7. 常见场景的配置

按时间滚动日志

```xml
<RollingFile name="RollingFileAppender" fileName="${log.path}" filePattern="logs/app-%d{MM-dd-yyyy}.log">
    <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
    <Policies>
        <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
    </Policies>
</RollingFile>
```

`TimeBasedTriggeringPolicy` 用于按时间间隔滚动日志文件。

按大小滚动日志

```xml
<RollingFile name="RollingFileAppender" fileName="${log.path}" filePattern="logs/app-%i.log">
    <PatternLayout pattern="%d [%t] %-5p %c{1} - %m%n"/>
    <Policies>
        <SizeBasedTriggeringPolicy size="10MB"/>
    </Policies>
</RollingFile>
```

`SizeBasedTriggeringPolicy` 用于日志文件超过指定大小时滚动。

## 二、实战篇，定义不同的Logger，验证不同的Pattern

修改我们项目的Log4j2项目配置如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5p %logger{1}[%l] - %msg%n"/>
        </Console>
        <Console name="d-pattern" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} - %m%n"/>
        </Console>
        <Console name="c-pattern" target="SYSTEM_OUT">
            <PatternLayout pattern="%c - %m%n"/>
        </Console>
    </Appenders>
    <Loggers>
        <Logger name="com.coderli.one.log.log4j2.DPatternLogger" level="info" additivity="false">
            <AppenderRef ref="d-pattern"/>
        </Logger>
        <Logger name="com.coderli.one.log.log4j2.CPatternLogger" level="info" additivity="false">
            <AppenderRef ref="c-pattern"/>
        </Logger>
        <Root level="info">
            <AppenderRef ref="Console"/>
        </Root>
    </Loggers>
</Configuration>
```

即定义了两个个性化的Logger，***CPatternLogger***和***DPatternLogger***，其分别对应各自的日志格式化定义。一个只输出%c（Logger名），一个只输出%d(时间)，其他未明确定义的按默认Root Logger对应的Pattern输出。对应代码和日志输出如下：

***CPatternLogger***

```java
package com.coderli.one.log.log4j2;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 本类用于验证%c Logger Pattern
 * @author OneCoder
 * @Blog https://www.coderli.com
 * @source https://github.com/lihongzheshuai/java-all-in-one
 */
public class CPatternLogger {

    public static void main(String[] args) {
        Logger logger = LoggerFactory.getLogger(CPatternLogger.class);
        logger.info("%c pattern: Hello World");
    }

}
```

```console
com.coderli.one.log.log4j2.CPatternLogger - %c pattern: Hello World
```

***DPatternLogger***

```java
package com.coderli.one.log.log4j2;

import com.coderli.one.log.Slf4jLogMain;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 本类用于验证%d Logger Pattern
 * @author OneCoder
 * @Blog https://www.coderli.com
 * @source https://github.com/lihongzheshuai/java-all-in-one
 */
public class DPatternLogger {
    public static void main(String[] args) {
        Logger logger = LoggerFactory.getLogger(DPatternLogger.class);
        logger.info("%d pattern: Hello World");
    }
}
```

```console
14:31:24.643 - %d pattern: Hello World
```

***CommonPatternLogger***

```java
package com.coderli.one.log.log4j2;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 本类用于验证Rooter Logger Pattern
 * @author OneCoder
 * @Blog https://www.coderli.com
 * @source https://github.com/lihongzheshuai/java-all-in-one
 */
public class CommonPatternLogger {
    public static void main(String[] args) {
        Logger logger = LoggerFactory.getLogger(CommonPatternLogger.class);
        logger.info("Common Rooter pattern: Hello World");
    }
}
```

```console
2024-09-28 14:38:00.690 [main] INFO  CommonPatternLogger[com.coderli.one.log.log4j2.CommonPatternLogger.main(CommonPatternLogger.java:15)] - Common Rooter pattern: Hello World
```

至此，一个项目的Log框架，基本就搭建完成了。

---

所有代码已上传至：[***https://github.com/lihongzheshuai/java-all-in-one***](https://github.com/lihongzheshuai/java-all-in-one)