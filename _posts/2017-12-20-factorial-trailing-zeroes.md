---
title: LeetCode Factorial Trailing Zeroes
tags: [LeetCode,Python]
categories: [算法学习]
date: 2017-12-20 15:11:24 +0800
comments: true
author: onecode
---
# Problem

Given an integer n, return the number of trailing zeroes in n!.

Note: Your solution should be in logarithmic time complexity.

即计算n!末尾0的个数。要求用对数时间复杂度
<!--break-->

# Python 实现

``` python

# Given an integer n, return the number of trailing zeroes in n!.
#
# Note: Your solution should be in logarithmic time complexity.

# author li.hzh
class Solution:
    def trailingZeroes(self, n):
        """
        :type n: int
        :rtype: int
        """
        result = 0
        while n >= 5:
            result += n // 5
            n = n // 5
        return result


solution = Solution()
print(solution.trailingZeroes(102))


```

## 分析

思路其实很直接，因为想出现0。就是 2 * 5（的倍数）。注意25是两个5。2足够。因此题目就变成求1 到 n。有多少个5。

然后，就是这个计算多少个5，却让我想了一段时间，确实不应该。就是就是递归的/5即可。因为第一次/5相等于计算有多少个5。再加上第二次，相当于求多少个25。第三次就是多少个125。叠加到一次，正好就是所有的5的个数。