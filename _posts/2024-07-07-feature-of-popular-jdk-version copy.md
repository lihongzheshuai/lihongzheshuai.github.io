---
layout: post
title: 2024年主流使用的JDK版本及其核心特性介绍
date: 2024-07-07 22:32 +0800
author: onecoder
comments: true
tags: [jdk,Java]
thread_key: 202407072232
---
在群里交流的时候，经常遇到不同同学使用的JDK版本五花八门，并且很多不知道其使用版本的特点。作为Java开发者，理解不同JDK版本的核心特性和优势不仅能提高我们的开发效率，还能帮助我们更好地选择适合自己项目的版本。
<!--more-->

# 一、JDK22（最新版）
截至2024年，最新的JDK版本是Java SE Development Kit 22（JDK 22）。Oracle在2024年3月19日正式发布了JDK 22，并在其后发布了JDK 22.0.1版本作为最新的稳定版本​。
JDK 22引入了多个新的特性和改进，包括：
1. **Unnamed Variables & Patterns (JEP 456) 未命名变量和模式**:
    - 这项特性帮助开发者在需要声明但不使用变量或嵌套模式时，减少错误的机会，提升代码的可读性和可维护性​​。
2. **String Templates (Second Preview) (JEP 459) 字符串模板（第二次预览）**:
    - 简化了包括运行时计算值的字符串的表达，并提高了由用户提供值的程序的安全性。此特性改善了混合文本和表达式的可读性，并允许创建不通过中间字符串表示的非字符串值​。
3. **Implicitly Declared Classes and Instance Main Methods (Second Preview) (JEP 463) 隐式声明类和实例主方法（第二次预览）:**
    - 为初学者提供了一种平滑的 Java 编程入门途径，使其在不需要理解为大型程序设计的语言特性的情况下编写其第一个程序​ ​。
4. **Structured Concurrency (Second Preview) (JEP 462) 结构化并发（第二次预览）:**
    - 通过引入结构化并发 API，简化了错误处理和取消操作，并增强了并发代码的可观察性，帮助消除常见的取消和关闭风险​​。
5. **Scoped Values (Second Preview) (JEP 464) 范围值（第二次预览）:**
    - 允许在线程之间共享不可变数据，提高了项目的易用性、可理解性、性能和鲁棒性​​。
6. **Foreign Function & Memory API (JEP 454) 外部函数与内存 API:**
    - 提供了一个 API，使 Java 程序能够与 Java 运行时外部的代码和数据进行交互，提高了易用性、灵活性、安全性和性能​​。
7. **Vector API (Seventh Incubator) (JEP 460) 向量 API（第七次孵化器）**:
    - 引入了向量计算 API，使其在支持的 CPU 架构上能可靠地编译为向量指令，性能优于等效的标量计算​​。
8. **Class-File API (Preview) (JEP 457) 类文件 API（预览）:**
    - 提供了一个标准 API，用于解析、生成和转换 Java 类文件，提高了开发者的生产力​​。
9. **Launch Multi-File Source-Code Programs (JEP 458) 启动多文件源代码程序:**
    - 增强了 Java 应用启动器，使其能够运行由多个 Java 源文件组成的程序，使从小型程序到大型程序的过渡更加平滑​​。
10. **Stream Gatherers (Preview) (JEP 461) 流收集器（预览）:**
    - 增强了 Stream API，支持自定义中间操作，使数据转换更加灵活和高效​。
11. **Region Pinning for G1 (JEP 423) G1 的区域固定:**
    - 通过允许在某些 JNI 调用期间进行垃圾收集，减少了延迟，从而改进了性能​。
这些特性在Java社区的协作下不断演进，旨在提高Java开发者的生产力和代码的性能。

# 二、其他JDK版本
除了最新发布的JDK 22外，还有许多主流的JDK版本正在广泛使用。以下是一些常见的主流JDK版本及其特点：

## 1.JDK 21
JDK 21 是一个长期支持 (LTS) 版本。这意味着它将获得长期的更新和支持，为开发人员提供一个稳定的开发环境。Oracle 确认 JDK 21 将作为 LTS 版本，延续 Java 17 的 LTS 支持模式，并提供长期支持和维护。

核心特性：
1. **Virtual Threads (JEP 444) 虚拟线程:**
    - 虚拟线程是一种轻量级的线程实现，可以极大地提高并发编程的性能和可伸缩性。虚拟线程允许开发人员以更低的开销创建和管理大量线程。
2. **Pattern Matching for Switch (Third Preview) (JEP 433) Switch 语句的模式匹配（第三次预览）:**
    - 扩展 switch 语句和表达式，以支持模式匹配。这使得代码更加简洁和可读。
3. **Record Patterns (Second Preview) (JEP 432) 记录模式（第二次预览）:**
    - 引入记录模式，允许在模式匹配中解构记录类的实例，从而更方便地访问记录类的组件。
4. **Unnamed Patterns and Variables (JEP 443) 未命名模式和变量:**
    - 引入未命名模式和变量，用于捕获不需要使用的匹配结果，简化代码书写。
5. **Sequenced Collections (JEP 431) 有序集合:**
    - 提供了新的接口用于表示有序集合，例如 List、Set 和 Map 的有序变体，增强了集合操作的灵活性。
6. **Scoped Values (Preview) (JEP 429) 作用域值（预览）:**
    - 引入作用域值，这是一种新的共享不可变数据的方法，可以跨线程共享数据，提高代码的可维护性和性能。
7. **String Templates (First Preview) (JEP 430) 字符串模板（第一次预览）:**
    - 提供了一种新的字符串模板机制，使得在字符串中嵌入表达式更加简洁和安全，增强了代码的可读性和维护性。
8. **Foreign Function & Memory API (Third Preview) (JEP 434) 外部函数和内存 API（第三次预览）:**
    - 提供了一种新的 API，使得 Java 程序能够调用外部函数并访问外部内存，简化了与本地代码的交互。
9. **Generational ZGC (JEP 439) 分代 ZGC:**
    - 改进了 ZGC 垃圾收集器，引入了分代收集机制，以提高内存管理性能。
10. **Structured Concurrency (JEP 428) 结构化并发:**
    - 引入了一种新的并发编程模型，简化了并发任务的管理，提高了错误处理和取消操作的可控性。
这些特性和改进旨在提升开发者的生产力，增强 Java 应用的性能和安全性，并确保 Java 在现代开发环境中继续保持竞争力。

## 2.JDK 17
这是一个长期支持（LTS）版本，发布于2021年9月。LTS版本提供了长期的更新和支持，是许多企业的首选。目前，JDK 17在生产环境中的应用非常广泛，使用率超过35%
核心特性：
1. **Sealed Classes (JEP 409) 密封类:**
    - Allows classes or interfaces to restrict which other classes or interfaces can extend or implement them. This feature enhances the control over inheritance hierarchies.
    - 允许类或接口限制哪些其他类或接口可以扩展或实现它们。目的是更好地控制继承层次结构。
2. **Foreign Function & Memory API (Incubator) (JEP 412) 外部函数与内存 API（孵化器）:**
    - Provides a pure Java API to call external code and access external memory, making it easier and safer to interact with native code.
    - 提供一种纯 Java API 来调用外部代码和访问外部内存，更容易和更安全地与本地代码交互。
3. **Pattern Matching for Switch (Preview) (JEP 406) Switch 的模式匹配（预览）:**
    - Extends switch statements and expressions to support pattern matching, enabling more complex condition checks and operations.
    - 扩展 switch 语句和 switch 表达式，以进行模式匹配。可以根据模式进行更复杂的条件检查和操作。
4. **Strongly Encapsulate JDK Internals (JEP 403) 强封装 JDK 内部 API:**
    - Strengthens the encapsulation of JDK internals by making internal APIs inaccessible by default, enhancing modularity and security.
    - 强化对 JDK 内部 API 的封装，默认情况下禁止访问 JDK 内部 API，进一步提高模块系统的封装性和安全性。
5. **Context-Specific Deserialization Filters (JEP 415) 特定上下文的反序列化过滤器:**
    - Provides a mechanism to control deserialization behavior through filters, enhancing security.
    - 提供一种机制，通过过滤器来控制反序列化操作的行为，增强安全性。
6. **Remove the Experimental AOT and JIT Compiler (JEP 410) 移除实验性的 AOT 和 JIT 编译器:**
    - Removes the experimental Ahead-of-Time (AOT) and Just-In-Time (JIT) compilers due to low usage and high maintenance costs.
    - 移除实验性的 AOT（Ahead-of-Time）和 JIT（Just-In-Time）编译器，这些编译器的使用率低且维护成本高。
7. **Deprecate the Applet API for Removal (JEP 398) 弃用并计划移除 Applet API:**
    - Deprecates the Applet API and plans to remove it in future releases.
    - 将 Applet API 标记为弃用并计划在未来的版本中移除。
8. **New macOS Rendering Pipeline (JEP 382) 新的 macOS 渲染管道:**
    - Introduces a new macOS rendering pipeline based on Apple's Metal API, replacing the previous OpenGL pipeline.
    - 引入新的 macOS 渲染管道，基于 Apple 的 Metal API，替代之前的 OpenGL 渲染管道。
9. **Vector API (Second Incubator) (JEP 414) 向量 API（第二次孵化器）:**
    - Introduces a new Vector API for vector computations, which can improve performance.
    - 引入新的向量 API，提供矢量计算的支持，可以提高性能。
10. **Restore Always-Strict Floating-Point Semantics (JEP 306) 恢复严格的浮点数语义:**
    - Restores strict floating-point semantics, making all floating-point operations conform to the IEEE 754 standard.
    - 恢复严格的浮点数运算语义，使所有浮点数操作都遵循 IEEE 754 标准。

## 3. JDK 11
也是一个LTS版本，发布于2018年9月。尽管较旧，但仍然在许多企业中使用。JDK 11引入了许多重要特性和性能改进，如新的垃圾回收器和更快的启动时间
核心特性：
1. **Nest-Based Access Control (JEP 181) 基于嵌套的访问控制:**
    - Introduces the concept of nests, allowing classes within the same nest to access each other's private members directly, simplifying compiler-generated access code and enhancing maintainability.
    - 引入了 nest（嵌套）的概念，允许同一个 nest 中的类直接访问彼此的私有成员，从而简化编译器生成的访问代码并增强可维护性。
2. **Dynamic Class-File Constants (JEP 309) 动态类文件常量:**
    - Introduces a new constant pool item CONSTANT_Dynamic, allowing delayed constant computation, supporting more flexible and efficient constant handling.
    - 引入新的常量池项 CONSTANT_Dynamic，延迟常量的计算，支持更加灵活和高效的常量处理。
3. **Local-Variable Syntax for Lambda Parameters (JEP 323) Lambda 参数的局部变量语法:**
    - Allows the use of the var keyword in lambda expressions to declare parameters, providing consistency and enhancing code readability.
    - 允许在 lambda 表达式中使用 var 关键字来声明参数，提供一致性和增强代码的可读性。
4. **HTTP Client (Standard) (JEP 321) HTTP 客户端（标准）:**
    - Standardizes the new HTTP Client API for sending HTTP requests and receiving responses, supporting HTTP/1.1 and HTTP/2, and providing synchronous and asynchronous operations.
    - 标准化新的 HTTP 客户端 API，用于发送 HTTP 请求和接收响应，支持 HTTP/1.1 和 HTTP/2，并提供同步和异步操作。
5. **Removal of the Java EE and CORBA Modules (JEP 320) 移除 Java EE 和 CORBA 模块:**
    - Removes the Java EE and CORBA modules, which have been deprecated and are used less in modern Java development.
    - 移除了 Java EE 和 CORBA 模块，这些模块已经被弃用并且在现代 Java 开发中使用较少。
6. **Epsilon: A No-Op Garbage Collector (JEP 318) Epsilon：无操作垃圾收集器:**
    - Introduces a new garbage collector, Epsilon, which does not perform any memory reclamation, mainly used for performance testing and memory pressure testing.
    - 引入了一个新的垃圾收集器 Epsilon，该垃圾收集器不执行任何内存回收操作，主要用于性能测试和内存压力测试。
7. **Flight Recorder (JEP 328) 飞行记录器:**
    - Provides a low-overhead event collection framework, allowing the collection of diagnostic and monitoring data for analyzing and debugging Java application performance issues.
    - 提供了一个低开销的事件收集框架，允许收集诊断和监控数据，用于分析和调试 Java 应用程序的性能问题。
8. **Launch Single-File Source-Code Programs (JEP 330) 启动单文件源代码程序:**
    - Allows the java command to run a single Java source file directly, simplifying the process of writing and executing small programs.
    - 允许使用 java 命令直接运行单个 Java 源文件，简化了小型程序的编写和执行流程。
9. **ZGC: A Scalable Low-Latency Garbage Collector (Experimental) (JEP 333) ZGC：可伸缩的低延迟垃圾收集器（实验性）:**
    - Introduces the Z Garbage Collector (ZGC), a scalable low-latency garbage collector designed to handle large memory applications with low latency.
    - 引入了 Z Garbage Collector (ZGC)，一个可伸缩的低延迟垃圾收集器，旨在处理大内存的低延迟应用。
10. **Deprecate the Pack200 Tools and API (JEP 336) 弃用 Pack200 工具和 API:**
    - Marks the Pack200 tools and API as deprecated, planning to remove them in future releases.
    - 将 Pack200 工具和 API 标记为弃用，计划在未来的版本中移除。
这些特性和改进使 JDK 11 在性能、可维护性和现代化开发支持方面得到了显著提升。

## 4. JDK 8
发布于2014年3月，是Java历史上使用最广泛的版本之一。它引入了Lambda表达式、流API和新的日期时间API等重要特性，尽管不再是LTS版本，但在一些老旧系统中仍然使用
核心特性：
JDK 8 引入了许多关键的新特性和改进，以下是其核心特性：
1. **Lambda Expressions (JEP 126) Lambda 表达式:**
    - 允许将功能作为方法参数传递或将代码作为数据处理，极大简化了集合的处理和多线程编程。
    - 例如：
    ```java
    List<String> list = Arrays.asList("a", "b", "c");
    list.forEach(item -> System.out.println(item));
    ```
2. **Stream API (JEP 107) 流 API:**
    - 提供了一种新的方法来处理集合，支持链式操作、过滤、映射和减少操作，使得集合处理更加简洁和高效。
    - 例如：
    ```java
    List<String> list = Arrays.asList("a", "b", "c");
    list.stream()
        .filter(s -> s.startsWith("a"))
        .forEach(System.out::println);
    ```
3. **Date and Time API (JSR 310) 日期和时间 API:**
    - 引入了新的日期和时间库 java.time，取代了旧的 java.util.Date 和 java.util.Calendar，提供了更好的日期和时间处理支持。
    - 例如：
     ```java
    LocalDate today = LocalDate.now();
    LocalDate birthday = LocalDate.of(1990, Month.JANUARY, 1);
    Period age = Period.between(birthday, today);
    ```
4. **Default Methods (JEP 126) 默认方法:**
    - 允许在接口中定义默认方法，从而为接口添加新的方法而不需要修改实现该接口的现有类。
    - 例如：
    ```java
    public interface Vehicle {
        default void print() {
            System.out.println("I am a vehicle");
        }
    }
    ```
5. **Nashorn JavaScript Engine (JEP 174) Nashorn JavaScript 引擎:**
    - 引入了一个新的 JavaScript 引擎 Nashorn，允许在 JVM 上执行 JavaScript 代码，提升了与 JavaScript 的互操作性。
    - 例如：
    ```java
    ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");
    engine.eval("print('Hello, Nashorn');");
    ```
6. **Optional Class (JEP 126) Optional 类:**
    - 引入了 Optional 类来避免空指针异常，提供了一种更优雅的处理可能为空的值的方法。
    - 例如：
    ```java
    Optional<String> optional = Optional.of("hello");
    optional.ifPresent(System.out::println);
    ```
7. **Metaspace:**
    - 将永久代（PermGen）替换为元空间（Metaspace），改善了内存管理。
8. **Compact Profiles (JEP 161) 精简配置:**
    - 允许创建包含 JDK 一部分功能的精简配置，从而在资源受限的设备上运行 Java 应用。
这些特性大大提升了 Java 的功能和性能，简化了编程过程，并提供了更多现代化编程的支持。


通过了解这些不同的JDK版本及其核心特性，我们可以更有针对性地选择和使用合适的版本，提升开发效率并确保项目的稳定性和性能。希望这篇博文能帮助大家在选择JDK版本时更加明智，避免盲目跟风。
