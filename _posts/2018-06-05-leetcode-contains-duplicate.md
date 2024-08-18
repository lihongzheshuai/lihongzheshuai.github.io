---
title: LeetCode Contains Duplicate
tags: [LeetCode,Python]
date: 2018-06-05 11:03:24 +0800
comments: true
author: onecode
---
# Problem

Given an array of integers, find if the array contains any duplicates.

Your function should return true if any value appears at least twice in the array, and it should return false if every element is distinct.

Example 1:

```
Input: [1,2,3,1]
Output: true
```

Example 2:

```
Input: [1,2,3,4]
Output: false
```

Example 3:

```
Input: [1,1,1,3,3,4,3,2,4,2]
Output: true
```

即判断数据中是否有重复元素
<!--break-->

# Python3

``` python
# Given an array of integers, find if the array contains any duplicates.
#
# Your function should return true if any value appears at least twice in the array, and it should return false
# if every element is distinct.
#
# Example 1:
#
# Input: [1,2,3,1]
# Output: true
# Example 2:
#
# Input: [1,2,3,4]
# Output: false
# Example 3:
#
# Input: [1,1,1,3,3,4,3,2,4,2]
# Output: true

class Solution:
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        temp_dict = {}
        for val in nums:
            if val in temp_dict:
                return True
            temp_dict[val] = val
        return False

    def containsDuplicate_via_set(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        return len(nums) != len(set(nums))
```

## 分析

两种直接的办法，一是利用dict，判断key是否存在。另一种是利用set的特性直接转换成set判断长度是否一致。