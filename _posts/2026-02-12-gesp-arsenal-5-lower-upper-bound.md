---
layout: post
title: 【GESP/CSP】编程武器库-5, 二分查找标准库(lower_bound/upper_bound)
date: 2026-02-12 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 武器库-STL]
categories: [GESP, 必备技能]
---

> 在编程竞赛（如GESP、CSP-J/S）中，查找是一个非常高频的操作。对于无序数组，我们通常只能使用线性查找（$O(n)$）；但对于**有序数组**，利用**二分查找**可以将复杂度降低到 $O(\log n)$。C++ 标准库 `<algorithm>` 提供了两个非常强大的二分查找函数：`lower_bound` 和 `upper_bound`。熟练掌握它们，是通往高分的必备技能。
{: .prompt-info}

当前武器库清单

| 分类 | 功能 | 教程 |
|------|------|----------|
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为数字(0-9) | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为字母(a-z/A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为大写字母(A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为小写字母(a-z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [进制转换](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E8%BF%9B%E5%88%B6%E8%BD%AC%E6%8D%A2/) | 十进制和十六进制转换 |  [【GESP/CSP】编程武器库-2, 十进制转换十六进制](https://www.coderli.com/gesp-arsenal-2-dec-hex-conversion) |
| [进制转换](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E8%BF%9B%E5%88%B6%E8%BD%AC%E6%8D%A2/) | 十进制和十六进制转换 |  [【GESP/CSP】编程武器库-3, 十六进制转换十进制](https://www.coderli.com/gesp-arsenal-3-hex-dec-conversion/) |
| [数论](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E6%95%B0%E8%AE%BA/) | 最大公约数和最小公倍数 | [【GESP/CSP】编程武器库-4, 最大公约数和最小公倍数](https://www.coderli.com/gesp-arsenal-4-gcd-lcm/) |
| [STL](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-STL/) | 二分查找(lower_bound/upper_bound) | [【GESP/CSP】编程武器库-5, 二分查找(lower_bound/upper_bound)](https://www.coderli.com/gesp-arsenal-5-lower-bound) |

> 本人也是边学、边实验、边总结。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

<!--more-->

---

## 一、概念辨析

### 1. lower_bound

- **含义**：查找**第一个大于等于**（$\ge$）目标值 `val` 的元素的位置。
- **直观理解**：如果你要把 `val` 插入到这个有序序列中，且保持有序，那么 `lower_bound` 返回的就是**第一个**可以插入的位置（如果有多个相同的元素，插在它们的最前面）。


### 2. upper_bound

- **含义**：查找**第一个大于**（$>$）目标值 `val` 的元素的位置。
- **直观理解**：如果你要把 `val` 插入到这个有序序列中，且保持有序，那么 `upper_bound` 返回的就是**最后一个**可以插入的位置（即插在所有相同元素的后面）。

### 3. 举例说明

假设有一个有序数组 `a = {1, 2, 4, 4, 4, 6, 7}`：

- 查找 `4`：`lower_bound` 返回第一个 `4` 的位置（下标为 `2`）；`upper_bound` 返回 `6` 的位置（下标为 `5`）。
- 查找 `3`：两者都返回第一个 `4` 的位置（因为第一个 $\ge 3$ 和第一个 $> 3$ 的数都是 `4`）。
- 查找 `5`：两者都返回 `6` 的位置。

在使用 `lower_bound`/`upper_bound` 之前，必须强调一个**前提条件**：

> **序列必须是有序的！**
> - 默认为**升序**（从小到大）。
> - 如果是**降序**（从大到小），则必须添加比较器 `greater<int>()`（详见第四章第4节）。
> - 如果序列无序，结果是未定义的（错误的）。

---

## 二、语法与返回值

这两个函数都包含在头文件 `<algorithm>` 中。

### 函数原型

```cpp
// 1. 默认版本（用于升序）
// first: 数组名 或 容器的 begin() 迭代器
// last: 数组结束地址 或 容器的 end() 迭代器
// val: 要查找的值
std::lower_bound(first, last, val);
std::upper_bound(first, last, val);

// 2. 自定义比较器版本（常用 std::greater<type>() 用于降序）
std::lower_bound(first, last, val, std::greater<int>());
```

### 调用示例

```cpp
// 1. 在数组 a 中查找 5
std::lower_bound(a, a + n, 5);       

// 2. 在 vector v 中查找 5
std::lower_bound(v.begin(), v.end(), 5); 

// 3. 在降序数组 a 中查找 5
std::lower_bound(a, a + n, 5, std::greater<int>()); 
```

### 返回值详解

`lower_bound` 和 `upper_bound` 返回的都是**迭代器（Iterator）**。

- 对于**数组**，迭代器就是**指针**。
- 对于 **vector**，迭代器是 `vector<int>::iterator` 类型。

#### 1. 找到的情况

* **数组**：返回指向该元素的**指针**。
    * 可以通过解引用 `*p` 获取该位置的值。
    * 可以通过 `p - 数组首地址` 获取该元素的**下标**。
* **Vector**：返回指向该元素的**迭代器**。
    * 可以通过解引用 `*it` 获取该位置的值。
    * 可以通过 `it - v.begin()` 获取该元素的**下标**。



#### 2. 没找到的情况

如果整个序列中都没有大于等于（或大于）`val` 的元素，函数会返回传入的查找范围的**结束位置**。

* **数组**：返回 `数组首地址 + 数组长度` (即 `last` 指针)。
* **Vector**：返回 `v.end()`。

> **注意**：返回的结束位置是**越界**的，**不能**直接解引用，否则会报错。使用前务必判断返回值是否等于结束位置。
{: .prompt-warning}

#### 3. 代码演示

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // --- 1. 数组示例 ---
    int a[] = {10, 20, 30, 40};
    // 查找 >= 30 的第一个元素
    int* p = std::lower_bound(a, a + 4, 30); // 返回指针
    
    std::cout << "数组找到的值: " << *p << std::endl;        // 解引用取值 -> 30
    std::cout << "数组下标: " << p - a << std::endl;         // 指针减法取下标 -> 2
    
    // --- 2. Vector 示例 ---
    std::vector<int> v = {10, 20, 30, 40};
    // 查找 >= 30 的第一个元素
    auto it = std::lower_bound(v.begin(), v.end(), 30); // 返回迭代器
    
    std::cout << "Vector找到的值: " << *it << std::endl;     // 解引用取值 -> 30
    std::cout << "Vector下标: " << it - v.begin() << std::endl; // 迭代器减法取下标 -> 2
    
    return 0;
}
```

**运行结果：**

```text
数组找到的值: 30
数组下标: 2
Vector找到的值: 30
Vector下标: 2
```

## 三、完整应用举例（重点）

为了彻底搞懂，我们看一个具体的例子。假设有一个有序数组 `a`：

```cpp
// 下标： 0   1   2   3   4   5
int a[] = {10, 20, 20, 30, 40, 50};
int n = 6;
```

### 场景 1：查找存在的元素，例如 20

* `lower_bound(a, a + n, 20)`：寻找第一个 **$\ge$ 20** 的位置。
    * 结果：指向下标 **1** 的位置（第一个 20）。
* `upper_bound(a, a + n, 20)`：寻找第一个 **$>$ 20** 的位置。
    * 结果：指向下标 **3** 的位置（30 的位置）。

### 场景 2：查找不存在的元素，例如 25
* `lower_bound(a, a + n, 25)`：寻找第一个 **$\ge$ 25** 的位置。
    * 结果：指向下标 **3** 的位置（30 的位置）。因为 30 是第一个大于等于 25 的数。
* `upper_bound(a, a + n, 25)`：寻找第一个 **$>$ 25** 的位置。
    * 结果：指向下标 **3** 的位置（30 的位置）。
* **注意**：当查找元素不存在时，`lower` 和 `upper` 的返回值通常是相同的，都指向“它应该被插入的位置”。

### 场景 3：查找比所有元素都大的数，例如 100

* 所有元素都小于 100，所以找不到。
* `lower_bound(a, a + n, 100)` 和 `upper_bound(a, a + n, 100)` 都会返回 `a + n`（即下标 6，**越界位置**）。
* **判断未找到的方法**：检查返回值是否等于 `end()`（对于数组是 `a + n`）。

### 场景 4：查找比所有元素都小的数，例如 5

* `lower_bound(a, a + n, 5)`：寻找第一个 **$\ge$ 5** 的位置。
    * 结果：指向下标 **0** 的位置（10 的位置）。
* `upper_bound(a, a + n, 5)`：寻找第一个 **$>$ 5** 的位置。
    * 结果：指向下标 **0** 的位置（10 的位置）。

### 完整的可直接运行代码示例

将上述逻辑整合到 C++ 代码中，可以直接复制运行查看结果：

```cpp
#include <iostream>
#include <algorithm> // 必须包含 lower_bound 和 upper_bound

int main() {
    // 准备有序数组
    int a[] = {10, 20, 20, 30, 40, 50};
    int n = 6;

    std::cout << "数组内容: {10, 20, 20, 30, 40, 50}" << std::endl << std::endl;

    // --- 场景 1: 查找存在的元素 (20) ---
    std::cout << "=== 场景 1: 查找 20 ===" << std::endl;
    // 1. 使用 int* 接收返回值（迭代器/指针）
    // 注意：如果是 vector，则使用 std::vector<int>::iterator 或 auto
    int* ptr_lb_20 = std::lower_bound(a, a + n, 20); // 返回指向第一个 >= 20 的元素的指针
    int* ptr_ub_20 = std::upper_bound(a, a + n, 20); // 返回指向第一个 > 20 的元素的指针
    
    // 2. 将指针转换为下标 (通过减去数组首地址 a)
    int lb_20 = ptr_lb_20 - a; 
    int ub_20 = ptr_ub_20 - a;
    
    std::cout << "lower_bound(20) 下标: " << lb_20 << " (对应值: " << *ptr_lb_20 << ")" << std::endl; // 输出: 1 (值为 20)
    std::cout << "upper_bound(20) 下标: " << ub_20 << " (对应值: " << *ptr_ub_20 << ")" << std::endl; // 输出: 3 (值为 30)

    // --- 场景 2: 查找不存在的元素 (25) ---
    std::cout << "\n=== 场景 2: 查找 25 ===" << std::endl;
    int* ptr_lb_25 = std::lower_bound(a, a + n, 25);
    int* ptr_ub_25 = std::upper_bound(a, a + n, 25);
    
    int lb_25 = ptr_lb_25 - a;
    int ub_25 = ptr_ub_25 - a;
    
    std::cout << "lower_bound(25) 下标: " << lb_25 << " (对应值: " << *ptr_lb_25 << ")" << std::endl; // 输出: 3 (值为 30)
    std::cout << "upper_bound(25) 下标: " << ub_25 << " (对应值: " << *ptr_ub_25 << ")" << std::endl; // 输出: 3 (值为 30)

    // --- 场景 3: 查找超大元素 (100) ---
    std::cout << "\n=== 场景 3: 查找 100 ===" << std::endl;
    int* ptr_lb_100 = std::lower_bound(a, a + n, 100);
    int* ptr_ub_100 = std::upper_bound(a, a + n, 100);
    
    // 判断是否越界 (即没找到)
    if (ptr_lb_100 == a + n) {
        std::cout << "lower_bound(100) 返回 a + n，表示未找到 (越界)" << std::endl;
    }
    if (ptr_ub_100 == a + n) {
        std::cout << "upper_bound(100) 返回 a + n，表示未找到 (越界)" << std::endl;
    }

    // --- 场景 4: 查找超小元素 (5) ---
    std::cout << "\n=== 场景 4: 查找 5 ===" << std::endl;
    int* ptr_lb_5 = std::lower_bound(a, a + n, 5);
    int* ptr_ub_5 = std::upper_bound(a, a + n, 5);
    
    std::cout << "lower_bound(5) 下标: " << ptr_lb_5 - a << " (对应值: " << *ptr_lb_5 << ")" << std::endl; // 输出: 0 (值为 10)
    std::cout << "upper_bound(5) 下标: " << ptr_ub_5 - a << " (对应值: " << *ptr_ub_5 << ")" << std::endl; // 输出: 0 (值为 10)

    return 0;
}
```

**程序运行输出结果：**

```text
数组内容: {10, 20, 20, 30, 40, 50}

=== 场景 1: 查找 20 ===
lower_bound(20) 下标: 1 (对应值: 20)
upper_bound(20) 下标: 3 (对应值: 30)

=== 场景 2: 查找 25 ===
lower_bound(25) 下标: 3 (对应值: 30)
upper_bound(25) 下标: 3 (对应值: 30)

=== 场景 3: 查找 100 ===
lower_bound(100) 返回 a + n，表示未找到 (越界)
upper_bound(100) 返回 a + n，表示未找到 (越界)

=== 场景 4: 查找 5 ===
lower_bound(5) 下标: 0 (对应值: 10)
upper_bound(5) 下标: 0 (对应值: 10)
```

### Vector 完整代码示例（含迭代器说明）

在 `vector` 中，`lower_bound`/`upper_bound` 返回的是 **迭代器 (Iterator)**，而不是指针。
*   **指针**：用于数组。可以直接理解为内存地址。
*   **迭代器**：用于容器（如 vector, set, map）。可以理解为“广义的指针”，用法和指针非常像（支持解引用 `*it`，支持加减运算）。
*   **区别**：要获取下标时，数组是用 `ptr - 数组首地址`，而 vector 是用 `it - v.begin()`。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // 准备有序 vector
    std::vector<int> v = {10, 20, 30, 30, 30, 40, 50};
    
    std::cout << "Vector内容: {10, 20, 30, 30, 30, 40, 50}" << std::endl << std::endl;

    // --- 查找 30 的范围 ---
    std::cout << "=== 查找 30 ===" << std::endl;
    
    // 1. 使用迭代器接收返回值
    // std::vector<int>::iterator 是完整类型名，太长了，通常用 auto 关键字自动推导
    std::vector<int>::iterator it_lb = std::lower_bound(v.begin(), v.end(), 30);
    auto it_ub = std::upper_bound(v.begin(), v.end(), 30); // 推荐用 auto
    
    // 2. 将迭代器转换为下标 (通过减去 v.begin())
    int idx_lb = it_lb - v.begin();
    int idx_ub = it_ub - v.begin();
    
    std::cout << "lower_bound(30) 下标: " << idx_lb << " (对应值: " << *it_lb << ")" << std::endl; // 输出: 2
    std::cout << "upper_bound(30) 下标: " << idx_ub << " (对应值: " << *it_ub << ")" << std::endl; // 输出: 5
    
    std::cout << "30 出现的次数: " << idx_ub - idx_lb << std::endl; // 输出: 3
    std::cout << "30 出现的下标范围: [" << idx_lb << ", " << idx_ub - 1 << "]" << std::endl;

    // --- 查找不存在的元素 35 ---
    std::cout << "\n=== 查找 35 ===" << std::endl;
    auto it_35 = std::lower_bound(v.begin(), v.end(), 35);
    
    // 判断是否越界 (即没找到)
    if (it_35 == v.end()) {
        std::cout << "没找到 35 (越界)" << std::endl;
    } else {
        std::cout << "35 应该插入的位置下标: " << it_35 - v.begin() << std::endl; // 输出: 5 (40的位置)
    }

    return 0;
}
```

**关键点总结：**
* **数组**：返回值类型是 `int*`，计算下标用 `ptr - a`。
* **Vector**：返回值类型是 `vector<int>::iterator`，计算下标用 `it - v.begin()`。
* **通用性**：`auto` 关键字非常方便，它可以自动推导这两种类型，建议熟练使用。

## 四、关键概念补充：迭代器与 auto

在使用 `lower_bound`/`upper_bound` 时，经常遇到返回类型很长的情况，这时 `auto` 关键字就非常有用了。

### 1. 迭代器 (Iterator)与指针 (Pointer) 的区别
* **指针**：主要用于**原始数组**。例如 `int* p = &a[0];`。它指向内存中的具体地址。
* **迭代器**：主要用于**STL容器**（如 `vector`, `set`）。它行为像指针（可以 `*it` 解引用，也可以 `it++` 移动），但它本质上是一个封装好的类对象。

#### 为什么一定要用迭代器？

试想一下，`vector`（动态数组）、`list`（链表）、`set`（红黑树）它们的**底层存储结构完全不同**。
* 数组内存是连续的，可以用下标访问。
* 链表内存是分散的，只能顺藤摸瓜。
* 树结构更加复杂。

如果我们要为每种数据结构都写一套查找、排序算法，工作量巨大且容易出错。
**迭代器**的作用就是**屏蔽底层的差异**，提供一套**统一的操作接口**（比如都用 `*it` 取值，`it++` 找下一个）。这样 `std::lower_bound` 只需要通过迭代器操作，就能通用于各种容器，极大地提高了代码的复用性。


### 2. 巧用 auto 简化代码
C++11 引入了 `auto` 关键字，它可以让编译器自动推导变量的类型。

**不使用 auto (类型非常长):**
```cpp
std::vector<int>::iterator it = std::lower_bound(v.begin(), v.end(), 20);
```

**使用 auto (简洁):**
```cpp
auto it = std::lower_bound(v.begin(), v.end(), 20);
```

**代码对比示例：**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {1, 3, 5, 7, 9};

    // 1. 传统繁琐写法
    // std::vector<int>::iterator 是完整类型名
    std::vector<int>::iterator it1 = std::lower_bound(nums.begin(), nums.end(), 5);
    std::cout << "Index (传统): " << it1 - nums.begin() << std::endl;

    // 2. auto 现代写法（强烈推荐）
    // 编译器会自动推导出 it2 也是 std::vector<int>::iterator 类型
    auto it2 = std::lower_bound(nums.begin(), nums.end(), 5);
    std::cout << "Index (auto): " << it2 - nums.begin() << std::endl;
    
    return 0;
}
```

---

## 五、常见应用场景

### 1. 判断元素是否存在
虽然 `binary_search` 可以直接判断是否存在，但在做题时，我们往往需要知道“如果存在，在哪里”或者“如果不存在，它应该在哪里”。
使用 `lower_bound` 可以更灵活地判断：

```cpp
int pos = std::lower_bound(a, a + n, val) - a;
if (pos < n && a[pos] == val) {
    // 存在
} else {
    // 不存在
}
```

### 2. 查找某个数的出现次数

对于有序数组，数值 `val` 出现的次数等于 `upper_bound` 的位置减去 `lower_bound` 的位置。

```cpp
int count = std::upper_bound(a, a + n, val) - std::lower_bound(a, a + n, val);
```
- 如果 `val` 不存在，两者返回位置相同，相减为 0。

### 3. 查找第一个大于等于某数的位置

这是题目中最直接的考法。例如：在一组数据中，找到第一个及格（$\ge 60$）的分数。

### 4. 降序数组的查找

如果数组是从大到小排好序的，默认的 `lower_bound`（找 $\ge$）就不适用了。我们需要传入比较器 `greater<int>()`。
**注意**：在降序情况下，`lower_bound` 的含义变为查找**第一个小于等于**（$\le$）`val` 的元素。

```cpp
// 降序数组
int b[] = {9, 7, 5, 5, 2, 1};
// 查找第一个 <= 5 的位置
int idx = std::lower_bound(b, b + 6, 5, std::greater<int>()) - b; 
// 结果是下标 2 (即数组中的第一个 5)

// 查找第一个 < 5 的位置
int idx_upper = std::upper_bound(b, b + 6, 5, std::greater<int>()) - b;
// 结果是下标 4 (即数组中的 2)
```

---

{% include custom/custom-post-content-footer.md %}
