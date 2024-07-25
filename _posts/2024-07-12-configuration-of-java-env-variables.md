---
layout: post
title: 给Java初学者-Java环境变量的本质和配置方法（Windows、Linux）
date: 2024-07-12 10:57 +0800
author: onecoder
comments: true
tags: [Java,windows,linux]
thread_key: 202407121058
---
经常遇到初学者问到关于Java环境变量配置的问题，基本围绕在集中情况：（1）环境变量要配哪些；（2）2024年了还需不需要配；（3）为啥我这个没配、那个没配也好用。会不会有什么影响。今天我就展开讲讲关于Java环境变量的定位和本质。
在配置 Java 环境变量时，主要涉及两个重要的变量：JAVA_HOME 、 PATH和一个目前可能不太重要的CLASSPATH。
<!--more-->
# Java 环境变量的本质
Java环境变量的本质就是操作系统的环境变量。在操作系统中，环境变量是存储在操作系统中的一组键值对，用于配置操作系统和应用程序的运行环境。如：变量名"AAA"值对应为"123"。配置后，任何程序从系统层面读取变量AAA，就会获取到值123。

# Java 环境变量的类型和定位
在配置 Java 环境变量时，主要涉及两个重要的变量JAVA_HOME 、 PATH以及一个可能存在的CLASSPATH变量
1. JAVA_HOME 变量：
    - JAVA_HOME 是一个环境变量，指向 JDK 的安装目录。很多 Java 开发工具和框架（如 Maven、Gradle、Tomcat 等）使用 JAVA_HOME 来定位 JDK。
    - 它确保所有工具使用同一个 JDK，避免版本不一致的问题。
    也就是说，如果其他工具和框架不使用的这个系统级别的环境，则无需配置，该变量不影响java、javac命令的使用。
2. PATH 变量：
    - PATH 环境变量决定了操作系统在执行命令时搜索可执行文件的目录，这个是系统定义的规范，所有程序都要遵守。
    - 通过将 JAVA_HOME/bin 添加到 PATH 中，操作系统可以在任意目录下找到 java、javac 等命令，从而方便执行 Java 应用程序和编译 Java 源代码。
3. CLASSPATH 变量：
    - CLASSPATH是一个重要的 Java 环境变量，它指定了 Java 运行时和编译器查找类文件和包的路径。
    - 当 JVM 启动一个应用程序时，它会使用 CLASSPATH 中指定的路径查找所需的类文件（.class 文件）。CLASSPATH 可以包括目录和 JAR 文件。JVM 会在这些路径中搜索类。
    - 大多数现代 Java 项目使用构建工具如 Maven、Gradle 或其他类似工具，这些工具自动管理项目的依赖和类路径，无需手动设置 CLASSPATH。
  
# Java 环境变量配置方法
## Windows 系统
1. 设置 JAVA_HOME：
    - 右键点击“此电脑”或“我的电脑”，选择“属性”。
    - 点击“高级系统设置”。
    - 在“系统属性”对话框中，点击“环境变量”按钮。
    - 在“系统变量”区域，点击“新建”按钮，输入以下内容：
        - 变量名：JAVA_HOME
        - 变量值：JDK 的安装路径（例如：C:\Program Files\Java\jdk-22）
2. 更新 PATH 变量：
    - 在同一“系统变量”区域，找到并选择 Path 变量，点击“编辑”。
    - 点击“新建”并添加以下路径：%JAVA_HOME%\bin
    - 确保新路径添加到已有的路径列表中。

## macOS 和 Linux 系统
在 Linux 系统中，环境变量可以在多个位置进行设置，具体取决于变量的作用范围（全局系统范围、特定用户范围或临时生效）。

### 临时环境变量
在命令行中，环境变量可以动态设置，但这些设置仅在当前会话有效。
使用 export 命令临时设置环境变量：
```bash
export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

### 用户级别的环境变量
用户级别的环境变量仅对特定用户有效，通常设置在用户的主目录下的配置文件中。
1. ~/.bashrc：
    - 适用于使用 Bash 作为默认 shell 的用户。
    - 在用户登录终端或打开新的终端窗口时加载。
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
    ```
2. ~/.bash_profile 或 ~/.profile：
    - 适用于登录 shell，会话开始时加载。
    - ~/.bash_profile 通常用于 Bash，而 ~/.profile 是通用的，适用于多种 shell。
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
    ```

### 系统级别的环境变量
系统级别的环境变量对所有用户有效，通常设置在系统配置文件中。文件编辑可以用vi/vim
1. /etc/profile：
    - 为所有用户设置环境变量。
    - 在用户登录 shell 会话开始时加载。
    - 示例：在 /etc/profile 中添加环境变量：
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
    ```
2. /etc/bash.bashrc：
    - 为所有使用 Bash 的用户设置环境变量。
    - 在每次启动交互式 shell 时加载。
    - 示例：在 /etc/bash.bashrc 中添加环境变量：
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
    ```
3. /etc/environment：
    - 为所有用户设置环境变量。
    - 该文件内容格式为 VAR=value，无需 export 关键字。
    - 示例：在 /etc/environment 中添加环境变量：
    ```bash
    JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$JAVA_HOME/bin"
    ```
4. /etc/profile.d/*.sh：
    - 在 /etc/profile.d/ 目录下，可以放置多个脚本文件，这些脚本在 /etc/profile 加载时会被执行。
    - 示例：创建 /etc/profile.d/java.sh 文件，并添加以下内容：
    ```bash
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
    ```

## 验证方法
要验证 Java 环境变量的配置是否正确，可以通过以下命令：
```bash
echo $JAVA_HOME
```
这个命令会输出 JAVA_HOME 变量的值，应该是 JDK 的安装路径。
同样，可以通过以下命令检查 java 和 javac 命令是否在 PATH 中：
```bash
java -version
javac -version
```
这两个命令应该分别输出 Java 运行时和编译器的版本信息。

总之，了解Java和系统环境变量的定位、本质和配置方法对于正确配置和优化系统环境至关重要。