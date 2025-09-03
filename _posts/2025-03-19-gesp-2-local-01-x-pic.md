---
layout: post
title: 【GESP】C++二级练习 图形输出练习01-X图形
date: 2025-03-19 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 多重循环, 输出图形]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## X图形输出

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/01_x.jpg)

---

### 题目分析

#### 解题思路

1. 首先，我们需要理解题目的核心要求：
   - 输入一个正整数 n，表示X图形的大小
   - 输出一个由星号(*)组成的X形状图案
   - 图形大小为 n×n 的方阵
   - 只在对角线位置打印星号，其他位置为空格

2. 解题思路：
   - 基本方法：
     - 使用双重循环实现X图形的打印
     - 外层循环控制行数，从0到n-1
     - 内层循环控制每行打印的字符数
   - 实现步骤：
     - 获取输入的正整数 n
     - 外层循环i从0到n-1，控制行数
     - 内层循环j从0到n-1，控制每行字符
     - 当j=i或j=n-i-1时打印星号，否则打印空格
   - 优化考虑：
     - 使用cout输出，简化代码
     - 使用endl确保每行结束换行
   - 时间复杂度：
     - O(n²)，其中n为输入的大小
   - 特殊情况：
     - 输入n需要为奇数，才能保证X的中心点正确显示
     - n应当大于等于3，才能形成有效的X形状

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
        // 内层循环控制每行的字符输出
        for (int j = 0; j < n; j++) {
            // 当j等于i或者j等于n-i-1时，输出星号
            // 这样可以在对角线位置打印星号，形成X形状
            if (j == i || j == n - i - 1) {
                cout << "*";
            } else {
                // 其他位置输出空格
                cout << " ";
            }
        }
        // 每行结束后换行
        cout << endl;
    }
    // 程序结束
    return 0;
}
```

---

{% include custom/custom-post-content-footer.md %}
