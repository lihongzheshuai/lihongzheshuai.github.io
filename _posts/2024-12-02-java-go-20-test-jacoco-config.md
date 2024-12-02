---
layout: post
title: 一起学Java(20)-[测试篇]教你通过Gradle配置和使用JaCoCo单元测试覆盖率检查工具
date: 2024-12-02 11:30 +0800
author: onecoder
comments: true
tags: [Java, 单元测试, Gradle, JaCoCo, 一起学Java]
categories: [一起学Java系列,（4）测试篇]
---
在[***《一起学Java(19)-[测试篇]教你通过Gradle配置和使用JUnit5》***](https://www.coderli.com/java-go-19-test-junit5-config/)中，我们引入了JUnit5单元测试框架。在进行单元测试时，我们不仅要关注测试的正确性和完整性，还要关注测试的覆盖率。覆盖率反映了测试用例对代码的覆盖程度，能够帮助我们发现潜在的测试盲区，确保代码的每个部分都得到了适当的验证。

为了更好地分析代码覆盖率，我们可以使用像 JaCoCo 这样的工具，它可以自动生成详细的覆盖率报告，帮助开发者直观地查看哪些代码已经被测试覆盖，本文将详细介绍如何在 Gradle 项目中集成 JaCoCo 以及如何生成代码覆盖率报告。

<!--more-->

## 什么是JaCoCo

JaCoCo 是一个强大的 Java 代码覆盖率工具，可以帮助开发者评估单元测试的覆盖范围，以便更好地保证代码的质量。JaCoCo 支持多种类型的代码覆盖率指标，常见的包括：

- 行覆盖率（Line Coverage）：评估代码中每一行是否被测试用例执行过。如果某行代码没有被执行，报告中会明确指出。
- 分支覆盖率（Branch Coverage）：检查代码中每个条件语句的每个分支（例如 if-else 语句）是否都被执行。这个指标对于验证条件逻辑特别重要。
- 方法覆盖率（Method Coverage）：检查每个方法是否被调用过。方法覆盖率通常用于评估函数级别的测试覆盖情况。
- 类覆盖率（Class Coverage）：评估每个类是否被测试执行过

## 在 Gradle 项目中配置 JaCoCo

首先，在 `build.gradle.kts` 文件中添加 JaCoCo 插件：

```kotlin
plugins {
    id("jacoco")// 添加 JaCoCo 插件
}
```

JaCoCo 插件默认包含在 Gradle 的插件库中，在 Gradle 中，**插件**（Plugins）的作用是为构建过程提供特定的功能，简化构建配置，增强构建脚本的可重用性和可扩展性。插件可以帮助你集成特定的工具或框架，自动化执行常见的任务，提升构建效率。其主要作用如下：

1. **提供功能**：插件是 Gradle 构建中核心的扩展机制。每个插件通常会向 Gradle 提供一组任务（tasks）和功能（功能模块）。比如，配置 `jacoco` 插件后，Gradle 会自动处理与 JaCoCo 相关的任务，并包含 JaCoCo 所需的依赖。
2. **简化配置**：使用插件后，很多常见的构建任务可以通过简单的配置来自动化处理，无需手动编写冗长的构建脚本。例如，启用`jacoco`插件后，你可以简单地配置报告路径，而不需要额外编写代码来实现覆盖率的收集和报告生成。
3. **提高可维护性**：插件封装了特定的构建逻辑，使得你的构建脚本更加简洁，且可以集中管理构建逻辑。比如，使用插件时，插件的功能通常会进行版本控制，减少了不同开发者或不同项目间的配置不一致问题。
4. **扩展性**：Gradle 本身是高度可扩展的，你可以根据需要选择官方插件、第三方插件，或者自定义插件。通过插件，Gradle 可以集成大量工具（如构建工具、代码质量工具、持续集成工具等）。

可以进一步配置 JaCoCo的版本以及生成报告的具体需求，例如报告的格式和路径。

```kotlin
jacoco {
    toolVersion = "0.8.12"  // 可以指定 JaCoCo 工具版本
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)  // 确保在运行测试之后生成报告

    reports {
        xml.required.set(true)  // 启用 XML 格式报告
        html.required.set(true)  // 如果不需要 HTML 格式报告，可以禁用
    }
}
```

在上述配置中，我们将 JaCoCo 的版本设置为 `0.8.12`，并指定生成 XML 和 HTML 格式的报告。HTML 报告用于可视化的检查，XML 报告用于集成其他工具（例如 SonarQube）来进行进一步的代码分析。

## 生成代码覆盖率报告

本项目使用Gradle Wrapper，通过以下命令运行测试并生成 JaCoCo 报告：

```bash
gradlew jacocoTestReport
```

- 根据配置，在运行`jacocoTestReport`任务前，会先运行`test` 任务执行所有的单元测试。
- `jacocoTestReport` 任务生成代码覆盖率报告。

### 查看代码覆盖率报告

执行上述命令后，代码覆盖率报告会保存在以下目录：

- **HTML 报告**： `build/reports/jacoco/test/html/index.html`。你可以打开这个 HTML 文件来查看覆盖率报告。
- **XML 报告**： `build/reports/jacoco/test/test.exec`。此报告可用于自动化工具进一步处理。

HTML 报告提供了直观的界面来展示哪些代码行和分支被测试覆盖，哪些没有覆盖，使得开发者可以轻松找到测试盲区。

![JaCoCo Report](/images/post/java-go-20/jacoco-report.png)

## 代码覆盖率阈值设置

为了确保代码的测试覆盖率达到一定标准，可以设置覆盖率阈值，若未达到要求，构建将失败。这可以保证团队中的所有成员遵守相同的代码质量标准。

在 `build.gradle.kts` 中配置覆盖率检查：

```kotlin
tasks.jacocoTestCoverageVerification {
    dependsOn(tasks.jacocoTestReport)
    violationRules {
        rule {
            limit {
                counter = "CLASS"
                value = "COVEREDRATIO"
                minimum = "0.80".toBigDecimal()  // 设置类级别的覆盖率阈值
            }
        }
        rule {
            limit {
                counter = "METHOD"
                value = "COVEREDRATIO"
                minimum = "0.80".toBigDecimal()  // 设置方法级别的覆盖率阈值
            }
        }
        rule {
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = "0.80".toBigDecimal()  // 设置行级别的覆盖率阈值
            }
        }
    }
}
```

通过上述配置，当代码覆盖率低于 80% 时，构建会失败，如：

```console
Execution failed for task ':one-test:jacocoTestCoverageVerification'.
> Rule violated for bundle one-test: classes covered ratio is 0.33, but expected minimum is 0.80
  Rule violated for bundle one-test: methods covered ratio is 0.37, but expected minimum is 0.80
  Rule violated for bundle one-test: lines covered ratio is 0.05, but expected minimum is 0.80
```

## 在 CI/CD 中集成 JaCoCo

通常，代码覆盖率是 CI/CD 管道中的重要部分。例如，在 Jenkins 或 GitLab CI 中集成 JaCoCo，可以实现自动化测试和报告生成。

在 CI/CD 环境中，运行以下命令：

```bash
gradlew clean build jacocoTestReport
```

在生成覆盖率报告后，你可以将 XML 文件作为输入给代码质量工具，如 SonarQube，来进行全面的质量分析。

## 总结

至此，我们已初步完成JaCoCo覆盖率检查工具的配置和基本使用介绍。从另一个侧面，我们也初步了解了这些工具在 `Jenkins` 或 `GitLab CI` 中集成 `JaCoCo`自动调用和阈值检查和门禁校验的原理。

---

所有代码已上传至：[***https://github.com/lihongzheshuai/java-all-in-one***](https://github.com/lihongzheshuai/java-all-in-one)
