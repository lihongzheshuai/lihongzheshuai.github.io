---
title: LeetCode Majority Element
tags: [LeetCode,Python]
categories: [算法学习]
date: 2017-12-18 16:32:24 +0800
comments: true
author: onecode
---
# Problem

Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.

找到数组中重复出现次数超过数组长度⌊ n/2 ⌋ 的元素

<!--break-->

# Python 实现

``` python

# Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.
#
# You may assume that the array is non-empty and the majority element always exist in the array.

#author li.hzh
class Solution:
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        target = len(nums) // 2
        if target == 0:
            return nums[0]
        map = {}
        for val in nums:
            if val in map:
                map[val] += 1
                if map[val] > target:
                    return val
            else:
                map[val] = 1

    def majorityElement_sort(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums.sort()
        return nums[len(nums)//2]

print(Solution().majorityElement_sort([8,8,7,7,7]))

```

## 分析

给出两种方法，一种就是利用map保存值及其对应出现的次数。最直接的想法了。

不过这道题，有个比较巧的思路。就是如果一个元素出现的次数超过一半，那么排序后，[n/2]位的元素，一定是该元素。我觉得这个可能是出题者的意图吧。于是有了解法二。