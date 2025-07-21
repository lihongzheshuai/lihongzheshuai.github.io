---
layout: post
title: 【GESP】C++四级考试大纲知识点梳理, (10) 文件读写和重定向
date: 2025-07-21 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 四级]
---
孩子放假，出游一周，没有更新。刚刚归来，继续学习。

GESP C++四级官方考试大纲中，共有11条考点，本文针对第10条考点进行分析介绍。
> （10）掌握文件操作中的重定向，实现文件读写操作，了解文本文件的分类，掌握写操作、读操作、读写操作。
{: .prompt-info}

其实，由于本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。

***四级其他考点回顾：***

> * [【GESP】C++四级考试大纲知识点梳理, (1) 指针](https://www.coderli.com/gesp-4-exam-syllabus-pointer/)
> * [【GESP】C++四级考试大纲知识点梳理, (2) 结构体和二维数组](https://www.coderli.com/gesp-4-exam-syllabus-struct-two-dimensional-array/)
> * [【GESP】C++四级考试大纲知识点梳理, (3) 模块化和函数](https://www.coderli.com/gesp-4-exam-syllabus-module-function/)
> * [【GESP】C++四级考试大纲知识点梳理, (4) 变量和作用域](https://www.coderli.com/gesp-4-exam-syllabus-variable-scope/)
> * [【GESP】C++四级考试大纲知识点梳理, (5) 值传递](https://www.coderli.com/gesp-4-exam-syllabus-pass-by-value-reference-pointer/)
> * [【GESP】C++四级考试大纲知识点梳理, (6) 递推算法](https://www.coderli.com/gesp-4-exam-syllabus-iteration-algo/)
> * [【GESP】C++四级考试大纲知识点梳理, (7) 排序算法基本概念](https://www.coderli.com/gesp-4-exam-syllabus-sorting-algo-conception/)
> * [【GESP】C++四级考试大纲知识点梳理, (8) 冒泡、插入、选择排序](https://www.coderli.com/gesp-4-exam-syllabus-three-sorting-methods/)
> * [【GESP】C++四级考试大纲知识点梳理, (9) 简单算法复杂度的估算](https://www.coderli.com/gesp-4-exam-syllabus-estimation-of-algorithm-time-complexity/)
{: .prompt-tip}

<!--more-->

---

## 一、文件操作中的重定向

重定向（Redirection）通常指将标准输入/输出（如`cin`/`cout`）切换到文件或其他流。  

这句话的意思可以分解为两个关键部分来理解：即：

* 什么是“标准输入/输出”
* 什么是“重定向”

### 1.1 什么是“标准输入/输出”？

“标准输入/输出”（**Standard Input/Output，简称 Standard I/O**）是指在程序运行时，操作系统默认提供的一组**输入与输出通道**，用于与用户或其他程序进行交互。

在 C/C++ 中，这种机制提供了一个**抽象的设备接口**，可以简化 I/O 操作，不需要开发者直接与底层硬件或文件系统打交道。

#### 1.1.1 标准输入/输出的组成

| 名称   | 标识符               | 默认连接的设备 | 用途      |
| ---- | ----------------- | ------- | ------- |
| 标准输入 | `stdin`  | 键盘      | 接收输入    |
| 标准输出 | `stdout` | 显示器（终端） | 输出结果    |
| 标准错误 | `stderr` | 显示器（终端） | 输出错误或日志 |

这些是由操作系统在程序启动时自动打开的三个“文件流”。

---

#### 1.1.2 在C中的实现方式

* 使用 `<stdio.h>` 中的全局流指针：

```c
int main() {
    int x;
    scanf("%d", &x);            // 从 stdin 读取
    printf("x = %d\n", x);      // 向 stdout 输出
    fprintf(stderr, "error\n"); // 向 stderr 输出
}
```

#### 1.1.3 在C++中的实现方式

* 使用 `<iostream>` 中的全局对象：

```cpp
#include <iostream>

int main() {
    int x;
    std::cin >> x;               // 从标准输入stdin读取
    std::cout << "x = " << x;    // 向标准输出stdout输出
    std::cerr << "error\n";      // 向标准错误stderr输出
}
```

---

#### 1.1.4 为什么要使用“标准”输入输出？

✅ 1. **统一接口，抽象底层**

* 不管是从键盘输入，还是从文件中读取，都可以抽象为“输入流”
* 便于程序移植，平台无关

✅ 2. **简化操作**

* 无需用户手动打开/关闭输入输出设备
* 操作系统启动程序时自动创建和管理

✅ 3. **支持重定向**

* 例如：用户可以在命令行中重定向输入/输出：

```bash
./a.out < input.txt > output.txt
```

此时：

* `stdin` → `input.txt`
* `stdout` → `output.txt`

---

### 1.2 什么是“重定向”？

**重定向（Redirection）** 的意思是：**把标准输入输出“指向”的对象从默认设备（如键盘、屏幕）切换为“文件”或“其他流”**。

举个例子来理解，默认情况下：

```cpp
int x;
cin >> x;  // 从键盘读取
cout << x; // 输出到屏幕
```

使用**重定向**后，让 cin/cout 不再连着键盘/屏幕，而是连到“文件”：

> 重定向的本质是什么？
>
> 重定向只是改变了数据的"流向"，就像把水管接到了不同的水源和出水口
>
> * **默认状态：**
>
> ```plaintext
> [键盘] ——(cin)——> 程序 ——(cout)——> [屏幕]
> ```
>
> * **重定向后：**
>
>```plaintext
> [文件input.txt] ——(cin)——> 程序 ——(cout)——> [文件output.txt]
> ```
>
> * `cin`依然是输入流（`istream`类型），`cout`依然是输出流（`ostream`类型）
> * 重定向不会改变它们的本质功能和使用方式，只是改变了数据来源和去向
{: .prompt-tip}

#### 1.2.1 重定向常用场景

| 场景        | 原因/好处           |
| --------- | --------------- |
| 读写大批量测试数据 | 避免手工输入，提高效率     |
| 自动化测试     | 输入输出由文件控制，可重复测试 |
| 竞赛/OJ平台   | 程序需要从特定文件中读写数据  |
| 日志输出      | 将 cout 重定向为日志文件 |

#### 附：重定在信奥竞赛中的应用，信奥做题文件输入输出说明（CSP开始做题的方法）

{% include embed/{bilibili}.html id='{BV17a411M7Wh}' %}

## 二、C/C++中重定向的方法

在C/C++中，输入输出重定向是将程序的标准输入（`stdin`）、标准输出（`stdout`）或标准错误（`stderr`）从默认的键盘/终端重定向到文件或其他设备的过程。C++中实现重定向主要有以下几种方式：

### 2.1 **使用 `freopen` 函数**

C标准库提供的 `freopen` 函数可以在程序运行时将标准输入输出流重定向到文件。

* 函数原型：

  ```cpp
  FILE* freopen(const char* filename, const char* mode, FILE* stream);
  ```

* 常用方式：
  * 重定向标准输入：`freopen("input.txt", "r", stdin);`
  * 重定向标准输出：`freopen("output.txt", "w", stdout);`
  * 重定向标准错误：`freopen("error.txt", "w", stderr);`

* **优点**：
  * 在程序内部实现重定向，灵活性高，可动态指定文件。
  * 跨平台，适用于大多数C/C++环境。
* **缺点**：
  * 一旦重定向，标准输入输出流全局改变，无法方便地在程序中切换回默认终端。
  * 不适合需要频繁切换输入输出源的场景。
* **适用场景**：
  * 需要在程序内部指定输入输出文件的场景。
  * 竞赛编程（如ACM、OJ、CSP）中常用于从文件读取测试数据。
  * 需要将输出保存到文件的固定场景。

#### 代码示例

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

int main() {
    // 重定向标准输入到 input.txt
    freopen("input.txt", "r", stdin);
    // 重定向标准输出到 output.txt
    freopen("output.txt", "w", stdout);

    int x;
    while (cin >> x) {
        cout << x * 2 << endl;
    }
    return 0;
}
```

**运行效果**：

* 输入文件 `input.txt`：`1 2 3`
* 输出文件 `output.txt`：`2 4 6`

---

### 2.2 **使用文件流（C++ `fstream`）**

C++的 `<fstream>` 库提供 `ifstream` 和 `ofstream` 类，用于直接操作文件流，而非依赖标准输入输出。

* 使用 `ifstream` 读取文件，代替 `cin`。
* 使用 `ofstream` 写入文件，代替 `cout`。

* **优点**：
  * 完全在程序内部控制，灵活性高，可同时操作多个文件。
  * 支持动态打开/关闭文件流，不影响标准输入输出。
  * 提供更细粒度的文件操作（如随机访问、格式化）。
* **缺点**：
  * 代码复杂度略高于 `freopen` 或命令行重定向。
  * 需要显式管理文件的打开和关闭。
* **适用场景**：
  * 需要同时处理多个输入输出文件。
  * 需要精细控制文件操作（如追加、格式化输出）。
  * 不希望影响标准输入输出的场景。

#### 代码示例

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ifstream inFile("input.txt");  // 打开输入文件
    ofstream outFile("output.txt"); // 打开输出文件

    if (!inFile || !outFile) {
        cerr << "Error opening file" << endl;
        return 1;
    }

    int x;
    while (inFile >> x) {
        outFile << x * 2 << endl;
    }

    inFile.close();
    outFile.close();
    return 0;
}
```

**运行效果**：

* 输入文件 `input.txt`：`1 2 3`
* 输出文件 `output.txt`：`2 4 6`

---

### 2.3 **使用系统调用（`dup` 和 `dup2`）**

在类Unix系统中（如Linux），使用低级文件描述符操作（如 `dup` 和 `dup2`）实现重定向。这是操作系统级别的重定向，适用于需要底层控制的场景。

* 使用 `open` 打开文件，获取文件描述符。
* 使用 `dup2` 将标准输入（0）、标准输出（1）或标准错误（2）的文件描述符替换为目标文件描述符。

* **优点**：
  * 提供底层控制，适合需要精细管理文件描述符的场景。
  * 可与管道、套接字等结合使用。
* **缺点**：
  * 平台相关，仅适用于类Unix系统（如Linux、macOS）。
  * 代码复杂，调试困难，容易出错。
  * 不如高级方法（如 `fstream`）直观。
* **适用场景**：
  * 需要与操作系统其他功能（如管道、进程间通信）结合的场景。
  * 系统编程或需要低级控制的场景。

#### 代码示例

```cpp
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
using namespace std;

int main() {
    // 打开输入文件
    int in_fd = open("input.txt", O_RDONLY);
    if (in_fd == -1) {
        perror("Error opening input file");
        return 1;
    }

    // 打开输出文件
    int out_fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (out_fd == -1) {
        perror("Error opening output file");
        return 1;
    }

    // 重定向标准输入和输出
    dup2(in_fd, STDIN_FILENO);
    dup2(out_fd, STDOUT_FILENO);

    // 关闭文件描述符
    close(in_fd);
    close(out_fd);

    int x;
    while (cin >> x) {
        cout << x * 2 << endl;
    }

    return 0;
}
```

**运行效果**：

* 输入文件 `input.txt`：`1 2 3`
* 输出文件 `output.txt`：`2 4 6`

---

### 2.4 使用 C++ std::cin, std::cout 的 rdbuf 重定向（C++风格）

使用 C++ 的 `rdbuf` 方法进行重定向是一种更加 C++ 风格的方案。这种方式的特点如下：

* **优点**：
  * 完全符合 C++ 的面向对象设计理念
  * 可以方便地保存和恢复原有的缓冲区
  * 提供更细粒度的控制
  * 异常安全
* **缺点**：
  * 代码相对复杂一些
  * 需要理解流缓冲区的概念
* **适用场景**：
  * 需要临时重定向后还原的场景
  * 面向对象的 C++ 工程项目
  * 需要异常安全保证的场景

这种方式通过直接操作流的缓冲区（buffer）来实现重定向，是一种更加底层和灵活的方案。

#### 代码示例

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ifstream inFile("input.txt");
    std::ofstream outFile("output.txt");

    // 备份原来的缓冲区指针
    std::streambuf* cinBackup = std::cin.rdbuf();
    std::streambuf* coutBackup = std::cout.rdbuf();

    // 重定向
    std::cin.rdbuf(inFile.rdbuf());
    std::cout.rdbuf(outFile.rdbuf());

    int x;
    while (std::cin >> x) {
        std::cout << "Read: " << x << std::endl;
    }

    // 恢复原来的缓冲区
    std::cin.rdbuf(cinBackup);
    std::cout.rdbuf(coutBackup);

    return 0;
}
```

### 2.5 **命令行重定向**

通过操作系统的命令行重定向符号（`>`、`>>`、`<`等）实现输入输出重定向。这是外部重定向方式，无需修改程序代码。

* **输入重定向**：使用 `<` 将文件内容作为程序的输入。
  * 示例：`./program < input.txt`
* **输出重定向**：
  * `>`：覆盖目标文件。
    * 示例：`./program > output.txt`
  * `>>`：追加到目标文件。
    * 示例：`./program >> output.txt`
* **输入输出同时重定向**：
  * 示例：`./program < input.txt > output.txt`

* **优点**：
  * 无需修改程序代码，简单易用。
  * 由操作系统处理，适用于快速测试或临时重定向。
* **缺点**：
  * 依赖命令行环境，无法在程序内部动态控制重定向。
  * 不适合复杂场景（如动态选择文件或管道）。
* **适用场景**：
  * 快速测试程序输入输出。
  * 批处理脚本中处理文件输入输出。
  * 不需要程序内部控制重定向逻辑的场景。

#### 代码示例

```cpp
#include <iostream>
using namespace std;

int main() {
    int x;
    // 从标准输入读取
    while (cin >> x) {
        // 输出到标准输出
        cout << x * 2 << endl;
    }
    return 0;
}
```

**运行示例**：

* 输入文件 `input.txt` 内容：`1 2 3`
* 运行：`./program < input.txt > output.txt`
* 输出文件 `output.txt` 内容：`2 4 6`

---

### 对比总结

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **`freopen`** | 程序内控制，跨平台，简单易用 | 全局修改流，难以切换 | 竞赛编程、固定文件输入输出 |
| **C++ `fstream`** | 灵活，支持多文件操作，不影响标准流 | 代码稍复杂，需管理文件 | 复杂文件操作、动态文件处理 |
| **系统调用（`dup2`）** | 底层控制，适合系统编程 | 平台相关，代码复杂 | 系统编程、管道或套接字结合 |
| **C++ `rdbuf`** | 面向对象，异常安全，支持流缓冲 | 代码复杂，需理解流缓冲 | 临时重定向、面向对象编程 |
| **命令行重定向** | 简单，无需改代码，跨平台 | 依赖命令行，无法动态控制 | 快速测试、批处理脚本 |

---
{% include custom/custom-post-content-footer.md %}
