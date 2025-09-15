---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (6) 二分查找和二分答案
date: 2025-09-15 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 五级]
---
GESP C++五级官方考试大纲中，共有`9`条考点，本文针对第`6`条考点进行分析介绍。
> （6）掌握二分查找和二分答案算法（也称二分枚举法）的基本原理，能够在有序数组中快速定位目标值。
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
{: .prompt-tip}

<!--more-->

---

在算法学习中，二分法是一种非常经典的思想。它的核心在于**不断将问题规模对半缩小**，直到找到答案或者确定答案所在的范围。二分法不仅用于查找具体数值，还常常被用来解决一些具有单调性的最优化问题。我们通常将前者称为 **二分查找**，后者称为 **二分答案** 或 **二分枚举法**。

---

## 一、二分查找的基本原理

### 1.1 前提条件

二分查找要求数据序列是 **有序的**。只有在有序数组中，我们才能通过比较中间值来判断目标值应该落在左半部分还是右半部分。

### 1.2 基本思想

设定搜索区间 `[L, R]`：

1. 取中点 `mid = (L + R) / 2`。
2. 比较 `a[mid]` 与目标值 `x`：

   * 如果 `a[mid] == x`，则找到目标。
   * 如果 `a[mid] < x`，说明目标在右半部分，更新区间为 `[mid+1, R]`。
   * 如果 `a[mid] > x`，说明目标在左半部分，更新区间为 `[L, mid-1]`。
3. 不断缩小区间，直至找到目标值或区间为空。

### 1.3 时间复杂度

由于每次操作都会将区间缩小一半，所以时间复杂度为

$$
O(\log n)
$$

远优于顺序查找的 $O(n)$。

### 1.4 二分查找题目示例

#### 1.4.1 题目描述

在一个 **升序排列** 的数组中，给定一个目标值 `x`，请用二分查找判断目标值是否存在，若存在则输出其下标，否则输出 `-1`。

例如：

* 数组：`[1, 3, 5, 7, 9, 11]`
* 目标：`7`
* 结果：`3` （因为下标从 0 开始，`a[3] = 7`）

---

#### 1.4.2 C++ 代码样例

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 二分查找函数
int binary_search(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2; // 避免溢出
        if (arr[mid] == target) {
            return mid; // 找到目标
        } else if (arr[mid] < target) {
            left = mid + 1; // 目标在右边
        } else {
            right = mid - 1; // 目标在左边
        }
    }
    return -1; // 未找到
}

int main() {
    vector<int> arr = {1, 3, 5, 7, 9, 11};
    int target;
    cout << "请输入要查找的数字: ";
    cin >> target;

    int result = binary_search(arr, target);
    if (result != -1) {
        cout << "目标 " << target << " 出现在下标 " << result << endl;
    } else {
        cout << "目标 " << target << " 不存在于数组中" << endl;
    }
    return 0;
}
```

---

**运行效果：**

输入：

```plaintext
7
```

输出：

```plaintext
目标 7 出现在下标 3
```

输入：

```plaintext
8
```

输出：

```plaintext
目标 8 不存在于数组中
```

---

## 二、二分答案的基本原理

二分查找主要是为了**定位某个值**，而二分答案的思想更偏向于**寻找满足条件的最优解**。

### 2.1 适用场景

当问题的答案在某个区间内，并且满足某种**单调性**时，就可以使用二分答案。

所谓单调性，指的是如果某个值满足条件，比这个值大（或小）的所有值也都满足（或都不满足）条件。例如：

* 求最大运载重量：如果货车能运载 100kg，那它一定也能运载 50kg
* 求最小花费：如果 100 元不够买到所需物品，那 80 元也一定不够。

### 2.2 基本步骤

1. 确定答案的搜索范围 `[L, R]`。
2. 取中点 `mid`，并设计一个 **判定函数 check(mid)** 来判断该答案是否可行。
3. 根据 `check(mid)` 的结果决定保留哪一半区间：

   * 如果 `mid` 可行，继续尝试更优解；
   * 如果 `mid` 不可行，扩大或缩小范围。
4. 最终得到的 `L` 或 `R` 即为最优解。

### 2.3 核心要点

* **区间的单调性**：答案必须具备“如果某个值可行，那么更大/更小的值也可行或不可行”的特征。
* **判定函数的设计**：如何判断一个候选答案是否满足要求，是二分答案的关键。

### 2.4 二分答案题目示例

#### 2.4.1 题目描述

给你一个 **正整数数组** `nums`（长度为 n），以及一个整数 `m`。
你需要把 `nums` **分成 m 个连续子数组**（每个子数组不能为空）。

定义：每个子数组都有一个“和”（即里面所有数的总和），这 m 个子数组中最大的那个和记为 **最大子数组和**。

**目标**：让这个“最大子数组和”尽可能小，并返回它的最小值。

##### 输入输出格式

* 输入：数组 `nums` 和一个整数 `m`
* 输出：一个整数，表示分割后的 **最小的最大子数组和**

---

##### 示例

例如，输入：

```plaintext
nums = [7, 2, 5, 10, 8], m = 2
```

可能的分割方式：

1. `[7,2,5]` 和 `[10,8]`

   * 子数组和：14, 18
   * 最大值 = 18

2. `[7,2]` 和 `[5,10,8]`

   * 子数组和：9, 23
   * 最大值 = 23

3. `[7]` 和 `[2,5,10,8]`

   * 子数组和：7, 25
   * 最大值 = 25

所有分割方式中，最小的最大值是 **18**。

输出：

```plaintext
18
```

---

#### 2.4.2 思路解析

1. **分析问题特征**
   * 需要将数组分成m个连续子数组
   * 每个子数组都有一个和
   * 目标是让最大的子数组和尽可能小

2. **寻找解题方向**
   * 如果直接枚举所有分割方案，复杂度会很高
   * 注意到子数组和有一个特点：如果某个值可以作为最大子数组和，那么比它大的值一定也可以
   * 这种单调性提示我们可以用二分答案

3. **确定搜索范围**
   * 最小可能值：数组中的最大元素（因为任何分割方案中都至少要包含这个元素）
   * 最大可能值：整个数组的和（即只分成一段的情况）

4. **设计判定函数**
   * 给定一个最大子数组和的候选值 `maxSum`
   * 判断能否将数组分成不超过 `m` 个子数组，使得每个子数组的和都不超过 `maxSum`
   * 贪心地从左到右扫描，尽可能多地将数字放入当前子数组
   * 如果分段数超过 `m`，说明当前 `maxSum` 太小

5. **二分查找过程**
   * 初始化左边界 `left = max(nums)`（数组中的最大值）
   * 初始化右边界 `right = sum(nums)`（整个数组的和）
   * 每次取中点 `mid = (left + right) / 2`
   * 调用判定函数 `check(mid)`：
     * 如果可行，说明答案可能更小，更新 `right = mid - 1`
     * 如果不可行，说明答案一定更大，更新 `left = mid + 1`
   * 最终 `left` 就是答案

6. **时间复杂度分析**
   * 二分查找的次数：$O(\log(sum-max))$
   * 每次判定需要遍历数组：$O(n)$
   * 总时间复杂度：$O(n \log(sum-max))$

这个解题过程展示了二分答案的典型特征：

* 将最优化问题转化为判定问题
* 利用答案的单调性进行二分
* 通过不断缩小范围逼近最优解

---

#### 2.4.3 C++代码样例

```cpp
#include <iostream>     // 输入输出流
#include <vector>       // 使用vector容器
#include <numeric>      // 使用accumulate函数
#include <algorithm>    // 使用max_element函数
using namespace std;

// 判定函数：给定最大子数组和 maxSum，是否能分成 <= m 段
bool check(vector<int>& nums, int m, long long maxSum) {
    long long curSum = 0;   // 当前子数组的和
    int count = 1;          // 至少有一段
    
    for (int num : nums) {  // 遍历数组中的每个元素
        if (curSum + num > maxSum) {  // 如果加入当前数字会超过最大和
            count++;                   // 分段数加1
            curSum = num;              // 新开一段
            
            if (count > m) {
                return false;          // 段数超过m，不可行
            }
        } else {
            curSum += num;             // 当前数字可以加入当前段
        }
    }
    
    return true;            // 分段数未超过m，方案可行
}

int splitArray(vector<int>& nums, int m) {
    // 初始化二分查找的左右边界
    long long left = *max_element(nums.begin(), nums.end());    // 左边界为数组中的最大值
    long long right = accumulate(nums.begin(), nums.end(), 0LL); // 右边界为数组总和
    long long ans = right;  // 初始化答案为右边界

    // 二分查找过程
    while (left <= right) {
        long long mid = left + (right - left) / 2;  // 计算中间值，避免溢出
        if (check(nums, m, mid)) {     // 如果当前最大和可行
            ans = mid;                  // 更新答案
            right = mid - 1;            // 尝试更小的值
        } else {
            left = mid + 1;            // 当前值太小，需要增大
        }
    }
    return ans;             // 返回最终答案
}

int main() {
    vector<int> nums = {7, 2, 5, 10, 8};  // 测试数组
    int m = 2;                            // 需要分成的段数
    cout << "最小的最大子数组和是: " << splitArray(nums, m) << endl;
    return 0;
}
```

---

**输出结果:**

```plaintext
最小的最大子数组和是: 18
```

---

## 三、二分查找与二分答案的比较小结

| 特点 | 二分查找    | 二分答案        |
| -- | ------- | ----------- |
| 目标 | 查找具体值   | 求最优解        |
| 前提 | 有序数组    | 答案具有单调性     |
| 判定 | 与目标值比较  | 自定义判定函数     |
| 应用 | 数组查找、定位 | 排队、分配、最优化问题 |

总之，二分法的精髓在于“**缩小一半，快速定位**”。

* 在 **有序数组** 中，二分查找可以在 $O(\log n)$ 时间内找到目标值。
* 在 **答案区间具有单调性** 的问题中，二分答案可以通过“猜答案+判定函数”的方式，快速求解最优解。

掌握二分查找和二分答案，不仅能提升算法效率，也为解决更复杂的最优化问题打下了坚实基础。

---
{% include custom/custom-post-content-footer.md %}
