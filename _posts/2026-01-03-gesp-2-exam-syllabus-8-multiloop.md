---
layout: post
title: 【GESP】C++二级考试大纲知识点梳理, （8）多层循环结构
date: 2026-01-03 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 多重循环]
categories: [GESP, 二级]
---
如果说单层循环是“跑圈”，那么多层循环就是“时钟”。掌握多层循环，就能解决著名的“打印图形”和“穷举求解”类问题，这是二级考试中最核心的难点之一。本篇详细剖析大纲第 8 条考点。

> （8）掌握多层循环结构，掌握 for 语句、while 语句、do...while 语句，及相互嵌套的方法。
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

## 一、嵌套循环的“时钟模型”

### 1.1 什么是嵌套循环？

简单说，就是在一个循环体里面，再写一个循环。
`for` 套 `for`，`while` 套 `while`，或者 `for` 套 `while` 都可以。

### 1.2 核心逻辑：外层走一步，内层跑一圈

想象一个时钟：

* **外层循环**好比**时针**。
* **内层循环**好比**分针**。

时针走 1 格（外层循环执行 1 次），分针就要走 60 格（内层循环要把它的所有次数都执行完）。

```cpp
// 外层循环：i 从 1 到 3
for (int i = 1; i <= 3; i++) {
    cout << "外层第" << i << "次: ";
    
    // 内层循环：j 从 1 到 5
    // 【重点】每次外层进来，j 都会重新从 1 开始！
    for (int j = 1; j <= 5; j++) {
        cout << j << " ";
    }
    cout << endl;
}
/* 输出：
外层第1次: 1 2 3 4 5 
外层第2次: 1 2 3 4 5 
外层第3次: 1 2 3 4 5 
*/
```

---

## 二、经典应用 1：打印图形

在二级考试中，**打印图形**是嵌套循环最直观的应用。
**解题口诀**：

1. **外层循环**控制**行数**（高度）。
2. **内层循环**控制**列数**（每一行打印的内容）。
3. **找规律**：找到每一行的符号数量与行号 `i` 的关系。

### 2.1 打印矩形

打印 $n$ 行 $n$ 列的星号。
```cpp
for (int i = 1; i <= n; i++) {       // 控制行
    for (int j = 1; j <= n; j++) {   // 控制列
        cout << "*";
    }
    cout << endl; // 每一行结束记得换行！
}
```

### 2.2 打印直角三角形

第 1 行 1 个星，第 2 行 2 个星 ... 第 $i$ 行 $i$ 个星。

* 行数：$1 \sim n$
* 列数：$1 \sim i$ （内层循环的终点是变量 $i$）

```cpp
for (int i = 1; i <= n; i++) {
    // 这里的 j <= i 是关键！
    for (int j = 1; j <= i; j++) {
        cout << "*";
    }
    cout << endl;
}
```

### 2.3 打印乘法口诀表

这就和直角三角形一模一样！
```cpp
for (int i = 1; i <= 9; i++) {
    for (int j = 1; j <= i; j++) {
        cout << j << "*" << i << "=" << i*j << "\t";
    }
    cout << endl;
}
```

{% include custom/custom-post-content-inner.html %}

---

## 三、经典应用 2：穷举求解 (暴力破解)

计算机最擅长的就是“笨办法”——把所有可能性都试一遍。这就是**穷举法**（Enumeration）。
对于多变量问题，通常用多层循环来实现。

### 3.1 案例：百钱百鸡
**题目**：公鸡 5 元一只，母鸡 3 元一只，小鸡 1 元 3 只。用 100 元买 100 只鸡，问公鸡、母鸡、小鸡各多少只？

**分析**：

* 设公鸡 $x$ 只，母鸡 $y$ 只，小鸡 $z$ 只。
* 条件 1：$x + y + z = 100$
* 条件 2：$5x + 3y + z/3 = 100$ （这里的 $z/3$ 在编程中要注意整除问题，最好写成 $15x + 9y + z = 300$ 或者保证 $z \% 3 == 0$）

**代码实现**：
```cpp
// 确定边界：100元全买公鸡最多20只，全买母鸡最多33只
for (int x = 0; x <= 20; x++) {
    for (int y = 0; y <= 33; y++) {
        // 【优化技巧】小鸡不用循环试，直接算出来！
        int z = 100 - x - y;
        
        // 验证条件：
        // 1. 钱数总和为100
        // 2. 小鸡必须是3的倍数（题目说1元3只，通常隐含整数买卖）
        if (z % 3 == 0 && 5 * x + 3 * y + z / 3 == 100) {
            cout << "公鸡:" << x << " 母鸡:" << y << " 小鸡:" << z << endl;
        }
    }
}
```

---

## 四、break 和 continue 在嵌套中的表现

> **`break` 和 `continue` 只对它所在的“那一层”循环有效！**
> 它**不能**直接跳出多层循环。
{: .prompt-warning}

```cpp
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 5; j++) {
        if (j == 3) break; // 只跳出内层循环！
        cout << "(" << i << "," << j << ") ";
    }
    cout << "EndInner ";
}
/* 输出片段：
(1,1) (1,2) EndInner (2,1) (2,2) EndInner ...
*/
```
如果想直接跳出所有循环（比如找到了答案），通常有两种办法：

1. 使用 `goto` 语句（虽不推荐但有效）。
2. 设置一个 `bool` 旗帜变量，在外层检测到旗帜也进行 `break`。
3. 直接 `return 0` 结束整个程序。

---

## 五、时间复杂度初探

虽然二级不考复杂的算法分析，但要有**效率意识**。

* 单层循环 $n$ 次：复杂度 $O(n)$。
* 双层循环 $n \times n$ 次：复杂度 $O(n^2)$。

当 $n = 1000$ 时：

* $O(n)$ 大约运行 1000 次，瞬间完成。
* $O(n^2)$ 大约运行 1,000,000 次（一百万），也很快。
* 但如果 $n = 100000$，$O(n^2)$ 就是 100 亿次，现在的普通电脑就要跑几十秒甚至更久了（超时）。

所以在写多层循环时，要看看 $n$ 有多大。对于 $n \le 1000$ 的范围，双层循环通常是安全的。

---

{% include custom/custom-post-content-footer.md %}
