---
title: LeetCode Contains Duplicate II
tags: [LeetCode,Python]
categories: [算法学习]
date: 2018-06-05 14:54:24 +0800
comments: true
author: onecode
---
# Problem

Given an array of integers and an integer k, find out whether there are two distinct indices i and j in the array such that nums[i] = nums[j] and the absolute difference between i and j is at most k.

Example 1:

```
Input: nums = [1,2,3,1], k = 3
Output: true
```

Example 2:

```
Input: nums = [1,0,1,1], k = 1
Output: true
```

Example 3:

```
Input: nums = [1,2,3,1,2,3], k = 2
Output: false
```

给定一个整数数组和一个整数 k，判断数组中是否存在两个不同的索引 i 和 j，使得 nums [i] = nums [j]，并且 i 和 j 的差的绝对值最大为 k。

<!--break-->

# Python3

``` python
# Given an array of integers and an integer k, find out whether there are two distinct indices i and j
# in the array such that nums[i] = nums[j] and the absolute difference between i and j is at most k.
#
# Example 1:
#
# Input: nums = [1,2,3,1], k = 3
# Output: true
# Example 2:
#
# Input: nums = [1,0,1,1], k = 1
# Output: true
# Example 3:
#
# Input: nums = [1,2,3,1,2,3], k = 2
# Output: false

class Solution:
    def containsNearbyDuplicate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """
        temp_dict = {}
        for idx in range(len(nums)):
            if nums[idx] in temp_dict:
                if idx - temp_dict.get(nums[idx]) <= k:
                    return True
            temp_dict[nums[idx]] = idx
        return False

```

## 分析

用dict保存值对应的索引位，当发现相同的元素时，计算距离。如果满足题意，返回True即可，否则更新最新索引位，继续计算。