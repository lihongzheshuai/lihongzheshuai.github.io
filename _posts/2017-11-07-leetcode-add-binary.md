---
title: LeetCode  Add Binary
tags: [LeetCode,Java]
date: 2017-11-07 23:32:24 +0800
comments: true
author: onecode
---
# Problem

Given two binary strings, return their sum (also a binary string).

For example,
a = "11"
b = "1"
Return "100".

题目的意思就是按二进制的方式计算两个数相加。

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Given two binary strings, return their sum (also a binary string).
 * <p>
 * For example,
 * a = "11"
 * b = "1"
 * Return "100".
 *
 * @author OneCoder 2017-11-07 21:26
 */
public class AddBinary {

    public static void main(String[] args) {
        AddBinary addBinary = new AddBinary();
        System.out.println(addBinary.addBinary("11", "1"));
        System.out.println(addBinary.addBinary("11", "11"));
        System.out.println(addBinary.addBinary("11", "111"));
        System.out.println(addBinary.addBinary("1", "111"));
        System.out.println(addBinary.addBinary("0", "0"));
    }

    public String addBinary(String a, String b) {
        int aLength = a.length();
        int bLength = b.length();
        int length = aLength >= bLength ? aLength : bLength;
        char[] chars = new char[length];
        int carryDigit = 0;
        for (int i = 0; i < length; i++) {
            int tempSum = 0;
            if (i < aLength && i < bLength) {
                tempSum = a.charAt(aLength - 1 - i) + b.charAt(bLength - 1 - i) + carryDigit - 96;
            } else if (aLength > bLength) {
                tempSum = a.charAt(aLength - 1 - i) + carryDigit - 48;
            } else if (aLength < bLength) {
                tempSum = b.charAt(bLength - 1 - i) + carryDigit - 48;
            }
            carryDigit = tempSum >= 2 ? 1 : 0;
            chars[length - i - 1] = tempSum % 2 == 0 ? (char) 48 : (char) 49;
        }
        String result = new String(chars);
        if (carryDigit != 0) {
            result = "1" + result;
        }
        return result;
    }

}

```

## 分析

跟题目[Plus One][1]很相近，只是把固定的加1变成了另一个字符串。处理方式都完全一致。只是额外需要注意的是char转int 利用 '0' = 48 额外计算一下即可。

[1]: http://www.coderli.com/leetcode-plus-one/