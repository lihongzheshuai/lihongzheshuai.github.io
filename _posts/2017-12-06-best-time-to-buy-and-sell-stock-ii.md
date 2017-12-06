---
title: LeetCode Best Time to Buy and Sell Stock II
tags: [LeetCode,Python]
date: 2017-12-06 17:19:24 +0800
comments: true
author: onecode
---
# Problem

Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times). However, you may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

上一个问题的变形，即求累计利润的最大值。就是按顺序相减的和。

<!--break-->

# Python 实现

``` python

'''
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like
(ie, buy one and sell one share of the stock multiple times).
However, you may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).
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
        buy = sell = prices[0]
        profit = 0
        for index in range(1,len(prices)):
            if prices[index] < sell:
                profit += (sell - buy)
                buy = sell = prices[++index]
            else:
                sell = prices[index]
        profit += (sell - buy)
        return profit


print(Solution().maxProfit([7, 1, 5, 3, 6, 4]))
print(Solution().maxProfit([7, 6, 4, 3, 1]))
print(Solution().maxProfit([7, 6, 7, 3, 5]))

```

## 分析

并不是最简代码，其实有个很简单的思路。就是遍历，如果i+1 > i 的值，就相减。如此累计即可。代码非常简洁。粘一个Java版本的样例

```java
public class Solution {
public int maxProfit(int[] prices) {
    int total = 0;
    for (int i=0; i< prices.length-1; i++) {
        if (prices[i+1]>prices[i]) total += prices[i+1]-prices[i];
    }
    
    return total;
}
```