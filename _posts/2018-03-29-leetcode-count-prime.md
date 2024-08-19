---
title: LeetCode Count Primes
tags: [LeetCode,Python]
categories: [算法学习]
date: 2018-03-29 23:26:24 +0800
comments: true
author: onecode
---
# Problem

Description:

Count the number of prime numbers less than a non-negative number, n.

即统计小于n的质数个数

<!--break-->

# Python3

``` python
# Count the number of prime numbers less than a non-negative number, n.

class Solution:
    def countPrimes(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n < 3:
            return 0
        primes = [True] * n
        primes[0] = primes[1] = False
        for i in range(2, int(n ** 0.5) + 1):
            if primes[i]:
                primes[i * i: n: i] = [False] * len(primes[i * i: n: i])
        return sum(primes)


solution = Solution()
print(solution.countPrimes(2))
print(solution.countPrimes(499979))


```

## 分析

采用空间换时间的方式。否则会超时。