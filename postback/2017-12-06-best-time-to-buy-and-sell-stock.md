---
title: LeetCode Best Time to Buy and Sell Stock
tags: [LeetCode,Python]
date: 2017-12-06 11:51:24 +0800
comments: true
author: onecode
---
# Problem

Say you have an array for which the ith element is the price of a given stock on day i.

If you were only permitted to complete at most one transaction (ie, buy one and sell one share of the stock), design an algorithm to find the maximum profit.

Example 1:

```
Input: [7, 1, 5, 3, 6, 4]
Output: 5

max. difference = 6-1 = 5 (not 7-1 = 6, as selling price needs to be larger than buying price)
```

Example 2:

```
Input: [7, 6, 4, 3, 1]
Output: 0

In this case, no transaction is done, i.e. max profit = 0.
```

即给定一个数组，按从前往后顺序计算，求最大差。

<!--break-->

# Python 实现

``` python

'''
Say you have an array for which the ith element is the price of a given stock on day i.

If you were only permitted to complete at most one transaction (ie, buy one and sell one share of the stock),
design an algorithm to find the maximum profit.

Example 1:
Input: [7, 1, 5, 3, 6, 4]
Output: 5

max. difference = 6-1 = 5 (not 7-1 = 6, as selling price needs to be larger than buying price)
Example 2:
Input: [7, 6, 4, 3, 1]
Output: 0

In this case, no transaction is done, i.e. max profit = 0.
'''

#author li.hzh

class Solution:
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if prices is None or len(prices) <= 1:
            return 0
        min_val = prices[0]
        profit = 0
        for index in range(1, len(prices)):
            cur_val = prices[index]
            if cur_val < min_val:
                min_val = cur_val
            cur_profit = cur_val - min_val
            if cur_profit > profit:
                profit = cur_profit
        return profit


print(Solution().maxProfit([7, 1, 5, 3, 6, 4]))
print(Solution().maxProfit([7, 6, 4, 3, 1]))
print(Solution().maxProfit([7, 6, 7, 3, 5]))

```

## 分析

开始把问题想复杂了，写了个递归的解法。代码很简单，结果时间超时了。

考虑O(n)的解法，其实只要考虑最小值就好了。