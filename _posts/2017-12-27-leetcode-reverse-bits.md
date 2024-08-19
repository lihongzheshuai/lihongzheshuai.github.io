---
title: LeetCode Reverse Bits
tags: [LeetCode, Python]
categories: [算法学习]
date: 2017-12-27 09:21:24 +0800
comments: true
author: onecode
---
# Problem

Reverse bits of a given 32 bits unsigned integer.

For example, given input 43261596 (represented in binary as 00000010100101000001111010011100), return 964176192 (represented in binary as 00111001011110000010100101000000).

Follow up:
If this function is called many times, how would you optimize it?

即将整数的32个bit，逆序后，输出对应的整数。

<!--break-->

# Python3

``` python
# Reverse bits of a given 32 bits unsigned integer.
#
# For example, given input 43261596 (represented in binary as 00000010100101000001111010011100), return 964176192 (represented in binary as 00111001011110000010100101000000).
#
# Follow up:
# If this function is called many times, how would you optimize it?

# author li.hzh
class Solution:
    # @param n, an integer
    # @return an integer
    def reverseBits(self, n):
        result = 0
        digits = 0
        while digits < 32:
            temp = n & 1
            result <<= 1
            result |= temp
            n >>= 1
            digits += 1
        return result

solution = Solution()
print(solution.reverseBits(43261596))
```


## 分析

通过位运算取整移位。不得不说，算是自己的一个进步吧，能应用位运算了。