---
layout: post
title: 【GESP】C++七级考试大纲知识点梳理 (4) 哈希表：概念、实现与应用
date: 2026-01-22 07:40 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 哈希表]
categories: [GESP, 七级]
---

GESP C++七级考试大纲的第 4 条考点聚焦于**哈希表 (Hash Table)**。这是一种非常高效的数据结构，能够在理想情况下实现 $O(1)$ 的快速查找、插入和删除操作。在算法竞赛和实际开发中，哈希表是处理“查找”、“统计”和“判重”类问题的神兵利器。

> （4）掌握哈希表的概念与知识及其应用。
{: .prompt-info}

> 哈希表的核心思想可以概括为：**将复杂的“键”通过函数映射为一个简单的“索引”，从而直接定位数据**。这就像查字典时直接根据拼音翻到某一页，而不是一页页地翻书。
{: .prompt-tip}

> 本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

---

## 一、哈希表的基本概念

### 1.1 什么是哈希表？

哈希表（也叫散列表）是一种根据**键 (Key)** 直接访问在内存存储位置的数据结构。它通过一个**哈希函数 (Hash Function)**，将 Key 转换成一个数组的**下标 (Index)**，在这个下标对应的位置存储**值 (Value)**。

* **映射思想**：$Index = Hash(Key)$
* **例子**：我们要存 100 个学生的成绩。如果学号是 1, 2, 3...100，我们可以直接开一个数组 `score[101]`。但如果学号是 20240101, 20240999 这样很大的数字，直接开数组会爆内存。这时候就需要哈希函数，把大整数（或字符串）映射到一个较小的范围内。

### 1.2 哈希函数 (Hash Function)

哈希函数的作用是把任意长度的输入（Key）变换成固定长度的输出（Index）。

一个好的哈希函数应该：

1. **计算简单**：速度快。
2. **分布均匀**：让不同的 Key 尽量映射到不同的 Index，减少冲突。

**常见的哈希方法**：

* **除留余数法**：$Hash(x) = x \pmod P$。通常 $P$ 取一个质数，且离数组大小 $M$ 比较近。这是最常用的方法。

### 1.3 哈希冲突 (Hash Collision)

由于数组空间是有限的，而 Key 的取值范围可能是无穷的，难免会出现两个不同的 Key 经过哈希函数计算后，得到了相同的 Index。这就叫**哈希冲突**。

即：$Key_1 \neq Key_2$，但 $Hash(Key_1) = Hash(Key_2)$。

### 1.4 冲突解决方法

#### (1) 拉链法 (Chaining) —— **常用**

就像字典里的每一个条目下面挂了一串解释一样。我们在哈希表的每个位置维护一个**链表**（或者 `vector`）。如果不幸发生了冲突，就把新来的元素挂在这个位置的链表后面。

* **优点**：处理冲突简单，且不存在堆积现象。
* **缺点**：需要额外的指针空间。

#### (2) 开放寻址法 (Open Addressing)

如果计算出的位置 $H(x)$ 已经被占了，那就按照某种规则（比如往后看一个坑 $H(x)+1$）去找下一个空位。

* **线性探测**：位置被占了就找下一个，$index+1, index+2...$ 直到找到空位。容易产生“聚集”现象（Primary Clustering）。
* **二次探测 (Quadratic Probing)**：为了解决聚集现象，步长不再是1，而是 $1^2, -1^2, 2^2, -2^2...$ 跳着找。
* **双重哈希 (Double Hashing)**：使用第二个哈希函数来计算步长，即 $index + i \times Hash_2(key)$。这是最不容易产生聚集的方法。

---

## 二、STL 中的哈希表

在 C++11 标准中，STL 正式引入了基于哈希表实现的容器：`unordered_map` 和 `unordered_set`。它们的使用方式和 `map` / `set` 非常像，但底层实现和复杂度完全不同。

### 2.1 `unordered_map` 与 `map` 对比

| 特性 | `std::map` | `std::unordered_map` |
| :--- | :--- | :--- |
| **底层实现** | 红黑树 (Red-Black Tree) | 哈希表 (Hash Table) |
| **是否有序** | Key 自动排序 | **无序** (乱序) |
| **查找/插入/删除** | $O(\log N)$ | 平均 **$O(1)$**，最坏 $O(N)$ |
| **头文件** | `<map>` | `<unordered_map>` |

### 2.2 `unordered_set` 与 `set` 对比

| 特性 | `std::set` | `std::unordered_set` |
| :--- | :--- | :--- |
| **用途** | 去重 + 自动排序 | **仅去重** |
| **底层实现** | 红黑树 | 哈希表 |
| **复杂度** | $O(\log N)$ | 平均 **$O(1)$** |
| **头文件** | `<set>` | `<unordered_set>` |

**考试建议**：

> 1. 如果只需要**快速查找**或**统计频率**，且**不需要排序**，优先使用 `unordered_map` / `unordered_set`，因为 $O(1)$ 比 $O(\log N)$ 快得多。
> 2. 如果题目要求输出结果**按键值排序**，可以通过 `unordered_map` 统计完后，再拷贝到 `vector` 中排序，或者直接使用 `map`。
> 3. 注意：`unordered_map` 在最坏情况下（大量哈希冲突）会退化成 $O(N)$，容易被特殊数据卡超时（Codeforces Hack 常客），但在 GESP 考级中通常不需要担心这个问题，除非题目明确构造了针对性的数据。
{: .prompt-tip}

{% include custom/custom-post-content-inner.html %}

---

## 三、哈希表的应用场景与代码

### 3.1 统计字符/数字出现次数 (Frequency Counting)

**问题**：给定一个包含 $N$ 个整数的序列（数字范围很大，这就不能用普通数组计数了），求每个数字出现的次数。

```cpp
#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    // 定义一个哈希映射，Key是数字(int)，Value是次数(int)
    unordered_map<int, int> cnt;
    
    int n, x;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> x;
        cnt[x]++; // 极为方便！直接像数组一样操作，自动处理初始化
    }
    
    // 遍历输出
    // 注意：unordered_map 的遍历顺序是随机的
    for (auto p : cnt) {
        // p.first 是 Key (数字), p.second 是 Value (次数)
        cout << "数字 " << p.first << " 出现了 " << p.second << " 次" << endl;
    }
    
    return 0;
}
```

### 3.2 快速判重 (Deduplication)

**问题**：给定一串名字，判断某个名字之前是否出现过。

```cpp
#include <iostream>
#include <string>
#include <unordered_set>
using namespace std;

int main() {
    unordered_set<string> seen; // 只需要存Key，不需要Value
    
    int n;
    cin >> n;
    while (n--) {
        string name;
        cin >> name;
        
        // count(key) 返回 1 表示存在，0 表示不存在
        if (seen.count(name)) { 
            cout << name << " 已经出现过了！" << endl;
        } else {
            cout << name << " 第一次出现。" << endl;
            seen.insert(name); // 把它加入集合
        }
    }
    return 0;
}
```

### 3.3 两数之和 (Two Sum) —— 经典优化

**问题**：在一个数组中找到两个数，使得它们的和等于 Target。

**暴力解法**：两层循环枚举，$O(N^2)$。
**哈希解法**：遍历数组，对于每个数 `x`，检查 `Target - x` 是否在之前出现过。$O(N)$。

```cpp
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for(int i=0; i<n; i++) cin >> nums[i];

    unordered_map<int, int> mp; // Key: 数值, Value: 下标
    for (int i = 0; i < n; i++) {
        int complement = target - nums[i];
        
        // 查找 complement 是否在哈希表中
        if (mp.count(complement)) {
            // 找到了！输出两个数的下标
            cout << "Found: index " << mp[complement] << " and " << i << endl;
            return 0;
        }
        
        // 没找到，把当前数和下标存入哈希表
        mp[nums[i]] = i;
    }
    
    cout << "Not Found" << endl;
    return 0;
}
```

---

## 四、手动实现哈希表（考点补充）

虽然实战主要用 STL，但考级可能会考**拉链法**的原理。我们可以用简单的结构展示其内部逻辑。

```cpp
#include <iostream>
#include <vector>
using namespace std;

const int MOD = 100003; // 取一个大质数作为哈希表的长度

// 哈希表结构
vector<int> hashTable[MOD]; 

// 哈希函数
int get_hash(int key) {
    // 保证结果为正数
    return (key % MOD + MOD) % MOD; 
}

// 插入
void insert(int key) {
    int index = get_hash(key);
    hashTable[index].push_back(key); // 拉链法：挂在后面
}

// 查找
bool find(int key) {
    int index = get_hash(key);
    // 遍历对应的链表/vector
    for (int x : hashTable[index]) {
        if (x == key) return true;
    }
    return false;
}

int main() {
    insert(10);
    insert(100013); // 假设这两个数发生了冲突，拉链法会把它们存在同一个 bucket 里
    
    if (find(10)) cout << "Found 10" << endl;
    if (find(100013)) cout << "Found 100013" << endl;
    if (!find(20)) cout << "20 Not Found" << endl;
    
    return 0;
}
```

---

## 五、备考总结

1. **核心概念**：明白“映射”的思想，知道 $Index = Hash(Key)$。
2. **冲突处理**：理解什么是冲突，以及“拉链法”和“开放寻址法”的基本原理。
3. **STL 熟练度**：
    * 必须熟练掌握 `unordered_map` 和 `unordered_set` 的 `insert`, `count` (`find`), `erase` 操作。
    * `mp[key]` 的用法：如果 key 不存在，会自动创建一个默认值（例如 int 为 0），这一特性常用来计数 `mp[x]++`。
4.  **复杂度分析**：知道哈希表平均 $O(1)$，但最坏 $O(N)$。

---

{% include custom/custom-post-content-footer.md %}
