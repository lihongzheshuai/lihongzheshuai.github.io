---
layout: post
title: 一起学Java(21)-[配置篇]Gradle控制台乱码问题配置和解决
date: 2024-12-17 23:00 +0800
author: onecoder
comments: true
tags: [Java, Gradle, 一起学Java]
categories: [一起学Java系列,（5）配置篇]
---
在[***《一起学Java(18)-[配置篇]一个诡异(有趣)的Gradle Wrapper问题》***](https://www.coderli.com/java-go-18-gradle-wrapper-problem/)中，我们解决了一个有趣的Gradle Wrapper使用问题，这次我们在研究Java String编码的时候，又遇到了Gradle使用中的控制台乱码问题，遂记录并分享问题的现象和解决的过程。

<!--more-->

## 问题现象

为了研究Java中关于String的编码实现原理和码点的使用，我在项目中加入了如下的代码:

```java
package com.coderli.one.jdk.common;

public class StringCodeDemo {
    public static void main(String[] args) {
        String str = "Hello, 😀!";

        // 获取字符串长度
        System.out.println("字符串的长度（字符数）：" + str.length()); // 8

        // 使用 codePointAt 来处理完整字符
        System.out.println("字符 '😀' 的 Unicode 码点：" + str.codePointAt(7)); // 128512 (U+1F600)

        // 遍历字符串中的每个字符（注意代理对会被分开）
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            System.out.println("字符 " + c + " 的编码是：" + (int)c);
        }

        // 使用 codePointAt 获取完整的Unicode码点
        for (int i = 0; i < str.length(); ) {
            int codePoint = str.codePointAt(i);
            System.out.println("Unicode 码点: " + codePoint); // 会显示 U+1F600
            i += Character.charCount(codePoint); // 处理代理对
        }
    }
}
```

通过Gradle编译运行后，控制台输出乱码如下：

```console
22:41:14: Executing ':one-jdk:com.coderli.one.jdk.common.StringCodeDemo.main()'…

Starting Gradle Daemon...
Gradle Daemon started in 1 s 146 ms
> Task :one-jdk:compileJava UP-TO-DATE
> Task :one-jdk:processResources NO-SOURCE
> Task :one-jdk:classes UP-TO-DATE

> Task :one-jdk:com.coderli.one.jdk.common.StringCodeDemo.main()
�ַ����ĳ��ȣ��ַ�������10
�ַ� '?' �� Unicode ��㣺128512
�ַ� H �ı����ǣ�72
�ַ� e �ı����ǣ�101
�ַ� l �ı����ǣ�108
�ַ� l �ı����ǣ�108
�ַ� o �ı����ǣ�111
�ַ� , �ı����ǣ�44
�ַ�   �ı����ǣ�32
�ַ� ? �ı����ǣ�55357
�ַ� ? �ı����ǣ�56832
�ַ� ! �ı����ǣ�33
Unicode ���: 72
Unicode ���: 101
Unicode ���: 108
Unicode ���: 108
Unicode ���: 111
Unicode ���: 44
Unicode ���: 32
Unicode ���: 128512
Unicode ���: 33

BUILD SUCCESSFUL in 5s
2 actionable tasks: 1 executed, 1 up-to-date
22:41:20: Execution finished ':one-jdk:com.coderli.one.jdk.common.StringCodeDemo.main()'.
```

而若修改IDEA配置，改为由IDEA内置的编译器进行编译和运行，控制台输出正常：

![IDEA Setting](/images/post/java-go-21/java-build-and-run.png)

```console
D:\SoftwareInstall\jdk-22_windows-x64_bin\jdk-22.0.2\bin\java.exe -javaagent:D:\SoftwareInstall\ideaIC\lib\idea_rt.jar=11882:D:\SoftwareInstall\ideaIC\bin -Dfile.encoding=UTF-8 -Dsun.stdout.encoding=UTF-8 -Dsun.stderr.encoding=UTF-8 -classpath D:\MyCode\java-all-in-one\one-jdk\out\production\classes com.coderli.one.jdk.common.StringCodeDemo
字符串的长度（字符数）：10
字符 '😀' 的 Unicode 码点：128512
字符 H 的编码是：72
字符 e 的编码是：101
字符 l 的编码是：108
字符 l 的编码是：108
字符 o 的编码是：111
字符 , 的编码是：44
字符   的编码是：32
字符 ? 的编码是：55357
字符 ? 的编码是：56832
字符 ! 的编码是：33
Unicode 码点: 72
Unicode 码点: 101
Unicode 码点: 108
Unicode 码点: 108
Unicode 码点: 111
Unicode 码点: 44
Unicode 码点: 32
Unicode 码点: 128512
Unicode 码点: 33

Process finished with exit code 0
```

## 解决方法

出现乱码自然是编码不匹配，IDEA中的控制台使用的UTF-8编码，但是Gradle中的控制台使用的是系统默认的GBK编码，这就导致了乱码的问题。

解决方法：网上查到的方法大多都说在`gradle.properties`文件中添加配置:

```properties
org.gradle.jvmargs=-Dfile.encoding=UTF-8
```

在我的项目中测试无效，且从配置选项的字面意思来看应该也不是处理控制台的编码的配置。

参考IDEA编辑器输出中的信息，我在`build.gradle.kts`文件中添加了下面的配置：

```kotlin
    tasks.withType<JavaExec> {
        // 设置 Java 进程的编码为 UTF-8
        systemProperty("file.encoding", "UTF-8")
        systemProperty("sun.stdout.encoding", "UTF-8")
        systemProperty("sun.stderr.encoding", "UTF-8")
    }
```

这样配置后，Gradle的控制台输出正常。根据配置项字面意思猜测，实际对控制台正常输出编码起作用的选项应该是

```kotlin
    tasks.withType<JavaExec> {
        // 设置 Java 进程的编码为 UTF-8
        systemProperty("sun.stdout.encoding", "UTF-8")
    }
```

只保留该选项再次运行，控制台输出正常，问题解决。

---

所有代码已上传至：[***https://github.com/lihongzheshuai/java-all-in-one***](https://github.com/lihongzheshuai/java-all-in-one)
