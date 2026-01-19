---
layout: post
title: 【GESP】C++七级考试大纲知识点梳理, (1) 数学库常用函数
date: 2026-01-19 08:15 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 数学函数]
categories: [GESP, 七级]
---
GESP C++七级考试大纲中共有`4`条考点，第`1`条考点要求我们熟练掌握数学库中的常用函数。在解决复杂的算法问题（如几何计算、概率统计、数值模拟）时，这些“轮子”能帮我们省去大量的造车时间。

> （1）掌握数学库常用函数（三角、对数、指数），三角函数包括 sin(x)，cos(x)等；
> 对数函数包括 log10(x)：返回 x 以 10 为底的对数，log2(x)：返回 x 以 2 为底的对数；
> 指数函数包括 exp(x)：计算指数函数，返回 x 的以 e 为底的指数函数。
{: .prompt-info}

> 本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

在使用这些函数之前，别忘了引入头文件：

```cpp
#include <cmath>
// 或者万能头文件
#include <bits/stdc++.h>
```

> ⚠️ **注意**：`<cmath>` 中的函数参数和返回值通常都是 `double` 类型（浮点数）。在涉及整数运算时要小心精度丢失问题，或者显式进行类型转换。
{: .prompt-danger}

---

## 一、三角函数 (Trigonometric Functions)

三角函数是几何计算的基础。在 C++ 中，最需要注意的一点是：**所有三角函数的参数都是“弧度制” (Radians)，而不是“角度制” (Degrees)。**

### 1.1 常用函数表

| 函数 | 描述 | 数学公式 |
| :--- | :--- | :--- |
| `sin(x)` | 正弦函数 | $\sin(x)$ |
| `cos(x)` | 余弦函数 | $\cos(x)$ |
| `tan(x)` | 正切函数 | $\tan(x)$ |
| `asin(x)` | 反正弦函数，返回弧度 | $\arcsin(x)$ |
| `acos(x)` | 反余弦函数，返回弧度 | $\arccos(x)$ |
| `atan(x)` | 反正切函数，返回弧度 | $\arctan(x)$ |

### 1.2 角度与弧度的转换

考试中给出的题目往往是角度（例如 30°, 90°），直接传给 C++ 的 `sin(30)` 是错的！必须先转为弧度。

* **公式**：
  $$ \text{弧度} = \text{角度} \times \frac{\pi}{180} $$
  $$ \text{角度} = \text{弧度} \times \frac{180}{\pi} $$

* **$\pi$ (Pi) 的获取**：
  建议使用 `acos(-1.0)` 来获取高精度的 $\pi$ 值。

### 1.3 代码示例

```cpp
#include <iostream>
#include <cmath>
#include <iomanip> // 用于 setprecision
using namespace std;

int main() {
    double pi = acos(-1.0); // 获取 pi
    double angle = 60.0;    // 60度
    
    // 错误示范：直接传角度
    cout << "sin(60) = " << sin(angle) << " (这是错的！)" << endl;
    
    // 正确示范：转弧度
    double radian = angle * (pi / 180.0);
    cout << "sin(60°) = " << sin(radian) << endl; // 应该是 0.866...
    cout << "cos(60°) = " << cos(radian) << endl; // 应该是 0.5
    
    return 0;
}
```

---

## 二、对数函数 (Logarithmic Functions)

对数在算法复杂度分析（如 $O(\log n)$）和处理大数运算时非常有用。

### 2.1 常用函数表

| 函数 | 描述 | 数学公式 | 备注 |
| :--- | :--- | :--- | :--- |
| `log(x)` | **自然对数**，底数为 $e$ | $\ln(x)$ 或 $\log_e(x)$ | 注意不是 $\log_{10}$ |
| `log10(x)` | 常用对数，底数为 10 | $\lg(x)$ 或 $\log_{10}(x)$ | 考纲重点 |
| `log2(x)` | 二进制对数，底数为 2 | $\log_2(x)$ | 考纲重点，常用于计算完全二叉树高度 |

> 💡 **小贴士**：如果需要计算任意底数 $a$ 的对数 $\log_a(b)$，可以使用换底公式：
> $$ \log_a(b) = \frac{\ln(b)}{\ln(a)} \quad \Rightarrow \quad \text{code: } \texttt{log(b) / log(a)} $$
{: .prompt-tip}

### 2.2 代码示例

```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    double x = 100.0;
    
    cout << "log10(100) = " << log10(x) << endl; // 输出 2
    cout << "log2(8) = " << log2(8.0) << endl;   // 输出 3
    cout << "ln(e) = " << log(exp(1.0)) << endl; // 输出 1 (ln e = 1)
    
    return 0;
}
```

---

## 三、指数函数 (Exponential Functions)

指数函数与对数函数互为逆运算，常用于计算幂次、根号等。

### 3.1 常用函数表

| 函数 | 描述 | 数学公式 |
| :--- | :--- | :--- |
| `exp(x)` | 计算 $e$ 的 $x$ 次方 | $e^x$ |
| `pow(x, y)` | 计算 $x$ 的 $y$ 次方 | $x^y$ |
| `sqrt(x)` | 计算 $x$ 的平方根 | $\sqrt{x}$ |

### 3.2 代码示例

```cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    // 1. exp(x)
    cout << "e^1 = " << exp(1.0) << endl; // e 的近似值 2.71828...
    
    // 2. pow(x, y) - 极其常用
    cout << "2^10 = " << pow(2, 10) << endl; // 1024
    cout << "3^3 = " << pow(3, 3) << endl;   // 27
    
    // 3. sqrt(x)
    cout << "sqrt(16) = " << sqrt(16) << endl; // 4
    
    // 勾股定理示例: c = sqrt(a^2 + b^2)
    double a = 3.0, b = 4.0;
    double c = sqrt(pow(a, 2) + pow(b, 2));
    cout << "勾股数 3, 4 的斜边是: " << c << endl; // 5
    
    return 0;
}
```

---

## 四、备考总结 & 易错点

对于 GESP 七级考生，掌握这些函数的使用只是第一步，更重要的是在实际题目中灵活运用。

1. **类型陷阱**：如果不小心把整数传给某些数学函数，可能会发生隐式转换。虽然现代编译器很聪明，但建议养成操作 `double` 的习惯。尤其是 `pow` 函数，计算整数次幂时，如果是很大的整数，建议自己写**快速幂**算法，因为 `double` 类型的 `pow` 可能会有精度误差导致WA（例如 `pow(5, 2)` 算出 `24.999999`，转 int 变成 24）。
2. **定义域错误**：
   * `sqrt(x)` 中 $x$ 不能为负数。
   * `log(x)` 中 $x$ 必须大于 0。
   * `asin(x)` / `acos(x)` 中 $x$ 必须在 $[-1, 1]$ 之间。
   * 这些错误通常会导致程序返回 `NaN` (Not a Number) 或运行时错误。
3. **$\pi$ 的写法**：`acos(-1.0)` 是最稳健的写法，不要手打 `3.1415926`，容易抄错且精度不够。

掌握了这些数学工具，你就在通往高级算法（如计算几何）的路上迈出了坚实的一步！

---

{% include custom/custom-post-content-footer.md %}
