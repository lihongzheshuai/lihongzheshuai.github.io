---
layout: post
title: 一起学Java(19)-[测试篇]教你通过Gradle引入配置JUnit5
date: 2024-11-26 12:00 +0800
author: onecoder
comments: true
tags: [Java, 单元测试, Gradle, JUni5, 一起学Java]
categories: [一起学Java系列,（4）测试篇]
---
前文已详细介绍了JUnit框架的特点以及JUnit5和JUnit4版本的核心差异([***《一起学Java(17)-[测试篇]教你认识Java单元测试框架JUnit，JUnit5和JUnit4区别详解》***](https://www.coderli.com/java-go-17-test-junit-intro/))。本文将进入应用实战，详细介绍如何在Gradle项目中引入、配置和使用JUnit5测试框架。

<!--more-->

## 在Gradle项目中引入配置JUnit5框架

为了验证JUnit5相关功能，特意在`java-all-in-one`项目中增加了`one-test`子模块，用于验证单元测试相关框架的功能和使用方法。

### JUnit5 依赖配置

为引入JUnit框架，我们在`one-test`子模块的 `build.gradle.kts` 文件中，添加以下依赖项：

```kotlin
testImplementation("org.junit.jupiter:junit-jupiter")
```

此配置的作用是引入 JUnit Jupiter 的聚合工件（artifact），它包含了编写和运行 JUnit 5 测试所需的核心组件。 具体而言，`junit-jupiter` 包括以下模块：

- **`junit-jupiter-api`**：提供编写测试所需的注解和断言等 API。
- **`junit-jupiter-params`**：支持参数化测试功能。
- **`junit-jupiter-engine`**：JUnit Jupiter 的测试引擎，负责在运行时发现和执行测试。

通过引入 `junit-jupiter`，您无需单独添加上述各个模块的依赖，即可获得完整的 JUnit 5 测试功能。 这简化了依赖管理，确保您的项目具备编写和运行 JUnit 5 测试所需的所有组件。

但，你可能发现了上述配置项中并没有配置JUnit的版本号，根据[JUnit官方文档](https://junit.org/junit5/docs/current/user-guide)，建议通过配置***junit-bom***的方式，统一配置JUnit版本号。

```kotlin
dependencies {
    // JUnit 5 的 API 和运行时依赖
    testImplementation(platform("org.junit:junit-bom:${rootProject.ext["junitVersion"]}"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}
```

其中，变量`junitVersion`统一配置在根项目中的`build.gradle.kts`文件中。

```kotlin
allprojects {
    group = "com.coderli"
    version = "0.1"

    ext["log4j2Version"] = "2.23.1"
    ext["slf4jVersion"] = "2.0.16"
    ext["jacocoVersion"] = "0.8.12"
    ext["junitVersion"] = "5.11.3"
}
```

### 配置JUnit Platform执行测试

在`build.gradle.kts`添加配置，使用`JUnit Platform`执行测试

```kotlin
tasks.test {
    useJUnitPlatform()
}
```

`useJUnitPlatform()` 在 Gradle 中的作用是告诉 Gradle 使用 **JUnit Platform** 来执行测试。JUnit Platform 是 JUnit 5 的一个核心组件，它提供了一个统一的测试引擎，可以运行 JUnit 5 的测试（JUnit Jupiter 引擎）、兼容 JUnit 4 的测试（JUnit Vintage 引擎），以及其他兼容的测试引擎。

#### 具体定位作用

1. **指定测试引擎**：
   `useJUnitPlatform()` 指定了 Gradle 使用 JUnit Platform 来执行测试，而不是使用默认的 JUnit 4 测试引擎。
   - **JUnit 4 默认行为**：如果不配置 `useJUnitPlatform()`，Gradle 默认会使用 JUnit 4 来运行测试。
   - **JUnit 5 行为**：配置 `useJUnitPlatform()` 后，Gradle 会启动 JUnit Platform 引擎，允许执行 JUnit 5 测试（JUnit Jupiter 引擎）。

2. **支持多种测试引擎**：
   JUnit Platform 是一个统一的接口，它支持不同的测试引擎，包括：
   - **JUnit Jupiter**：这是 JUnit 5 的核心测试引擎，支持 JUnit 5 的所有特性（如新的注解、生命周期方法等）。
   - **JUnit Vintage**：兼容 JUnit 3 和 JUnit 4 的测试引擎。如果你的项目中有 JUnit 3 或 JUnit 4 的测试用例，JUnit Vintage 可以用来执行这些老版本的测试。

3. **支持其他第三方测试引擎**：
   JUnit Platform 还允许集成其他测试引擎，例如：
   - **TestNG**
   - **Spock**
   - **Cucumber**（用于行为驱动开发测试）

4. **自动发现测试**：
   配置了 `useJUnitPlatform()` 后，JUnit Platform 会自动发现测试类并执行。它支持通过注解（如 `@Test`）和其他元数据（例如条件化执行）来标识和选择测试。

#### 如果不配置 `useJUnitPlatform()`

- **默认使用 JUnit 4**：Gradle 默认使用 JUnit 4 引擎运行测试。
- **JUnit 5 测试不被识别**：如果你使用了 JUnit 5 的特性，但没有配置 `useJUnitPlatform()`，Gradle 会忽略这些 JUnit 5 测试，无法执行。

如此，便完成了JUnit5单元测试框架的引入。

{% include custom/custom-post-content-inner.html %}

---

## 在Gradle项目中使用JUnit5框架

### 执行测试用例

在`one-test`子模块中，添加JUnit单元测试样例代码

**被测试类：**

```java
package com.coderli.one.test.junit;

public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int divide(int a, int b) {
        if (b == 0) throw new ArithmeticException("Division by zero");
        return a / b;
    }
}
```

**单元测试代码：**

```java
package com.coderli.one.test.jacoco;

import com.coderli.one.test.junit.Calculator;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class CalculatorTest {

    @Test
    void testAdd() {
        Calculator calculator = new Calculator();
        int result = calculator.add(2, 3);
        assertEquals(5, result, "Addition result should be 5");
    }

    @Test
    void testDivisionByZero() {
        Calculator calculator = new Calculator();
        assertThrows(ArithmeticException.class, () -> calculator.divide(1, 0));
    }
}
```

在根项目中运行命令，统一执行项目中所有单元测试代码

```console
 .\gradlew.bat test 
```

控制台输出如下告警

```console
The automatic loading of test framework implementation dependencies has been deprecated. This is scheduled to be removed in Gradle 9.0. Declare the desired test framework directly on the test suite or explicitly declare the test framework implementation dependencies on the test's runtime classpath. Consult the upgrading guide for further information: https://docs.gradle.org/8.10.2/userguide/upgrading_version_8.html#test_framework_implementation_dependencies
```

上述错误信息的是指，在Gradle 9.0中，自动加载测试框架实现依赖项的功能将被移除。为避免此问题，请直接在测试套件中声明所需的测试框架，或者在测试的运行时类路径上明确声明测试框架实现依赖项。更多信息请参考升级指南：[https://docs.gradle.org/8.10.2/userguide/upgrading_version_8.html#test_framework_implementation_dependencies](https://docs.gradle.org/8.10.2/userguide/upgrading_version_8.html#test_framework_implementation_dependencies)

为解决次问题，在`one-test`的`build.gradle.kts`文件中配置指定的JUnit Platform

```kotlin
dependencies {
    // JUnit 5 的 API 和运行时依赖
    testImplementation(platform("org.junit:junit-bom:${rootProject.ext["junitVersion"]}"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
```

再次执行，错误消失。

```console
 .\gradlew.bat test 
 ```

控制台输出成功结果

```console
BUILD SUCCESSFUL in 10s
12 actionable tasks: 11 executed, 1 up-to-date
```

### 查看结果报告

在 Gradle 中执行 JUnit 5 测试时，测试的执行结果会生成报告。Gradle 提供了不同格式的报告，通常包括文本报告、HTML 报告和JUnit XML 格式的报告。

Gradle 默认会在 `build/reports/tests/test` 目录下生成测试报告，测试结果会包含以下几种格式：

1. **HTML报告**：适合通过浏览器查看的格式，显示图形化的测试结果。
2. **JUnit XML报告**：用于持续集成工具（如 Jenkins）处理的格式。

#### **查看 HTML 测试报告**

   测试执行完毕后，你可以在项目的 `build/reports/tests/test/` 目录下找到 `index.html` 文件。使用浏览器打开这个文件，即可查看详细的图形化测试结果。

![JUnit5 Report Demo](/images/post/java-go-19/junit5-report.png)

#### **查看 JUnit XML 报告**

   Gradle 还会生成一个 JUnit XML 格式的报告，这对于持续集成工具（如 Jenkins）非常有用。XML 报告默认位于：

   ```console
   <project-root>/build/test-results/test/
   ```

   这里会生成一个或多个以 `TEST-` 开头的 XML 文件，每个文件对应一次测试运行。

这些报告帮助你了解测试的执行情况，并在需要时进行详细的分析和调试。

至此，我们已经完成了 JUnit 5 测试配置和测试执行，为我们的项目引入了JUnit 5测试框架。

---

所有代码已上传至：[***https://github.com/lihongzheshuai/java-all-in-one***](https://github.com/lihongzheshuai/java-all-in-one)
