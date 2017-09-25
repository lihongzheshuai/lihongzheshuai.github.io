---
layout: post
title: 《Gradle user guide》翻译 — 7.3 多工程Java构建
date: 2013-09-24 22:38 +0800
author: onecoder
comments: true
tags: [Gradle]
thread_key: 1517
---
现在我们来看一个典型的多项目构建的例子。下面是工程的布局：

样例7.10 多项目构建 - 分层布局

构建结构

```
multiproject/
 api/
 services/webservice/
 shared/
```

> 注意：本样例的代码可以在Gradle完整安装包的samples/java/multiproject目录下找到

这里我们有三个工程。api工程生成用于Java客户端访问XML webservice服务的JAR包。webservice工程是一个web应用，用于返回XML信息。shared工程包含了api和webservice工程共同使用的代码。

## 7.3.1 定义一个多项目构建

为了定义一个多项目构建，你需要创建一个配置文件(settings file)。该配置文件存放在源码树的根目录，指定了哪些项目需要包含在构建任务之中。该配置文件必须命名位settings.gradle。在本例中，我们使用一个简单的层次布局。下面是相关的配置文件：

样例7.11 多项目构建 - settings.gradle 文件

```groovy
include "shared", "api","services:webservice", "services:shared"
```

更多关于配置文件的信息，可在第56章的多项目构建中找到。

## 7.3.2 常用配置

对于大多数的多项目构建来说，有一些对所有项目都常用的配置。在我们的样例中，我们使用一种叫做配置注入的技术，将这些通用配置定义在根项目中。这里，根项目就像一个容易，子项目在这种情况下覆盖了该容器中的元素 - 并注入了特殊的配置。这样，我们可以轻松的给所有归档定义清单内容和一些通用的依赖:

样例7.12 多项目构建 - 通用配置

```groovy
subprojects {
    apply plugin: 'java'
    apply plugin: 'eclipse-wtp'
    repositories {
       mavenCentral()
}
    dependencies {
        testCompile 'junit:junit:4.11'
}
    version = '1.0'
    jar {
        manifest.attributes provider: 'gradle'
} }
```

注意到，我们的样例对每个子项目都应用Java插件。这意味着我们在之前部分看过的任务和配置属性对每个子项目都是可用的。因此，你可以通过在项目根路径执行gradle build命令给所有的工程进行编译，测试并打成JAR包。

## 7.3.3 项目间依赖

你可以在同一个构建中增加项目间的依赖，例如，一个项目的JAR包被用于另一个项目的编译。在api项目的构建文件中，我们将增加一个对shared工程JAR包的依赖。由于这个依赖的存在，Gradle将会确保shared工程总是在api项目之前先进行构建。

样例7.13 多项目构建 - 项目间依赖

```groovy
dependencies {
    compile project(':shared')
}
```

关于如何关闭该功能，可参见第56.7.1章节的"关闭依赖项目的构建"部分。

## 7.3.4 创建一个分支

我们可以增加一个分支，用于打包给客户端使用：

样例7.14 多项目构建 - 分支文件

```groovy
task dist(type: Zip) {
    dependsOn spiJar
    from 'src/dist'
    into('libs') {
        from spiJar.archivePath
        from configurations.runtime
    }
}
artifacts {
   archives dist
}
```