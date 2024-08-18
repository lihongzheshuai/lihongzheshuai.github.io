---
title: LeetCode Two Sum II - Input array is sorted
tags: [LeetCode,Python]
date: 2017-12-16 13:24:24 +0800
comments: true
author: onecode
---
# Problem

Given an array of integers that is already sorted in ascending order, find two numbers such that they add up to a specific target number.

The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.

You may assume that each input would have exactly one solution and you may not use the same element twice.

Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2

即找到数组中两个元素的和等于给定数字的元素，数组已排序。

<!--break-->

# Python 实现

``` python

# Given an array of integers that is already sorted in ascending order, find two numbers such that they add up to a specific target number.
#
# The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.
#
# You may assume that each input would have exactly one solution and you may not use the same element twice.
#
# Input: numbers={2, 7, 11, 15}, target=9
# Output: index1=1, index2=2

# author li.hzh
class Solution:

    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        map = {}
        index = 1
        for val in numbers:
            other = target - val
            if other in map:
                return [map.get(other), index]
            map[val] = index
            index += 1

    def twoSum_without_extra_space(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        head, tail = 0, -1
        cur_sum = numbers[head] + numbers[tail]
        while cur_sum != target:
            if cur_sum < target:
                head += 1
            else:
                tail -= 1
            cur_sum = numbers[head] + numbers[tail]
        return [head + 1, len(numbers) + tail + 1]



```

## 分析

这里也做了两个解法，解法1，是通用解法。即，不关心数组中元素的排列规律，借助一个map来寻找成对的元素。

但是，题目明确说明数组中的元素已排序，那么显然是有特殊的解法。即解法二，通过首尾元素相加，与给定值比较。如果小于给定元素，显然只能首指针向后移位，再相加比较。如果大于则尾指针前移。每次比较后，都是明确的单向移动，直到最终找到匹配结果。