---
layout: post
title: 【GESP】C++一级考试大纲知识点梳理(考点12), (5) 循环结构
date: 2025-12-31 08:30 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 基础语句]
categories: [GESP, 一级]
---
如果不使用循环，计算机的强大计算能力就无法体现。**循环** (Loop) 是编程中最常用的结构之一，它让我们可以用几行代码完成成千上万次的重复计算。本篇对应大纲第 `12` 条考点。

> （12）掌握循环结构程序的编写，掌握 for、while、do-while 循环语句的使用以及 continue 语句和 break 语句在循环中的应用。
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

## 一、三种循环语句

> 对应考点：（12）掌握循环结构程序的编写，掌握 for、while、do-while 循环语句的使用。

C++ 提供了三种循环：`for`、`while` 和 `do-while`。一级考试要求全部掌握。

### 1.1 `for` 循环

最常用、结构最紧凑的循环，适合**已知循环次数**的情况。

```cpp
// 语法结构
for (初始化; 条件判断; 变量更新) {
    // 循环体：需要重复执行的代码
}

// 示例：输出 1 到 5
for (int i = 1; i <= 5; i++) {
    cout << i << " "; 
}
// 输出：1 2 3 4 5
```

### 1.2 `while` 循环

适合**循环次数未知**，只知道循环条件的情况。

```cpp
// 语法结构
while (条件) {
    // 循环体
    // 注意：一定要在内部改变条件，否则会变成“死循环”！
}

// 示例：输出 1 到 5
int i = 1;
while (i <= 5) {
    cout << i << " ";
    i++; // 千万别忘了这一步
}
```

### 1.3 `do-while` 循环

比较少用。特点是**先执行一次循环体，再判断条件**。也就是说，无论条件是否成立，循环体**至少会执行一次**。

```cpp
int i = 6;
do {
    cout << i << endl;
    i++;
} while (i <= 5); // 注意这里有个分号
// 输出：6 （虽然 6<=5 不成立，但还是输出了一次）
```

---

## 二、循环控制语句

> 对应考点：（12）掌握 continue 语句和 break 语句在循环中的应用。

有时候我们需要在循环过程中强行退出或跳过某一次循环，这就需要用到 `break` 和 `continue`。

### 2.1 `break` (跳出)

**作用**：立即**终止**整个循环，跳出循环体，执行循环后面的代码。
**场景**：找到了想要的结果，不需要再找了。

```cpp
// 寻找第一个能被 7 整除的数（从 1 开始）
for (int i = 1; i <= 100; i++) {
    if (i % 7 == 0) {
        cout << "找到了：" << i << endl;
        break; // 找到了就跑，不用再往后试了
    }
}
```

### 2.2 `continue` (继续)

**作用**：立即**结束本次循环**（跳过 `continue` 后面尚未执行的代码），直接进入下一次循环条件的判断。
**场景**：当前的这个数不符合要求，直接看下一个。

```cpp
// 输出 1 到 5 中，除了 3 以外的数
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        continue; // 遇到 3 就跳过本次循环，不执行下面的 cout
    }
    cout << i << " ";
}
// 输出：1 2 4 5
```

---

## 三、经典算法案例：累加求和

这是循环最基础的应用：计算 $1 + 2 + 3 + ... + n$ 的和。

```cpp
#include <iostream>
using namespace std;

int main() {
    int n, sum = 0; // sum 必须初始化为 0！
    cin >> n;
    
    for (int i = 1; i <= n; i++) {
        sum = sum + i; // 把 i 累加到盒子 sum 里
    }
    
    cout << sum << endl;
    
    return 0;
}
```

---

## 四、考试总结

1.  **死循环**：写 `while` 循环时，时刻警惕是否有一个“出口”，或者循环变量是否在更新，否则程序会卡死（Time Limit Exceeded）。
2.  **边界问题**：`i <= n` 还是 `i < n`？这是通过 `for` 循环时的常见错误，需要根据题目要求仔细判定。
3.  **变量初始化**：涉及累加（求和）、累乘（求积）时，变量 `sum` 一定要初始化（求和为0，求积为1）。

一级考试对循环的考察通常比较基础，不会涉及太复杂的嵌套循环（那是二级的内容），重点在于理解循环的执行流程。

{% include custom/custom-post-content-footer.md %}
