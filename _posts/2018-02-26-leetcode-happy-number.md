---
title: LeetCode Happy Number
tags: [LeetCode,Python]
date: 2018-02-26 16:02:24 +0800
comments: true
author: onecode
---
# Problem

Write an algorithm to determine if a number is "happy".

A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.

Example: 19 is a happy number

1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1


<!--break-->

# Python3

``` python
# Write an algorithm to determine if a number is "happy".
#
# A happy number is a number defined by the following process: Starting with any positive integer, replace the number by
#  the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay),
# or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy
# numbers.
#
# Example: 19 is a happy number
#
# 1^2 + 9^2 = 82
# 8^2 + 2^2 = 68
# 6^2 + 8^2 = 100
# 1^2 + 0^2 + 0^2 = 1

class Solution:
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        temp_result = {}
        return self.docharge(n, temp_result)

    def docharge(self, n, temp_result):
        if temp_result.get(n) is not None:
            return False
        temp_result[n] = n
        cur_sum = 0
        while n > 0:
            cur_num = n % 10
            cur_sum += cur_num ** 2
            n //= 10
        if cur_sum == 1:
            return True
        else:
            return self.docharge(cur_sum, temp_result)

solution = Solution()
print(solution.isHappy(19))
print(solution.isHappy(23))
print(solution.isHappy(22))
```

## 分析

根据题意，直接计算即可。