---
title: LeetCode Number of 1 Bits
tags: [LeetCode, Python]
categories: [算法学习]
date: 2017-12-28 16:16:24 +0800
comments: true
author: onecode
---
# Problem

Write a function that takes an unsigned integer and returns the number of ’1' bits it has (also known as the Hamming weight).

For example, the 32-bit integer ’11' has binary representation 00000000000000000000000000001011, so the function should return 3.

求整数转化为二进制数中，1的个数

<!--break-->

# Python3

``` python
# Write a function that takes an unsigned integer and returns the number of ’1' bits
# it has (also known as the Hamming weight).
#
# For example, the 32-bit integer ’11' has binary representation 00000000000000000000000000001011,
# so the function should return 3.

# author li.hzh
class Solution(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """
        result = 0
        while n:
            n = n & n - 1
            result += 1
        return  result

print(Solution().hammingWeight(11))
```


## 分析

其实完全可以通过Reverst Bit中的方法，通过 & 1，右移把1统计出来。不过效率会略低。因为每一位都要检查。

这里通过一个技巧 n & (n-1)，想象一下，每次都会消掉一个1，就加快了效率。