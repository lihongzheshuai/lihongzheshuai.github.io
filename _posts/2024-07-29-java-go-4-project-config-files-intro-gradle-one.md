---
layout: post
title: 一起学Java(4)-java-all-in-one协作项目相关文件研究（Gradle篇-上）
date: 2024-07-29 11:10 +0800
author: onecoder
comments: true
tags: [Java,Gradle,一起学Java]
categories: [一起学Java系列,Gradle]
---
将思绪拉回[java-all-in-one](https://www.coderli.com/java-go-1-new-gradle-project/)项目，如果你[fork并下载了代码](https://github.com/lihongzheshuai/java-all-in-one)，你会看到在项目中除了HelloWorldMain代码外，还存在很多文件。如果你并不了解他们的作用并有足够的好奇心，那你应该想要知道他们的作用。带着好奇，今天我也来研究一下，先从Gradle相关的开始。

<!--more-->

# Gradle配置相关文件

## （一）settings.gradle.kts

`settings.gradle.kts` 是 Gradle 构建系统中的一个配置文件，用于配置和管理一个 Gradle 构建项目的设置。该文件是使用 Kotlin DSL 编写的（与 Groovy 编写的 `settings.gradle` 对应）。其作用如下：

### 1. 定义多项目构建结构

在多项目构建中，`settings.gradle.kts` 文件用于定义哪些子项目包含在构建中。通过 `include` 方法，可以指定子项目的名称。这是为了告诉Gradle哪些子项目是构建的一部分。

```kotlin
// 定义包含的子项目
include("projectA", "projectB")
```

- **作用**：明确指定需要构建的子项目。Gradle将根据这些子项目进行构建配置和依赖管理。
- **实际应用**：在大型项目中，通常会有多个模块（子项目），如应用模块、库模块等。通过 `include` 方法，可以将这些模块纳入同一个构建系统中，便于统一管理和构建。

### 2. 设置构建逻辑

在 `settings.gradle.kts` 文件中，可以设置一些全局的构建属性，例如项目的根名称。这些设置可以影响整个构建的行为。

```kotlin
// 设置根项目名称
rootProject.name = "MyMultiProject"
```

- **作用**：设置根项目的名称，以便在整个构建过程中统一使用。例如，生成的构建输出文件可能会使用这个名称。
- **实际应用**：为整个项目设置一个统一的名称，便于识别和管理。在多项目构建中，这样的设置有助于确保所有模块使用相同的根名称。

### 3. 配置插件管理

在 `settings.gradle.kts` 文件中，可以配置插件管理。通过 `pluginManagement` 块，可以指定插件仓库，确保在构建初始化阶段正确应用和管理插件。

```kotlin
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}
```

- **作用**：配置插件仓库，以便在构建过程中下载和使用所需的插件。这可以确保插件在构建开始时被正确解析和应用。
- **实际应用**：在使用多个插件的项目中，配置插件管理可以确保所有插件都来自可信的仓库，避免由于插件下载失败或版本不匹配而导致的构建问题。

### 4. 初始化脚本

在 `settings.gradle.kts` 文件中，可以执行一些初始化脚本或配置，以便在项目加载和配置之前进行一些预处理操作。

```kotlin
gradle.rootProject {
    beforeEvaluate {
        println("Initializing project: $name")
    }
}
```

- **作用**：在项目配置之前执行一些操作，例如打印日志、设置一些全局变量等。这样可以确保这些操作在项目真正开始构建之前完成。
- **实际应用**：在一些复杂项目中，可能需要在构建开始之前进行一些预处理工作，例如初始化环境变量、打印调试信息、设置动态属性等。这些操作可以通过初始化脚本来完成。

总体来看，`settings.gradle.kts` 主要用于定义多项目构建（multi-project build）的结构和配置。在多项目构建中，这个文件用于指定哪些子项目包含在构建中，并进行一些**全局**的初始化配置。
在我们的项目里，在初始化时只配置了根项目名称

```kotlin
// 设置根项目名称
rootProject.name = "java-all-in-one"
```

## （二）build.gradle.kts

主要用于定义**单个项目或子项目**的构建逻辑和任务。这个文件包含了项目的依赖、插件应用、任务配置等具体构建信息。

### 1. 插件应用

**作用**：

- 插件用于扩展Gradle的功能，提供特定领域的构建逻辑，例如支持Java、Kotlin、Android领域，支持编译Java、Kotlin代码或生成文档等。
- 通过应用插件，可以简化和规范项目的构建过程。

**示例**：

```kotlin
plugins {
    // 应用Java插件
    java

    // 应用Kotlin插件
    kotlin("jvm") version "1.5.21"
}
```

### 2. 项目依赖管理

**作用**：

- 依赖管理用于定义项目所需的外部库和模块。
- 通过配置依赖，Gradle会自动下载和配置这些库，从而简化开发和构建过程。

**示例**：

```kotlin
dependencies {
    // 引入Kotlin标准库
    implementation(kotlin("stdlib"))

    // 引入JUnit测试库
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.7.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.7.0")
}
```

### 3. 仓库配置

**作用**：

- 仓库配置用于指定依赖项的下载源，例如Maven Central、JCenter或自定义仓库。
- 通过配置仓库，Gradle可以从指定的源下载依赖项。

**示例**：

```kotlin
repositories {
    // 使用Maven Central仓库
    mavenCentral()

    // 使用JCenter仓库
    jcenter()
}
```

### 4. 任务定义

**作用**：

- 任务是Gradle构建的基本单位，定义了具体的构建操作，例如编译、测试、打包等。
- 可以创建自定义任务以满足特定需求。

**示例**：

```kotlin
tasks.register("hello") {
    // 定义一个简单的自定义任务
    doLast {
        println("Hello, Gradle!")
    }
}
```

### 5. 构建脚本块配置

**作用**：

- 构建脚本块用于配置项目的构建逻辑，例如编译选项、测试选项等。
- 可以根据项目需求进行自定义配置。

**示例**：

```kotlin
java {
    // 配置Java编译选项
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

kotlin {
    // 配置Kotlin编译选项
    jvmTarget = "11"
}
```

### 6. 配置构建生命周期

**作用**：

- 构建生命周期配置用于在特定阶段执行特定操作，例如在构建之前或之后执行某些任务。
- 可以通过钩子函数实现构建过程的定制化。

**示例**：

```kotlin
gradle.buildFinished {
    // 构建完成后执行的操作
    println("Build finished!")
}
```

### 综合示例

以下是一个完整的 `build.gradle.kts` 文件示例，包含了上述所有核心配置：

```kotlin
plugins {
    // 应用Java和Kotlin插件
    java
    kotlin("jvm") version "1.5.21"
}

repositories {
    // 配置仓库
    mavenCentral()
    jcenter()
}

dependencies {
    // 配置项目依赖
    implementation(kotlin("stdlib"))
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.7.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.7.0")
}

tasks.register("hello") {
    // 定义自定义任务
    doLast {
        println("Hello, Gradle!")
    }
}

java {
    // 配置Java编译选项
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

kotlin {
    // 配置Kotlin编译选项
    jvmTarget = "11"
}

gradle.buildFinished {
    // 构建完成后执行的操作
    println("Build finished!")
}
```

### 多项目构建配置文件结构

在Gradle的多项目构建中，每个子项目都可以有自己的 `build.gradle.kts` 配置文件。在多项目情况下，整体的配置文件结构如下：

```arduino
MyMultiProject/
├── build.gradle.kts      // 根项目的构建脚本
├── settings.gradle.kts   // 包含所有子项目的设置脚本
├── projectA/
│   └── build.gradle.kts  // 子项目A的构建脚本
└── projectB/
    └── build.gradle.kts  // 子项目B的构建脚本
```

其中，根项目通常也会有一个 `build.gradle.kts` 配置文件，但它的用途可能与子项目的 `build.gradle.kts` 略有不同。根项目的`build.gradle.kts` 文件主要用于定义全局配置、公用依赖和插件应用，或是定义适用于所有子项目的任务和配置。

1. 定义全局配置：
   - 配置所有子项目共享的仓库、插件和依赖管理。
   - 设置一些适用于所有子项目的通用属性和配置。

2. 管理子项目：
    - 通过 subprojects 块，可以对所有子项目进行统一配置。
    - 定义公共任务或在所有子项目中应用的插件。

例如：

```kotlin
plugins {
    kotlin("jvm") version "1.5.21" apply false
}

repositories {
    mavenCentral()
    jcenter()
}

subprojects {
    apply(plugin = "org.jetbrains.kotlin.jvm")

    repositories {
        mavenCentral()
    }

    dependencies {
        implementation(kotlin("stdlib"))
    }

    tasks.withType<Test> {
        useJUnitPlatform()
    }
}
```

## （三）其他说明

### 1. 为什么仓库配置和插件库配置分别放置在 **build.gradle.kts** 和 **settings.gradle.kts** 文件中？

不知道你看完了上面的介绍，是否有此疑惑。反正我是有的。因此特别梳理如下：在Gradle构建系统中，仓库配置和插件库配置分别放置在 `build.gradle.kts` 和 `settings.gradle.kts` 文件中，主要是因为它们在构建过程中的作用和时机不同。

#### 仓库配置在 **build.gradle.kts** 中原因

1. **依赖管理**：
   - 项目的依赖（如库和框架）通常是在 `build.gradle.kts` 文件中定义的。
   - 这些依赖需要从特定的仓库下载和解析，因此仓库配置放在 `build.gradle.kts` 中是合适的。

2. **构建时依赖解析**：
   - `build.gradle.kts` 文件中的仓库配置用于在构建过程中解析和下载项目所需的依赖。
   - 这些仓库可以是Maven Central、JCenter，或者是企业内部的私有仓库。

**示例**：

```kotlin
repositories {
    mavenCentral()
    jcenter()
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib:1.5.21")
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.7.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.7.0")
}
```

#### 插件库配置在 **settings.gradle.kts** 中原因

1. **构建初始化阶段**：
   - 插件管理在构建的初始化阶段进行，插件库配置需要在构建脚本执行之前进行解析。
   - `settings.gradle.kts` 文件在整个构建过程的最开始就被解析和执行，因此适合用于插件库的配置。

2. **全局插件管理**：
   - 插件可以应用到多个项目中，尤其是在多项目构建中，全局配置插件库可以确保所有项目都能访问这些插件。
   - `settings.gradle.kts` 文件中的 `pluginManagement` 块可以集中管理和配置插件库。

**示例**：

```kotlin
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

include("projectA", "projectB")
rootProject.name = "MyMultiProject"
```

这种配置方式确保了Gradle构建系统的灵活性和高效性，同时也简化了配置管理，使得构建过程更加清晰和可控。

# 总结

通过这些核心配置，你可以全面掌控Gradle构建脚本的功能和行为。这些配置不仅可以帮助你定义和管理项目的依赖，还可以通过插件扩展构建功能，定义自定义任务以满足特定需求，以及配置构建生命周期以实现构建过程的自动化和定制化。

为了避免篇幅过长，本文先重点介绍这两个最重要的配置文件.其实还有一个维度本文没有提及，在项目协作中，这些文件是否应该纳入Git版本管理，也就是是否应该全团队保持一致，根个人本地环境无关或在本地自动生成，显然这两个文件是应该纳入Git管理的。

后续，我们将继续对仓库中存在的其他Gradle相关文件进行研究说明，并判断其是否应该上传到Github之上，敬请期待。
