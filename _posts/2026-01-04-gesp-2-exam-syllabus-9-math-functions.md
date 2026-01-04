---
layout: post
title: 【GESP】C++二级考试大纲知识点梳理, （9）常用数学函数
date: 2026-01-04 08:30 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 数学函数]
categories: [GESP, 二级]
---
编程不仅是逻辑，也是计算。C++ 标准库为我们准备了丰富的数学工具，让我们不用自己去造轮子（比如求平方根）。掌握这些函数，是解决数学计算类题目的捷径。本篇详细剖析大纲第 9 条考点。

> （9）掌握常用的数学函数：绝对值函数、平方根函数、最大值函数、最小值函数、随机数函数理解相应的算法原理。
{: .prompt-info}

***二级考点系列：***

> * [【GESP】C++二级考试大纲知识点梳理, （1）计算机存储的基本概念及分类](https://www.coderli.com/gesp-2-exam-syllabus-computer-storage/)
> * [【GESP】C++二级考试大纲知识点梳理, （2）计算机网络的基本概念及分类](https://www.coderli.com/gesp-2-exam-syllabus-network/)
> * [【GESP】C++二级考试大纲知识点梳理, （3）计算机程序设计语言相关知识](https://www.coderli.com/gesp-2-exam-syllabus-coding-language/)
> * [【GESP】C++二级考试大纲知识点梳理, （4）流程图](https://www.coderli.com/gesp-2-exam-syllabus-flow-chart/)
> * [【GESP】C++二级考试大纲知识点梳理, （5）编码与 ASCII](https://www.coderli.com/gesp-2-exam-syllabus-5-coding-ascii/)
> * [【GESP】C++二级考试大纲知识点梳理, （6）数据类型转换](https://www.coderli.com/gesp-2-exam-syllabus-6-type-conversion/)
> * [【GESP】C++二级考试大纲知识点梳理, （7）多层分支结构](https://www.coderli.com/gesp-2-exam-syllabus-7-multibranch/)
> * [【GESP】C++二级考试大纲知识点梳理, （8）多层循环结构](https://www.coderli.com/gesp-2-exam-syllabus-8-multiloop/)
> * [【GESP】C++二级考试大纲知识点梳理, （9）常用数学函数](https://www.coderli.com/gesp-2-exam-syllabus-9-math-functions/)
{: .prompt-tip}

<!--more-->

---

## 一、头文件准备

要使用这些函数，你需要根据函数的来源包含正确的头文件：

1. **`<cmath>`** (或 `<math.h>`): 包含绝大多数数学函数（abs, sqrt, pow 等）。
2. **`<algorithm>`**: 包含算法相关的（max, min）。
3. **`<cstdlib>`** (或 `<stdlib.h>`): 包含随机数相关的（rand, srand, abs(整数版)）。
4. **`<ctime>`** (或 `<time.h>`): 用于获取时间种子（time）。

> 考试时如果不确定，可以直接使用万能头文件 `#include <bits/stdc++.h>`，但了解每个函数的归属是专业素养的体现。
{: .prompt-tip}

---

## 二、常用数值计算函数

### 2.1 绝对值 (Absolute Value)

**数学含义**：$|x|$，即数轴上点到原点的距离（非负数）。

* `abs(int x)`: 用于整数。
* `fabs(double x)`: 用于浮点数。（其实在 C++ 中 `abs` 也可以重载用于浮点数，但 `fabs` 最明确）。

```cpp
cout << abs(-5);    // 输出 5
cout << fabs(-3.14); // 输出 3.14
```

### 2.2 平方根 (Square Root)

**数学含义**：$\sqrt{x}$。

* `sqrt(double x)`: 返回 $x$ 的非负平方根。
* **注意**：参数 $x$ 必须 $\ge 0$。如果传入负数，结果是 `NaN` (Not a Number)。

```cpp
cout << sqrt(16); // 输出 4
cout << sqrt(2);  // 输出 1.414...
```

### 2.3 幂运算 (Power)

**数学含义**：$x^y$。

* `pow(double base, double exp)`: 计算 base 的 exp 次方。
* **注意**：返回值通常是 `double`，如果你算的是整数次方（比如 $2^3$），可能需要强制转换回 `int`。

```cpp
cout << pow(2, 3); // 输出 8
cout << pow(10, 2); // 输出 100
```

### 2.4 最大值和最小值 (Max / Min)

**功能**：比较两个数，返回较大或较小的那个。
* 需包含 `<algorithm>`。

```cpp
cout << max(10, 20); // 输出 20
cout << min(5, 8);   // 输出 5
```

*进阶：如果有 3 个数 a, b, c 怎么求最大值？*
`max(a, max(b, c))` —— 套娃大法好！

{% include custom/custom-post-content-inner.html %}

---

## 三、随机数函数 (Random)

随机数也是必考点，常用于模拟类问题。

### 3.1 `rand()` 函数

* **功能**：返回一个 `0` 到 `RAND_MAX`（通常是 32767 或更大）之间的伪随机整数。
* **问题**：如果不设置种子，每次程序运行产生的随机数序列是一模一样的！

### 3.2 `srand()` 和种子

为了让每次运行结果不一样，我们需要给随机数生成器一个变化的“起点”，通常用当前时间作为种子。

```cpp
#include <cstdlib>
#include <ctime>

int main() {
    // 1. 设置种子（在 main 开头写一次即可）
    srand(time(0)); 
    
    // 2. 生成随机数
    cout << rand(); 
    return 0;
}
```

### 3.3 生成指定范围 [a, b] 的随机数

这是考试重点公式，必须背下来！
目标：生成 $a$ 到 $b$ 之间的随机整数（包含 $a$ 和 $b$）。

**公式**：
$$ r = a + \text{rand}() \% (b - a + 1) $$

**推导**：

1. `rand() % N` 生成的是 $0 \sim N-1$ 的数。
2. 我们需要区间长度是 $b - a + 1$。
3. 所以 `rand() % (b - a + 1)` 生成 $0 \sim (b-a)$。
4. 最后加上偏移量 $a$，范围就变成了 $a \sim b$。

**示例**：生成 1 到 6 的随机数（掷骰子）。

```cpp
int dice = 1 + rand() % 6;
// rand() % 6 -> 0~5
// + 1 -> 1~6
```

---

## 四、考试总结

| 函数 | 说明 | 参数类型 | 返回值 | 需注意 |
| :--- | :--- | :--- | :--- | :--- |
| **abs** | 绝对值 | int | int | 浮点数建议用 fabs |
| **fabs** | 浮点绝对值 | double | double |  |
| **sqrt** | 平方根 | double | double | 参数必须 $\ge 0$ |
| **pow** | 幂运算 | double, double | double | 结果是浮点型 |
| **max** | 最大值 | 任意同类 | 同参数 | 需要 `<algorithm>` |
| **min** | 最小值 | 任意同类 | 同参数 | 需要 `<algorithm>` |
| **ceil** | 向上取整 | double | double | 返回 $\ge x$ 的最小整数 |
| **floor** | 向下取整 | double | double | 返回 $\le x$ 的最大整数 |
| **round** | 四舍五入 | double | double | 返回最接近的整数 |
| **rand** | 随机数 | 无 | int | 记得用公式计算范围 |

掌握了这些工具，你的兵器库里就又多了几件趁手的家伙。无论是解决几何问题（勾股定理用到 sqrt），还是模拟游戏（用到 rand），都能游刃有余。

---

{% include custom/custom-post-content-footer.md %}
