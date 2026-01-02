---
layout: post
title: 【GESP】C++二级考试大纲知识点梳理, （7）多层分支结构
date: 2026-01-02 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 分支嵌套]
categories: [GESP, 二级]
---

程序并不总是一条直线走到底，经常需要根据情况“拐弯”。一级考试要求掌握简单的 `if`，而二级考试的难度立刻升级到了**多层嵌套**。这就是逻辑思维能力的体现。本篇详细剖析大纲第 7 条考点。

> （7）掌握多层分支结构，掌握 if 语句、if...else 语句、switch 语句，及相互嵌套的方法。
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

## 一、多层分支结构 (Nested if-else)

所谓的“多层分支”，通俗点说就是**套娃**：在 `if` 或 `else` 的大括号里，再写 `if`。
这通常用于处理**多维度**或**递进式**的判断条件。

### 1.1 语法结构

```cpp
if (条件A) {
    if (条件B) {
        // 条件A 和 条件B 都满足
    } else {
        // 条件A 满足，但 条件B 不满足
    }
} else {
    // 条件A 不满足
}
```

### 1.2 经典案例：闰年判断

判断某一年是否为闰年，是嵌套分支的经典练兵场。

**规则**：
1. 能被 4 整除。
2. 但（如果是整百年）必须能被 400 整除。

**写法 1：逻辑运算符（扁平化，推荐）**

```cpp
if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) {
    cout << "是闰年";
}
```

**写法 2：嵌套结构（层层递进，考点所在）**

```cpp
if (year % 4 == 0) {
    // 可能是，还得看是不是整百
    if (year % 100 == 0) {
        // 是整百，那得看能不能被400整除
        if (year % 400 == 0) 
            cout << "是闰年";
        else 
            cout << "不是闰年";
    } else {
        // 能被4整除且不是整百
        cout << "是闰年";
    }
} else {
    cout << "不是闰年";
}
```
*虽然写法 2 看着繁琐，但它清晰展示了判断的步骤。在复杂的业务逻辑中，嵌套结构往往比一个超长的 `&& / ||` 表达式更容易阅读和调试。*

### 1.3 悬空 else 问题 (Dangling else)

这是一个经典的 C++ 坑点。**原则**：`else` 总是与**最近的、未配对的** `if` 结合。

```cpp
if (A)
    if (B)
        cout << "B";
else // 这个 else 属于谁？
    cout << "C";
```

**答案**：这个 `else` 属于 `if(B)`！如果 `A` 为真且 `B` 为假，输出 C。如果 `A` 为假，啥也不输出。
**建议**：无论只有一行代码还是多行，**永远加上大括号 `{}`**，这样能彻底杜绝歧义。

```cpp
if (A) {
    if (B) {
        cout << "B";
    } else {
        cout << "C";
    }
}
```

---

## 二、Switch 语句

`switch` 是一种专门用于**多选一**的结构，特别适合判断**整型**或**字符型**的具体数值（离散值）。

### 2.1 语法结构

```cpp
switch (表达式) {
    case 常量1:
        // 代码块 1
        break; // 必不可少！
    case 常量2:
        // 代码块 2
        break;
    ...
    default:
        // 如果上面都没匹配上，执行这里
        break;
}
```

### 2.2 核心要点

1. **类型限制**：`switch` 括号里的表达式结果必须是 **整数 (int, long, char)**。不能是 `double`，也不能是字符串。

2. **Break 非常重要**：
    * `break` 的作用是跳出 switch。
    * 如果没有 `break`，程序会**“穿透” (Fall-through)**：继续向下执行下一个 `case` 的代码，不管条件是否匹配！
    * *利用穿透特性：* 比如输入月份判断季节，3,4,5 月都是春季，可以写在一起。
      ```cpp
      switch (month) {
          case 3:
          case 4:
          case 5:
              cout << "春季";
              break;
      }
      ```

3. **Case 必须是常量**：不能写 `case a > 5:` 这种范围判断。

### 2.3 案例：简单的计算器

输入两个数和一个运算符 `+ - * /`，输出结果。
```cpp
double a, b;
char op;
cin >> a >> op >> b;

switch (op) {
    case '+': 
        cout << a + b; 
        break;
    case '-': 
        cout << a - b; 
        break;
    case '*': 
        cout << a * b; 
        break;
    // 注意除法分母不能为0
    case '/': 
        if (b != 0) cout << a / b;
        else cout << "Error";
        break;
    default: 
        cout << "无效符号";
}
```

{% include custom/custom-post-content-inner.html %}

---

## 三、if-else if 还是 switch？

| 场景 | 推荐使用 | 理由 |
| :--- | :--- | :--- |
| **范围判断** (如 `score >= 90`) | `if-else` | switch 没法直接处理范围 |
| **浮点数判断** | `if-else` | switch 不支持 float/double |
| **特定点值匹配** (如 `按下按键 1, 2, 3`) | `switch` | 代码结构更清晰，效率略高 |
| **复杂逻辑** (嵌套多) | `if-else` | 灵活性最强 |

---

## 四、备考技巧

1. **缩进要规范**：写嵌套分支时，一定要注意代码缩进。乱糟糟的格式会让你在检查逻辑时瞬间崩溃。
2. **大括号不要省**：虽然 C++ 允许单行省略 `{}`，但考试或写复杂逻辑时，请务必加上。
3. **注意边界**：多层分支极其容易漏掉某些情况（比如 `else` 没写全），写完代码后，试着在脑子里跑几个测试用例覆盖所有分支。

---

{% include custom/custom-post-content-footer.md %}
