---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (7) 递归算法
date: 2025-09-29 08:00 +0800
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
{: .prompt-tip}

<!--more-->

---

在计算机科学中，递归算法常被称作“解决问题的艺术”。它的核心思想是：**用同类问题的更小规模去解释和解决原问题**。换句话说，递归就是“自己调用自己”，直到问题被分解到足够简单为止。

## 一、递归的基本原理

**定义**：递归是指函数直接或间接调用自身。

递归解法由两部分组成：

* **基准情形（base case）**：能直接返回结果、不再递归的情形（必须有）。
* **递归情形（recursive case）**：将原问题分解为规模更小的子问题并递归求解，然后把子问题结果组合成原问题的结果。

**工作机制（调用栈）**：每次调用都会在栈上分配一帧（局部变量、返回地址等）。直观理解：递归等同于重复压栈、展开计算、再逐层返回并合并结果。

**示例：** 求阶乘

```cpp
long long fact(int n) {
    if (n <= 1) {
        return 1; // 基准情形，即当n<=1时，直接返回1
    }
    return n * fact(n-1); // 递归情形
}
```

**调用 `fact(4)` 的执行顺序**：

* `fact(4)` 调用 `fact(3)`。
* `fact(3)` 调用 `fact(2)`。
* `fact(2)` 调用 `fact(1)`。
* `fact(1)` 直接返回 `1`。
* `fact(2)` 返回 `2 * 1 = 2`。
* `fact(3)` 返回 `3 * 2 = 6`。
* `fact(4)` 返回 `4 * 6 = 24`。

---

## 二、常见递归模式

>本部分涉及5种常见递归模式，前3种相对比较容易理解，后2种相对比较复杂。咱不理解执行过程我认为也不必太过纠结，可通过后续的编程练习我们一起逐步理解、加深。
{: .prompt-tip}

### 2.1 线性递归（Linear Recursion）

**线性递归（Linear recursion）**：每次只递归一个子问题（如：链表长度、阶乘、递归求和）。

**例题：** 求 n 的阶乘

数学定义：
$$
n! = \begin{cases}
1, & n=0 \text{ 或 } n=1\\
n \times (n-1)!, & n>1
\end{cases}
$$

**代码示例：**

```cpp
long long factorial(int n) {
    if (n <= 1) {
        return 1; // 基准情形，即当n<=1时，直接返回1
    }
    return n * factorial(n - 1); // 递归情形
}
```

**调用过程：**

```cpp
factorial(4)
= 4 * factorial(3)
= 4 * (3 * factorial(2))
= 4 * (3 * (2 * factorial(1)))
= 4 * 3 * 2 * 1
```

特点：递归链条像一条直线，逐层压栈，再逐层返回。

---

### 2.2 树形递归（Tree Recursion）

**二叉/树形递归（Tree recursion）**：每次递归产生多个子调用（如：斐波那契朴素实现、二叉树遍历）。

**例题：** 斐波那契数列

数学定义：
$$
F(n) = \begin{cases}
0, & n=0 \\
1, & n=1 \\
F(n-1) + F(n-2), & n>1
\end{cases}
$$

**代码示例：**

```cpp
int fibonacci(int n) {
    if (n <= 1) {
        return n; // 基准情形，即当n<=1时，直接返回n
    }
    return fibonacci(n-1) + fibonacci(n-2); // 两个递归分支
}
```

**调用过程（树状展开）：**

```cpp
fibonacci(4)
= fibonacci(3) + fibonacci(2)

fibonacci(3) = fibonacci(2) + fibonacci(1)
fibonacci(2) = fibonacci(1) + fibonacci(0)
```

最终形成一棵二叉树，节点数量随 n 指数增长。

特点：同一个子问题会被多次计算（如 fibonacci(2) 重复出现）。

---

### 2.3 分治（Divide & Conquer）

**分治（Divide & Conquer）**：把问题分为若干独立子问题，子问题规模通常是 `n/2` 等（如：归并排序、快速排序、二分搜索）。

**例题：** 二分查找，在有序数组中查找目标值。

**代码示例：**

```cpp
// 二分查找递归实现：在有序数组 arr 的 [left, right] 区间内查找 target
int binarySearch(vector<int>& arr, int left, int right, int target) {
    // 递归终止条件：区间为空，查找失败
    if (left > right) {
        return -1;  // 查找失败，未找到目标值
    }
    int mid = (left + right) / 2; // 计算中间位置
    if (arr[mid] == target) {
        return mid;     // 找到目标值，返回下标
    } else if (arr[mid] > target) { // 目标值在左半区间
        return binarySearch(arr, left, mid - 1, target);
    } else {                       // 目标值在右半区间
        return binarySearch(arr, mid + 1, right, target);
    }
}
```

**调用过程：** 例如：binarySearch([1,3,5,7,9], target=7)

```cpp
查 [1..9], mid=5 → target > 5 → 去右半边
查 [7..9], mid=7 → 找到
```

特点：每次递归只进入一个分支，问题规模减半。

---

### 2.4 回溯（Backtracking / DFS）

**回溯（Backtracking / DFS）**：在解空间树上做深度优先搜索并回退（如：全排列、子集、N 皇后）。

**例题：全排列** 给定数组，输出所有排列。

**基本算法逻辑**  

1. 固定第 1 位，依次与后面每个元素交换，得到新首元素；  
2. 对剩余部分递归执行“固定+交换”，直到只剩 1 个元素，即得到一个完整排列；  
3. 回溯：撤销刚才的交换，恢复数组原状，继续尝试下一个候选。  

如此深度优先地“选-递归-回退”，即可不重不漏地生成全部 n! 种排列。

**代码：**

```cpp
// 回溯法生成全排列
void backtrack(vector<int>& nums, int start, vector<vector<int>>& result) {
    // 如果已经到达数组末尾，说明生成了一个完整排列
    if (start == nums.size()) {         
        result.push_back(nums); // 保存当前排列
        return;
    }
    // 枚举当前位置可以选择的所有数字
    for (int i = start; i < nums.size(); ++i) {
        swap(nums[start], nums[i]);     // 选择：将第 i 个数字放到当前位置
        backtrack(nums, start + 1, result); // 递归：处理下一个位置
        swap(nums[start], nums[i]);     // 撤销选择（回溯）：恢复原状
    }
}
```

**调用过程：**

```cpp
第一层：选择 1 → 递归排列 [2,3]
    第二层：选择 2 → 递归排列 [3]
        第三层：选择 3 → 得到 [1,2,3]
        回溯 → 撤销 3
    第二层：选择 3 → 递归排列 [2]
        第三层：选择 2 → 得到 [1,3,2]
        回溯 → 撤销 2
    回溯 → 撤销 1
...
```

* 特点：典型“试探—回溯”过程，像深度优先搜索。

---

### 2.5 尾递归（Tail Recursion）

**尾递归（Tail recursion）**：递归调用是函数最后一步（有利于编译器优化为循环，但 C++ 不保证 尾调用优化（TCO））。

**例题：** 阶乘（尾递归写法）与线性递归不同，这里递归调用在函数末尾。

**代码：**

```cpp
long long factorialTail(int n, long long acc = 1) {
    // 基准情形：当 n ≤ 1 时，累积结果 acc 即为阶乘值，直接返回
    if (n <= 1) {
        return acc;  // 基准情形
    }
    // 尾递归：将当前累积值 acc * n 作为参数传入下一次调用
    // 问题规模缩小为 n-1，保持调用栈深度不变（可优化为循环）
    return factorialTail(n - 1, acc * n); // 尾递归
}
```

>注：C++ 标准并不保证尾递归优化（TCO），但尾递归写法可轻松转化为迭代。
{: .prompt-tip}

**调用过程：**

```cpp
factorialTail(4, 1)
→ factorialTail(3, 4)
→ factorialTail(2, 12)
→ factorialTail(1, 24)
返回 24
```

特点：递归调用在函数最后一步，状态通过参数传递，没有额外计算，容易转为迭代。

---

### 2.6 小结

* 线性递归 → 一条直链，逐层返回。
* 树形递归 → 每层分支，形成递归树。
* 分治 → 每次只走一个分支，问题规模缩小。
* 回溯 → 深度探索，遇到尽头再回退。
* 尾递归 → 类似循环，参数不断更新。

---

## 三、 递归时间复杂度分析

分析的核心思路：**识别子问题个数（分支因子 b）与每层工作量，结合深度 d**，或建立并解递推式（recurrence）。

### 3.1 常用递归式与结论（常考）

以下给出 C++ 递归中最常出现的 4 条递推式，帮助理解“为什么是这个复杂度”。

| 递推式 | 展开思路 | 结论 |
|--------|----------|------|
| $T(n) = T(n-1) + O(1)$ | 每次问题规模减 1，共 $n$ 层，每层常数工作量 | $T(n)=O(n)$ |
| $T(n) = T(n/2) + O(1)$ | 规模每轮减半，深度 $\log_2 n$，每层常数 | $T(n)=O(\log n)$ |
| $T(n) = 2T(n/2) + O(n)$ | 每层总工作量 $O(n)$，共 $\log_2 n$ 层 | $T(n)=O(n\log n)$ |
| $T(n)=aT(n/b)+f(n)$ | 主定理（Master Theorem）直接判阶 | 见下方例题 |

#### 3.1.1 递归主定理介绍（需要一定数学基础，有兴趣的可以了解）

在递归算法中，时间复杂度往往通过一个**递推式**来描述，比如：

$$
T(n) = aT\left(\frac{n}{b}\right) + f(n)
$$

这里每一项的意义：

* $a$：把问题拆成的子问题个数。
* $n/b$：每个子问题的规模（假设均等划分）。
* $f(n)$：分解问题和合并子问题的代价。

例如：

* **归并排序**：$T(n) = 2T(n/2) + O(n)$
* **二分查找**：$T(n) = T(n/2) + O(1)$

---

主定理告诉我们，复杂度主要取决于**子问题工作量** $aT(n/b)$ 和 **分解/合并开销** $f(n)$ 谁更“占主导”。

设(仅考虑子问题递归展开时的总工作量的为)：
$$
c_{\text{crit}} = n^{\log_b a} \quad \text{（也叫临界函数）}
$$

它表示仅递归部分消耗的复杂度。那么问题来了

##### 1.它从哪里来？

递推式一般是：
$$
T(n) = aT\left(\frac{n}{b}\right) + f(n)
$$

* 把规模为 $n$ 的问题拆成 $a$ 个子问题；
* 每个子问题的规模是 $n/b$。

如果忽略掉分解/合并的额外代价 $f(n)$，只考虑递归部分：
$$
T(n) \approx aT\left(\frac{n}{b}\right)
$$

这是一个“纯递归树”。递归树深度大约是 $\log_b n$（每次规模缩小 $1/b$，直到变成常数规模）。在每一层，子问题个数大约是 $a^k$，每个子问题的规模大约是 $n/b^k$。

---

##### 2. 子问题总量的计算

每一层的 **问题规模 × 数量** 大约是：
$$
\left(\frac{n}{b^k}\right) \times a^k = n \cdot \left(\frac{a}{b}\right)^k
$$

递归树一共有 $\log_b n$ 层。整体规模叠加起来，主导项就对应于：
$$
n^{\log_b a}
$$

---

##### 3. 怎么理解

* $a$：递归分支的“宽度”。
* $b$：规模缩小的“速度”。
* $\log_b a$：表示递归树“展开后有多少工作量”，是递归的 **增长指数**。
* $n^{\log_b a}$：就是递归部分整体的复杂度，主定理把它当作一个基准，和 $f(n)$ 比大小。

---

##### 4. 怎么运用主定理

你可以把它类比成一个“基准工作量”：

* 如果 $f(n)$ 比它小 → **递归部分更重**；
* 如果 $f(n)$ 与它同阶 → **两者势均力敌，需再乘 $\log n$；
* 如果 $f(n)$ 比它大 → **分解/合并部分更重**。

---

#### 3.1.2 主定理的三种情况

##### 情况 1：$f(n)$ 比 $n^{\log_b a}$ 小

如果
$$
f(n) = O\big(n^{\log_b a - \epsilon}\big) \quad (\epsilon > 0)
$$
也就是说，分解/合并的开销比递归本身还小。

**结论**：
$$
T(n) = \Theta\big(n^{\log_b a}\big)
$$

✅ 例如：二分查找

* $T(n) = T(n/2) + O(1)$
* 这里 $a = 1, b = 2, \log_b a = 0$，所以 $n^{\log_b a} = n^0 = 1$
* $f(n) = O(1)$
* 套用情况 1，结果 $T(n) = \Theta(\log n)$。

---

##### 情况 2：$f(n)$ 大小“刚好相等”

如果
$$
f(n) = \Theta\big(n^{\log_b a}\big)
$$

**结论**：
$$
T(n) = \Theta\big(n^{\log_b a} \cdot \log n\big)
$$

✅ 例如：归并排序

* $T(n) = 2T(n/2) + O(n)$
* $a=2, b=2, \log_b a = 1$，所以 $n^{\log_b a} = n$
* $f(n) = \Theta(n)$
* 套用情况 2，结果 $T(n) = \Theta(n \log n)$。

---

##### 情况 3：$f(n)$ 更大

如果
$$
f(n) = \Omega\big(n^{\log_b a + \epsilon}\big) \quad (\epsilon > 0)
$$
并且满足“正则性条件”：
$$
a f\left(\frac{n}{b}\right) \leq c f(n) \quad (c < 1)
$$

>这句话的简单理解是：**子问题分解后的总工作量，在渐近意义下不能超过原问题工作量的一定比例。**
>
>* 如果 $f(n)$ 已经非常大（比 $n^{\log_b a}$ 高一个指数），那么递归部分的贡献必须在每层都“快速衰减”，最终不会影响整体复杂度。
>* 这样我们才能放心地说：复杂度就是 $\Theta(f(n))$。
>
>似乎越来越复杂。。这里就不再展开了。
{: .prompt-tip}

---

**结论**：
$$
T(n) = \Theta(f(n))
$$

✅ 例如：线性遍历加递归

* $T(n) = 2T(n/2) + O(n^2)$
* $a=2, b=2, \log_b a = 1$，所以 $n^{\log_b a} = n$
* $f(n) = \Theta(n^2)$（更大）
* 满足正则性条件 → $T(n) = \Theta(n^2)$。

---

##### 直观理解

你可以这样简单理解：

* $n^{\log_b a}$：递归树里“子问题消耗的总量”。
* $f(n)$：每一层分解/合并的代价。
* 比较两者的增长速度，谁大谁主导。

**例题**  
$T(n)=3T(n/3)+n$  
$a=3,\;b=3\Rightarrow c_{\text{crit}}=\log_3 3=1$，而 $f(n)=n=\Theta(n^1)$，恰为情况 2（$k=0$），  
故 $T(n)=\Theta(n\log n)$。

---

## 四、递归空间复杂度分析


1. **递归栈**  
   深度 $D$ × 单帧常数大小 $\Rightarrow O(D)$。  
   例如：  
   - 线性递归 $D=n\Rightarrow O(n)$  
   - 二分递归 $D=\log n\Rightarrow O(\log n)$

2. **额外存储**  
   memo 数组、归并排序辅助数组等需单独累加。  
   总空间 = 递归栈空间 + 额外数据结构空间。

---

# 4. 递归优化策略（考试重点）

1. **记忆化搜索 / 备忘录（Memoization）**
   把重复子问题的结果缓存，避免重复计算（自顶向下的动态规划）。
   示例：将斐波那契优化为 `O(n)`：

   ```cpp
   int fib_memo(int n, vector<int>& mem) {
       if (n <= 1) return n;
       if (mem[n] != -1) return mem[n];
       return mem[n] = fib_memo(n-1, mem) + fib_memo(n-2, mem);
   }
   // 调用： vector<int> mem(n+1, -1); fib_memo(n, mem);
   ```

   时间 `O(n)`，空间 `O(n)`（含递归栈）。

2. **自底向上动态规划（DP）**
   把递归改写为迭代，通常能节省栈空间与调用开销（如 Fibonacci 的迭代解法）。

   ```cpp
   int fib_iter(int n) {
       if (n <= 1) return n;
       int a = 0, b = 1;
       for (int i = 2; i <= n; ++i) {
           int c = a + b;
           a = b; b = c;
       }
       return b;
   }
   ```

3. **尾递归（Tail recursion）与 TCO（Tail Call Optimization）**
   将递归写成尾递归形式，某些编译器可优化为循环；但**不能依赖 C++ 标准保证 TCO**，面试/考试中要说明此点。实务上更稳妥的做法是直接改为迭代。

4. **剪枝（Pruning）与分支限界（Branch-and-bound）**
   回溯时提前判断某些分支不可能产生更优解并剪掉（常用于 N 皇后、子集和、TSP 的分支限界）。

5. **转为显式栈（iterative with stack）**
   在递归深度可能超限时，用手动栈模拟递归，避免系统栈溢出并可更好控制内存。

6. **减少每帧开销**
   把不必在每帧创建的大对象提到外层，减少栈空间消耗与复制开销。

---

# 5. 考试中如何展示你的解题、分析能力（答题技巧）

1. **先写伪代码/递推式**，明确基准情形与递归情形。
2. **写出递推式并解它**（或用树形估计节点数），给出时间复杂度（大 O）与空间复杂度（包括栈）。
3. **指出是否有重叠子问题**（若有，提示用 memo 或 DP）。
4. **给出优化思路**（如改为迭代 / 加 memo / 剪枝），并说明优化后复杂度变化。
5. **注意边界与实现细节**（基准条件、输入为 0 或负数的处理、栈深度风险）。

示例评分要点（阅卷者会看）：

* 基本正确的递归实现（必须有 base case）。
* 正确写出递推式并合理求解复杂度。
* 能指出并给出一种或多种优化方法并说明效果。

---

# 6. 常见易错点与注意事项

* **忘写 base case → 无限递归/栈溢出**。
* **重复计算**（如朴素斐波那契）：必须识别并建议 memo。
* **忽视递归栈空间**：分析中要把栈空间算进去。
* **误信所有编译器都做尾递归优化**（不可假设）。
* **回溯复杂度常常被低估**，输出规模或解空间大小会影响时间。

---

# 7. 练习题（含提示与答案要点）

1. 写出 `fact(n)` 的时间与空间复杂度（非尾递归）。

   * 时间：`O(n)`；空间（栈深）：`O(n)`。

2. 朴素 `fib(n)` 的时间复杂度？如何优化到 `O(n)`？

   * 朴素：指数 `O(φ^n)`；优化：记忆化或自底向上 DP → `O(n)`。

3. 归并排序复杂度（时间/空间）？递推式是什么？

   * `T(n)=2T(n/2)+O(n)` → `O(n log n)`；额外空间 `O(n)`（合并数组），栈深 `O(log n)`。

4. 全排列（生成 n 个数的排列）的时间复杂度？如何在生成过程中节省不必要分支？

   * 时间 `O(n!)`（输出量级）。可通过剪枝（如重复元素去重）或界定搜索深度减少分支。

5. 给出 `T(n)=3T(n/3) + n` 的解（主定理）。

   * `n^{log_3 3} = n`，所以 `T(n)=Θ(n log n)`。

---

递归的重要性主要体现在以下几个方面：

1. **自然表达复杂问题**：许多问题本身具有递归结构，比如树的遍历、分治算法、图的深度优先搜索，用递归能直接贴合问题的逻辑。
2. **简化代码逻辑**：相较于繁琐的循环和状态管理，递归代码往往更简洁，更接近数学定义。
3. **联系动态规划与分治的桥梁**：递归是动态规划的基础思想（自顶向下+记忆化），也是分治策略的自然表达形式。
4. **算法学习的必经之路**：递归不仅是考纲重点，也是理解算法思想、掌握问题分解与建模能力的重要工具。

因此，掌握递归不仅是为了应对考试题目，更是深入理解算法与程序设计思维的必修课。

---
{% include custom/custom-post-content-footer.md %}
