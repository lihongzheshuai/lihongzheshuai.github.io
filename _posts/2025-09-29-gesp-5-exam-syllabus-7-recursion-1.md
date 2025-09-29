---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (7) 递归算法 - 1 基本原理
date: 2025-09-29 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 五级]
---
GESP C++五级官方考试大纲中，共有`9`条考点，本文针对第`7`条考点进行分析介绍。
> （7）掌握递归算法的基本原理，能够应用递归解决问题，能够分析递归算法的时间复杂度和空间复杂度，了解递归的优化策略。
{: .prompt-info}

> 本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

***五级其他考点回顾：***

> * [【GESP】C++五级考试大纲知识点梳理, (1) 初等数论](https://www.coderli.com/gesp-5-exam-syllabus-elementary-number-theory/)
> * [【GESP】C++五级考试大纲知识点梳理, (2) 模拟高精度计算](https://www.coderli.com/gesp-5-exam-syllabus-simulate-high-precision-arithmetic/)
> * [【GESP】C++五级考试大纲知识点梳理, (3-1) 链表-单链表](https://www.coderli.com/gesp-5-exam-syllabus-linked-list-1-singly/)
> * [【GESP】C++五级考试大纲知识点梳理, (3-2) 链表-双向链表](https://www.coderli.com/gesp-5-exam-syllabus-linked-list-2-double/)
> * [【GESP】C++五级考试大纲知识点梳理, (3-3) 链表-单向循环链表](https://www.coderli.com/gesp-5-exam-syllabus-3-linked-list-3-singly-circle/)
> * [【GESP】C++五级考试大纲知识点梳理, (3-4) 链表-双向循环链表](https://www.coderli.com/gesp-5-exam-syllabus-3-linked-list-4-double-circle/)
> * [【GESP】C++五级考试大纲知识点梳理, (4) 辗转相除法、素数表和唯一性定理](https://www.coderli.com/gesp-5-exam-syllabus-4-three-theorem-and-algorithm/)
> * [【GESP】C++五级考试大纲知识点梳理, (5) 算法复杂度估算（多项式、对数）](https://www.coderli.com/gesp-5-exam-syllabus-5-estimation-of-algorithm-polynomial-logarithmic/)
> * [【GESP】C++五级考试大纲知识点梳理, (6) 二分查找和二分答案](https://www.coderli.com/gesp-5-exam-syllabus-6-binary-search/)
{: .prompt-tip}

<!--more-->

---

>在梳理的过程中，我发现想尽可能说清楚考纲要求的内容，越总结篇幅越长，为了避免总结遗漏和阅读匹配，我计算分三次介绍本部分内容，即：
>
> 1. 递归算法基本原理和常见形式
> 2. 递归算法时间、空间复杂度分析
> 3. 递归算法优化策略
>
> 本次为第一部分介绍。
{: .prompt-info}

在计算机科学中，递归算法常被称作“解决问题的艺术”。它的核心思想是：**用同类问题的更小规模去解释和解决原问题**。换句话说，递归就是“自己调用自己”，直到问题被分解到足够简单为止。

## 一、递归的基本原理

**定义**：递归是指函数直接或间接调用自身。

递归解法由两部分组成：

* **基准情形（base case）**：能直接返回结果、不再递归的情形（必须有）。
* **递归情形（recursive case）**：将原问题分解为规模更小的子问题并递归求解，然后把子问题结果组合成原问题的结果。

**工作机制（调用栈）**：每次调用都会在栈上分配一帧（局部变量、返回地址等）。直观理解：递归等同于重复压栈、展开计算、再逐层返回并合并结果。

**示例：** 求阶乘

```cpp
long long fact(int n) {
    if (n <= 1) {
        return 1; // 基准情形，即当n<=1时，直接返回1
    }
    return n * fact(n-1); // 递归情形
}
```

**调用 `fact(4)` 的执行顺序**：

* `fact(4)` 调用 `fact(3)`。
* `fact(3)` 调用 `fact(2)`。
* `fact(2)` 调用 `fact(1)`。
* `fact(1)` 直接返回 `1`。
* `fact(2)` 返回 `2 * 1 = 2`。
* `fact(3)` 返回 `3 * 2 = 6`。
* `fact(4)` 返回 `4 * 6 = 24`。

---

## 二、常见递归模式

>本部分涉及5种常见递归模式，前3种相对比较容易理解，后2种相对比较复杂。暂不理解执行过程我认为也不必太过纠结，可通过后续的编程练习我们一起逐步理解、加深。
{: .prompt-tip}

### 2.1 线性递归（Linear Recursion）

**线性递归（Linear recursion）**：每次只递归一个子问题（如：链表长度、阶乘、递归求和）。

**例题：** 求 n 的阶乘

数学定义：
$$
n! = \begin{cases}
1, & n=0 \text{ 或 } n=1\\
n \times (n-1)!, & n>1
\end{cases}
$$

**代码示例：**

```cpp
long long factorial(int n) {
    if (n <= 1) {
        return 1; // 基准情形，即当n<=1时，直接返回1
    }
    return n * factorial(n - 1); // 递归情形
}
```

**调用过程：**

```cpp
factorial(4)
= 4 * factorial(3)
= 4 * (3 * factorial(2))
= 4 * (3 * (2 * factorial(1)))
= 4 * 3 * 2 * 1
```

特点：递归链条像一条直线，逐层压栈，再逐层返回。

---

### 2.2 树形递归（Tree Recursion）

**二叉/树形递归（Tree recursion）**：每次递归产生多个子调用（如：斐波那契朴素实现、二叉树遍历）。

**例题：** 斐波那契数列

数学定义：
$$
F(n) = \begin{cases}
0, & n=0 \\
1, & n=1 \\
F(n-1) + F(n-2), & n>1
\end{cases}
$$

**代码示例：**

```cpp
int fibonacci(int n) {
    if (n <= 1) {
        return n; // 基准情形，即当n<=1时，直接返回n
    }
    return fibonacci(n-1) + fibonacci(n-2); // 两个递归分支
}
```

**调用过程（树状展开）：**

```cpp
fibonacci(4)
= fibonacci(3) + fibonacci(2)

fibonacci(3) = fibonacci(2) + fibonacci(1)
fibonacci(2) = fibonacci(1) + fibonacci(0)
```

最终形成一棵二叉树，节点数量随 n 指数增长。

特点：同一个子问题会被多次计算（如 fibonacci(2) 重复出现）。

---

### 2.3 分治（Divide & Conquer）

**分治（Divide & Conquer）**：把问题分为若干独立子问题，子问题规模通常是 `n/2` 等（如：归并排序、快速排序、二分搜索）。

**例题：** 二分查找，在有序数组中查找目标值。

**代码示例：**

```cpp
// 二分查找递归实现：在有序数组 arr 的 [left, right] 区间内查找 target
int binarySearch(vector<int>& arr, int left, int right, int target) {
    // 递归终止条件：区间为空，查找失败
    if (left > right) {
        return -1;  // 查找失败，未找到目标值
    }
    int mid = (left + right) / 2; // 计算中间位置
    if (arr[mid] == target) {
        return mid;     // 找到目标值，返回下标
    } else if (arr[mid] > target) { // 目标值在左半区间
        return binarySearch(arr, left, mid - 1, target);
    } else {                       // 目标值在右半区间
        return binarySearch(arr, mid + 1, right, target);
    }
}
```

**调用过程：** 例如：binarySearch([1,3,5,7,9], target=7)

```cpp
查 [1..9], mid=5 → target > 5 → 去右半边
查 [7..9], mid=7 → 找到
```

特点：每次递归只进入一个分支，问题规模减半。

---

### 2.4 回溯（Backtracking / DFS）

**回溯（Backtracking / DFS）**：在解空间树上做深度优先搜索并回退（如：全排列、子集、N 皇后）。

**例题：全排列** 给定数组，输出所有排列。

**基本算法逻辑**  

1. 固定第 1 位，依次与后面每个元素交换，得到新首元素；  
2. 对剩余部分递归执行“固定+交换”，直到只剩 1 个元素，即得到一个完整排列；  
3. 回溯：撤销刚才的交换，恢复数组原状，继续尝试下一个候选。  

如此深度优先地“选-递归-回退”，即可不重不漏地生成全部 n! 种排列。

**代码：**

```cpp
// 回溯法生成全排列
void backtrack(vector<int>& nums, int start, vector<vector<int>>& result) {
    // 如果已经到达数组末尾，说明生成了一个完整排列
    if (start == nums.size()) {         
        result.push_back(nums); // 保存当前排列
        return;
    }
    // 枚举当前位置可以选择的所有数字
    for (int i = start; i < nums.size(); ++i) {
        swap(nums[start], nums[i]);     // 选择：将第 i 个数字放到当前位置
        backtrack(nums, start + 1, result); // 递归：处理下一个位置
        swap(nums[start], nums[i]);     // 撤销选择（回溯）：恢复原状
    }
}
```

**调用过程：**

```cpp
第一层：选择 1 → 递归排列 [2,3]
    第二层：选择 2 → 递归排列 [3]
        第三层：选择 3 → 得到 [1,2,3]
        回溯 → 撤销 3
    第二层：选择 3 → 递归排列 [2]
        第三层：选择 2 → 得到 [1,3,2]
        回溯 → 撤销 2
    回溯 → 撤销 1
...
```

* 特点：典型“试探—回溯”过程，像深度优先搜索。

---

### 2.5 尾递归（Tail Recursion）

**尾递归（Tail recursion）**：递归调用是函数最后一步（有利于编译器优化为循环，但 C++ 不保证 尾调用优化（TCO））。

**例题：** 阶乘（尾递归写法）与线性递归不同，这里递归调用在函数末尾。

**代码：**

```cpp
long long factorialTail(int n, long long acc = 1) {
    // 基准情形：当 n ≤ 1 时，累积结果 acc 即为阶乘值，直接返回
    if (n <= 1) {
        return acc;  // 基准情形
    }
    // 尾递归：将当前累积值 acc * n 作为参数传入下一次调用
    // 问题规模缩小为 n-1，保持调用栈深度不变（可优化为循环）
    return factorialTail(n - 1, acc * n); // 尾递归
}
```

>注：C++ 标准并不保证尾递归优化（TCO），但尾递归写法可轻松转化为迭代。
{: .prompt-tip}

**调用过程：**

```cpp
factorialTail(4, 1)
→ factorialTail(3, 4)
→ factorialTail(2, 12)
→ factorialTail(1, 24)
返回 24
```

特点：递归调用在函数最后一步，状态通过参数传递，没有额外计算，容易转为迭代。

---

### 2.6 小结

* 线性递归 → 一条直链，逐层返回。
* 树形递归 → 每层分支，形成递归树。
* 分治 → 每次只走一个分支，问题规模缩小。
* 回溯 → 深度探索，遇到尽头再回退。
* 尾递归 → 类似循环，参数不断更新。

---
{% include custom/custom-post-content-footer.md %}
