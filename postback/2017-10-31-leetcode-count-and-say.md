---
title: LeetCode Count And Say
tags: [LeetCode,Java]
date: 2017-10-31 14:01:24 +0800
comments: true
author: onecoder
---
# Problem

The count-and-say sequence is the sequence of integers with the first five terms as following:

1. 1
2. 11
3. 21
4. 1211
5. 111221


1 is read off as "one 1" or 11.
11 is read off as "two 1s" or 21.
21 is read off as "one 2, then one 1" or 1211.
Given an integer n, generate the nth term of the count-and-say sequence.

Note: Each term of the sequence of integers will be represented as a string.

Example 1:

Input: 1
Output: "1"
Example 2:

Input: 4
Output: "1211"


题目的意思就是反复的计算字符中，从左向右，每种字符的数量和值。  
1 -> 1个1，即11。
11 -> 2个1，即21。
21 -> 1个2，1个1，即1211。以此类推。


<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * The count-and-say sequence is the sequence of integers with the first five terms as following:
 * <p>
 * 1.     1 <br>
 * 2.     11<br>
 * 3.     21<br>
 * 4.     1211<br>
 * 5.     111221<br>
 * 1 is read off as "one 1" or 11.<br>
 * 11 is read off as "two 1s" or 21.<br>
 * 21 is read off as "one 2, then one 1" or 1211.<br>
 * Given an integer n, generate the nth term of the count-and-say sequence.
 * <p>
 * Note: Each term of the sequence of integers will be represented as a string.
 * <p>
 * Example 1:
 * <p>
 * Input: 1
 * Output: "1"
 * <p>
 * Example 2:
 * <p>
 * Input: 4
 * Output: "1211"
 *
 * @author li.hzh 2017-10-30 13:06
 */
public class CountAndSay {

    public static void main(String[] args) {
        System.out.println(new CountAndSay().countAndSay(1));
        System.out.println(new CountAndSay().countAndSay(2));
        System.out.println(new CountAndSay().countAndSay(3));
        System.out.println(new CountAndSay().countAndSay(4));
        System.out.println(new CountAndSay().countAndSay(5));

    }

    public String countAndSay(int n) {
        String result = "1";
        for (int i = 1; i < n; i++) {
            StringBuilder builder = new StringBuilder();
            char pre = result.charAt(0);
            int count = 0;
            for (int k = 0; k < result.length(); k++) {
                if (result.charAt(k) == pre) {
                    count++;
                } else {
                    builder.append(count);
                    builder.append(pre);
                    count = 1;
                    pre = result.charAt(k);
                }
            }
            builder.append(count);
            builder.append(pre);
            result = builder.toString();
        }
        return result;
    }
}


```

## 分析

似乎没什么好分析的，遍历字符串，统计每种字符的数量，然后把数量和值依次拼接成一个新的字符串。