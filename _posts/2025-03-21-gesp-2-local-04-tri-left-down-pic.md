---
layout: post
title: 【GESP】C++二级练习 图形输出练习04-三角形（左对齐-倒置）
date: 2025-03-21 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 三角形（左对齐-倒置）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/04_tri_left_down.jpg)

---

### 题目分析

#### 解题思路

1. 题目分析：
   - 输入：一个正整数n，表示三角形的行数
   - 输出：倒置的左对齐星号三角形
   - 每行星号数量：从n开始递减到1
   - 对齐方式：左对齐，无需空格填充

2. 解题思路：
   - 算法设计：
     - 使用双重循环打印倒三角形
     - 外循环控制行数（从n到1）
     - 内循环控制每行星号数量（从n-i+1到1）
   - 具体步骤：
     - 读取用户输入n
     - 外层循环i从1到n：
       - 内层循环j从1到n-i+1：打印星号
       - 每行结束打印换行
   - 算法复杂度：
     - 时间复杂度：O(n²)
   - 边界处理：
     - 确保n为正整数
     - n=1时打印一个星号

{% include custom/custom-post-content-inner.html %}

---

### 示例代码

```cpp
#include <iostream>
using namespace std;
int main() {
    // 定义变量n用于存储用户输入的三角形行数
    int n;
    // 从标准输入读取n的值
    cin >> n;
    // 外层循环控制行数
    for (int i = 0; i < n; i++) {
        // 内层循环控制每行字符的打印
        for (int j = 0; j < n; j++) {
            // 如果当前位置应该打印星号
            if (j < n - i) {
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
