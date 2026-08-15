---
layout: post
title: 【CSP】CSP-J 2023 第一轮真题解析（三）：完善程序题
date: 2026-08-15 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [CSP, C++, 第一轮, 初赛, 完善程序]
categories: [CSP, J]
---

2023 年 CCF 非专业级软件能力认证（CSP-J/S 2023）第一轮认证于 2023 年 9 月 16 日举行。继前两篇单项选择题与阅读程序题解析后，本文为您带来 **第三部分：完善程序题（共 2 大题，10 小题，每小题 3 分，共计 30 分）** 的全题型深度解析。

完善程序题主要考查对 **二分查找（寻找有序等差数列缺失项与边界收敛）** 和 **动态规划（经典编辑距离 Levenshtein Distance 的状态定义与转移方程）** 的理解与代码填空能力。

<!--more-->

---

## 📌 三、完善程序（单选题，每小题 3 分，共计 30 分）

---

### 📍 第一题：寻找被移除的元素（二分查找）

#### 📖 题目描述

原有长度为 $n+1$、公差为 $1$ 的等差数列，将数列输入到程序的数组时移除了一个元素，导致长度为 $n$ 的连续数组可能不再连续，除非被移除的是第一个或最后一个元素。需要在数组不连续时，找出被移除的元素。试补全程序。

#### 💻 源码展示

```cpp
#include <iostream>
#include <vector>
using namespace std;

int find_missing(vector<int>& nums) {
    int left = 0, right = nums.size() - 1;
    while (left < right){
        int mid = left + (right - left) / 2;
        if (nums[mid] == mid + ①) {
            ②;
        } else {
            ③;
        }
    }
    return ④;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) cin >> nums[i];
    int missing_number = find_missing(nums);
    if (missing_number == ⑤) {
        cout << "Sequence is consecutive" << endl;
    } else {
        cout << "Missing number is " << missing_number << endl;
    }
    return 0;
}
```

---

#### 💡 算法核心原理解析

原数列是一个长度为 $n+1$、公差为 $1$ 的升序等差数列：
$$a_0, a_0 + 1, a_0 + 2, \dots, a_0 + n$$

从数列中移除一个元素后，输入数组 `nums` 长度为 $n$。

##### 1. 数列的性质与偏移特征

- **正常连续时**：对于任意下标 $i$（$0 \le i < n$），元素值应满足：
  $$\text{nums}[i] = \text{nums}[0] + i$$
- **中间缺失一个元素时**：设被移除的元素原先位于下标 $k$（$1 \le k \le n-1$）：
  - 当 $i < k$ 时（缺失位置之前）：$\text{nums}[i] = \text{nums}[0] + i$（未受影响，值与下标偏移一致）；
  - 当 $i \ge k$ 时（缺失位置之后）：$\text{nums}[i] = \text{nums}[0] + i + 1$（由于前面少了一个数，导致后面的每个数都比理论值大 $1$）。

##### 2. 二分查找定位缺失位置

利用上述单调性，我们可以通过二分查找快速锁定**第一个出现偏移的位置**（即第一个满足 $\text{nums}[i] \ne \text{nums}[0] + i$ 的下标）：

- 若 $\text{nums}[mid] == mid + \text{nums}[0]$：说明从下标 $0$ 到 $mid$ 的元素均连续无缺失，缺失的元素必然在 $mid$ 的右侧，因此调整左边界为 `left = mid + 1`；
- 若 $\text{nums}[mid] \ne mid + \text{nums}[0]$：说明缺失元素出现在 $mid$ 或 $mid$ 的左侧，此时 $mid$ 可能是第一个发生偏移的位置，不能排除，因此调整右边界为 `right = mid`；
- 当 `left == right` 时循环结束，`left` 即为第一个发生偏移的位置，原本应该处于该位置的数值就是被移除的元素：
  $$\text{missing} = \text{nums}[0] + left$$

##### 3. 判断是否连续（特殊边界处理）

若移除的是第一个元素（$a_0$）或最后一个元素（$a_0 + n$）：
- 剩下的 $n$ 个元素依然是连续的等差数列，即对所有 $0 \le i < n$，都有 $\text{nums}[i] == \text{nums}[0] + i$；
- 二分过程中条件 `nums[mid] == mid + nums[0]` 始终成立，`left` 会不断向右推进，最终 `left = right = n - 1`；
- 函数返回值为 $\text{nums}[0] + (n - 1) = \text{nums}[n - 1]$；
- 因此在 `main` 函数中，只要判断 `missing_number == nums[n - 1]`，即可断定原数组依然连续（Sequence is consecutive）！

---

#### ❓ 逐题精解

##### 1. ① 处应填（ ）

> A. `1`  
> B. `nums[0]`  
> C. `right`  
> D. `left`  
> **正确答案：** B

**深度解析：**  
在未发生缺失的区间内，第 $mid$ 个元素的值应该等于首项加上偏移量，即 $\text{nums}[mid] = \text{nums}[0] + mid = mid + \text{nums}[0]$。因此 ① 处必须填首元素 **`nums[0]`**。

---

##### 2. ② 处应填（ ）

> A. `left = mid + 1`  
> B. `right = mid - 1`  
> C. `right = mid`  
> D. `left = mid`  
> **正确答案：** A

**深度解析：**  
当 $\text{nums}[mid] == mid + \text{nums}[0]$ 成立时，表明区间 $[0, mid]$ 内没有缺失任何元素，缺失的数必定在 $mid$ 右边（下标 $> mid$）。因此下一轮搜索区间应缩减为 $[mid + 1, right]$，即更新 **`left = mid + 1`**。

---

##### 3. ③ 处应填（ ）

> A. `left = mid + 1`  
> B. `right = mid - 1`  
> C. `right = mid`  
> D. `left = mid`  
> **正确答案：** C

**深度解析：**  
当 $\text{nums}[mid] \ne mid + \text{nums}[0]$ 时，说明从 $mid$ 开始（或在 $mid$ 之前）已经出现了数据偏移。此时 $mid$ 本身很可能就是第一个发生偏移的位置，不能被排除在外。因此右边界应收缩到 $mid$，即更新 **`right = mid`**。

---

##### 4. ④ 处应填（ ）

> A. `left + nums[0]`  
> B. `right + nums[0]`  
> C. `mid + nums[0]`  
> D. `right + 1`  
> **正确答案：** A

**深度解析：**  
二分查找结束时满足 `left == right`，此时 `left` 就是第一个出现数值偏移的位置。原本应该放在该位置的数应为 **`nums[0] + left`**（即 `left + nums[0]`）。
注：由于循环结束时 `mid` 不在作用域内（`mid` 定义在 `while` 内部），选项 C 存在语法编译错误；选项 D 缺乏首项基准；因此唯有 A 选项符合逻辑与语法。

---

##### 5. ⑤ 处应填（ ）

> A. `nums[0] + n`  
> B. `nums[0] + n - 1`  
> C. `nums[0] + n + 1`  
> D. `nums[n - 1]`  
> **正确答案：** D

**深度解析：**  
若数组内部没有缺失（即移除的是首项或尾项，剩下的 $n$ 个数完全连续）：
二分查找中 `left` 会一直自增直到数组末尾 `n - 1`，最终 `find_missing` 返回的值为 $\text{nums}[0] + (n - 1)$，而对于连续数组，这个值恰好等于数组的最后一个元素 **`nums[n - 1]`**。
若数组内部有缺失，则返回的缺失值必然满足 $\text{nums}[0] < \text{missing\_number} < \text{nums}[n - 1]$，绝对不可能等于 `nums[n - 1]`。
因此，通过比较 `missing_number == nums[n - 1]` 即可精确区分数列是否连续。故选 D。

---

### 📍 第二题：编辑距离（动态规划）

#### 📖 题目描述

给定两个字符串，每次操作可以选择删除（Delete）、插入（Insert）、替换（Replace）一个字符，求将第一个字符串转换为第二个字符串所需要的最少操作次数。

#### 💻 源码展示

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int min(int x, int y, int z) {
    return min(min(x, y), z);
}

int edit_dist_dp(string str1, string str2) {
    int m = str1.length();
    int n = str2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0)
                dp[i][j] = ①;
            else if (j == 0)
                dp[i][j] = ②;
            else if (③)
                dp[i][j] = ④;
            else
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], ⑤);
        }
    }
    return dp[m][n];
}

int main() {
    string str1, str2;
    cin >> str1 >> str2;
    cout << "Mininum number of operation:" << edit_dist_dp(str1, str2) << endl;
    return 0;
}
```

---

#### 💡 算法核心原理解析

**编辑距离（Edit Distance，又称 Levenshtein 距离）** 是计算机科学中最经典的动态规划问题之一。

##### 1. 状态定义

设字符串 `str1` 的长度为 $m$，`str2` 的长度为 $n$。  
定义二维数组 `dp[i][j]` 表示：将 `str1` 的前 $i$ 个字符（`str1[0...i-1]`）转换为 `str2` 的前 $j$ 个字符（`str2[0...j-1]`）所需的 **最少操作次数**。

##### 2. 边界条件（Base Cases）

- **$i = 0$（`str1` 为空串）**：要将长度为 $0$ 的空串转换成长度为 $j$ 的 `str2` 前缀，唯一的办法就是执行 $j$ 次 **插入（Insert）** 操作。
  $$dp[0][j] = j$$
- **$j = 0$（`str2` 为空串）**：要将长度为 $i$ 的 `str1` 前缀转换成长度为 $0$ 的空串，唯一的办法就是执行 $i$ 次 **删除（Delete）** 操作。
  $$dp[i][0] = i$$

##### 3. 状态转移方程（State Transition）

当 $i > 0$ 且 $j > 0$ 时，考察 `str1` 的第 $i$ 个字符（`str1[i-1]`）与 `str2` 的第 $j$ 个字符（`str2[j-1]`）：

1. **若末尾字符相同（`str1[i-1] == str2[j-1]`）**：
   无需进行任何编辑操作，直接继承前面的匹配结果：
   $$dp[i][j] = dp[i-1][j-1]$$
2. **若末尾字符不同（`str1[i-1] != str2[j-1]`）**：
   必须通过一次操作使其匹配，取三种可能操作的最小值加 $1$：
   - **插入操作（Insert）**：在 `str1` 末尾插入 `str2[j-1]`，转换为求将 `str1[0...i-1]` 变成 `str2[0...j-2]` 的代价 $\implies dp[i][j-1] + 1$
   - **删除操作（Delete）**：将 `str1[i-1]` 删除，转换为求将 `str1[0...i-2]` 变成 `str2[0...j-1]` 的代价 $\implies dp[i-1][j] + 1$
   - **替换操作（Replace）**：将 `str1[i-1]` 替换为 `str2[j-1]`，转换为求将 `str1[0...i-2]` 变成 `str2[0...j-2]` 的代价 $\implies dp[i-1][j-1] + 1$

综合可得状态转移方程：
$$dp[i][j] = 1 + \min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])$$

---

#### ❓ 逐题精解

##### 1. ① 处应填（ ）

> A. `j`  
> B. `i`  
> C. `m`  
> D. `n`  
> **正确答案：** A

**深度解析：**  
当 $i = 0$ 时，`str1` 为空字符串。要将空字符串变换为长度为 $j$ 的 `str2` 前缀，必须连续插入 $j$ 个字符，因此操作次数为 $j$。故 ① 处应填 **`j`**。

---

##### 2. ② 处应填（ ）

> A. `j`  
> B. `i`  
> C. `m`  
> D. `n`  
> **正确答案：** B

**深度解析：**  
当 $j = 0$ 时，`str2` 为空字符串。要将长度为 $i$ 的 `str1` 前缀转换为空字符串，必须连续删除 $i$ 个字符，因此操作次数为 $i$。故 ② 处应填 **`i`**。

---

##### 3. ③ 处应填（ ）

> A. `str1[i-1] == str2[j-1]`  
> B. `str1[i] == str2[j]`  
> C. `str1[i-1] != str2[j-1]`  
> D. `str1[i] != str2[j]`  
> **正确答案：** A

**深度解析：**  
在 C++ 中，字符串下标基于 0 索引：
- 长度为 $i$ 的前缀的末尾字符是 `str1[i-1]`；
- 长度为 $j$ 的前缀的末尾字符是 `str2[j-1]`。
当两字符相等时，不需要任何额外编辑操作，直接沿用 `dp[i-1][j-1]`。因此条件应为 **`str1[i-1] == str2[j-1]`**。

---

##### 4. ④ 处应填（ ）

> A. `dp[i-1][j-1] + 1`  
> B. `dp[i-1][j-1]`  
> C. `dp[i-1][j]`  
> D. `dp[i][j-1]`  
> **正确答案：** B

**深度解析：**  
承接第 3 小题，当 `str1[i-1] == str2[j-1]` 时，当前字符已经匹配，所耗费的操作数为 $0$。此时的最少操作次数直接等于没有这两个字符时的状态，即 **`dp[i-1][j-1]`**。

---

##### 5. ⑤ 处应填（ ）

> A. `dp[i][j] + 1`  
> B. `dp[i-1][j-1] + 1`  
> C. `dp[i-1][j-1]`  
> D. `dp[i][j]`  
> **正确答案：** C

**深度解析：**  
当字符不匹配时，代码执行 `else` 分支：
`dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], ⑤);`
其中：
- `dp[i][j-1]` 对应 **插入操作**；
- `dp[i-1][j]` 对应 **删除操作**；
- 第三个参数必须对应 **替换操作** 的历史状态，即 **`dp[i-1][j-1]`**（外层已经统合加了 $1$，因此括号内无需再加 $1$）。故选 C。

---

## 💡 完善程序题核心提分策略与避坑指南

1. **识别经典算法模型**：
   - 寻找单调区间、缺失项 $\to$ **二分查找**；
   - 字符串转换、子序列、背包 $\to$ **动态规划**。
   - 看到熟悉的算法模板后，先在脑海中回忆标准代码结构，再对比题目中的变量命名。
2. **警惕 0 索引与 1 索引的转换**：
   - 在动态规划中，`dp` 数组大小通常开成 `(m+1) * (n+1)`，其中 `dp[i][j]` 代表前 $i$ 个和前 $j$ 个字符，其对应的字符串实际字符下标是 `str1[i-1]` 与 `str2[j-1]`，切莫混淆写成 `str1[i]`！
3. **推敲循环边界与不变量**：
   - 二分查找中，`while (left < right)` 配合 `left = mid + 1` 与 `right = mid` 是最典型的左闭右闭收敛写法，循环结束时必有 `left == right`。
4. **利用主函数验证与逆推**：
   - 例如第 1 大题的第 5 空 `if (missing_number == ⑤)`，如果直接推导有难度，可以通过模拟“连续序列”时 `find_missing` 函数的最终退出状态（`left` 必然走到 `n-1`），逆推出返回值为 `nums[n-1]`，从而秒杀答案！
