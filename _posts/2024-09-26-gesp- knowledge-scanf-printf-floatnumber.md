---
layout: post
title: 【GESP】C++知识点研究，scanf/printf浮点数格式化到底是%lf还是%f
date: 2024-09-26 22:00 +0800
author: OneCoder
image: /images/post/gesp/gesp-1.png
comments: true
tags: [GESP, C++]
categories: [GESP, 一级]
---
最近做基础练习时频繁使用到`scanf`和`printf`函数。在对`double`类型变量进行输入输出时发现，`scanf`标准为 ***%lf*** 而`printf`标准为 ***%f*** ，并且`printf`实际使用 ***%lf*** 和 ***%f*** ，效果似乎一样，遂想弄清一二。

<!--more-->

## C++中关于double类型变量格式化符号标准

在C++中，使用 `printf` 输出 `double` 类型的值时，正确的格式化符是 `%f`，而不是 `%lf`。

虽然在变量声明时，`double` 和 `float` 有区别，但 `printf` 在格式化时，`%f` 处理的是所有浮点数，包括 `float` 和 `double`。使用 `%lf` 只在 `scanf` 中用于读取 `double` 类型的值。

```cpp
#include <cstdio>

int main() {
    double num = 3.14159;
    printf("%f\n", num);  // 正确，输出 3.141590
    return 0;
}
```

### 总结

- **`printf` 输出 `double` 类型的值时：用 `%f`**。
- **`scanf` 读取 `double` 类型的值时：用 `%lf`；读取 `float`类型的值时：用%f** 。

## 对于printf，double类型值使用%f和%lf为何都有效

### 1. **历史原因与标准**

在标准 C 库中，`printf` 规范中规定了 `%f` 作为格式化浮点数的通用符号，适用于 `float` 和 `double` 类型。事实上，`float` 类型在调用 `printf` 时，会被自动提升为 `double`（称为默认的“浮点数提升”）。因此，对于 `printf` 来说，处理的是 `double` 类型的数据，而不是 `float`，所以 `%f` 足够处理两者。

`%lf` 虽然表示长浮点数（`long float`），但在 `printf` 中它并不是标准格式。实际上 `%lf` 的使用行为与 `%f` 相同，因为 `printf` 不区分 `float` 和 `double`。这也是为什么你看到使用 `%lf` 也能正常输出 `double` 的原因，但标准要求应该使用 `%f`。

### 2. **推荐使用 `%f`**

即使在某些编译器下，`%lf` 和 `%f` 都能正常输出 `double`，但根据标准 C/C++ 规范，**推荐使用 `%f`** 来格式化输出浮点数（包括 `double`）。

因此， **`printf` 输出 `double` 时，规范推荐使用 `%f`，虽然 `%lf` 也能工作，但不属于标准规定。**
