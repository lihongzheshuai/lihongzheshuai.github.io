---
layout: post
title: 【GESP】C++二级练习 图形输出练习06-菱形（实心）
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
   - 输入：一个正整数n，表示菱形的大小（总行数）
   - 输出：一个由星号组成的实心菱形
   - 菱形特点：
     - 上半部分星号逐行递增（奇数增长：1,3,5...）
     - 中间行星号最多
     - 下半部分星号逐行递减（奇数减少）
     - 左右对称

2. 解题思路：
   - 算法设计：
     - 将菱形分为上半部分（包括中间行）和下半部分
     - 使用两个独立的循环分别处理上下部分
     - 每行包含空格和星号两种字符
   - 具体步骤：
     - 计算中间行位置：mid = (n+1)/2
     - 上半部分（1到mid行）：
       - 每行空格数：从mid-1递减到0
       - 每行星号数：从1开始，每行加2
     - 下半部分（mid+1到n行）：
       - 每行空格数：从1递增
       - 每行星号数：从n-2开始，每行减2
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
    // 声明变量n用于存储用户输入的菱形大小
    int n;
    cin >> n;
    // ans表示每行需要打印的星号数量，初始为1
    int ans = 1;
    // y表示每行前面需要打印的空格数量，初始为菱形的中间位置
    int y = (n + 1) / 2;
    
    // 打印菱形的上半部分（包括中间行）
    for (int i = 1; i <= (n + 1) / 2; i++) {
        // 打印左侧空格
        for (int j = 1; j <= y - 1; j++) {
            cout << " ";
        }
        // 打印星号
        for (int k = 1; k <= ans; k++) {
            cout << "*";
        }
        // 打印右侧空格
        for (int p = 1; p <= y - 1; p++) {
            cout << " ";
        }
        // 更新下一行的参数：减少空格数，增加星号数
        y--;
        ans += 2;
        cout << endl;
    }
    
    // 重置参数，准备打印下半部分
    y = 1;
    ans = n - 2;
    // 打印菱形的下半部分
    for (int i = 1; i <= (n + 1) / 2 - 1; i++) {
        // 打印左侧空格
        for (int j = 1; j <= y; j++) {
            cout << " ";
        }
        // 打印星号
        for (int k = 1; k <= ans; k++) {
            cout << "*";
        }
        // 打印右侧空格
        for (int p = 1; p <= y; p++) {
            cout << " ";
        }
        // 更新下一行的参数：增加空格数，减少星号数
        y += 1;
        ans -= 2;
        cout << endl;
    }
    return 0;
}
```

---

{% include custom/custom-post-content-footer.md %}
