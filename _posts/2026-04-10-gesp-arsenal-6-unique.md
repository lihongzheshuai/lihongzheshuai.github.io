---
layout: post
title: 【GESP/CSP】编程武器库-6, 去重算法(unique)
date: 2026-04-10 12:30 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 武器库-STL]
categories: [GESP, 必备技能]
---

> 在信息学竞赛（如GESP、CSP-J/S）中，对数据去重是一项基石操作。在 C++ 的 STL（标准模板库）中，`<algorithm>` 头文件提供了一把处理数据的“去重”利器——`std::unique` 函数。熟知其“双指针覆盖”设计思想并结合 `sort` 与 `erase` 灵活运用，可以极大地精简代码、降低时间常数。
> {: .prompt-info}

当前武器库清单

| 分类                                                                                                       | 功能                              | 教程                                                                                                              |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为数字(0-9)               | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)          |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为字母(a-z/A-Z)           | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)          |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为大写字母(A-Z)           | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)          |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为小写字母(a-z)           | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)          |
| [进制转换](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E8%BF%9B%E5%88%B6%E8%BD%AC%E6%8D%A2/) | 十进制和十六进制转换              | [【GESP/CSP】编程武器库-2, 十进制转换十六进制](https://www.coderli.com/gesp-arsenal-2-dec-hex-conversion)         |
| [进制转换](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E8%BF%9B%E5%88%B6%E8%BD%AC%E6%8D%A2/) | 十进制和十六进制转换              | [【GESP/CSP】编程武器库-3, 十六进制转换十进制](https://www.coderli.com/gesp-arsenal-3-hex-dec-conversion/)        |
| [数论](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E6%95%B0%E8%AE%BA/)                       | 最大公约数和最小公倍数            | [【GESP/CSP】编程武器库-4, 最大公约数和最小公倍数](https://www.coderli.com/gesp-arsenal-4-gcd-lcm/)               |
| [STL](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-STL/)                                       | 二分查找(lower_bound/upper_bound) | [【GESP/CSP】编程武器库-5, 二分查找(lower_bound/upper_bound)](https://www.coderli.com/gesp-arsenal-5-lower-bound) |
| [STL](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-STL/)                                       | 去重算法(unique)                  | [【GESP/CSP】编程武器库-6, 去重算法(unique)](https://www.coderli.com/gesp-arsenal-6-unique/)                      |

> 本人也是边学、边实验、边总结。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
> {: .prompt-warning}

<!--more-->

---

## 一、概念辨析

### 1. 核心作用

顾名思义，`unique` 在 C++ 中的核心作用非常明确：**“消除”指定范围内相邻的重复元素**。
千万要注意这里的关键词——**相邻**。这也决定了如果要实现全体性质的彻底去重，它通常需要首先与 `std::sort`（排序算法）配合使用，使相同元素聚拢在一起，才能发挥最大的效能。

### 2. 设计思想与误区

初学者常常会对 `unique` 产生一个误解：_以为调用了它之后，数组或容器的真实长度就变短了。_
**事实上，`unique` 绝对不会改变数组或 `vector` 等容器的物理大小！**

STL 的算法在设计时遵循了一条铁律：**算法只操作迭代器产生的数据流，不负责容器空间的扩展或收缩**。因此，`unique` 的工作逻辑本质上是运用了 **双指针（读写指针）** 滑动覆盖的思想：

1. 它从前往后遍历序列。
2. 遇到连续相同的元素，它会选择跳过读取。
3. 遇到不同的新元素，它会紧接着将其**覆盖拷贝**到前面已经处理好的“无重复序列”的尾端处。
4. 遍历完成后，它会返回一个迭代器（或普通指针），指向**新生成的无重复序列有效数据的下一个位置**。

#### 图解演示：双指针的覆盖魔法

为了更直观地理解，我们来模拟一个具体过程。假设有排好序的数组 `[1, 1, 2, 2, 3]`，底层通常利用两个核心哨兵来完成遍历：**写指针（Write）** 与 **读指针（Read）**。

- **初始状态**：两只指针都在头部起始端。确定下绝对独一的第一个数字 `1`。  
  `[ 1(W, R),  1,  2,  2,  3 ]`
- **第一步**：`R 指针`往后探查，发现遇到了相同数字 `1`，于是直接无视跳过。  
  `[ 1(W),  1(R),  2,  2,  3 ]`
- **第二步**：`R 指针`继续前进探寻遇到新数字 `2`，因此迅速将其**拷贝**到 `W 指针`的正后方格子中，并让 `W 指针`向右跨一步。  
  `[ 1,  2(W),  2(R),  2,  3 ]` _(注意观察：这期间第二个位置的旧数字 `1` 已经被抹去，覆盖为了 `2`)_
- **第三步**：`R 指针`接着扫描走到第四格，遇到了同伙 `2`，再次判定重复而无视跳过。  
  `[ 1,  2(W),  2,  2(R),  3 ]`
- **第四步**：`R 指针`抵达末端格子，发现崭新的数字 `3`，同样复制并拍到 `W 指针`后方的格子里。  
  `[ 1,  2,  3(W),  2,  3(R) ]`

**遍历结束！**当 `R 指针`越界，代表全局检索完毕。细看此刻数组在内存中的物理布局，实际变成了 `[1, 2, 3, 2, 3]`。
其前半部 `[1, 2, 3]` 正是我们追求的无重序列；而后半部的 `[2, 3]` 则是未被覆盖区域留下的**废旧原迹**。此刻 `unique` 功成身退，但为了区分边界，它将返回 `W 指针`的**下一个位置**（即下标为 $3$ ），告诉外界：“真正的结尾划线划在这里！”

> **注意**：原地的覆盖操作并不缩容，这导致原序列末端会残留一些“废弃”的脏数据（悬浮状态）。如果不加处理直接遍历容器的原本长度，就会读到奇怪的残留数值。
> {: .prompt-warning}

### 3. 算法复杂度剖析

正如上述双指针推演模型所展现的那样：`unique` 底层内部仅仅靠着一层单向扫描循环走遍了整个给定的序列区间。

- **时间复杂度**：读指针（Read）由始至终精准滑过 $N$ 个元素，没有回溯动作，所有元素只被访问判定一次；写指针（Write）仅在触发需要时才执行单次的覆盖赋值动作，$N$ 次循环内这步操作最多发生 $N$ 次。因此，`unique` 核心去重过程带来的**时间复杂度是 $\mathcal{O}(N)$ (线性时间)**。
- **空间复杂度**：由于一切皆在数组原物理空间内进行（In-place 原地算法），它没有向操作系统提出任何新栈或新堆的大额内存申请，只额外动用了零星两三个局部游标变量，因此它的**空间复杂度为 $\mathcal{O}(1)$**。

基于其优秀的时空复杂度，在处理海量数据的离散化等场景时，使用 `sort` ($\mathcal{O}(N \log N)$) 搭配 `unique` ($\mathcal{O}(N)$) 已经成为业界与算法竞赛中的标准高效方案。

---

## 二、语法与使用方法

`unique` 函数包含在头文件 `<algorithm>` 中。

### 函数原型

```cpp
// 1. 默认版本（要求事先排序将相同元素靠拢）
// first: 数组名 或 容器的 begin() 迭代器
// last: 数组结束地址 或 容器的 end() 迭代器
std::unique(first, last);

// 2. 自定义比较器版本（告诉函数遇到什么情况认为两者相等）
std::unique(first, last, [](const Type& a, const Type& b){ return a == b; });
```

### 返回值详解

`unique` 返回的是**迭代器（Iterator）**（对于数组就是**指针**）。它指向的是**去重后无重复序列逻辑末端**的下一个位置。

- 通过返回的迭代器减去容器的首地址，就可以直接得到去重后的独立元素个数。
- 例如：`int k = std::unique(a, a + n) - a;`

---

## 三、完整应用举例（重点）

### 场景 1：全局普通大数组去重

在信息学竞赛编程或追求极致性能的代码中，如果使用全局大数组，巧妙利用指针相减来获取去重后的实际元素个数最为常用：

```cpp
#include <iostream>
#include <algorithm>

int main() {
    int a[] = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    int n = sizeof(a) / sizeof(a[0]);

    // 步骤1：先排序，相同的元素挨在一起，这是全局去重的必要前提
    std::sort(a, a + n);
    // 排序后为: 1, 1, 2, 3, 3, 4, 5, 5, 6, 9

    // 步骤2：使用 unique 覆盖相邻的重复元素
    // k 等同于非重复元素的个数
    int k = std::unique(a, a + n) - a;

    std::cout << "去重后的元素个数: " << k << std::endl;
    std::cout << "去重后的数组内容: ";
    // 注意：这里的循环上限变成了 k，摒弃了尾部的脏数据
    for (int i = 0; i < k; i++) {
        std::cout << a[i] << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

**运行结果：**

```text
去重后的元素个数: 6
去重后的数组内容: 1 2 3 4 5 6 9
```

### 场景 2：对 `vector` 彻底去重（Erase-Remove 惯用法）

想要在物理或逻辑层面为 `vector` 完全清理掉末尾留存的废弃部分，可以使用著名的 **Erase-Remove（Erase-Unique）连招**。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};

    // 1. 从小到大排序
    std::sort(v.begin(), v.end());

    // 2. 将 unique 返回的指向脏数据的头部指针传给 vector 自身的 erase 函数：
    // 执行一键区间抹除，实现物理上的缩容！
    auto it = std::unique(v.begin(), v.end());
    v.erase(it, v.end());

    // 一步到位紧凑写法：
    // v.erase(std::unique(v.begin(), v.end()), v.end());

    std::cout << "彻底去重后的新长度: " << v.size() << std::endl;
    for (int num : v) {
        std::cout << num << " ";
    }
    return 0;
}
```

---

## 四、常见高阶场景进阶

### 自定义比较规则（处理结构体等）

不仅仅用于 `int` 等基础类型，对于有着诸如 `id`、`name` 构成的学生对象等结构体，只要提供自定义判别同样游刃有余。

```cpp
struct Student { int id; std::string name; };

// 步骤1：排序时按 id 靠拢
std::sort(stu.begin(), stu.end(), [](const Student& a, const Student& b) {
    return a.id < b.id;
});

// 步骤2：去重时，只要 id 相同就算作重复元素消除
auto it = std::unique(stu.begin(), stu.end(), [](const Student& a, const Student& b) {
    return a.id == b.id;
});
stu.erase(it, stu.end());
```
