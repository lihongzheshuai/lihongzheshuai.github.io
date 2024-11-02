---
layout: post
title: 一起学Java(18)-[测试篇]教你通过Gradle引入配置JUnit5
date: 2024-10-28 23:00 +0800
author: onecoder
comments: true
tags: [Java, 单元测试, 一起学Java]
categories: [一起学Java系列,（4）测试篇]
---
前文已详细介绍了JUnit框架的特点以及JUnit5和JUnit4版本的核心差异([***《一起学Java(17)-[测试篇]教你认识Java单元测试框架JUnit，JUnit5和JUnit4区别详解》***](https://www.coderli.com/java-go-17-test-junit-intro/))。本文将进入应用实战，详细介绍如何在Gradle项目中引入和配置JUnit5测试框架。

通过本文，你将了解到：

- 如何在Gradle项目中添加JUnit5依赖
- JUnit5的基本配置方法
- 常见的Gradle测试任务配置

<!--more-->

## **一、JUnit 框架的发展历程和重要版本**

JUnit 是一个专为 Java 语言设计的测试自动化框架，广泛用于单元测试。它的历史可以追溯到1998年，由 Kent Beck 和 Erich Gamma 开发，旨在提供一个简单易用的框架来测试代码的每个单元。这一框架的出现标志着 Java 开发者开始重视单元测试的重要性，并推动了软件开发方法论的变革。

### JUnit 3

- **发布年份**：1998年
- **特点**：JUnit 3 引入了基本的测试结构，测试方法需要继承自 `junit.framework.TestCase`，并且测试方法必须以“test”开头。这个版本奠定了JUnit作为单元测试框架的基础。

### JUnit 4

- **发布年份**：2006年
- **特点**：
  - 引入了注解（如 `@Test`, `@Before`, `@After` 等），使得测试代码更加简洁和易读。
  - 支持参数化测试，允许同一测试方法使用不同参数运行。
  - 提供了更好的异常处理和更灵活的测试组织方式。

尽管 JUnit 4 在发布后获得了广泛应用，但由于缺乏对新兴开发模式（如函数式编程）的支持，以及其非模块化的设计，逐渐显露出局限性。

### JUnit 5

- **发布年份**：2017年
- **特点**：
  - **模块化设计**：JUnit 5 分为三个主要组件：JUnit Platform、JUnit Jupiter 和 JUnit Vintage。
    - **JUnit Platform**：提供运行测试的基础设施，支持多种测试引擎。
    - **JUnit Jupiter**：是 JUnit 5 的核心，包含新的编程模型和扩展模型，支持 Lambda 表达式和函数式编程。
    - **JUnit Vintage**：确保与 JUnit 3 和 JUnit 4 的兼容性，使旧版测试能够在新平台上运行。
  - 引入了新的生命周期注解，如 `@BeforeAll`, `@BeforeEach`, `@AfterEach`, `@AfterAll`，使得测试管理更加灵活。
  - 截止本文编写时（2024年10月28日）最新版本为[5.11.3](https://github.com/junit-team/junit5/releases/tag/r5.11.3)

---

## **二、JUnit 5 的核心架构设计理念和核心组件**

JUnit 5 是对 JUnit 4 的一次彻底重构和扩展，设计上更灵活和模块化，支持多种测试场景，适用于现代 Java 开发。下面详细介绍 JUnit 5 的**架构设计理念**和**核心组件**。

### **（一）核心设计理念**

#### **1. 模块化与灵活性**

- JUnit 5 不再是一个单一的框架，而是由多个模块组成，每个模块负责不同的功能。  
- 模块化的架构使得测试平台可以支持不止 JUnit 5，还兼容其他测试框架。

#### **2. 向后兼容性**

- 为了方便开发者从 JUnit 4 或 JUnit 3 迁移到 JUnit 5，JUnit 提供了 **JUnit Vintage** 模块来运行旧版本的测试。

#### **3. 可扩展性**

- 提供了灵活的扩展机制，允许开发者通过 `Extension API` 创建自定义扩展，并与其他框架（如 Spring）深度集成。

#### **4. 支持现代 Java 特性**

- 利用 **Java 8+ 的特性**，如 lambda 表达式、Stream API，让代码更简洁优雅。
- 支持参数化测试、动态测试，以及新的断言机制。

### **(二) JUnit 5的核心组件**

前面已经提到过，JUnit 5 分为 **三个主要模块**：**JUnit Platform**、**JUnit Jupiter** 和 **JUnit Vintage**。下面详细介绍每个组件的功能及作用。

#### **1. JUnit Platform（测试平台）**

**JUnit Platform** 是 JUnit 5 的基础层，为运行各种测试框架（包括 JUnit Jupiter 和 JUnit Vintage）提供支持。

- 定义了一个 **公共的运行接口**，支持多种测试框架。
- **IDE 和构建工具（如 Maven、Gradle）** 通过 JUnit Platform 执行测试。
- 提供了一个通用的 **测试发现和执行引擎**。

#### **2. JUnit Jupiter（JUnit 5 的核心 API 和实现）**

**JUnit Jupiter** 是 JUnit 5 的核心模块，定义了测试用例和测试生命周期的 API，实现了 JUnit 5 的新特性。

##### **JUnit Jupiter 提供的核心注解**

| **注解**         | **说明**                                |
|------------------|----------------------------------------|
| `@Test`          | 标记测试方法。                         |
| `@BeforeEach`    | 每个测试前运行的初始化方法。            |
| `@AfterEach`     | 每个测试后运行的清理方法。              |
| `@BeforeAll`     | 在所有测试之前执行（静态方法）。        |
| `@AfterAll`      | 在所有测试之后执行（静态方法）。        |
| `@DisplayName`   | 为测试方法或类设置展示名称。            |
| `@Disabled`      | 禁用测试方法或测试类。                  |
| `@ParameterizedTest` | 参数化测试的标记注解。               |

##### **JUnit Jupiter 的断言与异常处理**

- **断言**：提供丰富的断言 API，如 `assertAll()` 和 `assertThrows()`。
- **异常处理**：通过 `assertThrows()` 检查代码是否抛出预期的异常。

#### **3. JUnit Vintage（旧版本兼容模块）**

**JUnit Vintage** 模块允许在 JUnit 5 平台上运行 **JUnit 3 和 JUnit 4 的测试用例**。这确保了老项目可以逐步迁移到 JUnit 5，而不影响现有测试代码的运行。

- 支持老项目在迁移到 JUnit 5 期间的测试兼容性。
- 使用 JUnit Platform 运行旧版本测试，避免一次性重写所有测试代码。

---
{% include custom/custom-post-content-inner.html %}

## **三、JUnit 5 相比 JUnit 4 的主要改进和新特性**

### **1. 新的注解体系**

- JUnit 5 引入了新的注解，替代了 JUnit 4 的部分注解：
  - `@BeforeEach` 代替 `@Before`
  - `@AfterEach` 代替 `@After`
  - `@BeforeAll` 代替 `@BeforeClass`
  - `@AfterAll` 代替 `@AfterClass`

### **2. 参数化测试**

- JUnit 5 支持更灵活的参数化测试，可以从多种来源（如方法、CSV 文件）提供参数。

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class ParameterizedTestExample {

    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3, 5, 8})
    void testPositiveNumbers(int number) {
        assertTrue(number > 0);
    }
}
```

### **3. 新的断言和异常处理**

- JUnit 5 支持 **lambda 表达式**进行断言，更简洁。
- 使用 `assertThrows()` 检查异常。

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class ExceptionTest {

    @Test
    void testDivisionByZero() {
        assertThrows(ArithmeticException.class, () -> {
            int result = 1 / 0;
        });
    }
}
```

### **4. 更强的扩展机制**

- 通过 `@ExtendWith` 注解，JUnit 5 提供了灵活的扩展机制，方便与 Spring 等框架结合使用。

```java
import org.junit.jupiter.api.extension.ExtendWith;

@ExtendWith(CustomExtension.class)
public class ExtendedTest {
    // 测试逻辑
}
```

### **5. 支持动态测试**

- JUnit 5 支持**动态生成测试用例**，通过 `@TestFactory` 注解定义。

```java
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

import java.util.Arrays;
import java.util.Collection;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class DynamicTestExample {

    @TestFactory
    Collection<DynamicTest> dynamicTests() {
        return Arrays.asList(
            DynamicTest.dynamicTest("test1", () -> assertTrue(2 > 1)),
            DynamicTest.dynamicTest("test2", () -> assertTrue(3 > 2))
        );
    }
}
```

---

## 后记

在上述概念了解的基础上，后续，我们将进一步研究介绍如何在项目配置和使用JUnit5单元测试框架。

---

所有代码已上传至：[***https://github.com/lihongzheshuai/java-all-in-one***](https://github.com/lihongzheshuai/java-all-in-one)
