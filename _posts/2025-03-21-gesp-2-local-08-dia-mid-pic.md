---
layout: post
title: 【GESP】C++二级练习 图形输出练习08-菱形（十字）
date: 2025-03-21 09:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 多重循环, 输出图形]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 菱形（十字）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/08_dia_ten.png)

---

### 题目分析

#### 解题思路

1. 题目分析：
   - 输入：一个正整数n，表示菱形（十字）的大小（边长）
   - 输出：一个由星号组成的菱形和十字叠加图案
   - 图形特点：
     - 中间一行和一列为十字形
     - 外围为菱形图案
     - 整体呈对称分布

2. 解题思路：
   - 算法设计：
     - 使用双层循环处理行和列
     - 根据位置判断是否输出星号
   - 具体步骤：
     - 计算中间位置：mid = (n+1)/2
     - 判断输出位置：
       - 中间行和列输出星号
       - 上半部分对称位置输出星号
       - 下半部分对称位置输出星号
   - 实现细节：
     - 外层循环控制行数(1到n)
     - 内层循环控制列数(1到n)
     - 根据当前位置与中间位置的关系判断：
       - 是否在十字线上
       - 是否在菱形边界上
   - 算法复杂度：
     - 时间复杂度：O(n²)
     - 空间复杂度：O(1)
   - 边界处理：
     - 确保n为正奇数
     - n=1时只打印一个星号

{% include custom/custom-post-content-inner.html %}

---

### 示例代码

```cpp
#include <iostream>
using namespace std;
int main() {
    // 声明变量n用于存储输入的大小
    int n;
    // 从标准输入读取n的值
    cin >> n;
    // 计算中间位置索引
    int mid_idx = (n + 1) / 2;
    // 外层循环控制行数
    for (int i = 1; i <= n; i++) {
        // 内层循环控制每行的字符输出
        for (int j = 1; j <= n; j++) {
            // 处理十字交叉的中心线
            if (i == mid_idx || j == mid_idx) {
                cout << "*";
            } 
            // 处理上半部分的图案
            else if (i < mid_idx) {
                // 根据位置计算是否输出星号
                if (j == mid_idx - i + 1 || j == mid_idx + i - 1) {
                    cout << "*";
                } else {
                    cout << " ";
                }
            } 
            // 处理下半部分的图案
            else {
                // 根据位置计算是否输出星号
                if (j == i -mid_idx + 1 || j == n - i + mid_idx) {
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

---

{% include custom/custom-post-content-footer.md %}
