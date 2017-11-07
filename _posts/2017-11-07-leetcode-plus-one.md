---
title: LeetCode Plus One
tags: [LeetCode,Java]
date: 2017-11-07 13:21:24 +0800
comments: true
author: onecode
---
# Problem

Given a non-negative integer represented as a non-empty array of digits, plus one to the integer.

You may assume the integer do not contain any leading zero, except the number 0 itself.

The digits are stored such that the most significant digit is at the head of the list.

题目的意思即，用数组按从高位到低位的顺序表示一个非0的正整数。然后计算该整数 + 1后的结果。仍用数组表示。


<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

import java.util.stream.IntStream;

/**
 * Given a non-negative integer represented as a non-empty array of digits, plus one to the integer.
 * <p>
 * You may assume the integer do not contain any leading zero, except the number 0 itself.
 * <p>
 * The digits are stored such that the most significant digit is at the head of the list.
 *
 * @author li.hzh 2017-11-07 12:48
 */
public class PlusOne {

    public static void main(String[] args) {
        PlusOne plusOne = new PlusOne();
        printArray(plusOne.plusOne(new int[]{9, 7, 6, 5}));
        printArray(plusOne.plusOne(new int[]{9, 9, 9, 9}));
    }

    private static void printArray(int[] ints) {
        IntStream.of(ints).forEach(System.out::print);
        System.out.println();
    }

    public int[] plusOne(int[] digits) {
        boolean needCarry = false;
        for (int i = digits.length - 1; i >= 0; i--) {
            int tempSum = digits[i] + 1;
            if (tempSum != 10) {
                digits[i] = tempSum;
                needCarry = false;
                break;
            } else {
                digits[i] = 0;
                needCarry = true;
            }
        }
        if (needCarry) {
            int[] result = new int[digits.length + 1];
            result[0] = 1;
            return result;
        }
        return digits;
    }
}

```

## 分析

题目意思读懂了，很容易计算。只需要考虑一下进位即可。如果某一位 + 1后，没有进位，后面的高位也无需考虑了。数组长度变长，只有一种可能。就是全是9，这个时候数组长度加1，最高位值是1，后面都是0。

题目的意思就是考察这种计算思路，当然还有跑偏的想法就是把数组还原成整数，加1后，再转成数组。。