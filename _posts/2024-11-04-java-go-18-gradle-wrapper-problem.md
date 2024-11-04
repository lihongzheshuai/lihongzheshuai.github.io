---
layout: post
title: 一起学Java(18)-[配置篇]一个诡异(有趣)的Gradle Wrapper问题
date: 2024-11-04 21:00 +0800
author: onecoder
comments: true
tags: [Java, Gradle, 一起学Java]
categories: [一起学Java系列,（5）配置篇]
---
在研究JUnit使用的时候，遇到了一个有趣的Gradle Wrapper使用问题，经过若干天的研究，终于找到并解决了问题，记录分享如下，这也是我们一起学Java过程中遇到的问题。

<!--more-->

## **一、什么是Gradle Wrapper**

Gradle Wrapper 是一个工具，简称 "Wrapper"，用于确保在不同环境中都可以使用同一版本的 Gradle 构建项目。它主要由一组脚本（`gradlew` 和 `gradlew.bat`）和一些配置文件组成。这些文件存放在项目中，可以自动下载并使用指定的 Gradle 版本来构建项目，而不需要系统中预先安装 Gradle。

### （一）Gradle Wrapper 的应用场景

1. **项目的一致性构建环境**：在团队协作中，确保所有开发者和构建服务器使用相同版本的 Gradle，避免由于不同 Gradle 版本而导致的构建错误和不一致问题。

2. **便于持续集成和自动化构建**：在持续集成环境中，构建过程需要自动化执行。通过使用 Gradle Wrapper，构建服务器可以自动下载并使用指定的 Gradle 版本，而不必手动安装，简化了构建环境配置。

3. **提高项目的可移植性**：Gradle Wrapper 可以让项目在没有预装 Gradle 的环境中直接运行构建命令，如 `./gradlew build`，从而方便在不同的开发和生产环境中快速构建项目。

4. **便于控制不同项目的 Gradle 版本**：对于同时维护多个项目的情况，Gradle Wrapper 可以确保每个项目使用自己指定的 Gradle 版本，避免由于版本不兼容而引发的构建错误。

### （二）Gradle Wrapper 的原理

Gradle Wrapper 本质上是一个用于下载并执行特定 Gradle 版本的工具。它包含几个关键文件：

- **`gradlew` 和 `gradlew.bat`**：这是可执行脚本，分别用于 Linux/Mac 和 Windows 系统。这些脚本会检查指定版本的 Gradle 是否已经下载，若没有则自动下载并执行该版本的 Gradle。
- **`gradle/wrapper/gradle-wrapper.properties`**：此配置文件指定了 Gradle Wrapper 使用的 Gradle 版本和下载地址。构建时，Wrapper 会读取这个文件，从指定的 URL 下载对应版本的 Gradle。
- **`gradle/wrapper/gradle-wrapper.jar`**：这是一个小型的 Java 程序，负责从网络下载指定版本的 Gradle。

工作逻辑如下：

1. 当执行 `./gradlew <task>` 时，脚本会先检查本地目录中是否存在指定版本的 Gradle。
2. 如果指定版本的 Gradle 不存在，Wrapper 会通过 `gradle-wrapper.jar` 从配置文件中指定的 URL 下载该版本。
3. 下载完成后，Wrapper 调用该版本的 Gradle 执行构建任务。

### （三）Gradle Wrapper 的使用方法

1. **生成 Wrapper**：可以通过在项目目录下执行 `gradle wrapper` 命令来生成 Wrapper 文件。这会创建 `gradlew`、`gradlew.bat` 脚本文件以及 `gradle/wrapper` 文件夹中的相关文件。
2. **配置 Gradle 版本**：在 `gradle-wrapper.properties` 文件中指定所需的 Gradle 版本，例如：`distributionUrl=https\://services.gradle.org/distributions/gradle-8.10.2-bin.zip`。

3. **运行构建命令**：之后可以通过 `./gradlew build` 直接构建项目，而不必依赖系统中安装的 Gradle。

### （四）使用 Gradle Wrapper 的好处

1. **提高构建一致性**：确保项目在所有开发环境和 CI/CD 环境中都使用相同版本的 Gradle，减少因版本差异导致的错误。
2. **便于新开发者上手**：新加入的开发者无需额外安装 Gradle，直接使用项目中的 Wrapper 即可参与开发。
3. **更便捷的版本管理**：项目升级到新 Gradle 版本时，只需更新 `gradle-wrapper.properties` 中的版本号即可，无需手动更新团队中每个人的 Gradle 环境。

## 二、在java-all-in-one项目中遇到的问题

在[***《一起学Java(1)-[起步篇]教你如何创建一个Gradle管理的Java开源项目（java-all-in-one）》***](https://www.coderli.com/java-go-1-new-gradle-project/)中，我研究使用的项目就是通过Gradle Wrapper就行配置管理，当时生成的方式是通过IntelliJ内置的配置自动生成的。生成文件包括前文介绍的Gradle Wrapper所必须的`gradlew.bat`、`gradlew`、`gradle\wrapper\gradle-wrapper.properties`以及`gradle\wrapper\gradle-wrapper.jar`等必要文件。一直以来，我通过IntelliJ工具直接调用Gradle Task都正常执行，直到最近我在研究JUnit的使用的时候，想通过`graldew test`命令直接执行，却一直报错。

```console
gradlew.bat test
错误: 找不到或无法加载主类 test
原因: java.lang.ClassNotFoundException: test
```

并且，执行gradlew --version命令，显示的版本却是我环境Java的版本，而不是gradle的版本，这个现象让我觉得有些奇怪。我在网上进行了很多查询，大多讲的都是环境中缺失Gradle Wrapper运行必要的文件，但在我的项目中，文件都在。

百思不得其解，于是我查看了我环境中的gradlew.bat脚本内容。

```bat
@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  Gradle startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar


@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%"   %*

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%GRADLE_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
```

发现一个问题，脚本中执行Java程序的代码，只配置了执行参数和Classpath，但是没有指定gradle相关的运行程序，不太正常。

```bat
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%"   %*
```

为了印证猜测，我上网搜索了gradlew.bat脚本源码，上述代码应为

```bat
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
```

替换后，再次运行gradlew build命令验证，一切恢复正常了。如此看来，应该是IntelliJ初始化Gradle Wrapper项目时，相关文件内容生成除了点问题，具体原因未知。为了避免其他差异，我用命令

```bat
gradlew.bat wrapper
```

将我的项目重新初始化了一遍，`gradlew.bat`、`gradlew`、`gradle\wrapper\gradle-wrapper.properties`以及`gradle\wrapper\gradle-wrapper.jar`都重新生成了，仔细对比发现其实`gradlew.bat`文件差异还是挺大的。

好在问题解决了，暂结束这个话题。

---

所有代码已上传至：[***https://github.com/lihongzheshuai/java-all-in-one***](https://github.com/lihongzheshuai/java-all-in-one)
