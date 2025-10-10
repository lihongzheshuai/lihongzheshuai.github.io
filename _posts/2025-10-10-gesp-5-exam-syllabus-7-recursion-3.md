---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (7) 递归算法 -3 优化策略
date: 2025-10-10 08:00 +0800
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
> * [【GESP】C++五级考试大纲知识点梳理, (7) 递归算法 - 1 基本原理](https://www.coderli.com/gesp-5-exam-syllabus-7-recursion-1/)
> * [【GESP】C++五级考试大纲知识点梳理, (7) 递归算法 - 2 复杂度分析](https://www.coderli.com/gesp-5-exam-syllabus-7-recursion-2/)
{: .prompt-tip}

<!--more-->

---

>在梳理的过程中，我发现想尽可能说清楚考纲要求的内容，越总结篇幅越长，为了避免总结遗漏和阅读匹配，我计算分三次介绍本部分内容，即：
>
> 1. 递归算法基本原理和常见形式
> 2. 递归算法时间、空间复杂度分析
> 3. 递归算法优化策略
>
> 本次为第三部分算法优化策略介绍。

---

## 一、为什么要优化递归？

递归是编程中非常优雅的一种思想：

> “让函数自己解决自己的一部分问题。”
> {: .prompt-info}

但它也有两个明显的缺点：

1. **效率可能很低** —— 很多递归会重复计算相同的结果；
2. **容易爆栈** —— 每次递归都会在内存中开辟一个新的函数调用栈。

因此，在实际编程中，我们常常需要 **优化递归算法**，让它既保留递归的简洁性，又能提高运行性能、节省内存空间。

---

## 二、递归优化的核心目标

优化递归，主要有两个方向：

1. **减少重复计算**（让算法更快）
2. **减少递归层数或栈开销**（让算法更稳）

---

## 三、主要优化策略

### （1）尾递归优化（Tail Recursion Optimization）

>**原理：**
>当一个递归函数在“最后一步”调用自身，并且不再需要返回上一层结果时，编译器可以将它优化成“循环”，从而避免新建函数栈帧。
> {: .prompt-info}

***典型例子：计算阶乘***

***普通递归：***

```cpp
int factorial(int n) {
    if (n == 1) {
        return 1;                       // 递归终止条件：1! = 1
    }
    // 递归返回后仍需乘以 n，编译器无法做尾递归优化
    return n * factorial(n - 1);
}
```

***尾递归形式：***

```cpp
int factorialTail(int n, int result = 1) {
    if (n == 1) {
        return result;                    // 递归终止：累积结果已计算完毕
    }
    // 尾递归：将当前累积结果 n*result 传给下一层，无需保留当前栈帧
    return factorialTail(n - 1, n * result);
}
```

有的编译器（如 Clang、GCC 开启优化选项）会自动将尾递归转换为循环形式，从而大大降低栈空间消耗。

👉 效果：

* 时间复杂度不变（仍是 $O(n)$）；
* 空间复杂度从 $O(n)$ → $O(1)$。

---

### （2）记忆化搜索（Memoization）

>**原理：**
>如果递归中存在 **重复子问题**，就把中间结果缓存下来。下次遇到相同的输入，直接取结果，而不是重新计算。
> {: .prompt-info}

***典型例子：斐波那契数列***

***普通递归（效率极低）***

```cpp
int fib(int n) {
    // 基准情形：前两项均为 1
    if (n <= 2) {
        return 1;
    }

    // 普通递归：无缓存，指数级重复计算
    return fib(n - 1) + fib(n - 2);  // 大量重复计算
}
```

***记忆化递归（效率高很多）***

```cpp
int fibMemo(int n, vector<int>& memo) {
    // 如果当前 n 的结果已经计算过，直接返回缓存值，避免重复计算
    if (memo[n] != -1) {
        return memo[n];
    }

    // 基准情形：前两项均为 1，并将结果存入缓存
    if (n <= 2) {
        return memo[n] = 1;
    }

    // 递归计算并缓存结果：先计算前两项，再求和并保存
    return memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
}

int fib(int n) {
    // 创建记忆化数组，初始值设为 -1 表示尚未计算
    vector<int> memo(n + 1, -1);
    // 调用带记忆化的递归函数，返回第 n 项斐波那契数
    return fibMemo(n, memo);
}
```

👉 **效果：**

* 时间复杂度从 $O(2^n)$ → $O(n)$
因为递归树从：

    ```plaintext
    fib(n)
    ├── fib(n-1)
    │   ├── fib(n-2)
    │   └── fib(n-3)
    └── fib(n-2)
        ├── fib(n-3)
        └── fib(n-4)
    ...
    ```

    变成：

    ```plaintext
    fib(n)
    └── fib(n-1)
        └── fib(n-2)
            └── fib(n-3)
            ...
    ```

* 空间复杂度略升（需要存储表），但换来极大提速（*经典的空间换时间思维*）。

---

### （3）递归改写为迭代

>**原理：**
>递归其实是“系统帮你管理栈”的过程。
>如果自己维护一个**显式栈**或使用循环，也能实现同样的逻辑。
> {: .prompt-info}

***典型例子：二叉树的前序遍历***（可先了解有该思想，由于考纲尚未学到树，对于具体问题和代码尽量理解，掌握多少均可）

递归版：

```cpp
void preorder(TreeNode* root) {
    if (!root) {
        return;                 // 空节点直接返回
    }
    cout << root->val << " ";     // 访问当前节点
    preorder(root->left);         // 递归遍历左子树
    preorder(root->right);        // 递归遍历右子树
}
```

改写为迭代：

```cpp
void preorderIter(TreeNode* root) {
    stack<TreeNode*> s;               // 手动维护显式栈
    if (root) {                       // 根节点非空才入栈
        s.push(root);
    }
    while (!s.empty()) {              // 栈不空则继续遍历
        TreeNode* node = s.top();     // 取出栈顶节点
        s.pop();
        cout << node->val << " ";     // 访问当前节点
        if (node->right) {            // 右子节点先入栈（后出）
            s.push(node->right);
        }
        if (node->left) {             // 左子节点后入栈（先出）
            s.push(node->left);
        }
    }
}
```

👉 **效果：**

* 避免函数调用栈溢出；
* 控制更灵活；
* 性能稳定。

---

### （4）分治 + 剪枝优化（Pruning）

>**原理：**
>在递归搜索中，提前排除“不可能的情况”，减少不必要的递归分支。
> {: .prompt-info}

***典型例子：八皇后问题***（可先了解有该思想，对于具体问题和代码尽量理解，掌握多少均可）

***八皇后问题描述：***  
在 N×N 的棋盘上放置 N 个皇后，使得任意两个皇后都不能互相攻击。  
攻击规则：同一行、同一列或同一对角线上只能有一个皇后。  
目标：求出所有满足条件的放置方案总数。

普通递归会枚举所有可能位置，

```cpp
bool valid(int row, int col) {
    // 检查与前面已放置的皇后是否冲突（逐个比较）
    for (int r = 0; r < row; ++r) {
        int c = pos[r];
        if (c == col) return false;                // 同列
        if (abs(c - col) == abs(r - row)) return false; // 同对角线
    }
    return true;
}

void dfs(int row) {
    if (row == n) {
        cnt++; // 找到一种方案
        return;
    }
    for (int col = 0; col < n; col++) {
        // 尝试在第 row 行的每一列放置皇后
        if (valid(row, col)) {
            place(row, col);   // 放置皇后
            dfs(row + 1);      // 递归处理下一行
            remove(row, col);  // 回溯：撤销当前放置
        }
    }
}
```

而剪枝优化可以提前判断冲突：

```cpp
vector<bool> colUsed;     // 列标记
vector<bool> diag1;       // 主对角（row+col）
vector<bool> diag2;       // 副对角（row-col + (N-1)）
void dfs(int row) {
    if (row == n) {
        cnt++;          // 找到一种合法方案，计数加一
        return;         // 结束当前递归分支
    }
    for (int col = 0; col < n; col++) {
        if (colUsed[col] || diag1[row + col] || diag2[row - col + n]) {
            continue;   // 当前列或两条对角线已被占用，跳过
        }
        // 放置皇后
        colUsed[col] = diag1[row + col] = diag2[row - col + n] = true;
        dfs(row + 1);   // 递归处理下一行
        // 回溯：撤销当前选择，恢复状态
        colUsed[col] = diag1[row + col] = diag2[row - col + n] = false;
    }
}
```

👉 **效果：**

* 优化前：分支因子在前几层接近 N，总体节点数近 N! （暴力或大量排列），且常有很多重复或无效分支。
时间复杂度近似阶乘级 $O(N!)$。
* 优化后：分支因子大大减少，总体节点数远小于 N!，且没有无效分支。
时间复杂度虽仍近指数级，但相比阶乘级有明显提升。

---

### （5）递归深度限制与混合策略

有时递归深度太大（如上万层）会导致**栈溢出**。
常见优化做法：

* 限制最大深度，超出时转为迭代；
* 或者采用“分块递归 + 局部循环”混合方式。

***例如：快速排序的混合优化策略***

***经典递归版：***

```cpp
void quicksort(vector<int>& a, int l, int r) {
    if (l >= r) {
        return;                     // 区间无效或只剩一个元素，无需排序
    }
    int i = l, j = r;
    int pivot = a[(l + r) / 2];      // 选取中间元素作为基准值
    while (i <= j) {
        while (a[i] < pivot) {      // 从左向右找第一个 ≥ pivot 的元素
            i++;
        }
        while (a[j] > pivot) {      // 从右向左找第一个 ≤ pivot 的元素
            j--;
        }
        if (i <= j) {                 // 找到一对需要交换的元素
            swap(a[i++], a[j--]);   // 交换并收缩边界
        }
    }
    quicksort(a, l, j);              // 递归处理左半部分
    quicksort(a, i, r);              // 递归处理右半部分
}
```

***优化版：混合递归 + 循环 + 深度控制***

```cpp
const int MAX_DEPTH = 1000;

void quicksort_optimized(vector<int>& a, int l, int r, int depth = 0) {
    while (l < r) {
        if (depth > MAX_DEPTH) {  // 超出深度 → 转迭代或堆排序
            sort(a.begin() + l, a.begin() + r + 1);
            return;
        }
        int i = l, j = r, pivot = a[(l + r) / 2];
        while (i <= j) {
            while (a[i] < pivot) {
                i++;  // 从左找第一个 ≥ pivot 的位置
            }
            while (a[j] > pivot) {
                j--;  // 从右找第一个 ≤ pivot 的位置
            }
            if (i <= j) {
                swap(a[i++], a[j--]);  // 交换并收缩边界
            }
        }
        // 递归小区间，循环大区间 —— 减少递归深度
        if (j - l < r - i) {
            quicksort_optimized(a, l, j, depth + 1);  // 先递归处理较小段
            l = i;  // 剩余较大段用循环继续处理
        } else {
            quicksort_optimized(a, i, r, depth + 1);  // 先递归处理较小段
            r = j;  // 剩余较大段用循环继续处理
        }
    }
}
```

**优化点说明**：

1. 使用 `while` 替代部分递归；
2. 控制最大递归深度（`MAX_DEPTH`）；
3. 优先递归较小区间，循环处理较大区间，避免最坏深度 $O(n)$
4. 超过深度时切换到安全的`sort()`。

---

## 四、优化策略对比总结

| 优化策略  | 主要思想     | 优点      | 适用场景        |
| ----- | -------- | ------- | ----------- |
| 尾递归优化 | 减少调用栈层数  | 节省空间    | 线性递归（阶乘、求和） |
| 记忆化搜索 | 缓存中间结果   | 提升速度    | 动态规划类问题     |
| 递归转迭代 | 自建栈代替系统栈 | 防止爆栈    | 深度搜索、树遍历    |
| 剪枝优化  | 提前过滤无效分支 | 大幅减少搜索量 | DFS、回溯类问题   |
| 深度限制  | 控制递归层数   | 保证稳定性   | 超大规模数据递归    |

---

## 五、结语

递归优化并不是让递归“看起来更酷”，其核心目的是为了让它：

* **不重复做事（效率高）**
* **不占太多空间（更稳）**

---
{% include custom/custom-post-content-footer.md %}
