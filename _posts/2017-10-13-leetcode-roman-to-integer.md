---
layout: post
title: LeetCode Roman to Integer
tags: [LeetCode,Java]
categories: [算法学习]
date: 2017-10-13 13:08:24 +0800
comments: true
author: onecoder
thread_key: 1915
---
# Problem

Given a roman numeral, convert it to an integer.

Input is guaranteed to be within the range from 1 to 3999.

即将罗马数字1-3999转换成对应的整数。罗马数字规则见wiki：[罗马数字规则][1]

<!--break-->

# Java 实现

``` java

/**
 * Given a roman numeral, convert it to an integer.
 * <p>
 * Input is guaranteed to be within the range from 1 to 3999.
 *
 * @author li.hzh 2017-10-13 12:00
 */
public class RomanToInteger {

    public static void main(String[] args) {
        RomanToInteger romanToInteger = new RomanToInteger();
        System.out.println(romanToInteger.romanToInt("III"));
        System.out.println(romanToInteger.romanToInt("VI"));
        System.out.println(romanToInteger.romanToInt("XIX"));
        System.out.println(romanToInteger.romanToInt("MCDXXXVII"));
    }


    public int romanToInt(String s) {
        int pre = 0, result = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            char c = s.charAt(i);
            int value = 0;
            switch (c) {
                case 'M':
                    value = 1000;
                    break;
                case 'D':
                    value = 500;
                    break;
                case 'C':
                    value = 100;
                    break;
                case 'L':
                    value = 50;
                    break;
                case 'X':
                    value = 10;
                    break;
                case 'V':
                    value = 5;
                    break;
                case 'I':
                    value = 1;
                    break;
            }
            if (pre == 0) {
                result = pre = value;
            } else {
                result = value >= pre ? result + value : result - value;
                pre = value;
            }
        }
        return result;
    }
}


```

## 分析

仔细阅读wiki里介绍的罗马数字编写规则，其实并不难理解。尤其一种一条，领我让我顿悟：

> 但是，左减时不可跨越一个位值。比如，99不可以用IC（ {\displaystyle 100-1} 100-1）表示，而是用XCIX（ {\displaystyle [100-10]+[10-1]} [100-10]+[10-1]）表示。（等同于阿拉伯数字每位数字分别表示。）

括号里的文字，让我理解了罗马数字的规则，完全可以把罗马数字也拆成个人，十位，百位来分别对待，如此一来，这个转换规则就简单了。直接从右往左遍历字符串，左边比的右边的大或相等结果就加上该值，左边的比右边的小就减掉该值。而且，根据规则还不可能出现连续小于等于的情况。因此，如此简单处理就可以做到转换。

  [1]: https://zh.wikipedia.org/wiki/%E7%BD%97%E9%A9%AC%E6%95%B0%E5%AD%97


