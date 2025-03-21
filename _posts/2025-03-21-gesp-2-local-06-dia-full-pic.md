---
layout: post
title: 【GESP】C++二级练习 图形输出练习-菱形（实心）
date: 2025-03-21 09:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 菱形（实心）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/06_dia_full.png)

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

#### 方法一（我的）

```cpp
#include <iostream>
using namespace std;
int main() {
    // 声明变量n用于存储用户输入的菱形大小
    int n;
    // 从标准输入读取菱形大小
    cin >> n;
    // 计算菱形的中间行索引
    int mid_idx = (n + 1) / 2;
    // 外层循环控制行数
    for (int i =1; i <= n; i++) {
        // 内层循环控制每行的字符输出
        for (int j = 1; j <= n; j++) {
            // 处理中间行的情况（全部打印星号）
            if (i == mid_idx) {
                cout << "*";
            } 
            // 处理中间行以上的部分
            else if (i < mid_idx){
                // 根据当前位置判断是否打印星号
                // mid_idx - i + 1 到 mid_idx + i - 1 的范围内打印星号
                if (j >= mid_idx - i + 1 && j <= mid_idx + i - 1) {
                    cout << "*";
                } else {
                    cout << " ";
                }
            } 
            // 处理中间行以下的部分
            else {
                // 根据当前位置判断是否打印星号
                // i - mid_idx 到 n - (i - mid_idx) 的范围内打印星号
                if (j > i - mid_idx && j <= n - (i - mid_idx) ) {
                    cout << "*";
                } else {
                    cout << " ";
                }
            }
        }
        // 每行结束后换行
        cout << endl;
    }
    return 0;
}
```

#### 方法二（孩子）

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    int ans = 1;
    int y = (n + 1) / 2;
    for (int i = 1; i <= (n + 1) / 2; i++) {
        for (int j = 1; j <= y - 1; j++) {
            cout << " ";
        }
        for (int k = 1; k <= ans; k++) {
            cout << "*";
        }
        for (int p = 1; p <= y - 1; p++) {
            cout << " ";
        }
        y--;
        ans += 2;
        cout << endl;
    }
    y = 1;
    ans = n - 2;
    for (int i = 1; i <= (n + 1) / 2 - 1; i++) {
        for (int j = 1; j <= y; j++) {
            cout << " ";
        }
        for (int k = 1; k <= ans; k++) {
            cout << "*";
        }
        for (int p = 1; p <= y; p++) {
            cout << " ";
        }
        y += 1;
        ans -= 2;
        cout << endl;
    }
    return 0;
}
```

---

{% include custom/custom-post-content-footer.md %}
