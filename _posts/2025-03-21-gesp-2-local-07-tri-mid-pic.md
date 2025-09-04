---
layout: post
title: 【GESP】C++二级练习 图形输出练习07-三角形（等腰）
date: 2025-03-21 09:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 多重循环, 输出图形]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 三角形（等腰）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/07_tri_mid.png)

---

### 题目分析

#### 解题思路

1. 题目分析：
   - 输入：一个正整数n，表示三角形的高度（总行数）
   - 输出：一个由星号组成的等腰三角形
   - 三角形特点：
     - 每行星号逐行递增（奇数增长：1,3,5...）
     - 最后一行星号最多
     - 左右对称

2. 解题思路：
   - 算法设计：
     - 使用单个循环处理所有行
     - 每行包含空格和星号两种字符
   - 具体步骤：
     - 每行空格数：从n-1递减到0
     - 每行星号数：从1开始，每行加2
     - 总宽度为2n-1个字符
   - 实现细节：
     - 外层循环控制行数(1到n)
     - 内层循环控制每行字符输出：
       - 先输出空格：(n-i)个
       - 再输出星号：(2*i-1)个
   - 算法复杂度：
     - 时间复杂度：O(n²)
     - 空间复杂度：O(1)
   - 边界处理：
     - 确保n为正整数
     - n=1时只打印一个星号

{% include custom/custom-post-content-inner.html %}

---

### 示例代码

```cpp
#include <iostream>
using namespace std;
int main() {
    // 声明变量n用于存储输入的行数
    int n;
    // 从标准输入读取行数
    cin >> n;
    // 计算中间位置索引
    int mid_idx = n;
    
    // 外层循环控制行数
    for (int i = 1; i <= n; i++) {
        // 内层循环控制每行的字符输出
        for (int j = 1; j <= 2 * n - 1; j++) {
            // 判断当前位置是否需要打印星号
            // j >= mid_idx - i + 1：左边界条件
            // j <= mid_idx + i - 1：右边界条件
            if (j >= mid_idx - i + 1 && j <= mid_idx + i - 1) {
                cout << "*";  // 在范围内打印星号
            } else {
                cout << " ";  // 在范围外打印空格
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
