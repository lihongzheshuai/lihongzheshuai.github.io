---
title: LeetCode Single Number II
tags: [LeetCode,Python]
categories: [算法学习]
date: 2017-12-11 16:08:24 +0800
comments: true
author: onecode
---
# Problem

Given an array of integers, every element appears three times except for one, which appears exactly once. Find that single one.

Note:
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

一个整型数组，除一个元素外，其余的元素都出现三次，要求不用额外内存，线性时间内找到这个元素

<!--break-->

# Python 实现

``` python

# Given an array of integers, every element appears three times except for one, which appears exactly once.
# Find that single one.
#
# Note:
# Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

# author li.hzh

class Solution:
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        once = twice = three_times = 0
        for val in nums:
            twice |= once & val
            once ^= val
            three_times = once & twice
            once &= ~three_times
            twice &= ~three_times
        return once


print(Solution().singleNumber([1, 3, 1, 1, 3, 5, 3, 6, 6, 6]))


```

## 分析

这个题确实想了很久很久。最终解决问题的思路是这样。

先是受到一个思路的启发，就是出现三次，那么可以把每一位的数字相加，然后除以3，把不能整除的位留下来。这个位组成的数字就是那个single number。不过这个思路需要对每个数字的每一位进行遍历，效率不达标。但是，却给了我很好的启发。让我关注每一位的元素是否为1。

用3个变量来分别记录，元素出现1次，2次，3次对应位的情况。当出现3次后。1次和2次对应的位置就清0，最后剩下的元素的位置就保存在1次的那个变量中。这里利用还是异或的特性。

可以简单的过一下这个过程。[3,3,3,2] 为例。

遍历第一个3时，按照设计语义，twice = 1， once =3 ，three_times = 0。继续。
第二个3，once = 0， twice = 3,（因为3出现两次），thre3_times = 0，继续
第三个3，once = 3， twice = 3 ，three_times = 3。重置1,2对应的位置。

如此下去，最后得到的就是2。

这里理解的关键，就是once twice和three_times，不要看成具体的数字，而是对数字每一位变化情况的描述。
once 异或元素。对于某一位的变化规律是1,0,1
twice 当出现2次以上时，对应的位是1
three = once & twice ，出现3此时，自然为1。