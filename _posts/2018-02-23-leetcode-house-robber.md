---
title: LeetCode House Robber
tags: [LeetCode,Python]
date: 2018-02-23 17:26:24 +0800
comments: true
author: onecode
---
# Problem

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight without alerting the police.

<!--break-->

# Python3

``` python
# You are a professional robber planning to rob houses along a street.
# Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is
# that adjacent houses have security system connected and it will automatically contact the police
# if two adjacent houses were broken into on the same night.
#
# Given a list of non-negative integers representing the amount of money of each house, determine the maximum
# amount of money you can rob tonight without alerting the police.

# author li.hzh
class Solution:
    def rob(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        last = now = 0
        for i in nums:
            last, now = now, max(last + i, now)
        return now


solution = Solution()
print(solution.rob([5, 3, 1, 10]))


```

## 分析

即使用之前的最大值进行后续的计算。