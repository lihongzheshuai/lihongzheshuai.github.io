---
layout: post
title: 【GESP】C++二级练习 图形输出练习02-三角形（右对齐）
date: 2025-03-20 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 三角形（右对齐）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/02_tri_right.jpg)

---

### 题目分析

#### 解题思路

1. 首先，我们需要理解题目的核心要求：
   - 输入一个正整数 n，表示三角形的行数
   - 输出一个由星号(*)组成的右对齐三角形
   - 每行星号数量从1递增到n
   - 星号右对齐显示，左侧补充空格

2. 解题思路：
   - 基本方法：
     - 使用双重循环实现三角形的打印
     - 外层循环控制行数，从1到n
     - 内层循环控制每行打印的字符数
   - 实现步骤：
     - 获取输入的正整数 n
     - 外层循环i从1到n，控制行数
     - 内层循环分两部分：
       - 先打印空格：从1到n-i
       - 再打印星号：从n- i + 1到n-1
   - 时间复杂度：
     - O(n²)，其中n为输入的行数
   - 特殊情况：
     - n应当为正整数
     - 考虑n=1的边界情况处理

{% include custom/custom-post-content-inner.html %}

---

### 示例代码

```cpp
#include <iostream>
using namespace std;
int main() {
    // 定义变量n用于存储输入的大小
    int n;
    // 从标准输入读取n的值
    cin >> n;
    // 外层循环控制行数
    for (int i = 0; i < n; i++) {
        // 内层循环控制每行字符的打印
        for (int j = 0; j < n; j++) {
            // 当j大于等于n-i-1时打印星号，实现右对齐效果
            if (j >= n - i - 1) {
                cout << "*";
            } else {
                // 否则打印空格
                cout << " ";
            }
        }
        // 每行结束后换行
        cout << endl;
    }
    return 0;
}
```

---

{% include custom/custom-post-content-footer.md %}
