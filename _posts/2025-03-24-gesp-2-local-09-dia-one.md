---
layout: post
title: 【GESP】C++二级练习 图形输出练习09-菱形（中心点）
date: 2025-03-24 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 多重循环, 输出图形]
categories: [GESP, 二级]
---
GESP二级练习，一套图形输出，多层循环分支练习，考试常见，难度★✮☆☆☆。

<!--more-->

## 菱形（中心点）

### 题目要求

#### 题目描述

>输出下面图形（领会精神，废话不赘述）
>
>![X-OneCoder](/images/post/gesp/2/09_dia_one_point.png)

---

### 题目分析

#### 解题思路

跟[***图形8***](https://www.coderli.com/gesp-2-local-08-dia-mid-pic/#google_vignette)完全相似的题目，只需要把十字换成中间一个点即可。

1. 观察图形特点
   - 整体是一个n×n的方阵
   - 中心有一个十字形
   - 外围是一个菱形
   - 图形关于中心点对称

2. 确定关键点
   - 中心点坐标：(mid, mid)，其中mid = (n+1)/2
   - 十字线：所有行/列坐标等于mid的点
   - 菱形边界：到中心的曼哈顿距离等于mid-1的点

3. 实现方案
   - 使用双重循环遍历n×n矩阵
   - 对于每个点(i,j)，判断是否需要打印星号：
     - 如果在十字线上（i=mid 或 j=mid）打印星号
     - 如果到中心的距离等于mid-1，打印星号
     - 否则打印空格

4. 代码实现要点
   - 外层循环：i从1到n
   - 内层循环：j从1到n
   - 使用abs()函数计算距离
   - 每行结束输出换行

5. 复杂度分析
   - 时间复杂度：O(n²)
   - 空间复杂度：O(1)

6. 注意事项
   - 输入n必须是奇数
   - n=1时为特殊情况，只输出一个星号
   - 注意空格的打印，保持图形对称美观

{% include custom/custom-post-content-inner.html %}

---

### 示例代码

```cpp
#include <iostream>
using namespace std;
int main() {
    // 输入菱形大小n
    int n;
    cin >> n;
    // 计算中心点位置
    int mid_idx = (n + 1) / 2;
    // 外层循环控制行数
    for (int i = 1; i <= n; i++) {
        // 内层循环控制列数
        for (int j = 1; j <= n; j++) {
            // 处理中心点位置
            if (i == mid_idx && j == mid_idx) {
                cout << "*";
            } 
            // 处理上半部分菱形
            else if (i < mid_idx) {
                // 根据对称性计算菱形边界位置
                if (j == mid_idx - i + 1 || j == mid_idx + i - 1) {
                    cout << "*";
                } else {
                    cout << " ";
                }
            } 
            // 处理下半部分菱形
            else {
                // 根据对称性计算菱形边界位置
                if (j == i -mid_idx + 1 || j == n - i + mid_idx) {
                    cout << "*";
                } else {
                    cout << " ";
                }
            }
        }
        // 每行结束换行
        cout << endl;
    }
    return 0;
}
```

---

{% include custom/custom-post-content-footer.md %}
