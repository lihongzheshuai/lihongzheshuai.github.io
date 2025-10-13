---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (9) 分治算法
date: 2025-10-13 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 五级]
---
GESP C++五级官方考试大纲中，共有`9`条考点，本文针对第`9`条考点进行分析介绍。
> （9）掌握分治算法的基本原理，能够使用归并排序和快速排序对数组进行排序。
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
> * [【GESP】C++五级考试大纲知识点梳理, (7) 递归算法 - 1 基本原理](https://www.coderli.com/gesp-5-exam-syllabus-7-recursion-1/)
> * [【GESP】C++五级考试大纲知识点梳理, (7) 递归算法 - 2 复杂度分析](https://www.coderli.com/gesp-5-exam-syllabus-7-recursion-2/)
> * [【GESP】C++五级考试大纲知识点梳理, (7) 递归算法 - 3 优化策略](https://www.coderli.com/gesp-5-exam-syllabus-7-recursion-3/)
> * [【GESP】C++五级考试大纲知识点梳理, (8) 贪心算法](https://www.coderli.com/gesp-5-exam-syllabus-8-greedy-algorithm/)
{: .prompt-tip}

<!--more-->

---

## 一、什么是分治算法

“分治”就是 **分而治之（Divide and Conquer）**。是一种非常常见、也非常高效的算法思想。

> **核心思路：**
> 把一个复杂问题拆成几个规模更小的子问题，
> 分别求解后，再把子问题的结果组合起来，
> 从而得到整个问题的解。
{: .prompt-info}

一句话理解：

> **不会一次解决？那就分成几部分，一个个解决，再拼回去！**
{: .prompt-info}

---

## 二、分治算法的基本步骤

分治算法一般分为三个步骤：

| 步骤             | 含义               | 举例说明                 |
| -------------- | ---------------- | -------------------- |
| 1. 分解（Divide）  | 把原问题拆成若干规模更小的子问题 | 把一个数组拆成两半            |
| 2. 求解（Conquer） | 递归地解决这些子问题       | 对左右两半分别排序            |
| 3. 合并（Combine） | 把子问题的结果合并成原问题的解  | 把两半的有序数组合并成一个完整的有序数组 |

这个过程就像：

> “把一堆乱书分成两堆，分别整理，然后再合并成一排整齐的书。”
{: .prompt-info}

---

## 三、分治算法典型应用

### 3.1 归并排序（Merge Sort）

#### 1. 算法思想

归并排序是分治思想的经典代表。它的基本思想是：

* **分解：** 把数组分成左右两部分；
* **递归：** 分别对左右两部分进行排序；
* **合并：** 把两个有序数组合并成一个更大的有序数组。

#### 2. 执行过程举例

以数组 `[5, 2, 4, 1, 3]` 为例：

```plaintext
[5,2,4,1,3]
→ 分为 [5,2,4] 和 [1,3]
→ 继续分为 [5] [2,4] … 直到每组只有一个元素
→ 归并时： [2,4] → [2,4,5]
→ 最后合并：[2,4,5] 和 [1,3] → [1,2,3,4,5]
```

#### 3. 代码实现样例

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 合并两个已排好序的子区间 [l, m] 与 [m+1, r]
void merge(vector<int>& a, int l, int m, int r) {
    vector<int> temp;          // 临时数组，存放合并后的有序序列
    int i = l, j = m + 1;      // i 指向前半段首，j 指向后半段首

    // 双指针依次取较小元素放入 temp
    while (i <= m && j <= r) {
        if (a[i] <= a[j]) {
            temp.push_back(a[i++]);
        } else {
            temp.push_back(a[j++]);
        }
    }

    // 处理剩余元素
    while (i <= m) {
        temp.push_back(a[i++]);
    }
    while (j <= r) {
        temp.push_back(a[j++]);
    }

    // 把 temp 中的结果写回原数组对应位置
    for (int k = 0; k < temp.size(); ++k) {
        a[l + k] = temp[k];
    }

}

// 归并排序：对区间 [l, r] 进行排序
// 参数说明：
//   a: 待排序的整型数组（引用传递，排序结果直接写回）
//   l: 当前待排序区间的左端下标（包含）
//   r: 当前待排序区间的右端下标（包含）
void mergeSort(vector<int>& a, int l, int r) {
    if (l >= r) {              // 递归出口：区间长度 ≤ 1 时已有序
        return;
    }
    int m = (l + r) / 2;       // 取中点，将区间一分为二
    mergeSort(a, l, m);        // 递归排序左半部分
    mergeSort(a, m + 1, r);    // 递归排序右半部分
    merge(a, l, m, r);         // 合并两个有序子区间
}

int main() {
    vector<int> arr = {5, 2, 4, 1, 3};
    mergeSort(arr, 0, arr.size() - 1);   // 对整个数组进行归并排序
    for (int x : arr) {
        cout << x << " ";               // 输出排序结果
    }
    return 0;
}
```

#### 4. 复杂度分析

| 项目    | 分析结果           |
| ----- | -------------- |
| 时间复杂度 | $O(n \log n)$ |
| 空间复杂度 | $O(n)$        |
| 稳定性   | 稳定排序（相同元素顺序不变） |

---

### 3.2 快速排序（Quick Sort）

#### 1. 算法思想

快速排序同样是分治思想的代表，但它的“合并”步骤更巧妙。

* **分解：** 选择一个“基准元素”（pivot）。
  将数组分成两部分：
  左边 ≤ pivot，右边 ≥ pivot。
* **递归：** 分别对两边继续排序。
* **合并：** 两边排好后自然有序，无需额外操作。

#### 2. 执行过程举例

数组 `[5, 2, 4, 1, 3]`

1. 选 pivot = 3
2. 分区 → `[2,1] [3] [5,4]`
3. 左右递归排序 → `[1,2] [3] [4,5]`
4. 合并 → `[1,2,3,4,5]`

#### 3. 代码实现（C++）

```cpp
#include <iostream>
#include <vector>
using namespace std;

/**
 * 快速排序分区函数
 * 将区间 [l, r] 以 a[r] 为基准划分为两部分：
 * 左侧 ≤ pivot，右侧 ≥ pivot，返回基准最终下标
 * @param a 待分区数组（引用传递）
 * @param l 区间左端下标（包含）
 * @param r 区间右端下标（包含）
 * @return 基准元素最终所在下标
 */
int partition(vector<int>& a, int l, int r) {
    int pivot = a[r];          // 选取最右侧元素作为基准
    int i = l - 1;             // i 指向“已处理且 ≤ pivot”区间的右边界

    for (int j = l; j < r; ++j) {
        if (a[j] <= pivot) {   // 当前元素 ≤ 基准，需归入左侧
            ++i;
            swap(a[i], a[j]);
        }
    }

    // 将基准放到中间正确位置
    swap(a[i + 1], a[r]);
    return i + 1;              // 返回基准下标
}

/**
 * 快速排序（Quick Sort）主函数
 * 对数组区间 [l, r] 进行原地升序排序
 * @param a 待排序的整型数组（引用传递，排序结果直接写回）
 * @param l 当前待排序区间的左端下标（包含）
 * @param r 当前待排序区间的右端下标（包含）
 */
void quickSort(vector<int>& a, int l, int r) {
    if (l >= r) {               // 递归出口：区间长度 ≤ 1 时已有序
        return;
    }
    int p = partition(a, l, r); // 以 a[r] 为基准完成分区，返回基准最终下标
    quickSort(a, l, p - 1);     // 递归排序左半部分（所有元素 ≤ 基准）
    quickSort(a, p + 1, r);   // 递归排序右半部分（所有元素 ≥ 基准）
}

int main() {
    // 初始化待排序数组
    vector<int> arr = {5, 2, 4, 1, 3};
    // 调用快速排序，对数组区间 [0, arr.size()-1] 进行升序排序
    quickSort(arr, 0, arr.size() - 1);
    // 遍历输出排序后的结果
    for (int x : arr) {
        cout << x << " ";
    }
    // 程序正常结束
    return 0;
}
```

#### 4. 复杂度分析

| 项目      | 分析结果           |
| ------- | -------------- |
| 平均时间复杂度 | $O(n \log n)$     |
| 最坏时间复杂度 | $O(n^2)$（如数组本身有序） |
| 空间复杂度   | $O(\log n)$（递归栈）  |
| 稳定性     | 不稳定            |

---

### 3.3 归并排序与快速排序对比

| 比较项     | 归并排序       | 快速排序                         |
| ------- | ---------- | ---------------------------- |
| 算法思想    | 分治 + 合并    | 分治 + 分区                      |
| 是否原地排序  | 否，需要辅助数组   | 是，几乎不占额外空间                   |
| 稳定性     | 稳定         | 不稳定                          |
| 平均时间复杂度 | $O(n \log n)$ | $O(n \log n)$                   |
| 最坏情况    | $O(n \log n)$ | $O(n^2)$                        |
| 实际运行效率  | 稳定但略慢      | 通常更快（C++ `std::sort` 基于快排改进） |

---

## 四、总结

* **分治思想的精髓：**
  把大问题拆成小问题，通过递归逐步解决。
* **归并排序：**
  分开 → 排序 → 合并（稳定但空间大）。
* **快速排序：**
  分区 → 递归（更快，但不稳定）。

> 📘 小提示：
> 在算法学习中，分治思想不仅用于排序，还常用于二分查找、矩阵乘法等问题。
> 它是一种“将复杂问题分解为结构相似小问题”的通用方法论。
{: .prompt-tip}

---
{% include custom/custom-post-content-footer.md %}
