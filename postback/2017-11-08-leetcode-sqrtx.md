---
title: LeetCode Sqrt X
tags: [LeetCode,Java]
date: 2017-11-08 15:57:24 +0800
comments: true
author: onecode
---
# Problem

Implement int sqrt(int x).

Compute and return the square root of x.

x is guaranteed to be a non-negative integer.


Example 1:

Input: 4
Output: 2

Example 2:

Input: 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we want to return an integer, the decimal part will be truncated.

题目意思就是找出正数平方根，向下截断到整数位。


<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Implement int sqrt(int x).
 * <p>
 * Compute and return the square root of x.
 * <p>
 * x is guaranteed to be a non-negative integer.
 * <p>
 * <p>
 * Example 1:
 * <p>
 * Input: 4
 * Output: 2
 * <p>
 * <p>
 * Example 2:
 * <p>
 * Input: 8
 * Output: 2
 * Explanation: The square root of 8 is 2.82842..., and since we want to return an integer,
 * the decimal part will be truncated.
 *
 * @author li.hzh 2017-11-08 12:43
 */
public class SqrtX {

    public static void main(String[] args) {
        SqrtX sqrtX = new SqrtX();
        System.out.println(sqrtX.mySqrt(4));
        System.out.println(sqrtX.mySqrt(8));
        System.out.println(sqrtX.mySqrt(2));
        System.out.println(sqrtX.mySqrt(1));
        System.out.println(sqrtX.mySqrt(2147395599));
        System.out.println(sqrtX.mySqrt(2147483647));
    }


    public int mySqrt(int x) {
        if (x == 0) {
            return 0;
        }
        int left = 1;
        int right = x;
        int result = 0;
        for (int mid = left + ((right - left) >> 1); left <= right; mid = left + ((right - left) >> 1)) {
            int temp = x / mid;
            if (temp == mid) {
                return mid;
            } else if (temp > mid) {
                left = mid + 1;
                result = mid;
            } else {
                right = mid - 1;
            }
        }
        return result;
    }
}

```

## 分析

最暴力的就是线性遍历，但是时间复杂度不满足题目要求。那么自然想到二分查找。 这里需要注意的是考虑乘法可能造成整型溢出，所以都采用除法运算，不但规避里溢出风向。还天然截断吻合题意。
