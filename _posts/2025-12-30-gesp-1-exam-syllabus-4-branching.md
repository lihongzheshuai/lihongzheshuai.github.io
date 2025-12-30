---
layout: post
title: 【GESP】C++一级考试大纲知识点梳理(考点7,8,11), (4) 逻辑运算与分支结构
date: 2025-12-30 09:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 基础语句]
categories: [GESP, 一级]
---
程序如果不只是“流水账”，就需要具备**做判断**的能力。GSEP 一级考试的核心难点往往就出现在条件判断和下一篇的循环上。本篇涉及考点 `7`、`8`、`11`。

> （7）掌握逻辑运算与（&&）、或（||）、非（！）。
> （8）掌握关系运算：大于、大于等于、小于、小于等于、等于、不等于。
> （11）掌握分支结构程序的编写，掌握 if 语句、if-else 语句、switch 语句，了解三目运算。
{: .prompt-info}

***一级考点系列：***

> * [【GESP】C++一级考试大纲知识点梳理（1）计算机基础和操作系统](https://www.coderli.com/gesp-1-exam-syllabus-computer-basics/)
> * [【GESP】C++一级考试大纲知识点梳理(考点2,4,10,13), (2) 开发环境与程序基础](https://www.coderli.com/gesp-1-exam-syllabus-2-env-basics/)
> * [【GESP】C++一级考试大纲知识点梳理(考点3,5,6,9), (3) 变量、数据类型与输入输出](https://www.coderli.com/gesp-1-exam-syllabus-3-data-io/)
> * [【GESP】C++一级考试大纲知识点梳理(考点7,8,11), (4) 逻辑运算与分支结构](https://www.coderli.com/gesp-1-exam-syllabus-4-branching/)
> * [【GESP】C++一级考试大纲知识点梳理(考点12), (5) 循环结构](https://www.coderli.com/gesp-1-exam-syllabus-5-loops/)
{: .prompt-tip}

<!--more-->

---

## 一、关系运算 (Relational Operators)

> 对应考点：（8）掌握关系运算：大于、大于等于、小于、小于等于、等于、不等于。

关系运算就是“比较”，结果只有两种：**真 (true/1)** 或 **假 (false/0)**。

| 符号 | 含义 | 示例 | 结果 |
| :--- | :--- | :--- | :--- |
| `>` | 大于 | `5 > 3` | `true` |
| `<` | 小于 | `5 < 3` | `false` |
| `>=` | 大于等于 | `5 >= 5` | `true` |
| `<=` | 小于等于 | `4 <= 5` | `true` |
| `==` | **等于** | `5 == 5` | `true` |
| `!=` | **不等于** | `5 != 3` | `true` |

> ⚠️ **高频扣分点**：C++ 中判断相等用由两个等号组成的 `==`。一个等号 `=` 是赋值！
> `if (a = 5)` 永远为真（因为先把 5 赋给 a，表达式的值为 5，非 0 即真），这是初学者最容易犯的逻辑错误。

---

## 二、逻辑运算 (Logical Operators)

> 对应考点：（7）掌握逻辑运算与（&&）、或（||）、非（！）。

当我们需要组合多个条件时（例如：既要大于 10，又要小于 20），就需要用到逻辑运算。

| 符号 | 名称 | 含义 | 口诀 |
| :--- | :--- | :--- | :--- |
| `&&` | **逻辑与** (AND) | 两个条件**都成立**，结果才为真 | 一假则假，全真才真 |
| `||` | **逻辑或** (OR) | 两个条件**只要有一个成立**，结果就为真 | 一真则真，全假才假 |
| `!` | **逻辑非** (NOT) | 颠倒黑白 | 真变假，假变真 |

**示例**：判断变量 `x` 是否在区间 `[10, 20]` 内：

* `x >= 10 && x <= 20` (正确)
* ⚠️ **高频扣分点**：`10 <= x <= 20` (错误！这是数学写法，C++ 会先算 `10<=x` 得到 0 或 1，再用 0 或 1 去比较 `<=20`，结果永远是真)

---

## 三、分支结构 (Control Flow)

> 对应考点：（11）掌握分支结构程序的编写，掌握 if 语句、if-else 语句、switch 语句，了解三目运算。

### 3.1 `if` 语句
也就是“如果...就...”。

```cpp
if (条件) {
    // 条件成立时执行的代码
}
```

### 3.2 `if-else` 语句
也就是“如果...就...，否则...”。

```cpp
if (条件) {
    // 条件成立时执行
} else {
    // 条件不成立时执行
}
```

### 3.3 多重分支 (`if-else if-else`)
用于处理多种情况。

```cpp
int score = 85;
if (score >= 90) {
    cout << "优秀";
} else if (score >= 80) {
    cout << "良好"; // 满足 >=80 且 <90
} else if (score >= 60) {
    cout << "及格";
} else {
    cout << "不及格";
}
```

### 3.4 `switch` 语句
适用于**整数**或**字符**类型的**等值判断**。结构清晰，但不够灵活（不能直接判断范围）。

```cpp
char grade = 'A';
switch (grade) {
    case 'A':
        cout << "Great!";
        break; // 别忘了 break，否则会穿透往下执行
    case 'B':
        cout << "Good!";
        break;
    default: // 相当于 else
        cout << "Other";
}
```

### 3.5 三目运算符 (`? :`)
一种简写的 `if-else`，格式为：`条件 ? 真值 : 假值`。

```cpp
int a = 10, b = 20;
int maxVal = (a > b) ? a : b; // 如果 a > b，取 a，否则取 b
```

---

## 四、经典案例：判断闰年

这是一个几乎必考的逻辑题。**规则**：

1. 能被 4 整除，但不能被 100 整除。
2. 或者，能被 400 整除。

这就是一个**综合运用逻辑运算符**的例子。

```cpp
#include <iostream>
using namespace std;

int main() {
    int year;
    cin >> year;
    
    // 逻辑翻译：(被4整除 AND 不被100整除) OR (被400整除)
    if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) {
        cout << year << " 是闰年" << endl;
    } else {
        cout << year << " 是平年" << endl;
    }
    
    return 0;
}
```

{% include custom/custom-post-content-footer.md %}
