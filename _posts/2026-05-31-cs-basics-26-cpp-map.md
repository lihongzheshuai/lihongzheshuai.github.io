---
layout: post
title: 【信奥业余科普】C++ 的奇妙之旅 | 26：高效的键值对——映射（map）与多重映射（multimap）
date: 2026-05-31 08:00:00 +0800
author: OneCoder
comments: true
math: true
tags: [科普, 计算机科学基础, GESP, CSP, C++, STL, map, multimap]
categories: [信奥业余科普, C++的奇妙之旅]
---

上一篇文章我们介绍了 `set` 和 `multiset`，它们通过底层的红黑树实现自动去重、自动排序，以及在 $O(\log n)$ 时间内进行查找的机制。

但是，`set` 只能存放单一的元素（也就是 **键 Key**）。在很多实际的信奥问题或开发场景中，我们需要的是一种“对应关系”。例如：

- 给你一个学生的名字（Key），你需要快速查出他的信奥成绩（Value）；
- 给你一个英文单词（Key），你需要快速查出它的中文释义（Value）；
- 给你一个身份证号（Key），你需要快速查出对应的个人信息（Value）。

这种“键（Key）到值（Value）”的对应关系，在计算机科学中被称为 **“键值对（Key-Value Pair）”**。

今天，我们来学习 C++ STL 中用于处理键值对的关联容器—— **`map`（映射）** 与 **`multimap`（多重映射）**。

<!--more-->

**往期回顾：**

- [第一部分【计算机历史】系列文章合集（共8篇）](https://www.coderli.com/categories/%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%8E%86%E5%8F%B2/)
- [第二部分【C++的奇妙之旅】前25篇合集](https://www.coderli.com/categories/c-%E7%9A%84%E5%A5%87%E5%A6%99%E4%B9%8B%E6%97%85/)

---

## 一、 什么是 pair与映射（map）？

在深入 `map` 之前，我们需要先认识它的基本构建基石—— **`std::pair`**。

### 1.1 基础结构：`std::pair`

`pair` 也是 C++ STL 中的一个模板类（定义在 `<utility>` 中，但引入 `<map>` 时会自动包含）。它可以把两个不同类型的值“打包”绑定成一个单一的复合结构。

```cpp
#include <iostream>
#include <utility>
#include <string>

int main() {
    // 创建一个 pair，保存一个 string 和一个 int
    std::pair<std::string, int> p = {"Alice", 95};

    // 访问 pair 的两个成员：first 和 second
    std::cout << "键 (Key): " << p.first << std::endl;     // 输出：Alice
    std::cout << "值 (Value): " << p.second << std::endl;   // 输出：95

    // 也可以使用 std::make_pair 来创建
    auto p2 = std::make_pair("Bob", 88);
    return 0;
}
```

### 1.2 map的本质

C++ STL 中的 `map` 本质上就是**由众多键值对（`pair`）组成的集合**。

它有两个核心特征：

1. **键（Key）唯一**：映射中不允许出现两个相同的键。每个键只能对应唯一的一个值（Value）。但值（Value）本身是可以重复的（比如 Alice 和 Bob 都可以是 95 分）。
2. **按键（Key）排序**：容器内部会自动按照**键（Key）从小到大**的顺序排列（默认升序）。

### 1.3 底层结构

和 `set` 一样，`map` 的底层也是基于 **平衡二叉搜索树（红黑树）** 实现的。

- 只是在红黑树的每个节点上，保存的不仅是一个 Key，而是一个完整的 `pair<const Key, Value>`。
- 树的排序 and 平衡调整完全是基于 `pair` 中的 `first`（即 Key）来进行的，而 `second`（即 Value）只是作为一个挂载数据默默陪伴。
- 因此，`map` 的插入、删除和查找操作，时间复杂度同样是 **$O(\log n)$**。

---

## 二、 map的常用操作

使用 `map` 需要引入头文件 `<map>`。

### 2.1 创建与初始化

```cpp
#include <map>
#include <string>

// 创建一个以 string 为键，int 为值的空 map
std::map<std::string, int> scores;

// 创建并初始化
std::map<std::string, int> age_map = {
    {"Alice", 18},
    {"Bob", 19},
    {"Charlie", 17}
};
```

### 2.2 插入与更新：下标操作符 `[]`

在 `map` 中，插入和更新数据最常用、最直观的方式就是使用下标操作符 `[]`。

```cpp
std::map<std::string, int> m;

// 1. 插入新元素
m["Alice"] = 95;   // 发现 "Alice" 不存在，新建该键值对，并赋值为 95
m["Bob"] = 88;     // 发现 "Bob" 不存在，新建该键值对，并赋值为 88

// 2. 更新已有元素的值
m["Alice"] = 100;  // 发现 "Alice" 已经存在，将其值从 95 修改为 100

std::cout << "Alice 的成绩: " << m["Alice"] << std::endl; // 输出 100
```

> [!NOTE]
> 除了 `[]`，你也可以用传统的 `insert` 方式插入元素，但相对繁琐：
> `m.insert(std::make_pair("Charlie", 90));` 或 `m.insert({"Charlie", 90});`
> 需要特别注意的是，如果使用 `insert` 插入一个**已经存在**的键，`insert` 会**默默失败且不会覆盖原有的值**。而下标 `[]` 方式则会直接用新值覆盖旧值。

### 2.3 注意事项：使用 `[]` 查找时的副作用

虽然 `[]` 非常方便，但使用时也需要注意其特殊的行为特点。

**其行为原理是**：当访问 `m[key]` 时，如果该 `key` **不存在**，`map` 会**在容器中自动插入这个 `key`**，并将其值初始化为默认值（例如整型为 `0`，指针为 `nullptr`，`string` 为空字符串）。

这可能会引发非预期的行为：

```cpp
std::map<std::string, int> scores;
scores["Alice"] = 95;

// 假设我们只是想判断一下 Charlie 是否在 map 里
if (scores["Charlie"] == 100) {
    std::cout << "满分！" << std::endl;
}

// 此时检查 map 的大小：
std::cout << "Scores 大小: " << scores.size() << std::endl; // 输出为 2
```

**原因分析**：在执行 `scores["Charlie"]` 时，如果键 `"Charlie"` 不存在，`map` 会自动向容器中插入 `{"Charlie", 0}` 并返回其引用。如果原本只是为了查询或判断，这种写法会无意中改变容器的大小和内容。

### 💡 推荐写法：使用 `find` 或 `count` 进行查找

在不确定某个键是否存在时，建议使用以下两种方式进行查找以避免意外插入：

**方法一：使用 `find()` （最推荐）**
`find(key)` 会返回指向该元素的迭代器。如果没找到，会返回 `end()` 迭代器，且绝对不会插入新元素。

```cpp
auto it = scores.find("Charlie");
if (it != scores.end()) {
    std::cout << "找到了 Charlie，分数是: " << it->second << std::endl; // 通过迭代器访问 value
} else {
    std::cout << "Charlie 不在名册中" << std::endl; // 执行这一行，scores 大小依然是 1
}
```

**方法二：使用 `count()`**
`count(key)` 返回某个键出现的次数。因为 `map` 中键唯一，所以只可能返回 `0` 或 `1`。

```cpp
if (scores.count("Charlie")) {
    std::cout << "Charlie 存在，分数为: " << scores["Charlie"] << std::endl; // 此时用 [] 是安全的
} else {
    std::cout << "Charlie 不存在" << std::endl;
}
```

### 2.4 删除元素 (`erase`)

删除元素可以通过键直接删除，也可以传入迭代器：

{% raw %}

```cpp
std::map<std::string, int> m = {{"Alice", 95}, {"Bob", 88}};

m.erase("Bob"); // 直接根据 Key 删除，删除成功返回 1，若 Key 不存在返回 0

auto it = m.find("Alice");
if (it != m.end()) {
    m.erase(it); // 传入迭代器进行精确删除
}
```

{% endraw %}

### 2.5 遍历 map

因为 `map` 里的元素都是 `std::pair`，所以在遍历时，我们需要通过访问 `first` 和 `second` 来获取键和值。

**C++11 经典写法**：

{% raw %}

```cpp
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 88}};

// 推荐使用 const auto& 避免不必要的拷贝
for (const auto& kv : scores) {
    std::cout << kv.first << " 的成绩是: " << kv.second << std::endl;
}
```

{% endraw %}

**C++17 结构化绑定写法**：
C++17 引入了结构化绑定（Structured Binding），可以直接把 `pair` 的成员解构出来，使代码更加简洁：

```cpp
for (const auto& [name, score] : scores) {
    std::cout << name << " 的成绩是: " << score << std::endl;
}
```

---

## 三、 多重映射（`multimap`）

类似于 `multiset`，有的时候我们也需要**允许键（Key）重复**的映射容器。这时就需要用到 **`multimap`**。

使用 `multimap`，你可以让一个“英文单词”对应多个不同的“中文例句”。

```cpp
#include <map>
#include <string>
#include <iostream>

int main() {
    std::multimap<std::string, std::string> dict;

    // 插入重复键的元素
    dict.insert({"run", "奔跑"});
    dict.insert({"run", "运行"});
    dict.insert({"run", "经营"});

    std::cout << "run 含义的个数: " << dict.count("run") << std::endl; // 输出 3
    return 0;
}
```

### ⚠️ `multimap` 的重要不同点

因为允许键重复，`multimap` 在行为上与 `map` 有很大区别：

1. **绝对没有下标操作符 `[]`**：
   如果写 `dict["run"]`，编译器根本无法知道你想访问或修改哪一个 `run`。因此，`multimap` 没有实现 `[]` 操作符。插入数据必须使用 `insert`。
2. **删除某个键会将其“一网打尽”**：
   如果执行 `dict.erase("run")`，这会删掉**所有**键为 `"run"` 的键值对。如果只想删掉其中某一个，必须先用 `find()` 找到对应的特定迭代器，然后删除迭代器。
3. **寻找重复键的范围**：
   你可以使用 `lower_bound`、`upper_bound` 或者更方便的 `equal_range` 来获取某个键对应的所有元素区间。

   ```cpp
   // 获取所有键为 "run" 的区间 [range.first, range.second)
   auto range = dict.equal_range("run");
   for (auto it = range.first; it != range.second; ++it) {
       std::cout << it->first << " -> " << it->second << std::endl;
   }
   ```

---

## 四 对比：`std::map` vs `std::unordered_map`

除了有序的 `std::map`，在竞赛和开发中也经常使用另一个相似的映射容器：**`std::unordered_map`（无序映射）**。

这两种映射容器的主要区别如下表所示：

| 对比维度                     | `std::map`                                   | `std::unordered_map`                               |
| :--------------------------- | :------------------------------------------- | :------------------------------------------------- |
| **底层实现**                 | **红黑树**（平衡二叉搜索树）                 | **哈希表**（散列表）                               |
| **元素顺序**                 | **自动有序**（按 Key 升序排列）              | **完全无序**（取决于哈希函数）                     |
| **查找/插入/删除时间复杂度** | **$O(\log n)$**（稳定且有保障）              | 平均 **$O(1)$**，最坏 **$O(n)$**（哈希冲突严重时） |
| **内存占用**                 | 适中（每个节点 3 个指针 + 1 位颜色）         | 较高（有哈希桶数组的额外开销）                     |
| **对 Key 的类型要求**        | 必须支持 **`<` 比较运算符**（能比较大小）    | 必须提供 **哈希函数** 且支持 **`==` 运算符**       |
| **典型应用场景**             | 需要区间查询、找前驱后继、或者要求输出有序时 | 仅需极速判断是否存在、或快速建立关联且不在乎顺序时 |

### 💡 竞赛使用建议：

1. 在 GESP、CSP-J/S 等竞赛中，如果仅用于**计数、查重或记录状态**且不需要对 Key 进行排序，可以优先考虑使用 `unordered_map`，其平均 $O(1)$ 的时间复杂度在大数据量下效率较高。
2. **注意哈希冲突**：在少数情况下，若输入数据被刻意设计以制造哈希冲突，`unordered_map` 的效率可能会退化到 $O(n)$。若对时间复杂度稳定性要求极高，使用 `map` 是更为稳妥的选择。

---

## 结语与下期预告

通过这两篇文章的学习，我们了解了 STL 中的关联容器—— `set` 系列与 `map` 系列，它们通过底层的红黑树结构提供了高效的有序操作。

到此为止，我们已经学习了以下容器：

- 序列容器：`vector`（动态数组）、`stack`（栈）、`queue`（队列）、`deque`（双端队列）
- 关联容器：`set`（集合）、`map`（映射）

在实际编写程序时，除了这些用于存放数据的容器，我们还可以配合 STL 提供的通用算法库—— **`<algorithm>`**。

下一篇文章，我们将介绍 `<algorithm>` 中的常用函数，如 `sort`，`reverse`，`unique` 等，帮助你更高效地处理容器中的数据。
