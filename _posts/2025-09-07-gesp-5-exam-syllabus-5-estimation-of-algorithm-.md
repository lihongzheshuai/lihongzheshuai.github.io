---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (5) 掌握算法复杂度估算方法（含多项式、对数）
date: 2025-09-07 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 五级]
---
GESP C++五级官方考试大纲中，共有`9`条考点，本文针对第`5`条考点进行分析介绍。
> （5）掌握算法复杂度估算方法（含多项式、对数）。
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
{: .prompt-tip}

<!--more-->

---

## 一、算法复杂度回顾

关于算复杂的`基本概念`、`常见复杂度介绍`以及`基本的估算方法`我们已经在四级考试大纲：[【GESP】C++四级考试大纲知识点梳理, (9) 简单算法复杂度的估算](https://www.coderli.com/gesp-4-exam-syllabus-estimation-of-algorithm-time-complexity/)中基本都有介绍，这里就不再赘述。

本次直接介绍`多项式复杂度`和`对数复杂度`的常见例子和估算方法。

---

## 二、多项式复杂度

### 2.1 定义

* **多项式复杂度**：算法执行步骤数是输入规模 $n$ 的多项式函数，例如

  $$
  O(n),\ O(n^2),\ O(n^3),\dots
  $$
* 一般来自 **嵌套循环**，循环层数越多，次数相乘，指数越高。

### 2.2 常见场景

* 简单循环、嵌套循环。
* 逐个比较、逐个交换的排序算法。

### 2.3 排序算法例子：冒泡排序

```cpp
void bubbleSort(int a[], int n) {
    for (int i = 0; i < n; i++) {          // n 次
        for (int j = 0; j < n - i - 1; j++) { // n 次
            if (a[j] > a[j+1])
                swap(a[j], a[j+1]);
        }
    }
}
```

分析：

* 外层循环 $n$ 次
* 内层循环 $n$ 次
* 总操作 $n \times n = n^2$
* **复杂度：$O(n^2)$**

👉 **结论**：冒泡排序、选择排序、插入排序这类算法，普遍是 **多项式复杂度**。

---

## 三、对数复杂度

### 3.1 定义

* **对数复杂度**：算法执行步骤数与 $\log n$ 成正比，例如

  $$
  O(\log n),\ O(n \log n)
  $$
* 常见于：

  * **每次把问题规模缩小一半**（二分查找、倍增循环）。
  * **分治递归**（排序算法：快速排序、归并排序、堆排序）。

### 3.2 常见场景

* 二分查找：$\log n$
* 分治排序：$n \log n$
* 堆调整操作：$\log n$

### 3.3 排序算法例子

#### (1) 快速排序

```cpp
void quickSort(int a[], int l, int r) {
    // 基准情况：当区间长度为1或更小时，直接返回
    if (l >= r) return;
    
    // partition操作的时间复杂度为O(n)
    // 每次选择一个基准值，将数组分为两部分
    int pivot = partition(a, l, r); // O(n)
    
    // 递归处理左右两个子数组
    // 每次递归将问题规模缩小一半左右
    // 递归树的深度为log n
    quickSort(a, l, pivot - 1);     // T(n/2)
    quickSort(a, pivot + 1, r);     // T(n/2)
    
    // 总体时间复杂度分析：
    // T(n) = 2T(n/2) + O(n)
    // 根据主定理，最终复杂度为O(n log n)
}
```

分析：

* 每一层划分（partition）：$O(n)$
* 划分后问题对半，递归树深度 $\log n$
* 总复杂度：$O(n \log n)$

#### (2) 归并排序

```cpp
void mergeSort(int a[], int l, int r) {
    // 基准情况：当区间长度为1或更小时，直接返回
    if (l >= r) return;
    
    // 计算中点，将数组分成两半
    // 体现了分治思想，每次将问题规模缩小一半
    int mid = (l + r) / 2;
    
    // 递归处理左半部分
    // T(n/2) 复杂度
    mergeSort(a, l, mid);
    
    // 递归处理右半部分
    // T(n/2) 复杂度
    mergeSort(a, mid+1, r);
    
    // 合并两个有序数组
    // 时间复杂度为O(n)，需要遍历所有元素
    merge(a, l, mid, r); // O(n)
    
    // 总体时间复杂度分析：
    // T(n) = 2T(n/2) + O(n)
    // 根据主定理，最终复杂度为O(n log n)
}
```

分析：

* 每层合并：$O(n)$
* 总层数：$\log n$
* 总复杂度：$O(n \log n)$

#### (3) 堆排序

```cpp
void heapSort(int a[], int n) {
    // 构建最大堆
    // 从最后一个非叶子节点开始，向上调整
    // 时间复杂度为O(n)
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(a, n, i);
    }
    
    // 从堆中提取元素，构建有序数组
    // 每次提取根节点（最大值），然后调整堆
    // 时间复杂度为O(n log n)
    for (int i = n - 1; i > 0; i--) {
        // 交换根节点和当前最后一个节点
        swap(a[0], a[i]);
        // 对根节点进行调整，恢复最大堆性质
        heapify(a, i, 0);
    }
}
```

分析：

* 构建最大堆：$O(n)$
* 提取元素：$O(n \log n)$
* 总复杂度：$O(n \log n)$

---

## 四、对比总结

| 类型         | 定义                                         | 常见场景      | 排序算法例子                        |
| ---------- | ------------------------------------------ | --------- | ----------------------------- |
| **多项式复杂度** | 循环次数是 $n$ 的多项式（$O(n^2), O(n^3)$）       | 多层嵌套循环    | 冒泡排序、选择排序、插入排序：$O(n^2)$     |
| **对数复杂度**  | 问题规模缩小一半，或分治递归（$O(\log n), O(n \log n)$） | 二分查找、分治排序 | 快速排序、归并排序、堆排序：$O(n \log n)$ |

> * **多项式复杂度** → “简单循环 + 嵌套循环”，典型是低效排序（冒泡、插入、选择）。
> * **对数复杂度** → “规模减半 + 分治递归”，典型是高效排序（快排、归并、堆排序）。
{: .prompt-tip}

---
{% include custom/custom-post-content-footer.md %}
