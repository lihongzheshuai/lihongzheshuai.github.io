---
layout: post
title: 【信奥业余科普】C++ 的奇妙之旅 | 27：高效处理数据的利器——常用算法库（algorithm）
date: 2026-06-01 08:00:00 +0800
author: OneCoder
comments: true
math: true
tags: [科普, 计算机科学基础, GESP, CSP, C++, STL, algorithm, sort, unique]
categories: [信奥业余科普, C++的奇妙之旅]
---

在前面的文章中，我们介绍了 C++ STL 中的各种容器。在实际编写程序和参加竞赛时，仅存储数据是不够的，通常还需要对数据进行各种操作，例如：

- 将学生的成绩按照从高到低排序（`sort`）；
- 去掉数组中重复的数据（`unique`）；
- 在排好序的数据中用二分法快速查找某个数（`lower_bound / upper_bound`）；
- 将一串字符或数组的内容颠倒顺序（`reverse`）；
- 生成一组数据的所有排列方式（`next_permutation`）。

如果每次都手写循环和排序代码，不仅编写麻烦、容易出错，而且运行效率也可能不够高。

C++ STL 提供了通用算法库 **`<algorithm>`**，它包含了许多已经写好且经过优化的常用算法。我们只需调用一行函数，就能完成上述复杂的操作。本文将详细讲解这些常用算法的使用方法。

<!--more-->

**往期回顾：**

- [第一部分【计算机历史】系列文章合集（共8篇）](https://www.coderli.com/categories/%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%8E%86%E5%8F%B2/)
- [第二部分【C++的奇妙之旅】前26篇合集](https://www.coderli.com/categories/c-%E7%9A%84%E5%A5%87%E5%A6%99%E4%B9%8B%E6%97%85/)

---

## 一、 什么是 `<algorithm>` 与迭代器区间

`<algorithm>` 中的算法主要是通过 **迭代器（Iterator）** 来操作容器元素的。因此，不论你使用的是 `vector`、`string` 等 STL 容器，还是普通的数组，都可以使用相同的算法函数。

在使用这些算法时，需要传入一个操作区间。C++ 中的区间规定为 **“左闭右开”**，即：

$$[\text{first}, \text{last})$$

这意味着，区间包含 `first` 指向的第一个元素，但**不包含** `last` 指向的最后一个元素（对于 STL 容器，`last` 通常是末尾标识 `end()`）。

### 1.1 不同容器与数组的区间表示方法

调用算法函数时，我们需要根据数据源是 STL 容器还是普通数组，传入正确的区间：

| 容器/数组类型                              | 迭代器起点       | 迭代器终点           | 排序/处理区间示范                   |
| :----------------------------------------- | :--------------- | :------------------- | :---------------------------------- |
| **`std::vector<int> v`**                   | `v.begin()`      | `v.end()`            | `std::sort(v.begin(), v.end());`    |
| **`std::string s`**                        | `s.begin()`      | `s.end()`            | `std::reverse(s.begin(), s.end());` |
| **普通数组 `int a[100]`** (元素个数为 $n$) | `a` (或 `&a[0]`) | `a + n` (或 `&a[n]`) | `std::sort(a, a + n);`              |

下面我们来学习几个最常用的核心算法。

---

## 二、 排序与逆序：`sort` 与 `reverse`

### 2.1 常用排序函数：`std::sort`

`std::sort` 用于对区间内的元素进行排序。它的底层采用了 **内省排序（Introsort）**，这是一种混合排序算法，结合了快速排序、堆排序和插入排序的优点。

- **时间复杂度**：平均与最坏情况均为 $O(n \log n)$，运行效率极高。
- **排序规则**：默认按照从小到大的升序排列。

#### ① 基础用法（升序）

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // vector 排序
    std::vector<int> v = {3, 1, 4, 1, 5, 9};
    std::sort(v.begin(), v.end());
    // 排序后：1, 1, 3, 4, 5, 9

    // 普通数组排序
    int a[] = {9, 5, 2, 7};
    std::sort(a, a + 4);
    // 排序后：2, 5, 7, 9
    return 0;
}
```

#### ② 自定义降序排列

如果你想让数据从大到小排列，可以使用 C++ 提供的 `greater` 模板：

```cpp
std::sort(v.begin(), v.end(), std::greater<int>());
```

#### ③ 自定义比较函数（以结构体排序为例）

如果我们要对自定义的结构体（例如学生信息）进行排序，或者排序规则比较复杂，可以手写一个自定义比较函数 `cmp`。

例如：有学生的姓名和成绩，我们希望优先按照 **成绩从高到低（降序）** 排列；如果成绩相同，则按照 **姓名的字典序从小到大（升序）** 排列。我们可以这样写：

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

struct Student {
    std::string name;
    int score;
};

// 自定义比较函数
// 返回 true 代表 a 应该排在 b 的前面
bool cmp(const Student& a, const Student& b) {
    if (a.score != b.score) {
        return a.score > b.score; // 成绩从高到低（降序）
    }
    return a.name < b.name;       // 姓名按字典序从低到高（升序）
}

int main() {
    std::vector<Student> students = {
        {"Alice", 95},
        {"Bob", 88},
        {"Charlie", 95}
    };

    std::sort(students.begin(), students.end(), cmp);

    for (const auto& s : students) {
        std::cout << s.name << ": " << s.score << std::endl;
    }
    // 输出顺序：
    // Alice: 95
    // Charlie: 95  (Alice 和 Charlie 成绩相同，Alice 的字典序小，排在前面)
    // Bob: 88
    return 0;
}
```

> [!WARNING]
> 自定义比较函数 `cmp` 必须满足 **“严格弱序（Strict Weak Ordering）”**。简单来说，当两个元素完全相等时，`cmp` 必须返回 `false`。例如：在比较大小时必须使用 `>` 或 `<`，不能写成 `>=` 或 `<=`。如果写成 `>=`，在数据量较大时可能会导致程序崩溃（运行段错误）。

---

### 2.2 逆序函数：`std::reverse`

`std::reverse` 用于将指定区间内所有元素的顺序完全反转。它的时间复杂度为 **$O(n)$**。

```cpp
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s = "hello";
    std::reverse(s.begin(), s.end());
    std::cout << s << std::endl; // 输出：olleh

    int a[] = {1, 2, 3, 4};
    std::reverse(a + 1, a + 3); // 仅颠倒 a[1] 和 a[2]
    // 颠倒前 a: {1, 2, 3, 4}
    // 颠倒后 a: {1, 3, 2, 4}
    return 0;
}
```

---

## 三、 去重与填充：`unique` 与 `fill`

### 3.1 去重函数：`std::unique`

`std::unique` 用于去除区间内的相邻重复元素。它是去重操作中常用的函数，但使用时有两点需要特别注意：

> [!IMPORTANT]
> **使用注意事项**：
>
> 1. **必须先进行排序**：`unique` 只能去除**相邻**的重复元素。如果相同的元素不相邻，则无法去除。因此，去重前必须先调用 `std::sort` 对容器进行排序。
> 2. **不会改变容器大小**：`unique` 并没有真正删除重复元素，也不会改变容器的 `size()`。它只是把重复的元素移到了区间的末尾，并**返回一个迭代器，指向去重后有效数据末尾的下一个位置**。

#### ① `std::vector` 的完整去重写法（Erase-Unique 组合）

在 `std::vector` 中，如果需要把重复的元素彻底删除并缩减容器大小，我们需要配合 `vector::erase` 函数，把无用元素切除：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {3, 1, 1, 4, 1, 5, 2, 2};

    // 1. 必须先排序
    std::sort(v.begin(), v.end()); // v 变为 {1, 1, 1, 2, 2, 3, 4, 5}

    // 2. unique 去重新相邻元素，返回无用元素起点的迭代器
    auto new_end = std::unique(v.begin(), v.end()); // v 变为 {1, 2, 3, 4, 5, ?, ?, ?}

    // 3. 用 erase 把后面的无用元素删掉
    v.erase(new_end, v.end()); // v 变为真正的 {1, 2, 3, 4, 5}

    // 以上 2、3 步通常简写为一行代码：
    // v.erase(std::unique(v.begin(), v.end()), v.end());

    for (int x : v) std::cout << x << " "; // 输出：1 2 3 4 5
    return 0;
}
```

#### ② 普通数组的去重写法

如果是普通数组，我们可以通过“返回的指针”减去“数组首地址”来计算出有效去重后的新数组长度：

```cpp
int a[] = {1, 1, 2, 2, 3};
int n = 5;
std::sort(a, a + n);
int new_len = std::unique(a, a + n) - a; // new_len 等于 3
```

---

### 3.2 填充函数：`std::fill`

在编写算法时，我们经常需要初始化数组或 `vector`。

虽然可以使用 `memset`，但 `memset` 是按 **字节（Byte）** 填充的，通常只能安全地填充 `0` 或 `-1`。如果要把一个 `int` 数组的所有元素都初始化为其他数字（例如 `100` 或表示无穷大的 `1000000000`），就需要使用 `std::fill`。

`std::fill` 是按**元素的值**进行填充的，适用于所有数据类型，可以安全地填入任何数值。它的时间复杂度为 **$O(n)$**。

```cpp
#include <vector>
#include <algorithm>

int main() {
    // 将整个 vector 填充为 99
    std::vector<int> v(10);
    std::fill(v.begin(), v.end(), 99);

    // 将普通数组填充为极大值 1e9（用于最短路算法初始化）
    int dist[100];
    std::fill(dist, dist + 100, 1000000000);
    return 0;
}
```

---

## 四、 最值与二分查找：min/max_element 与二分查找

### 4.1 寻找最大值与最小值：std::min_element / std::max_element

这两个函数用于在指定区间内寻找最小值和最大值。它们返回的是指向该最值的**迭代器（如果是普通数组，则返回指针）**。时间复杂度为线性的 **$O(n)$**。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {30, 10, 50, 20, 40};

    // 寻找最大值的迭代器
    auto max_it = std::max_element(v.begin(), v.end());
    // 寻找最小值的迭代器
    auto min_it = std::min_element(v.begin(), v.end());

    // 1. 获取最大值和最小值
    std::cout << "最大值: " << *max_it << std::endl; // 输出：50
    std::cout << "最小值: " << *min_it << std::endl; // 输出：10

    // 2. 获取对应的下标（利用迭代器相减）
    int max_idx = max_it - v.begin();
    std::cout << "最大值所在的下标: " << max_idx << std::endl; // 输出：2
    return 0;
}
```

---

### 4.2 二分查找：std::lower_bound / std::upper_bound

如果我们需要在 `std::vector` 或普通数组中进行快速查找，可以使用这两个二分查找函数。

因为这些数据结构在内存中是连续的，支持随机访问，所以这两个函数查找的时间复杂度为极其高效的 **$O(\log n)$**。

> [!IMPORTANT]
> **使用前提**：进行查找的区间必须是**已经排好序**（默认升序）的。
>
> - **`std::lower_bound(first, last, x)`**：返回指向区间内第一个 **大于或等于 $\ge x$** 的元素的迭代器。
> - **`std::upper_bound(first, last, x)`**：返回指向区间内第一个 **严格大于 $> x$** 的元素的迭代器。

我们以排好序的数组 `a = {1, 3, 5, 5, 5, 8, 9}` 为例：

```cpp
#include <iostream>
#include <algorithm>

int main() {
    int a[] = {1, 3, 5, 5, 5, 8, 9};
    int n = 7;

    // 1. 查找第一个 >= 5 的位置
    auto it1 = std::lower_bound(a, a + n, 5);
    std::cout << "lower_bound(5) 下标: " << (it1 - a) << std::endl; // 输出：2

    // 2. 查找第一个 > 5 的位置
    auto it2 = std::upper_bound(a, a + n, 5);
    std::cout << "upper_bound(5) 下标: " << (it2 - a) << std::endl; // 输出：5

    // 💡 妙用：统计数字 5 在有序数组中出现的次数
    int count_5 = std::upper_bound(a, a + n, 5) - std::lower_bound(a, a + n, 5);
    std::cout << "数字 5 出现的次数: " << count_5 << std::endl; // 输出：3

    // 3. 判断某个数是否存在（必须完全匹配）
    auto it3 = std::lower_bound(a, a + n, 6);
    if (it3 != a + n && *it3 == 6) {
        std::cout << "找到了 6" << std::endl;
    } else {
        std::cout << "数组中没有 6" << std::endl; // 执行这一行
    }
    return 0;
}
```

---

## 五、 生成全排列：std::next_permutation

在一些需要枚举所有排列方式（爆搜或排列组合）的题目中，手写回溯（DFS）代码往往比较复杂。C++ 提供了 `std::next_permutation` 函数，可以自动将区间内的元素调整为**字典序的下一个更大的排列**。

- **返回值**：如果存在下一个更大的排列，则调整并返回 `true`；如果已经是字典序最大的排列（例如 `3 2 1`），则将其重置回最小的排列（升序，如 `1 2 3`），并返回 `false`。
- **时间复杂度**：生成一次排列的平均时间复杂度为 **$O(1)$**，最坏为 $O(n)$。

#### ① 输出 1 至 N 的全排列的经典写法

为了输出完整的所有排列，初始的数组或容器必须是 **升序排列（字典序最小）** 的，通常配合 `do-while` 循环使用：

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {3, 1, 2};

    // 1. 必须先排序，保证从字典序最小的排列开始
    std::sort(v.begin(), v.end()); // v 变为 {1, 2, 3}

    // 2. 配合 do-while 循环生成排列
    do {
        for (int x : v) {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    } while (std::next_permutation(v.begin(), v.end()));

    return 0;
}
```

**程序输出结果：**

```text
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
```

---

## 六、 常用算法函数汇总表

为了便于对比和复习，我们将上述算法函数的关键要点整理如下：

| 函数名称                    | 主要作用                            | 时间复杂度    | 对区间的排序要求               | 常见应用场景                                   |
| :-------------------------- | :---------------------------------- | :------------ | :----------------------------- | :--------------------------------------------- |
| **`std::sort`**             | 对区间内的元素进行升序/降序排列     | $O(n \log n)$ | 无要求                         | 离散化预处理、贪心算法、二分查找前置步骤       |
| **`std::reverse`**          | 将区间内所有元素的顺序完全反转      | $O(n)$        | 无要求                         | 字符串逆序、高精度计算、部分翻转操作           |
| **`std::unique`**           | 将区间内的**相邻**重复元素后移      | $O(n)$        | **必须是有序的**               | 数据查重、离散化步骤中的去重                   |
| **`std::fill`**             | 用指定的数值填充区间内的所有元素    | $O(n)$        | 无要求                         | 数组多组数据初始化、动态规划状态数组重置       |
| **`std::min/max_element`**  | 寻找区间内的最小值/最大值           | $O(n)$        | 无要求                         | 快速获取最值及其在容器中的下标                 |
| **`std::lower_bound`**      | 寻找首个 **$\ge$** 目标值的元素位置 | $O(\log n)$   | **必须是有序的**               | 快速数值检索、二分答案验证、最长上升子序列优化 |
| **`std::upper_bound`**      | 寻找首个 **$>$** 目标值的元素位置   | $O(\log n)$   | **必须是有序的**               | 统计元素重复个数、区间边界确定                 |
| **`std::next_permutation`** | 将区间重新排列为下一个字典序排列    | 平均 $O(1)$   | 生成完整排列时**需从升序开始** | 搜索枚举、深度优先搜索（DFS）替代方案          |

---

## 结语与下期预告

本文介绍了 C++ 标准算法库 `<algorithm>` 中常用算法的使用方法、时间复杂度和注意事项。熟练掌握并合理应用这些标准算法，不仅可以减少手写代码的负担，还能显著提升程序的运行效率。

在参加信奥比赛时，除了写出正确的算法代码外，如何正确地进行文件输入输出也是至关重要的。如果输入输出的文件名写错，可能会导致整道题得零分。

下一篇文章中，我们将详细讲解 C++ 竞赛中必须掌握的 **【文件操作与输入输出重定向（`freopen`）】**，帮助大家规范参赛代码，避免不必要的失分。
