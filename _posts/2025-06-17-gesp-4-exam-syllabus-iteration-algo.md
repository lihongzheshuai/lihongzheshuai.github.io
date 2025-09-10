---
layout: post
title: 【GESP】C++四级考试大纲知识点梳理, (6) 递推算法
date: 2025-06-17 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 四级]
---
GESP C++四级官方考试大纲中，共有11条考点，本文针对第6条考点进行分析介绍。
> （6）掌握递推算法基本思想、递推关系式的推导以及递推问题求解。
{: .prompt-info}

***四级其他考点回顾：***

> * [【GESP】C++四级考试大纲知识点梳理, (1) 指针](https://www.coderli.com/gesp-4-exam-syllabus-pointer/)
> * [【GESP】C++四级考试大纲知识点梳理, (2) 结构体和二维数组](https://www.coderli.com/gesp-4-exam-syllabus-struct-two-dimensional-array/)
> * [【GESP】C++四级考试大纲知识点梳理, (3) 模块化和函数](https://www.coderli.com/gesp-4-exam-syllabus-module-function/)
> * [【GESP】C++四级考试大纲知识点梳理, (4) 变量和作用域](https://www.coderli.com/gesp-4-exam-syllabus-variable-scope/)
> * [【GESP】C++四级考试大纲知识点梳理, (5) 值传递](https://www.coderli.com/gesp-4-exam-syllabus-pass-by-value-reference-pointer/)
{: .prompt-tip}

<!--more-->

---

## 一、递推算法基本思想

### 1.1 什么是递推？

递推是一种**通过已知值一步步推导出未知值**的算法策略，常用于解决“当前状态依赖前一个或前几个状态”的问题。

### 1.2 与递归的区别

| 特点   | 递推（Iteration） | 递归（Recursion） |
| ---- | ------------- | ------------- |
| 实现方式 | 循环            | 函数调用自身        |
| 计算顺序 | 自底向上          | 自顶向下          |
| 适合场景 | 数组/动态规划       | 树形结构、DFS等     |
| 资源消耗 | 更节省空间         | 占用调用栈多        |

### 1.3 递推的基本思想

**基本思想：**
先确定问题的**初始状态（边界条件）**，然后找出一个**从已知项推出下一项的规则（递推关系式）**，依次推算出目标项。

---

## 二、推导递推关系式的步骤

### 🔶 Step 1：确定状态（State）

用一个变量或数组表示问题的某个子结果。

例：`f[i]` 表示问题的第 `i` 步或状态。

### 🔶 Step 2：写出初始条件（Base Case）

找出最简单、已知的初始值，作为递推起点。

### 🔶 Step 3：建立递推关系（Transition）

分析当前状态与前面状态的关系，写出“状态转移公式”。

### 🔶 Step 4：使用循环进行求解

利用循环结构逐步计算出最终结果。

---

## 三、递推问题示例

### 🌟 例题 1：斐波那契数列

**❓题目描述：**

定义斐波那契数列如下：

* F(1) = 1
* F(2) = 1
* F(n) = F(n-1) + F(n-2)（n ≥ 3）

求 F(n)

---

**💭 递推分析：**

* 状态表示：`f[i]` 表示第 i 项的值
* 初始值：`f[1] = 1`, `f[2] = 1`
* 递推关系：`f[i] = f[i-1] + f[i-2]`

**💻 C++示例代码：**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int f[100] = {0};
    f[1] = f[2] = 1;
    for (int i = 3; i <= n; i++) {
        f[i] = f[i-1] + f[i-2];
    }
    cout << f[n] << endl;
    return 0;
}
```

---

### 🌟 例题 2：青蛙跳台阶

**❓题目描述：**

一只青蛙每次可以跳1级或2级台阶，跳上 `n` 级台阶有多少种跳法？

**### 💭 递推分析：**

* 状态表示：`f[i]` 表示跳上第 i 级的跳法数
* 初始值：

  * `f[0] = 1`（跳0级也算1种方式）
  * `f[1] = 1`
* 递推关系：

  * 跳到第 `i` 级，要么从 `i-1` 跳一步来，要么从 `i-2` 跳两步来
  * 所以 `f[i] = f[i-1] + f[i-2]`

**💻 C++代码示例：**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int f[100] = {0};
    f[0] = 1;
    f[1] = 1;
    for (int i = 2; i <= n; i++) {
        f[i] = f[i-1] + f[i-2];
    }
    cout << f[n] << endl;
    return 0;
}
```

---

### 🌟 例题 3：完全背包计数问题

**❓题目描述：**

有 `n` 种物品，每种物品可以选无限次。给定目标体积 `V`，求组合出体积为 `V` 的方法数。

> 输入：物品体积数组 `a[1..n]`，目标体积 `V`
> 输出：组合数

---

**💭 递推分析：**

* 状态表示：`f[i]` 表示体积为 `i` 的方案数
* 初始值：`f[0] = 1`（表示体积为0只有1种方式——不选）
* 状态转移：对每个物品 `a[i]`，从小到大更新 `f[v]`：

```cpp
for i in 1..n:
    for j in a[i]..V:
        f[j] += f[j - a[i]]
```

**💻 C++代码示例：**

```cpp
#include <iostream>
using namespace std;

int main() {
    int n, V;
    cin >> n >> V;
    int a[100];
    for (int i = 0; i < n; i++) cin >> a[i];

    int f[10001] = {0};
    f[0] = 1;
    for (int i = 0; i < n; i++) {
        for (int j = a[i]; j <= V; j++) {
            f[j] += f[j - a[i]];
        }
    }
    cout << f[V] << endl;
    return 0;
}
```

---

## 四、总结：递推建模口诀

> **“状态表示”要准确，
> “初始条件”需齐全，
> “转移方程”需逻辑清晰，
> “遍历顺序”不能错乱。**

---

## 五、递推与编程竞赛

在竞赛或算法题中，掌握递推思想有助于：

* **建模问题为状态转移**
* **找出高效的迭代计算方式**
* **避免暴力递归导致的栈溢出与重复计算**

**注意事项：**

* **初始值必须正确**：否则递推会错误。
* **数组开足空间**：避免越界。
* **注意边界处理**：循环范围要与初始值协调。
* **可以用滚动变量优化空间**：如只需最近两项，可以不用整个数组。

递推是一种**由小及大、由已知求未知**的思维方式，在算法设计中非常实用。掌握它需要多观察、思考状态之间的联系，并尝试用**数学规律或状态转移公式**表达问题的本质。

---
{% include custom/custom-post-content-footer.md %}
