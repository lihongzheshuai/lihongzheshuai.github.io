---
layout: post
title: 【GESP】Windows系统配置官方要求Dev-C++和g++13.2.0编译环境
date: 2024-09-07 08:00 +0800
author: OneCoder
image: /images/post/gesp/compile-version.png
comments: true
tags: [GESP, C++]
categories: [GESP, 一级]
---
本系列用于记录与孩子共同成长学习GESP的过程和练习，希望能有所积累给我和孩子形成一份资产沉淀。

<!--more-->

对于C++语言来说，2024年CCF GESP官方建议的C++开发环境为Dev-C++ 5.11，g++版本为13.2.0。

![IDE版本情况](/images/post/gesp/ide-version.png)

对Dev-C++在官方[考点编译环境说明及软件下载页面](https://gesp.ccf.org.cn/101/1002/10032.html)提供了下载地址，但下载页面只提供了Dev-C++ 5.11的安装包，并没有提供g++ 13.2.0的安装包。对于Windows系统来说，一般都是通过MinGW来进行g++的安装配置。

## 一、MinGW是什么

MinGW（Minimalist GNU for Windows）是一个开源项目，旨在将GNU编译器集合（GCC）及相关工具移植到Windows操作系统上。它为开发者提供了一个在Windows环境中编译和链接C、C++等语言程序的工具集，而无需依赖任何第三方运行时环境。

### （一）MinGW的主要特点

- **编译器和工具集**：MinGW包含了GCC编译器、GNU二进制工具（binutils）以及其他开发工具，如make等，支持C、C++和Fortran等多种编程语言。

- **原生Windows支持**：使用MinGW编译的程序可以直接在Windows上运行，不需要额外的动态链接库（DLL），因为它使用的是Windows的C运行库。

- **开源与自由**：MinGW是完全免费的开源软件，遵循GNU公共许可证（GPL），允许开发者自由使用和分发。

- **与MinGW-w64的区别**：MinGW主要支持32位Windows程序的编译，而其分支项目MinGW-w64则支持64位和32位程序的编译，并且更新频率更高。MinGW本身已经停止更新。

## 二、通过MinGW-w64配置Dev C++编译环境g++ 13.2.0

官网要求中给出了gcc和g++的版本要求，简单了解下gcc和g++的关系和区别，对GESP编程本身可能没有太多影响。但有助于理解本次MinGW-w64的安装配置。

### （一）gcc和g++

`gcc`是GNU编译器集合的一部分，`g++`是GCC的C++编译器。`g++` 和 `gcc` 都是 GCC（GNU Compiler Collection）中的编译器工具，但它们的用途略有不同。

#### 1. **编译语言默认处理**

- **`gcc`**：`gcc` 是GNU C编译器，默认用于编译 C 语言程序。尽管它也可以用来编译C++代码（通过适当的选项），但它的默认模式是C语言模式。
- **`g++`**：`g++` 是GNU C++编译器，专门用于编译 C++ 代码。它在默认情况下会将代码视为 C++ 代码，并会自动链接标准C++库（如`libstdc++`）。

#### 2. **链接标准库**

- **`gcc`**：当使用 `gcc` 编译C语言程序时，它不会自动链接 C++ 的标准库。如果用它来编译C++程序，必须手动指定链接C++标准库（使用`-lstdc++`）。
- **`g++`**：`g++`自动链接 C++ 标准库，因此用于编译C++程序时不需要手动指定库。

### 3. **文件扩展名的处理**

- **`gcc`**：根据文件的扩展名来决定如何编译。对于 `.c` 文件，`gcc`会将它们识别为C语言文件并以C编译器的方式进行处理。对于 `.cpp` 文件（或 `.cc`、`.cxx` 文件），`gcc`会以C++编译器的方式处理。
- **`g++`**：`g++`无论输入文件的扩展名如何，都会默认将其视为C++代码处理，因此即使编译 `.c` 文件，编译器也会按照C++语法规则进行处理。

### 4. **常见使用场景**

- **`gcc`**：适合编译 C 语言程序。如果要编译混合代码（C和C++），需要手动指定相应的编译和链接选项。
- **`g++`**：主要用于编译 C++ 程序。对于纯C++代码来说，`g++`更便捷，因为它自动处理C++的标准库和其他C++相关设置。

### （二）配置Dev-C++和MinGW-w64 g++ 13.2.0

MinGW-w64的官网地址为：<https://www.mingw-w64.org/>，选择MinGW-W64-builds版本进入下载页面，选择13.2.0版本，而不是最新版。

![MinGW-W64-builds](/images/post/gesp/mingw-w64-builds-13.2.0.png)

具体根据操作系统选择，Windows系统可以选择[x86_64-13.2.0-release-win32-seh-ucrt-rt_v11-rev0](https://github.com/niXman/mingw-builds-binaries/releases/download/13.2.0-rt_v11-rev0/x86_64-13.2.0-release-win32-seh-ucrt-rt_v11-rev0.7z)版本，即：

- 64 位 MinGW 编译器工具链（x86_64 架构）。
- 使用 GCC 13.2.0 版本。
- 面向 Windows 平台，使用 SEH 异常处理机制。
- 采用 UCRT 运行时库。(ucrt 是现代 Windows 系统上推荐使用的 CRT 版本，适用于大多数新的开发场景，而 msvcrt 则主要用于维护旧项目或兼容性需求场景。)
- 这是该工具链的 v11 运行时版本的初始修订版。

下载完成后，解压缩文件到一个合适的位置，例如 `C:\mingw64`。

接下来，我们需要安装配置 Dev-C++，下载并安装官方提供的Dev-C++ 5.11版本。(下载地址：[https://logserviceccf.oss-cn-hangzhou.aliyuncs.com/Dev-Cpp%205.11%20TDM-GCC%204.9.2.exe](https://logserviceccf.oss-cn-hangzhou.aliyuncs.com/Dev-Cpp%205.11%20TDM-GCC%204.9.2.exe))，然后配置g++13.2.0编译器。

1. 打开 Dev-C++。
2. 点击"工具" > "编译选项"。
3. 在"编译器"选项卡中，点击"添加"按钮。
4. 浏览并选择你刚刚解压的 MinGW-w64 目录（例如 `C:\mingw64`）。
5. 选择新添加的编译器，点击"设为默认"。
6. 点击"确定"保存设置。

现在，Dev-C++中的g++ 13.2.0编译环境就配置完成了。

## 三、验证配置

1. 在Dev-C++中创建一个新的C++源文件。
2. 输入一个简单的C++程序，例如：

   ```cpp
   #include <iostream>
   int main() {
       std::cout << "Hello, World!" << std::endl;
       return 0;
   }
   ```

3. 保存文件，然后点击工具栏上的"编译并运行"按钮。
4. 如果一切正常，你应该能看到程序成功编译并运行，输出"Hello, World!"，并且在编译日志中看到g++ 13.2.0的编译信息。

以上，就是我亲自配置Dev-C++和g++ 13.2.0编译环境的过程，从结果看很简单，但我在Dev-C++这个工具上确实折腾了很久，走了很多弯路，一眼难尽，不再赘述。
