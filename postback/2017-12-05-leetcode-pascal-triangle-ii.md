---
title: LeetCode Pascal's Triangle II
tags: [LeetCode,Python]
date: 2017-12-05 11:11:24 +0800
comments: true
author: onecode
---
# Problem

Given an index k, return the kth row of the Pascal's triangle.

For example, given k = 3,
Return [1,3,3,1].

Note:
Could you optimize your algorithm to use only O(k) extra space?

即直接返回杨辉三角形的某一行元素，额外要求是只让使用O（k）的空间

<!--break-->

# Python 实现

``` python

'''
Given an index k, return the kth row of the Pascal's triangle.

For example, given k = 3,
Return [1,3,3,1].

Note:
Could you optimize your algorithm to use only O(k) extra space?
'''


# author li.hzh

class Solution:
    def getRow(self, rowIndex):
        """
        :type rowIndex: int
        :rtype: List[int]
        """
        result = [1]
        for i in range(rowIndex):
            for index in range(len(result)):
                before = index - 1
                if before < 0:
                    continue
                elif index == 1:
                    result[index] = result[index] + result[before]
                else:
                    ori_val = 1
                    for i in range(1, index):
                        ori_val = result[i] - ori_val
                    result[index] += ori_val
            result.append(1)
        return result


print(Solution().getRow(0))
print(Solution().getRow(1))
print(Solution().getRow(2))
print(Solution().getRow(3))
print(Solution().getRow(4))

```

## 分析

这里只给出了我耿直的解法的代码。思路很直接，在空间限定的情况下，反推计算每行原始元素的值。然后求得新值，值的结果都保存在同一个数组中。

不过值得一提的是，在阅读别人的答案的过程中，学到了两个知识点。

一个是Python的map和lambda函数，其实跟Java8里的完全类似，用这个可以很方便的解答该问题，不过不知道空间控制如何。

另一个就是递归，其实这个是应该想到的思路，因为本次计算结果恰好依赖上次的结果。可能由于上一个问题的思维惯性，没有如此去想，还需要提高。