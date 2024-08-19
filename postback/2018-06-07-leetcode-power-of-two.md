---
title: LeetCode Power of Two
tags: [LeetCode,Python]
date: 2018-06-07 16:42:24 +0800
comments: true
author: onecode
---
# Problem

Given an integer, write a function to determine if it is a power of two.

Example 1:

```
Input: 1
Output: true 
Explanation: 2^0 = 1
```

Example 2:

```
Input: 16
Output: true
Explanation: 2^4 = 16
```

Example 3:

```
Input: 218
Output: false
```

判断一个整数是否是2的幂次方

<!--break-->

# Python3

``` python
# Given an integer, write a function to determine if it is a power of two.
#
# Example 1:
#
# Input: 1
# Output: true
# Explanation: 20 = 1
# Example 2:
#
# Input: 16
# Output: true
# Explanation: 24 = 16
# Example 3:
#
# Input: 218
# Output: false

class Solution:
    def isPowerOfTwo(self, n):
        """
        :type n: int
        :rtype: bool
        """
        if n == 0:
            return False
        binary_str = bin(n)[3:]
        for c in binary_str:
            if c is not '0' and not '':
                return False
        return True

    def isPowerOfTwo_bit_operation(self, n):
        """
        :type n: int
        :rtype: bool
        """
        if n <= 0:
            return False
        while n > 0:
            if n & 1 and n != 1:
                return False
            n = n >> 1
        return True
```

## 分析

给出两种办法。一种是解析二进制的字符串。因为2的次幂都是1后面接n个0的形式的，因此判断是否有0以外的字符串即可。

另一种是利用与运算，利用的性质是一样的。个人推荐第二种思考方式。