---
layout: post
title: Gradle打包可执行Jar
tags: [gradle,executable,jar,plugins]
date: 2016-03-03 09:24:56 +0800
comments: true
thread_key: 1877
---

为自己快速写博客开发的yami程序初稿基本完成了。需要打成jar通过命令行快速调用。具体可看Readme。

项目地址：[https://github.com/lihongzheshuai/yami
](https://github.com/lihongzheshuai/yami
)

搜了一下Gradle 打包executable jar的方法，确实如一个文章里所说，网上都会提到一个plugin，但是他试了却不好用，他好奇到底是谁转载谁的。
<!--break-->
其实我也先试用了那个plugin，抱歉名字我记不住了，在那个plugin的主页上推荐了另外一个plugin:capsule

主页地址：[https://github.com/danthegoodman/gradle-capsule-plugin](https://github.com/danthegoodman/gradle-capsule-plugin)

配置方式很简单，对于gradle 2.1后的版本，只需要在build脚本开通添加：

```groovy
 plugins {
     id "us.kirchmeier.capsule" version "1.0.2"
 }
```

老版本的话：

```groovy
 buildscript {
   repositories {
     maven {
       url "https://plugins.gradle.org/m2/"
     }
   }
   dependencies {
     classpath "us.kirchmeier:gradle-capsule-plugin:1.0.0"
   }
 }

 apply plugin: "us.kirchmeier.capsule"
```

然后定义一个Task即可：

```groovy
 task simpleCapsule(type: FatCapsule){
   applicationClass 'com.foo.SimpleCalculator

   baseName 'SimpleCalculator'
 }
```

最后通过执行simpleCapsule Task即可打出可执行的Jar。
