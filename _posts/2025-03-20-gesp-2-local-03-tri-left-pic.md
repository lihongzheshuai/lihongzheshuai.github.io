---
layout: post
title: 【GESP】C++二级练习 图形输出练习-三角形（左对齐）
date: 2025-03-20 21:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 三角形（左对齐）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/03_tri_left.jpg)

---

### 题目分析

#### 解题思路

1. 题目分析：
   - 输入：一个正整数n，表示三角形的行数
   - 输出：左对齐的星号三角形
   - 每行星号数量：从1开始递增到n
   - 对齐方式：左对齐，无需空格填充

2. 解题思路：
   - 算法设计：
     - 使用双重循环打印三角形
     - 外循环控制行数（1到n）
     - 内循环控制每行星号数量（1到i）
   - 具体步骤：
     - 读取用户输入n
     - 外层循环i从1到n：
       - 内层循环j从1到i：打印星号
       - 每行结束打印换行
   - 算法复杂度：
     - 时间复杂度：O(n²)
   - 边界处理：
     - 确保n为正整数
     - n=1时只打印一个星号打印一个星号

{% include custom/custom-post-content-inner.html %}

---

### 示例代码

```cpp
#include <iostream>
using namespace std;
int main() {
    // 定义变量n用于存储输入的行数
    int n;
    // 从标准输入读取行数
    cin >> n;
    // 外层循环控制行数
    for (int i = 0; i < n; i++) {
        // 内层循环控制每行字符的打印
        for (int j = 0; j < n; j++) {
            // 如果当前位置小于等于行号，打印星号
            if (j <= i) {
                cout << "*";
            } 
            // 否则打印空格
            else {
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
