---
layout: post
title: 【GESP】【GESP】C++三级知识点研究，cout输出进制转换
date: 2025-06-27 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++]
categories: [GESP, 三级] 
---
GESP C++三级考试大纲中，涉及进制转换的内容，之前在考纲介绍中重点针对进制转换的数学方法进行了介绍，在进行真题练习的过程中，发现其中涉及不少`cout`函数进制输出的题目，因此本文对此进行总结分享。

***相关考纲：***

> * [【GESP】C++三级考试大纲知识点梳理, （2）数据的进制转换](https://www.coderli.com/gesp-3-exam-syllabus-data-conversion/)
{: .prompt-info}

<!--more-->

---

在 C++ 编程中，我们经常需要以不同进制（如 **二进制、八进制、十六进制**）的形式输出整数。`cout` 提供了直观的格式控制方式，但每种进制的处理方式略有不同。

## 一、基础知识：`cout` 与格式控制符

C++ 中的 `cout`（定义于 `<iostream>`）可以通过 **操纵符（manipulators）** 来控制整数的进制输出。这些操纵符定义于头文件 `<iomanip>` 中。

## 二、常见格式控制符

| 控制符                         | 功能             | 恢复方法            |
| --------------------------- | -------------- | --------------- |
| `hex`, `oct`, `dec`         | 设置进制(十六，八，十进制)      | 设置为 `dec` 恢复    |
| `bitset<N>(x)` | 用于显示 `x` 的 N 位二进制表示 |设置为 `dec` 恢复    |
| `showbase`                  | 显示 `0x`、`0` 前缀 | `noshowbase`    |
| `uppercase`                 | 十六进制字母大写       | `nouppercase`   |
| `left`, `right`, `internal` | 对齐方向           | 设置为 `right` 等默认 |
| `setfill()`                 | 设置填充字符         | `setfill(' ')`  |

可以看到，格式控制符的设置不是一次性的，在设置后会持续作用于后续所有输出，直到你显式修改或恢复为默认，这点需要注意。当然也有一些一次性有效的格式控制符，如：

| 控制符               | 功能     | 特点             |
| ----------------- | ------ | -------------- |
| `setw(n)`         | 设置字段宽度 | **只作用于下一个输出项** |

### 🔸 综合示例

```cpp
#include <iostream>
#include <iomanip>   // oct, hex, dec, showbase, uppercase
#include <bitset>    // bitset 用于二进制输出

using namespace std;

int main() {
    int value = 255;

    // 十进制（默认）
    cout << "十进制: " << value << endl;

    // 八进制输出
    cout << oct;
    cout << "八进制（无前缀）: " << value << endl;
    cout << showbase << "八进制（带前缀）: " << value << endl;

    // 十六进制输出
    cout << hex;
    cout << "十六进制（小写）: " << value << endl;
    cout << uppercase << "十六进制（大写）: " << value << endl;
    cout << showbase << "十六进制（大写带前缀）: " << value << endl;

    // 恢复十进制
    cout << dec << nouppercase << noshowbase;
    cout << "恢复十进制: " << value << endl;

    // 二进制输出
    cout << "二进制（8位）: " << bitset<8>(value) << endl;
    cout << "二进制（16位）: " << bitset<16>(value) << endl;

    return 0;
}
```

---

**输出解释（value = 255）：**

```plaintext
十进制: 255
八进制（无前缀）: 377
八进制（带前缀）: 0377
十六进制（小写）: ff
十六进制（大写）: FF
十六进制（大写带前缀）: 0XFF
恢复十进制: 255
二进制（8位）: 11111111
二进制（16位）: 0000000011111111
```

---

### 🔸 同时按不同控制符输出

你可以一行中依次设置不同控制符：

```cpp
cout << "十六进制: " << hex << showbase << value << ", ";
cout << "八进制: " << oct << showbase << value << ", ";
cout << "十进制: " << dec << value << endl;
```

---

### 🔸 二进制格式控制（补零等）

```cpp
int n = 5;
cout << "补零二进制（8位）: " << bitset<8>(n) << endl;
// 输出：00000101
```

---

### 🔸 控制符影响与恢复

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int x = 255;

    cout << hex << showbase << uppercase;
    cout << "十六进制格式输出: " << x << endl;  // 输出: 0XFF

    // 下一行也会被格式影响（仍是 hex、showbase、uppercase）
    cout << "再次输出十六进制: " << x << endl;  // 输出: 0XFF

    // ✅ 显式恢复为默认设置
    cout << dec << noshowbase << nouppercase;
    cout << "恢复十进制输出: " << x << endl;   // 输出: 255

    // setw 只对下一个输出有效
    cout << setfill('0') << setw(5) << x << " ";
    cout << x << endl;  // 第二个 x 没有被 setw(5) 影响
}
```

## 三、与`printf`格式化输出对比

| 进制          | `cout` 操纵符（C++风格）                              | `printf` 格式控制（C风格）  | 示例值：`x = 255`    | 输出示例               |
| ----------- | ---------------------------------------------- | ------------------- | ---------------- | ------------------ |
| 十进制         | `cout << dec << x;`（默认）                        | `printf("%d", x);`  |                  | `255`              |
| 八进制         | `cout << oct << x;`                            | `printf("%o", x);`  |                  | `377`              |
| 八进制（前缀）     | `cout << showbase << oct << x;`                | `printf("%#o", x);` |                  | `0377`             |
| 十六进制        | `cout << hex << x;`                            | `printf("%x", x);`  |                  | `ff`               |
| 十六进制（大写）    | `cout << uppercase << hex << x;`               | `printf("%X", x);`  |                  | `FF`               |
| 十六进制（前缀）    | `cout << showbase << hex << x;`                | `printf("%#x", x);` |                  | `0xff`             |
| 十六进制（大写+前缀） | `cout << showbase << uppercase << hex << x;`   | `printf("%#X", x);` |                  | `0XFF`             |
| 二进制         | `cout << bitset<N>(x);`（需 `#include <bitset>`） | ❌ 不支持（需自定义实现）       | `bitset<8>(255)` | `11111111`         |
| 二进制（补零）     | `bitset<16>(x)`                                | ❌ 不支持               | `bitset<16>(5)`  | `0000000000000101` |

---

### 重点对比说明

| 项目       | `cout`（C++）                      | `printf`（C）            |
| -------- | -------------------------------- | ---------------------- |
| 风格       | 类型安全、链式操作、可组合                    | 控制字符串灵活、传统写法           |
| 默认输出进制   | 十进制（`dec`）                       | 十进制（`%d`）              |
| 八/十六进制支持 | 原生支持操纵符 `oct`, `hex`, `showbase` | 原生支持 `%o`, `%x`, `%#x` |
| 大小写控制    | `uppercase`                      | `%x` / `%X`            |
| 二进制输出    | 需使用 `bitset<N>(x)`               | 不支持，需要自己写函数            |
| 输出前缀     | `showbase` 控制                    | `%#o`、`%#x` 控制         |
| 灵活性      | 更现代、支持重载、自定义格式                   | 简洁快速、格式灵活              |

---

### 示例比较：输出 `255`

#### 使用 `cout`

```cpp
int x = 255;
cout << dec << x << endl;                        // 255
cout << oct << x << endl;                        // 377
cout << showbase << oct << x << endl;            // 0377
cout << hex << x << endl;                        // ff
cout << showbase << uppercase << hex << x << endl; // 0XFF
cout << bitset<8>(x) << endl;                    // 11111111
```

#### 使用 `printf`

```cpp
int x = 255;
printf("%d\n", x);      // 255
printf("%o\n", x);      // 377
printf("%#o\n", x);     // 0377
printf("%x\n", x);      // ff
printf("%#X\n", x);     // 0XFF
// 二进制需要自写函数，无法直接 printf
```

---

### 总结建议

| 场景               | 推荐使用            |
| ---------------- | --------------- |
| 类型安全、现代 C++ 风格   | `cout`          |
| 需要二进制输出、位操作调试    | `cout + bitset` |
| 需要快速格式化、多种格式混合打印 | `printf`        |
| 在嵌入式/老系统中（如比赛）   | `printf`        |

---
{% include custom/custom-post-content-footer.md %}
