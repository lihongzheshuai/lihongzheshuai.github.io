---
layout: post
title: 一起学Java(5)-java-all-in-one协作项目相关文件研究（Gradle篇-下）
date: 2024-07-30 17:01 +0800
author: onecoder
comments: true
tags: [Java,Gradle,一起学Java]
categories: [Java,Gradle,一起学Java]
---
接上篇《[一起学Java(4)-java-all-in-one协作项目相关文件研究（Gradle篇-上）](https://www.coderli.com/java-go-4-project-config-files-intro-gradle-one/)》，本文继续研究项目中Gradle相关文件。

<!--more-->

# Gradle配置相关文件

## （一）gradle.properties

`gradle.properties` 文件在Gradle构建系统中扮演着配置属性存储的角色。它用于定义一些全局的、项目级别的或用户级别的配置属性（键值对），这些属性可以在构建脚本和插件中使用。以下是一些常见的场景举例：

1. **JVM 内存设置**：
   - 通过 `gradle.properties` 文件可以配置JVM的内存设置，确保Gradle在构建过程中有足够的内存。

     ```properties
     org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m
     ```

2. **并行构建**：
   - 可以启用并行构建，以提高构建速度，特别是在多项目构建中。

     ```properties
     org.gradle.parallel=true
     ```

3. **守护进程配置**：
   - 配置Gradle守护进程，以加快后续的构建速度。

     ```properties
     org.gradle.daemon=true
     ```

4. **项目版本控制**：
   - 可以在 `gradle.properties` 文件中定义项目的版本号，供构建脚本使用。

     ```properties
     version=1.0.0
     ```

5. **自定义属性**：
   - 用户可以在 `gradle.properties` 文件中定义自定义属性，并在 `build.gradle.kts` 文件中引用这些属性。

     ```properties
     myCustomProperty=customValue
     ```

   - 在 `build.gradle.kts` 中引用：

     ```kotlin
     println("Custom Property: ${property("myCustomProperty")}")
     ```

场景绝不局限于上面提到的几种，比如在我们之前初始化项目调试的过程中就配置了警告日志的打印配置：

```properties
org.gradle.warning.mode=all
```

因此，更多的配置参数需要你在后续应用中慢慢的学习摸索。

### 作用范围

从作用域上来看`gradle.properties` 文件主要有两种作用域：**全局级别和项目级别**。

全局级别的 `gradle.properties`位于用户主目录下的 `.gradle` 目录中。

**示例路径**：

- Windows: `C:\Users\<Your Username>\.gradle\gradle.properties`
- Linux/Mac: `~/.gradle/gradle.properties`

项目级别的`gradle.properties`位于项目根目录下。项目文件中的配置优先级高于全局配置。如果同一个属性在项目级别和全局级别的 `gradle.properties` 文件中都有定义，则项目级别的配置将覆盖全局级别的配置。

例如，假设我们有以下全局配置：

```properties
# 全局gradle.properties（~/.gradle/gradle.properties）
org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m
org.gradle.daemon=true
```

在某个项目中，我们有以下项目级别配置：

```properties
# 项目级别gradle.properties（项目根目录下）
org.gradle.jvmargs=-Xmx4096m
```

在这种情况下，`org.gradle.jvmargs` 属性将使用项目级别的配置（`-Xmx4096m`），而 `org.gradle.daemon` 属性将使用全局配置（`true`）。

### 小结

`gradle.properties` 文件在Gradle构建系统中用于定义和存储全局配置属性和项目级别配置属性，这些属性在构建过程中被引用和使用，提供了一个灵活的方式来管理构建配置。通过合理使用 `gradle.properties` 文件，可以使构建脚本更加简洁和易于维护，同时提高构建过程的灵活性和可配置性。

# Gradle Wrapper及其相关文件

## (二) gradlew 、gradlew.bat和gradle文件夹

在团队协作项目中，使用`Gradle Wrapper`而不是本地的`Gradle`包是一种最佳实践。`Gradle Wrapper`确保版本一致性、简化了开发环境设置、增强了构建过程的可靠性，并且支持CI/CD环境中的一致构建。通过使用`Gradle Wrapper`，团队可以避免版本冲突，提高构建过程的稳定性和可维护性。

`gradlew` 和 `gradlew.bat` 以及`gradle`文件夹和其下面的文件都是Gradle Wrapper的一部分，文件位于项目根目录中，是Gradle构建工具的可执行脚本。这两个文件分别适用于Unix/Linux/macOS和Windows环境。

Gradle Wrapper也是由以上几个文件组成，具体介绍如下：

  - `gradlew`：Unix/Linux/macOS环境的可执行脚本。
  - `gradlew.bat`：Windows环境的可执行批处理脚本。
  - `gradle/wrapper/gradle-wrapper.jar`：Gradle Wrapper的二进制文件。
  - `gradle/wrapper/gradle-wrapper.properties`：Gradle Wrapper的配置文件。用于配置Gradle Wrapper的行为，特别是指定要使用的Gradle版本和下载位置。确保项目使用一致版本的Gradle构建工具。

`gradle-wrapper.properties`**常见配置项**如下：

- `distributionBase`：指定Gradle分发包(解压后)的基目录。
- `distributionPath`：指定存储Gradle分发包(解压后)的相对路径。
- `zipStoreBase`：指定下载的Gradle分发包的基目录。
- `zipStorePath`：指定存储下载的Gradle分发包的相对路径。
- `distributionUrl`：指定要下载的Gradle分发包的URL。
- `distributionSha256Sum`（可选）：指定下载的Gradle分发包的SHA-256校验和。
- `distributionType`（可选）：指定分发包的类型（`bin` 或 `all`）。

**本项目(java-all-in-one)示例**：

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.9-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists

```

其中：`GRADLE_USER_HOME` 是Gradle的用户主目录，用于存储Gradle的全局配置、缓存、依赖项和Wrapper分发包等。默认情况下，GRADLE_USER_HOME 的值是用户主目录下的 .gradle 目录。如：

```text
Windows：C:\Users\<Your Username>\.gradle
Linux/Mac：/home/<Your Username>/.gradle 或 /Users/<Your Username>/.gradle
```

可以通过设置环境变量 GRADLE_USER_HOME 来改变默认位置。

一般在项目下目录结构如下(我们的项目也与此一致)：

```arduino
MyProject/
├── gradlew
├── gradlew.bat
├── build.gradle.kts
├── settings.gradle.kts
└── gradle/
    └── wrapper/
        ├── gradle-wrapper.jar
        └── gradle-wrapper.properties
```

**最后一个问题，以上文件是否应该纳入Git版本管理？**
根据上面的分析，显然是应该纳入版本管理的，以保证团队的一致性。业界的实践也是如此的，这从我们初始化项目后，工具自动配置的`.gitignore`文件配置即可看出。具体原因分析如下：

1. **版本一致性**：
   - 确保所有开发人员使用相同版本的Gradle构建工具，无论他们的本地环境中安装了哪个版本的Gradle。
   - 避免因为Gradle版本不一致而导致的构建问题。

2. **便捷性**：
   - 开发人员不需要手动安装Gradle，只需使用Wrapper脚本，即可自动下载并使用指定版本的Gradle。
   - 简化项目的设置和配置过程。

3. **自动化构建**：
   - 在CI/CD环境中，使用Gradle Wrapper可以确保构建环境中使用指定版本的Gradle，从而保证构建过程的一致性和可靠性。

# 总结

至此，项目中Gradle相关的配置文件已基本介绍完成了。还剩余`.gitignore`文件和一些idea相关的文件，我们下次再仔细学习研究。