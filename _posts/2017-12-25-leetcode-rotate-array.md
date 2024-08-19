---
title: LeetCode Rotate Array
tags: [LeetCode, Python]
categories: [算法学习]
date: 2017-12-25 17:07:24 +0800
comments: true
author: onecode
---
# Problem

Rotate an array of n elements to the right by k steps.

For example, with n = 7 and k = 3, the array [1,2,3,4,5,6,7] is rotated to [5,6,7,1,2,3,4].

Note:
Try to come up as many solutions as you can, there are at least 3 different ways to solve this problem.

[show hint]

Hint:
Could you do it in-place with O(1) extra space?

即按照要求移位数组。最好不利用额外空间。

<!--break-->

# Python3

``` python
# Rotate an array of n elements to the right by k steps.
#
# For example, with n = 7 and k = 3, the array [1,2,3,4,5,6,7] is rotated to [5,6,7,1,2,3,4].
#
# Note:
# Try to come up as many solutions as you can, there are at least 3 different ways to solve this problem.
#
# [show hint]
#
# Hint:
# Could you do it in-place with O(1) extra space?
# Related problem: Reverse Words in a String II

# author li.hzh
class Solution:
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        length = len(nums)
        k = k % length
        if length <= 1 or k == 0:
            return
        end_index = length - 1
        for i in range(length):
            temp = nums[i]
            current_end = end_index - i
            if i < current_end:
                nums[i] = nums[current_end]
                nums[current_end] = temp
            else:
                break
        for i in range(k):
            temp = nums[i]
            current_end = k - i - 1
            if i < current_end:
                nums[i] = nums[current_end]
                nums[current_end] = temp
            else:
                break
        for i in range(k, length):
            temp = nums[i]
            current_end = end_index - i + k
            if i < current_end:
                nums[i] = nums[current_end]
                nums[current_end] = temp
            else:
                return


solution = Solution()
nums = [1, 2, 3]
solution.rotate(nums, 1)
print(nums)

```


## 分析

题目说用3种以上不同的解法。这里只给出了一种，O(n)时间，O(1) Space的，比较好理解的解法。就是
[1,2,3,4,5] ，先反转[5,4,3,2,1]，再按照k分割前后反转就是答案。比如k=2,[4,5,1,2,3]。代码很容易写。

如果使用额外空间，那么O(n)的解法也很直接。这里不再赘述。