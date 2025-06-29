---
layout: post
title: 【GESP】C++四级考试大纲知识点梳理, (8) 冒泡、插入、选择排序
date: 2025-06-29 22:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++]
categories: [GESP, 四级]
---
GESP C++四级官方考试大纲中，共有11条考点，本文针对第8条考点进行分析介绍。
> （8）掌握排序算法中的冒泡排序、插入排序、选择排序的算法思想、排序步骤及代码实现。
{: .prompt-info}

***四级其他考点回顾：***

> * [【GESP】C++四级考试大纲知识点梳理, (1) 指针](https://www.coderli.com/gesp-4-exam-syllabus-pointer/)
> * [【GESP】C++四级考试大纲知识点梳理, (2) 结构体和二维数组](https://www.coderli.com/gesp-4-exam-syllabus-struct-two-dimensional-array/)
> * [【GESP】C++四级考试大纲知识点梳理, (3) 模块化和函数](https://www.coderli.com/gesp-4-exam-syllabus-module-function/)
> * [【GESP】C++四级考试大纲知识点梳理, (4) 变量和作用域](https://www.coderli.com/gesp-4-exam-syllabus-variable-scope/)
> * [【GESP】C++四级考试大纲知识点梳理, (5) 值传递](https://www.coderli.com/gesp-4-exam-syllabus-pass-by-value-reference-pointer/)
> * [【GESP】C++四级考试大纲知识点梳理, (6) 递推算法](https://www.coderli.com/gesp-4-exam-syllabus-iteration-algo/)
> * [【GESP】C++四级考试大纲知识点梳理, (7) 排序算法基本概念](https://www.coderli.com/gesp-4-exam-syllabus-sorting-algo-conception/)
{: .prompt-tip}

<!--more-->

---

下面分别介绍三种经典的内排序算法——冒泡排序、插入排序和选择排序的核心思想、具体步骤及其 C++ 代码实现。

## 一、冒泡排序（Bubble Sort）

冒泡排序（bubble sort）通过连续地比较与交换相邻元素实现排序。这个过程就像气泡从底部升到顶部一样，因此得名冒泡排序。

### 1.1 算法思想

> **“相邻两两比较，大的往后冒”**

**🎯 思想要点：**

* 每轮从前往后扫描，比较相邻元素。
* 如果前面的数大于后面的，就交换。
* 一轮结束后，**最大值沉到末尾**。
* 重复 n-1 轮，直到全部有序。
* 可设置“是否发生交换”的标志位，优化提前结束。

### 1.2 算法流程

1. 外层循环从数组首位开始，控制趟数，共需 n−1 趟（n 为元素个数）。
2. 内层循环在未排序区间内（\[0, n−i−1]）依次比较相邻元素，若前者 > 后者，则交换。
3. 重复直到整个序列有序。

#### 1.2.1 流程示意

![冒泡排序流程示意](https://www.hello-algo.com/chapter_sorting/bubble_sort.assets/bubble_sort_overview.png)

>图片来自开源书籍：[***《Hello，算法》***](https://www.hello-algo.com/chapter_hello_algo/)
{: .prompt-tip}

### 1.3 时间复杂度

* 最优 $O(n)$，当序列已经有序时，只需一趟即可（可加标志位提前退出）。
* 平均/最差均为 $O(n^2)$。

### 1.4 空间复杂度

* $O(1)$，仅需要常数个辅助变量（交换时的临时变量）。
* 属于原地排序算法。

### 1.5 代码示例

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 冒泡排序函数
void bubbleSort(vector<int>& a) {
    int n = a.size();
    // 外层循环控制排序轮数，n-1轮
    for (int i = 0; i < n - 1; ++i) {
        // 设置标志位，用于优化：如果一轮中没有发生交换，则数组已经有序
        bool swapped = false;
        // 内层循环进行相邻元素比较，每轮将最大值冒泡到末尾
        for (int j = 0; j < n - i - 1; ++j) {
            // 如果前一个元素大于后一个元素，则交换
            if (a[j] > a[j + 1]) {
                swap(a[j], a[j + 1]);
                swapped = true;  // 发生交换，设置标志位
            }
        }
        // 如果没有发生交换，说明数组已经有序，提前退出
        if (!swapped) break;
    }
}

int main() {
    // 测试用例
    vector<int> arr = {4, 1, 3, 1, 5, 2};
    // 调用冒泡排序函数
    bubbleSort(arr);
    // 打印排序后的数组
    for (int num : arr) cout << num << " ";
    return 0;
}
```

**输出结果：**

```plaintext
1 1 2 3 4 5
```

#### 1.5.1 冒泡排序执行过程演示

**初始数组：**

```plaintext
[4, 1, 3, 1, 5, 2]
```

**第1轮（将最大数“冒”到最后）：**

* 比较 4 和 1 → 交换 → `[1, 4, 3, 1, 5, 2]`
* 比较 4 和 3 → 交换 → `[1, 3, 4, 1, 5, 2]`
* 比较 4 和 1 → 交换 → `[1, 3, 1, 4, 5, 2]`
* 比较 4 和 5 → 无交换
* 比较 5 和 2 → 交换 → `[1, 3, 1, 4, 2, 5]`

**第2轮（次大数冒到倒数第二）：**

* 比较 1 和 3 → 无交换
* 比较 3 和 1 → 交换 → `[1, 1, 3, 4, 2, 5]`
* 比较 3 和 4 → 无交换
* 比较 4 和 2 → 交换 → `[1, 1, 3, 2, 4, 5]`

**第3轮：**

* 比较 1 和 1 → 无交换
* 比较 1 和 3 → 无交换
* 比较 3 和 2 → 交换 → `[1, 1, 2, 3, 4, 5]`

**第4轮：**

* 比较 1 和 1 → 无交换
* 比较 1 和 2 → 无交换

**第5轮：**

* 比较 1 和 1 → 无交换

✅ **最终结果**：`[1, 1, 2, 3, 4, 5]`

**可视化运行：**

<div style="position: relative; padding-bottom: 56.25%;{height: 0; overflow: hidden;">
<div style="height: 531px; width: 100%;">
  <iframe src="https://pythontutor.com/iframe-embed.html#code=def%20bubble_sort%28nums%3A%20list%5Bint%5D%29%3A%0A%20%20%20%20%22%22%22%E5%86%92%E6%B3%A1%E6%8E%92%E5%BA%8F%22%22%22%0A%20%20%20%20n%20%3D%20len%28nums%29%0A%20%20%20%20%23%20%E5%A4%96%E5%BE%AA%E7%8E%AF%EF%BC%9A%E6%9C%AA%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%E4%B8%BA%20%5B0,%20i%5D%0A%20%20%20%20for%20i%20in%20range%28n%20-%201,%200,%20-1%29%3A%0A%20%20%20%20%20%20%20%20%23%20%E5%86%85%E5%BE%AA%E7%8E%AF%EF%BC%9A%E5%B0%86%E6%9C%AA%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%20%5B0,%20i%5D%20%E4%B8%AD%E7%9A%84%E6%9C%80%E5%A4%A7%E5%85%83%E7%B4%A0%E4%BA%A4%E6%8D%A2%E8%87%B3%E8%AF%A5%E5%8C%BA%E9%97%B4%E7%9A%84%E6%9C%80%E5%8F%B3%E7%AB%AF%0A%20%20%20%20%20%20%20%20for%20j%20in%20range%28i%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20nums%5Bj%5D%20%3E%20nums%5Bj%20%2B%201%5D%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%23%20%E4%BA%A4%E6%8D%A2%20nums%5Bj%5D%20%E4%B8%8E%20nums%5Bj%20%2B%201%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20nums%5Bj%5D,%20nums%5Bj%20%2B%201%5D%20%3D%20nums%5Bj%20%2B%201%5D,%20nums%5Bj%5D%0A%0A%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20nums%20%3D%20%5B4,%201,%203,%201,%205,%202%5D%0A%20%20%20%20bubble_sort%28nums%29%0A%20%20%20%20print%28%22%E5%86%92%E6%B3%A1%E6%8E%92%E5%BA%8F%E5%AE%8C%E6%88%90%E5%90%8E%20nums%20%3D%22,%20nums%29&codeDivHeight=800&codeDivWidth=600&cumulative=false&curInstr=4&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allowfullscreen></iframe>
  </div>
  <div style="margin-top: 5px;">
  <a href="https://pythontutor.com/iframe-embed.html#code=def%20bubble_sort%28nums%3A%20list%5Bint%5D%29%3A%0A%20%20%20%20%22%22%22%E5%86%92%E6%B3%A1%E6%8E%92%E5%BA%8F%22%22%22%0A%20%20%20%20n%20%3D%20len%28nums%29%0A%20%20%20%20%23%20%E5%A4%96%E5%BE%AA%E7%8E%AF%EF%BC%9A%E6%9C%AA%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%E4%B8%BA%20%5B0,%20i%5D%0A%20%20%20%20for%20i%20in%20range%28n%20-%201,%200,%20-1%29%3A%0A%20%20%20%20%20%20%20%20%23%20%E5%86%85%E5%BE%AA%E7%8E%AF%EF%BC%9A%E5%B0%86%E6%9C%AA%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%20%5B0,%20i%5D%20%E4%B8%AD%E7%9A%84%E6%9C%80%E5%A4%A7%E5%85%83%E7%B4%A0%E4%BA%A4%E6%8D%A2%E8%87%B3%E8%AF%A5%E5%8C%BA%E9%97%B4%E7%9A%84%E6%9C%80%E5%8F%B3%E7%AB%AF%0A%20%20%20%20%20%20%20%20for%20j%20in%20range%28i%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20nums%5Bj%5D%20%3E%20nums%5Bj%20%2B%201%5D%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%23%20%E4%BA%A4%E6%8D%A2%20nums%5Bj%5D%20%E4%B8%8E%20nums%5Bj%20%2B%201%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20nums%5Bj%5D,%20nums%5Bj%20%2B%201%5D%20%3D%20nums%5Bj%20%2B%201%5D,%20nums%5Bj%5D%0A%0A%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20nums%20%3D%20%5B4,%201,%203,%201,%205,%202%5D%0A%20%20%20%20bubble_sort%28nums%29%0A%20%20%20%20print%28%22%E5%86%92%E6%B3%A1%E6%8E%92%E5%BA%8F%E5%AE%8C%E6%88%90%E5%90%8E%20nums%20%3D%22,%20nums%29&codeDivHeight=800&codeDivWidth=600&cumulative=false&curInstr=4&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false" target="_blank" rel="noopener noreferrer">全屏观看 &gt;</a>
  </div>
</div>

### 1.6 小结

| 特性 | 说明 |
|-----|-----|
| 时间复杂度 | 最优：$O(n)$ - 数组已经有序<br>平均：$O(n^2)$<br>最差：$O(n^2)$ - 数组完全逆序 |
| 空间复杂度 | $O(1)$ - 只需要常数个临时变量 |
| 稳定性 | 稳定 - 相等元素相对位置不变 |
| 原地排序 | 是 - 不需要额外空间 |
| 适用场景 | 1. 数据规模较小<br>2. 数据接近有序<br>3. 需要稳定排序<br>4. 代码简单易实现 |
| 优化方案 | 1. 添加标志位提前结束<br>2. 记录最后交换位置<br>3. 双向冒泡 |
| 缺点 | 1. 大规模数据效率低<br>2. 交换次数较多 |

---

## 二、插入排序（Insertion Sort）

插入排序（insertion sort）是一种简单的排序算法，它的工作原理与手动整理一副牌的过程非常相似。

### 2.1 算法思想

> **“构建有序区，把当前元素插入到前面合适的位置”**

**🎯 思想要点：**

* 把数组分成 **有序区** 和 **无序区**。
* 初始有序区是第一个元素。
* 每次从无序区取一个数，从后往前比较插入到有序区。
* 插入过程中，遇到比当前元素大的，统统右移。

### 2.2 算法流程

1. 初始时，已排序区间为第 0 个元素。
2. 从索引 1 开始，取出 `key = a[i]`，在 `[0, i-1]` 中从后向前扫描，所有大于 `key` 的元素依次右移一位。
3. 将 `key` 插入到空出的位置。
4. 重复直至末尾。

#### 2.2.1 流程示意

![插入排序流程示意](https://www.hello-algo.com/chapter_sorting/insertion_sort.assets/insertion_operation.png)

>图片来自开源书籍：[***《Hello，算法》***](https://www.hello-algo.com/chapter_hello_algo/)
{: .prompt-tip}

### 2.3 时间复杂度

* 最优 $O(n)$，当序列已近乎有序，仅需简单比较。
* 平均/最差均为 $O(n^2)$。

### 2.4 空间复杂度

* $O(1)$，只需要一个临时变量存储 key 值。
* 属于原地排序算法。
* 不需要额外的辅助空间。

### 2.5 代码示例

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 插入排序函数，参数为待排序的整型向量的引用
void insertionSort(vector<int>& a) {
    // 获取数组长度
    int n = a.size();
    // 从第二个元素开始遍历，因为第一个元素可以视为已排序
    for (int i = 1; i < n; ++i) {
        // 保存当前要插入的元素
        int key = a[i];
        // j指向已排序区间的最后一个元素
        int j = i - 1;
        // 从后向前扫描已排序区间，将所有大于key的元素都向后移动一位
        while (j >= 0 && a[j] > key) {
            // 元素后移
            a[j + 1] = a[j];
            // 继续向前扫描
            --j;
        }
        // 找到key的正确插入位置，将key插入
        a[j + 1] = key;
    }
}

int main() {
    // 创建测试数组
    vector<int> arr = {4, 1, 3, 1, 5, 2};
    // 调用插入排序函数
    insertionSort(arr);
    // 打印排序后的数组
    for (int num : arr) cout << num << " ";
    return 0;
}
```

**输出结果：**

```plaintext
1 1 2 3 4 5
```

#### 2.5.1 插入排序执行过程演示

**初始数组：**

```plaintext
[4, 1, 3, 1, 5, 2]
```

**第1步：插入 1:**

* 1 < 4，向后移 → `[4, 4, 3, 1, 5, 2]` → 插入 → `[1, 4, 3, 1, 5, 2]`

**第2步：插入 3:**

* 3 < 4，向后移 → `[1, 4, 4, 1, 5, 2]`
* 3 > 1 → 插入 → `[1, 3, 4, 1, 5, 2]`

**第3步：插入 1：**

* 1 < 4 → `[1, 3, 4, 4, 5, 2]`
* 1 < 3 → `[1, 3, 3, 4, 5, 2]`
* 1 == 1 → 插入 → `[1, 1, 3, 4, 5, 2]`

**第4步：插入 5（无需移动）：**

→ `[1, 1, 3, 4, 5, 2]`

**第5步：插入 2：**

* 2 < 5 → `[1, 1, 3, 4, 5, 5]`
* 2 < 4 → `[1, 1, 3, 4, 4, 5]`
* 2 < 3 → `[1, 1, 3, 3, 4, 5]`
* 插入 → `[1, 1, 2, 3, 4, 5]`

✅ **最终结果**：`[1, 1, 2, 3, 4, 5]`

**可视化运行：**

<div style="position: relative; padding-bottom: 56.25%;{height: 0; overflow: hidden;">
  <iframe src="https://pythontutor.com/iframe-embed.html#code=def%20insertion_sort%28nums%3A%20list%5Bint%5D%29%3A%0A%20%20%20%20%22%22%22%E6%8F%92%E5%85%A5%E6%8E%92%E5%BA%8F%22%22%22%0A%20%20%20%20%23%20%E5%A4%96%E5%BE%AA%E7%8E%AF%EF%BC%9A%E5%B7%B2%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%E4%B8%BA%20%5B0,%20i-1%5D%0A%20%20%20%20for%20i%20in%20range%281,%20len%28nums%29%29%3A%0A%20%20%20%20%20%20%20%20base%20%3D%20nums%5Bi%5D%0A%20%20%20%20%20%20%20%20j%20%3D%20i%20-%201%0A%20%20%20%20%20%20%20%20%23%20%E5%86%85%E5%BE%AA%E7%8E%AF%EF%BC%9A%E5%B0%86%20base%20%E6%8F%92%E5%85%A5%E5%88%B0%E5%B7%B2%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%20%5B0,%20i-1%5D%20%E4%B8%AD%E7%9A%84%E6%AD%A3%E7%A1%AE%E4%BD%8D%E7%BD%AE%0A%20%20%20%20%20%20%20%20while%20j%20%3E%3D%200%20and%20nums%5Bj%5D%20%3E%20base%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20nums%5Bj%20%2B%201%5D%20%3D%20nums%5Bj%5D%20%20%23%20%E5%B0%86%20nums%5Bj%5D%20%E5%90%91%E5%8F%B3%E7%A7%BB%E5%8A%A8%E4%B8%80%E4%BD%8D%0A%20%20%20%20%20%20%20%20%20%20%20%20j%20-%3D%201%0A%20%20%20%20%20%20%20%20nums%5Bj%20%2B%201%5D%20%3D%20base%20%20%23%20%E5%B0%86%20base%20%E8%B5%8B%E5%80%BC%E5%88%B0%E6%AD%A3%E7%A1%AE%E4%BD%8D%E7%BD%AE%0A%0A%0A%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20nums%20%3D%20%5B4,%201,%203,%201,%205,%202%5D%0A%20%20%20%20insertion_sort%28nums%29%0A%20%20%20%20print%28%22%E6%8F%92%E5%85%A5%E6%8E%92%E5%BA%8F%E5%AE%8C%E6%88%90%E5%90%8E%20nums%20%3D%22,%20nums%29&codeDivHeight=800&codeDivWidth=600&cumulative=false&curInstr=4&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allowfullscreen></iframe>
</div>

### 2.6 小结

| 特性 | 说明 |
|-----|-----|
| 时间复杂度 | 最优：$O(n)$ - 数组已经有序<br>平均：$O(n^2)$<br>最差：$O(n^2)$ - 数组完全逆序 |
| 空间复杂度 | $O(1)$ - 只需要一个临时变量存储 key |
| 稳定性 | 稳定 - 相等元素相对位置不变 |
| 原地排序 | 是 - 不需要额外空间 |
| 适用场景 | 1. 数据规模较小<br>2. 数据接近有序<br>3. 需要稳定排序<br>4. 代码简单易实现 |
| 优化方案 | 1. 二分查找插入位置<br>2. 缩小有序区间扫描范围<br>3. Shell 排序改进 |
| 优点 | 1. 稳定排序<br>2. 适合小规模数据<br>3. 对近乎有序数据效率高 |
| 缺点 | 1. 大规模数据效率低<br>2. 元素移动次数较多 |

---

## 三、选择排序（Selection Sort）

选择排序（selection sort）的工作原理非常简单：开启一个循环，每轮从未排序区间选择最小的元素，将其放到已排序区间的末尾。

### 3.1 算法思想

> **“每轮选择最小值，放到最前面”**

🎯 思想要点：

* 将数组分成已排序区和未排序区。
* 每轮在未排序区中找到最小元素。
* 与未排序区起始元素交换，扩展已排序区。
* 不管顺序如何，总是 n-1 轮比较+交换。

⚠️ 注意：

>与冒泡不同，它是先“找”再交换，而不是每次都交换。
{: .prompt-warning}

### 3.2 算法流程

选择排序的具体执行流程如下:

1. **初始化已排序和未排序区间**
   * 将数组分成两个区间:已排序区间 `[0, i-1]` 和未排序区间 `[i, n-1]`
   * 初始时已排序区间为空,未排序区间为整个数组

2. **外层循环遍历未排序区间**
   * 循环变量 i 从 0 到 n-2
   * i 表示当前已排序区间的末尾位置
   * 每轮循环会将一个最小值放到已排序区间末尾

3. **内层循环寻找最小值**
   * 在未排序区间 `[i, n-1]` 中扫描
   * 用变量 minIdx 记录当前找到的最小值的索引
   * 初始时 minIdx = i
   * 遍历比较每个元素与 minIdx 位置的元素
   * 若发现更小的元素则更新 minIdx

4. **交换操作**
   * 如果找到的最小值索引 minIdx 不等于 i
   * 则将 a[i] 与 a[minIdx] 交换位置
   * 这样最小值就被放到了已排序区间的末尾

5. **重复执行直到结束**
   * 重复步骤 2-4,直到整个数组有序
   * 总共需要 n-1 轮操作
   * 每轮都会将一个最小值放到正确位置

⚠️ 注意：

>选择排序是不稳定的，如图所示：
>![选择排序不稳定性示意](https://www.hello-algo.com/chapter_sorting/selection_sort.assets/selection_sort_instability.png)
>
>图片来自开源书籍：[***《Hello，算法》***](https://www.hello-algo.com/chapter_hello_algo/)
{: .prompt-warning}

### 3.3 时间复杂度

* 无论初始状态，始终需要 $\frac{n(n-1)}{2}$ 次比较，都是 $O(n^2)$。

### 3.4 空间复杂度

* $O(1)$，只需要一个变量记录最小值索引。
* 属于原地排序算法。
* 不需要额外的辅助空间。

### 3.5 代码示例

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 选择排序函数
void selectionSort(vector<int>& a) {
    int n = a.size();
    // 外层循环，i表示已排序区间的末尾
    for (int i = 0; i < n - 1; ++i) {
        // minIdx记录未排序区间中最小元素的索引
        int minIdx = i;
        // 内层循环在未排序区间[i+1, n-1]中寻找最小元素
        for (int j = i + 1; j < n; ++j) {
            // 如果找到更小的元素，更新minIdx
            if (a[j] < a[minIdx]) {
                minIdx = j;
            }
        }
        // 如果找到的最小元素不是当前位置，则交换
        if (minIdx != i) swap(a[i], a[minIdx]);
    }
}

int main() {
    // 测试用例
    vector<int> arr = {4, 1, 3, 1, 5, 2};
    // 调用选择排序函数
    selectionSort(arr);
    // 打印排序后的数组
    for (int num : arr) cout << num << " ";
    return 0;
}
```

**输出结果：**

```plaintext
1 1 2 3 4 5
```

#### 3.5.1 选择排序流程示意

**初始数组：**

```plaintext
[4, 1, 3, 1, 5, 2]
```

**第1轮：**

选最小（1）与 4 交换 → `[1, 4, 3, 1, 5, 2]`

**第2轮：**

选最小（1）与 4 交换 → `[1, 1, 3, 4, 5, 2]`

**第3轮：**

选最小（2）与 3 交换 → `[1, 1, 2, 4, 5, 3]`

**第4轮：**

选最小（3）与 4 交换 → `[1, 1, 2, 3, 5, 4]`

**第5轮：**

选最小（4）与 5 交换 → `[1, 1, 2, 3, 4, 5]`

✅ **最终结果**：`[1, 1, 2, 3, 4, 5]`

**可视化运行：**

<div style="position: relative; padding-bottom: 56.25%;{height: 0; overflow: hidden;">

  <iframe src="https://pythontutor.com/iframe-embed.html#code=def%20selection_sort%28nums%3A%20list%5Bint%5D%29%3A%0A%20%20%20%20%22%22%22%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F%22%22%22%0A%20%20%20%20n%20%3D%20len%28nums%29%0A%20%20%20%20%23%20%E5%A4%96%E5%BE%AA%E7%8E%AF%EF%BC%9A%E6%9C%AA%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%E4%B8%BA%20%5Bi,%20n-1%5D%0A%20%20%20%20for%20i%20in%20range%28n%20-%201%29%3A%0A%20%20%20%20%20%20%20%20%23%20%E5%86%85%E5%BE%AA%E7%8E%AF%EF%BC%9A%E6%89%BE%E5%88%B0%E6%9C%AA%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%E5%86%85%E7%9A%84%E6%9C%80%E5%B0%8F%E5%85%83%E7%B4%A0%0A%20%20%20%20%20%20%20%20k%20%3D%20i%0A%20%20%20%20%20%20%20%20for%20j%20in%20range%28i%20%2B%201,%20n%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20nums%5Bj%5D%20%3C%20nums%5Bk%5D%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20k%20%3D%20j%20%20%23%20%E8%AE%B0%E5%BD%95%E6%9C%80%E5%B0%8F%E5%85%83%E7%B4%A0%E7%9A%84%E7%B4%A2%E5%BC%95%0A%20%20%20%20%20%20%20%20%23%20%E5%B0%86%E8%AF%A5%E6%9C%80%E5%B0%8F%E5%85%83%E7%B4%A0%E4%B8%8E%E6%9C%AA%E6%8E%92%E5%BA%8F%E5%8C%BA%E9%97%B4%E7%9A%84%E9%A6%96%E4%B8%AA%E5%85%83%E7%B4%A0%E4%BA%A4%E6%8D%A2%0A%20%20%20%20%20%20%20%20nums%5Bi%5D,%20nums%5Bk%5D%20%3D%20nums%5Bk%5D,%20nums%5Bi%5D%0A%0A%0A%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20nums%20%3D%20%5B4,%201,%203,%201,%205,%202%5D%0A%20%20%20%20selection_sort%28nums%29%0A%20%20%20%20print%28%22%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F%E5%AE%8C%E6%88%90%E5%90%8E%20nums%20%3D%22,%20nums%29&codeDivHeight=800&codeDivWidth=600&cumulative=false&curInstr=4&heapPrimitives=nevernest&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allowfullscreen></iframe>
</div>

---

### 3.6 小结

| 特性 | 说明 |
|-----|-----|
| 时间复杂度 | 最优/平均/最差均为 $O(n^2)$ |
| 空间复杂度 | $O(1)$ - 只需要一个变量记录最小值索引 |
| 稳定性 | 不稳定 - 可能改变相等元素的相对位置 |
| 原地排序 | 是 - 不需要额外空间 |
| 适用场景 | 1. 数据规模较小<br>2. 对稳定性要求不高<br>3. 需要最少的交换次数 |
| 优化方案 | 1. 同时找最大最小值<br>2. 堆排序改进 |
| 优点 | 1. 交换次数最少<br>2. 实现简单<br>3. 不占用额外内存 |
| 缺点 | 1. 时间复杂度固定<br>2. 不稳定排序<br>3. 大规模数据效率低 |

---

## 四、三种排序总结对比

| 特性 | 冒泡排序 | 插入排序 | 选择排序 |
|-----|---------|---------|---------|
| 时间复杂度 | 最优：$O(n)$<br>平均：$O(n^2)$<br>最差：$O(n^2)$ | 最优：$O(n)$<br>平均：$O(n^2)$<br>最差：$O(n^2)$ | 最优/平均/最差：$O(n^2)$ |
| 空间复杂度 | $O(1)$ | $O(1)$ | $O(1)$ |
| 稳定性 | 稳定 | 稳定 | 不稳定 |
| 原地排序 | 是 | 是 | 是 |
| 优点 | 1. 实现简单<br>2. 稳定排序<br>3. 适合小规模数据 | 1. 稳定排序<br>2. 适合小规模数据<br>3. 对近乎有序数据高效 | 1. 交换次数最少<br>2. 实现简单<br>3. 不占用额外内存 |
| 缺点 | 1. 交换次数多<br>2. 大规模数据效率低 | 1. 移动次数多<br>2. 大规模数据效率低 | 1. 时间复杂度固定<br>2. 不稳定排序 |
| 适用场景 | 1. 数据规模较小<br>2. 数据接近有序<br>3. 需要稳定排序 | 1. 数据规模较小<br>2. 数据接近有序<br>3. 需要稳定排序 | 1. 数据规模较小<br>2. 对稳定性要求不高<br>3. 需要最少交换次数 |

三种算法都属于简单直观的内部排序，适合小规模或初学时理解排序思想。对于大规模数据，建议学习快速排序、归并排序、堆排序等更高效的算法。

---
{% include custom/custom-post-content-footer.md %}
