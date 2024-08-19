---
title: LeetCode Single Number
tags: [LeetCode,Python]
date: 2017-12-07 10:01:24 +0800
comments: true
author: onecode
---
# Problem

Given an array of integers, every element appears twice except for one. Find that single one.

Note:
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

一个整型数组，除一个元素外，其余的元素都出现两次，要求不用额外内存，线性时间内找到这个元素

<!--break-->

# Python 实现

``` python

# Given an array of integers, every element appears twice except for one. Find that single one.

# Note:
# Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?
# author li.hzh

class Solution:
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        result = 0
        for val in nums:
            result ^= val
        return result


print(Solution().singleNumber([1, 1, 4, 4, 3, 5, 3, 6, 6]))

```

## 分析

题目要去不开额外内存，线性时间，显然需要特殊 运算的支持。这里位运算中的异或运算恰好满足 A ^ B ^ A = B 的规律，符合题意。