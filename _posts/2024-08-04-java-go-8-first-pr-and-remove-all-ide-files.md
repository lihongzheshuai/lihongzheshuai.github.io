---
layout: post
title: 一起学Java(8)-项目的第一个PR和将IDE相关文件移除版本控制
date: 2024-08-04 20:01 +0800
author: onecoder
comments: true
tags: [Java,Git,一起学Java]
categories: [Java,Git,一起学Java]
---
我们的[***java-all-in-one***](https://www.coderli.com/java-go-1-new-gradle-project/)项目的第一个PR比我预想的来的早了很多。感谢来自我的QQ群友(插播广告，欢迎大家加入[***Java技术交流群982860385***](https://qm.qq.com/q/Mrj1HGLl2E))的PR。今天就介绍一下这次PR和项目调整的主要内容。

<!--more-->

## 一、第一个PR

PR指的是Pull Request（拉取请求）。PR 是 GitHub 提供的一个功能，用于在协作开发中向他人展示自己所做的更改，并请求他们将这些更改合并到主代码库中。

本项目的第一个PR来自于一个群友的对于Gradle Wrapper源的修改请求。如图：

![gradle wrapper](/images/post/java-go-8/firstpr_2024-08-04_14-48-41.png)

该PR主要是修改了***gradle-wrapper.properties***文件，替换其中下载gradle包的源：

```properties
#Sun Jul 21 17:28:51 CST 2024
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
# distributionUrl=https\://services.gradle.org/distributions/gradle-8.9-bin.zip
distributionUrl=https\://mirrors.cloud.tencent.com/gradle/gradle-8.9-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

其实涉及镜像源的问题不止于此，比如Gradle需要使用的Maven中心库地址。本打算在进行依赖配置的时候进行说明，不过这个文件确实有所忽略，而且直接影响到大家下载并初始化项目的操作。现在处理很合理。

但由此却引出了另外一个问题：团队成员使用不同IDE协作时，比如该群友习惯使用VSCode进行Java开发，IDE相关的配置文件不应该纳入版本管理。

## 二、将IDE相关配置文件移除版本管理

之前还特意做过[.idea目录下配置文件的分析](https://www.coderli.com/java-go-6-project-config-files-intro-git-idea/)，当时默认以为群友应该基本都使用IntelliJ开发，没想到打脸来的如此之快。确实，仔细想想不论哪种情况，我认为这些文件都不应该纳入版本管理。因为有些配置文件是IntelliJ中自动生成的，我们只需要做好Gradle的配置管理就好。

那么如何`.idea`目录移除版本管理呢？即，在本地移除版本管理，不删除文件，在Github远端删除文件。操作步骤如下：

1. **从 Git 中删除文件**（仅从版本管理中移除，但保留本地文件）：

    ```bash
    git rm --cached -r .idea
    ```

    使用 `--cached` 选项，这样文件会从 Git 的版本控制中移除，但仍然保留在本地文件系统中。使用`-r`是因为.idea是目录。

2. **将*.idea*目录添加*.gitignore*文件**：

    ```properties
    ### IntelliJ IDEA ###
    .idea/
    ```

然后commit更改并推送到远端即可。

## 总结

今天的内容虽然有点像“番外篇”，但仔细看看你至少可以get到一个git的小操作，每天进步一点点，也是收获。
