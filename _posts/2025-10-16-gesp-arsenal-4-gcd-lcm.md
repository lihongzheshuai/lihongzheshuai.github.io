---
layout: post
title: 【GESP/CSP】编程武器库-4, 最大公约数和最小公倍数
date: 2025-10-16 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 武器库-数论]
categories: [GESP, 必备技能]
---

>在五级题目（[***【GESP】C++五级练习（初等数论考点） luogu-B3941 [GESP样题 五级] 小杨的锻炼***](https://www.coderli.com/gesp-5-luogu-b3941/)）中，涉及到最大公约数和最小公倍数的计算，需要用到数论中的基本概念和算法。这部分既是五级考试大纲中明确要求的内容([***【GESP】C++五级考试大纲知识点梳理, (1) 初等数论***](https://www.coderli.com/gesp-5-exam-syllabus-elementary-number-theory/))，又是编程考试中常见的、可复用的功能函数。因此，在我和孩子的学习过程中，已要求将这部分知识，纳入“武器库”中。
{: .prompt-info}

当前武器库清单

| 分类 | 功能 | 教程 |
|------|------|----------|
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为数字(0-9) | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为字母(a-z/A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为大写字母(A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为小写字母(a-z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [进制转换](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E8%BF%9B%E5%88%B6%E8%BD%AC%E6%8D%A2/) | 十进制和十六进制转换 |  [【GESP/CSP】编程武器库-2, 十进制转换十六进制](https://www.coderli.com/gesp-arsenal-2-dec-hex-conversion) |
| [进制转换](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E8%BF%9B%E5%88%B6%E8%BD%AC%E6%8D%A2/) | 十进制和十六进制转换 |  [【GESP/CSP】编程武器库-3, 十六进制转换十进制](https://www.coderli.com/gesp-arsenal-3-hex-dec-conversion/) |

> 本人也是边学、边实验、边总结。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

<!--more-->

---

在 C++ 中，**从 C++17 开始**，标准库已经内置了用于计算 **最大公约数（GCD）** 和 **最小公倍数（LCM）** 的函数，包含在`numeric`头文件中。但是由于CCF GESP考试要求使用 C++11 标准(`-std=c++11`)，因此我们不能直接使用这两个函数，需要掌握手动实现的方法。

手动实现的理论，是基于欧几里得算法和最大公约和最小公倍的基础公式，这部分内容已在文章([***【GESP】C++五级考试大纲知识点梳理, (1) 初等数论***](https://www.coderli.com/gesp-5-exam-syllabus-elementary-number-theory/))中详细介绍过。这里就不再赘述。下面直接给出代码的具体实现。

## 一、最大公约数（GCD）

根据欧几里得算法，最大公约数的计算可以通过循环和递归，两种方法实现。代码分别如下：

### 递归实现（推荐）

```cpp
/**
 * @brief 计算两个整数的最大公约数（GCD）——递归实现
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 返回 a 和 b 的最大公约数
 */
int gdc2(int a, int b) {
    int l = std::max(a, b); // 取较大值作为被除数
    int s = std::min(a, b); // 取较小值作为除数
    if (s == 0) {
        return l;           // 若除数为0，则最大公约数为被除数
    }
    return gdc2(s, l % s);  // 递归：用除数和余数继续计算
}
```

### 循环实现

```cpp
/**
 * @brief 计算两个整数的最大公约数（GCD）
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 返回 a 和 b 的最大公约数
 */
int gcd1(int a, int b) {
    // 确保 a 和 b 中的较大值作为被除数，较小值作为除数
    int l = std::max(a, b);
    int s = std::min(a, b);
    // 欧几里得算法：反复用余数替换除数，直到余数为 0
    while (s != 0) {
        int tmp = s;   // 暂存当前除数
        s = l % s;     // 计算余数，作为下一轮的被除数
        l = tmp;       // 上一轮除数变为下一轮的被除数
    }
    // 当余数为 0 时，l 即为最大公约数
    return l;
}
```

其实，聪明的你可能已经发现，不论是循环实现和递归实现，其实并不需要判断两个数`a`和`b`的大小，因为取模运算 `%` 的规则天然能处理两种情况：

1. **如果 a ≥ b**
   `a % b` 得到正常的余数，小于 `b`。
   下一轮就自动变成 `gcd(b, a % b)`。

2. **如果 a < b**
   `a % b == a`（因为 a 无法整除 b）。
   下一轮：

   ```cpp
   t = a % b = a;
   a = b;
   b = a;   // 即原来的 a
   ```

   相当于自动把两数“交换”了。
   下一次循环就恢复成“大的在前，小的在后”的正常状态。

循环亦如此，你可以自己推导一下。

---

## 二、最小公倍数

根据公式直接推导计算即可。

```cpp
/**
 * @brief 计算两个整数的最小公倍数（LCM）
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 返回 a 和 b 的最小公倍数
 */
int lcm(int a, int b) {
    // 利用公式：lcm(a,b) = a * b / gcd(a,b)
    return a * b / gcd1(a, b);
}
```

---

最后给出整体调用验证代码

```cpp
#include <iostream>
#include <cmath>

/**
 * @brief 计算两个整数的最大公约数（GCD）——循环实现
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 返回 a 和 b 的最大公约数
 */
int gcd1(int a, int b) {
    // 欧几里得算法：反复用余数替换除数，直到余数为 0
    while (s != 0) {
        int tmp = s;
        s = l % s;
        l = tmp;
    }
    return l;
}

/**
 * @brief 计算两个整数的最大公约数（GCD）——递归实现
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 返回 a 和 b 的最大公约数
 */
int gdc2(int a, int b) {
    if (s == 0) {
        return l;           // 若除数为0，则最大公约数为被除数
    }
    return gdc2(s, l % s);  // 递归：用除数和余数继续计算
}

/**
 * @brief 计算两个整数的最小公倍数（LCM）
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 返回 a 和 b 的最小公倍数
 */
int lcm(int a, int b) {
    // 利用公式：lcm(a,b) = a * b / gcd(a,b)
    return a * b / gcd1(a, b);
}

int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << gcd1(a, b) << std::endl;
    std::cout << gdc2(a, b) << std::endl;
    std::cout << lcm(a, b) << std::endl;
    return 0;
}
```

---

{% include custom/custom-post-content-footer.md %}
