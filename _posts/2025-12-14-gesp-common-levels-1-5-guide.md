---
layout: post
title: GESP 1-5级编程题核心考点与备考攻略及真题分类
date: 2025-12-14 10:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++]
categories: [GESP, 经验交流]
---

根据过往真题（截至2025年9月）的整理与分析，我们总结了GESP 1级到5级编程题的核心考点、常见题型及备考建议。同时，我们将历年真题进行了详细分类，帮助各位考生更有针对性地进行复习。

## GESP 一级：语法基础与简单逻辑

一级考试主要考察考生对C++基本语法的掌握程度，题目通常逻辑简单，直来直去。

### 核心考点与典型题型

1. **基础输入输出**：熟练使用 `cin`/`cout` 或 `scanf`/`printf`。
2. **基本数据类型与运算**：整型(`int`)、浮点型(`double`/`float`)、字符型(`char`)的定义与四则运算，特别是取模运算 `%` 的应用。
    * *典型题型*：公式计算类（如长方形面积、温度转换）。
3. **基础流程控制**：
    * **分支结构**：`if-else` 的使用，简单的逻辑判断（如奇偶判断、大小比较）。
    * *典型题型*：简单逻辑判断（如奇数和偶数、小明的幸运数）。
    * **循环结构**：基础的 `for` 或 `while` 循环，通常用于简单的累加、计数。
    * *典型题型*：简单循环（如累计相加、找因数）。

### 备考建议

* **严抓语法**：确保分号、括号匹配、变量声明等基础语法不出错。
* **数据范围**：注意题目中变量的范围，养成使用 `long long` 的意识。

### 精选真题分类练习

#### 1. 运算与公式计算

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **长方形面积** | 基础乘法、变量定义 | [点击练习](https://www.coderli.com/gesp-1-luogu-b3834/) |
| **温度转换** | 浮点数运算、公式转换 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4062/) |
| **立方数** | 简单的幂运算 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4001/) |
| **休息时间** | 时间单位换算（时分秒） | [点击练习](https://www.coderli.com/gesp-1-luogu-b4000/) |
| **商店折扣** | 简单的百分比/折扣计算 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4409/) |
| **四舍五入** | 浮点转整型的技巧 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4258/) |

#### 2. 分支逻辑（条件判断）

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **奇数和偶数** | 奇偶性判断 (`%2`) | [点击练习](https://www.coderli.com/gesp-1-luogu-b4063/) |
| **每月天数** | 多分支判断（闰年判断） | [点击练习](https://www.coderli.com/gesp-1-luogu-b3835/) |
| **小明的幸运数** | 整除判断 (`%n == 0`) | [点击练习](https://www.coderli.com/gesp-1-luogu-b3864/) |
| **小杨的考试** | 阈值判断、逻辑与或 | [点击练习](https://www.coderli.com/gesp-1-luogu-b3921/) |
| **小杨购物** | 条件分支 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4034/) |
| **图书馆里的老鼠** | 简单的坐标或逻辑判断 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4257/) |

#### 3. 基础循环（迭代）

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **累计相加** | 1到N求和 | [点击练习](https://www.coderli.com/gesp-1-luogu-b3839/) |
| **找因数** | 遍历 1到N 判断整除 | [点击练习](https://www.coderli.com/gesp-1-luogu-b3953/) |
| **小杨报数** | 跳过特定条件的数 (continue) | [点击练习](https://www.coderli.com/gesp-1-luogu-b3922/) |
| **小杨买书** | 简单的循环或逻辑 | [点击练习](https://www.coderli.com/gesp-1-luogu-b3952/) |
| **美丽数字** | 循环判断数位特征 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4035/) |
| **值日** | 寻找公倍数（简单循环实现） | [点击练习](https://www.coderli.com/gesp-1-luogu-b4355/) |
| **金字塔** | 平方和累加循环 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4410/) |
| **假期阅读** | 循环模拟阅读进度 | [点击练习](https://www.coderli.com/gesp-1-luogu-b4354/) |

---

## GESP 二级：多重循环与数位处理

二级难度有显著提升，重点考察逻辑思维能力，特别是处理嵌套结构和数字特性的能力。

### 核心考点与典型题型

1. **多重循环（嵌套循环）**：这是二级最大的门槛。
    * *典型题型*：图形打印类（如画三角形、X字矩阵），需要找准行号(i)与列号(j)之间的数学关系。
2. **数位处理**：利用 `% 10` 和 `/ 10` 提取数字的每一位。
    * *典型题型*：数位拆分类（如水仙花数、数位之和、数字黑洞）。
3. **简单数学函数与枚举**：平方、开方、暴力循环。
    * *典型题型*：简单数论（找素数）、应用题（百鸡问题）。

### 备考建议

* **画图找规律**：对于矩阵和图形打印题，在纸上画出坐标系，寻找 `i` 和 `j` 的关系。
* **熟练拆数**：闭着眼睛也要能写出 `while(n){ d = n%10; n/=10; }` 的模板。

### 精选真题分类练习

#### 1. 数位处理（拆数）

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **自幂数判断** | 水仙花数类题目，数位幂次和 | [点击练习](https://www.coderli.com/gesp-2-luogu-b3841/) |
| **数位之和** | 计算各位数字相加 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4036/) |
| **数字黑洞** | 数位重组、循环模拟 | [点击练习](https://www.coderli.com/gesp-2-luogu-b3866/) |
| **数位和** | 简单的数位统计 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4065/) |
| **寻找数字** | 特定数位特征的搜索 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4064/) |

#### 2. 图形打印（矩阵逻辑）

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **画三角形** | 字符构成的三角形 | [点击练习](https://www.coderli.com/gesp-2-luogu-b3837/) |
| **小杨的 X 字矩阵** | 对角线判断 (`i==j` 或 `i+j==n-1`) | [点击练习](https://www.coderli.com/gesp-2-luogu-b3865/) |
| **小杨的 H 字矩阵** | 特定行列的字符填充 | [点击练习](https://www.coderli.com/gesp-2-luogu-b3924/) |
| **小杨的日字矩阵** | 边界判断 | [点击练习](https://www.coderli.com/gesp-2-luogu-b3955/) |
| **小杨的 N 字矩阵** | 复杂对角线逻辑 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4037/) |
| **等差矩阵** | 矩阵填充规律 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4259/) |
| **菱形** | 复杂的空白与字符控制 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4412/) |

#### 3. 枚举与简单数学

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **百鸡问题** | 经典多重循环枚举 | [点击练习](https://www.coderli.com/gesp-2-luogu-b3836/) |
| **找素数** | 质数判断（试除法） | [点击练习](https://www.coderli.com/gesp-2-luogu-b3840/) |
| **乘法问题** | 因子枚举 | [点击练习](https://www.coderli.com/gesp-2-luogu-b3954/) |
| **平方之和** | 枚举或数学公式 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4002/) |
| **幂和数** | 数学函数应用 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4357/) |
| **数三角形** | 几何组合枚举 | [点击练习](https://www.coderli.com/gesp-2-luogu-b4356/) |

---

## GESP 三级：数组、字符串与进制转换

三级开始引入数据结构的概念，不再只是处理单个变量，而是处理“一批”数据。

### 核心考点与典型题型

1. **一维数组**：数组的定义、遍历、查找（最值）、统计。
    * *典型题型*：数组统计（如春游、小杨的储蓄）。
2. **字符串处理**：`string` 类的使用，长度、访问、拼接。
    * *典型题型*：字符串操作（如密码合规、回文拼接）。
3. **进制转换与位运算**：各进制转换、位运算（&, |, ^）。
    * *典型题型*：进制判断、奇偶校验、2025。
4. **简单模拟**：按步骤实现逻辑。
    * *典型题型*：小猫分鱼、分糖果。

### 备考建议

* **掌握 `string`**：熟练掌握 `string` 成员函数，理解 ASCII 码转换。
* **模拟耐心**：模拟题通常题目较长，需耐心将文字逻辑转化为代码。

### 精选真题分类练习

#### 1. 数组应用

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **春游** | 数组最值查找/匹配 | [点击练习](https://www.coderli.com/gesp-3-luogu-b3842/) |
| **小杨的储蓄** | 数组累加/模拟 | [点击练习](https://www.coderli.com/gesp-3-luogu-b3867/) |
| **寻找倍数** | 数组遍历+条件判断 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4004/) |
| **平衡序列** | 数组区间性质 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4038/) |
| **移位** | 数组元素移动/旋转 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4003/) |
| **数字替换** | 数组元素的查找与修改 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4066/) |
| **数组清零** | 数组操作 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4413/) |
| **日历制作** | 数组存储日期/星期 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4414/) |

#### 2. 字符串处理

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **密码合规** | 字符类型判断 (digit/upper/lower) | [点击练习](https://www.coderli.com/gesp-3-luogu-b3843/) |
| **回文拼接** | 回文串判断 (reverse) | [点击练习](https://www.coderli.com/gesp-3-luogu-b4039/) |
| **单位转换** | 字符串解析与数值计算 | [点击练习](https://www.coderli.com/gesp-3-luogu-b3926/) |
| **字母求和** | 字符转数字累加 | [点击练习](https://www.coderli.com/gesp-3-luogu-b3956/) |
| **词频统计** | 字符串匹配与计数 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4262/) |
| **完全平方数** | 可能是字符串与数字结合 | [点击练习](https://www.coderli.com/gesp-3-luogu-b3957/) |

#### 3. 进制与逻辑模拟

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **进制判断** | 检查数字字符是否符合某进制 | [点击练习](https://www.coderli.com/gesp-3-luogu-b3868/) |
| **奇偶校验** | 字符的二进制表示与校验 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4358/) |
| **2025** | 位运算或特定数字逻辑 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4261/) |
| **小猫分鱼** | 逆向推导或模拟 | [点击练习](https://www.coderli.com/gesp-3-luogu-b3925/) |
| **分糖果** | 模拟分配过程 | [点击练习](https://www.coderli.com/gesp-3-luogu-b4359/) |

---

## GESP 四级：函数、结构体与基础算法

四级标志着向正规算法竞赛的过渡，强调模块化编程和对数据组织形式的理解。

### 核心考点与典型题型

1. **函数与结构体**：自定义函数，结构体打包数据。
    * *典型题型*：函数封装（如幸运数）、复杂数据排序（如成绩排序、区间排序）。
2. **二维数组**：矩阵操作。
    * *典型题型*：矩阵/图像压缩、黑白方块。
3. **排序算法**：`std::sort` 与自定义 `cmp`。
    * *典型题型*：田忌赛马、字符排序。
4. **算法优化**：前缀和、滑动窗口。
    * *典型题型*：宝箱。

### 备考建议

* **学会写 `cmp`**：熟练掌握结构体排序的 `bool cmp(const Type& a, const Type& b)` 写法。
* **模块化思维**：尝试将独立逻辑封装成函数。
* **关注复杂度**：考虑是否能优化 $O(N^2)$ 的暴力解法。

### 精选真题分类练习

#### 1. 函数与模块化

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **幸运数** | 封装判断逻辑 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3850/) |
| **进制转换** | 封装不同进制转换函数 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3869/) |
| **相似字符串** | 封装字符串比较逻辑 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3958/) |
| **小杨的字典** | 字典序比较/自定义函数 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3927/) |

#### 2. 排序与结构体

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **田忌赛马** | 贪心思想 + 排序 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3928/) |
| **做题** | 简单的贪心排序 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3959/) |
| **字符排序** | 字符串数组排序 | [点击练习](https://www.coderli.com/gesp-4-luogu-b4069/) |
| **区间排序** | 结构体排序 | [点击练习](https://www.coderli.com/gesp-4-luogu-b4041/) |
| **最长连续段** | 排序后遍历 | [点击练习](https://www.coderli.com/gesp-4-luogu-b4416/) |
| **宝箱** | 排序结合前缀和/滑动窗口 | [点击练习](https://www.coderli.com/gesp-4-luogu-b4006/) |

#### 3. 多维数组与矩阵

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **图像压缩** | 矩阵遍历与统计 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3851/) |
| **变长编码** | 编码规则模拟 | [点击练习](https://www.coderli.com/gesp-4-luogu-b3870/) |
| **黑白方块** | 矩阵区域操作/前缀和优化 | [点击练习](https://www.coderli.com/gesp-4-luogu-b4005/) |
| **二阶矩阵** | 矩阵运算 | [点击练习](https://www.coderli.com/gesp-4-luogu-b4264/) |
| **排兵布阵** | 矩阵模拟 | [点击练习](https://www.coderli.com/gesp-4-luogu-b4415/) |

---

## GESP 五级：数论入门与进阶算法

五级是小学/初中阶段的一个分水岭，重点考察数学功底和常见算法模型。

### 核心考点与典型题型

1. **数论基础**：质因数分解、GCD/LCM、素数筛。
    * *典型题型*：因数分解、B-smooth数、最大公因数。
2. **贪心算法**：局部最优策略。
    * *典型题型*：巧夺大奖、烹饪问题、武器强化。
3. **二分算法**：二分查找、二分答案。
    * *典型题型*：奖品兑换（最大值最小）。

### 备考建议

* **数学补课**：复习初等数论，熟记 GCD 模板。
* **算法模板**：熟练掌握二分查找、素数筛的模板。
* **逻辑推理**：学会先推导数学性质再编程。

### 精选真题分类练习

#### 1. 数论基础

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **因数分解** | 质因数分解技巧 | [点击练习](https://www.coderli.com/gesp-5-luogu-b3871/) |
| **小杨的幸运数** | 因子/倍数性质 | [点击练习](https://www.coderli.com/gesp-5-luogu-b3929/) |
| **B-smooth 数** | 最大质因子判断 | [点击练习](https://www.coderli.com/gesp-5-luogu-b3969/) |
| **小杨的幸运数字** | 可能是数论规律 | [点击练习](https://www.coderli.com/gesp-5-luogu-p10720/) |
| **原根判断** | 模运算与阶 | [点击练习](https://www.coderli.com/gesp-5-luogu-p11961/) |
| **最大公因数** | 欧几里得算法 | [点击练习](https://www.coderli.com/gesp-5-luogu-p13014/) |

#### 2. 贪心算法

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **巧夺大奖** | 排序+选择 | [点击练习](https://www.coderli.com/gesp-5-luogu-b3872/) |
| **烹饪问题** | 时间分配贪心 | [点击练习](https://www.coderli.com/gesp-5-luogu-b3930/) |
| **挑战怪物** | 属性与策略 | [点击练习](https://www.coderli.com/gesp-5-luogu-b4050/) |
| **小杨的武器** | 性价比选择 | [点击练习](https://www.coderli.com/gesp-5-luogu-b4051/) |
| **平均分配** | 均值相关的贪心 | [点击练习](https://www.coderli.com/gesp-5-luogu-p11960/) |

#### 3. 其他进阶算法

| 题目名称 | 考察点 | 链接 |
| :--- | :--- | :--- |
| **黑白格** | 二维前缀和或优化 | [点击练习](https://www.coderli.com/gesp-5-luogu-p10719/) |
| **奖品兑换** | 典型的二分答案模型 | [点击练习](https://www.coderli.com/gesp-5-luogu-p13013/) |
| **有趣的数字和** | 前缀和应用 | [点击练习](https://www.coderli.com/gesp-5-luogu-p14074/) |

---

## 总结

* **1-2级**：重在“写代码”，把想法翻译成正确的C++语句。
* **3-4级**：重在“数据组织”，学会用数组、结构体、函数来管理数据和逻辑。
* **5级**：重在“算法与数学”，开始考察如何算得快、算得巧。

最后，**我现在找的练习题也是仅仅围绕这些考点进行的**。希望大家在学习之路多多交流。

---
{% include custom/custom-post-content-footer.md %}
