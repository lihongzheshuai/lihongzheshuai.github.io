---
layout: post
title: 【GESP】C++二级练习 图形输出练习05-三角形（右对齐-倒置）
date: 2025-03-21 08:30 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 三角形（右对齐-倒置）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/05_tri_right_down.jpg)

---

### 题目分析

#### 解题思路

1. 题目分析：
   - 输入：一个正整数n，表示三角形的行数
   - 输出：右对齐的倒置星号三角形
   - 每行星号数量：从n开始递减到1
   - 对齐方式：右对齐，需要空格填充左侧

2. 解题思路：
   - 算法设计：
     - 使用双重循环打印倒三角形
     - 外循环控制行数（从1到n）
     - 内循环分两部分：
       - 第一部分打印空格（从1到i-1）
       - 第二部分打印星号（从n-i+1到最后）
   - 具体步骤：
     - 读取用户输入n
     - 外层循环i从1到n：
       - 先打印i-1个空格
       - 再打印n-i+1个星号
       - 每行结束打印换行
   - 算法复杂度：
     - 时间复杂度：O(n²)
     - 空间复杂度：O(1)
   - 边界处理：
     - 确保n为正整数
     - n=1时只打印一个星号，无需空格

{% include custom/custom-post-content-inner.html %}

---

### 示例代码

```cpp
#include <iostream>
using namespace std;
int main() {
    // 声明变量n用于存储用户输入的三角形行数
    int n;
    // 从标准输入读取n的值
    cin >> n;
    // 外层循环控制行数
    for (int i = 0; i < n; i++) {
        // 内层循环控制每行的字符输出
        for (int j = 0; j < n; j++) {
            // 判断当前位置是否需要打印星号
            // j >= n-i-1 表示从右向左打印星号
            if (j >= n - i - 1) {
                cout << "*";
            } else {
                // 打印空格以实现右对齐
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
