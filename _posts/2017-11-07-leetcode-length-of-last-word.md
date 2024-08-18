---
title: LeetCode Length of Last Word
tags: [LeetCode,Java]
date: 2017-11-07 12:38:24 +0800
comments: true
author: onecode
---
# Problem

Given a string s consists of upper/lower-case alphabets and empty space characters ' ', return the length of last word in the string.

If the last word does not exist, return 0.

Note: A word is defined as a character sequence consists of non-space characters only.

Example:

Input: "Hello World"
Output: 5

简单题，计算字符串最后一个非空字符串的长度。


<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Given a string s consists of upper/lower-case alphabets and empty space characters ' ',
 * return the length of last word in the string.
 * <p>
 * If the last word does not exist, return 0.
 * <p>
 * Note: A word is defined as a character sequence consists of non-space characters only.
 * <p>
 * Example:
 * <p>
 * Input: "Hello World"
 * Output: 5
 *
 * @author li.hzh 2017-11-07 12:22
 */
public class LengthOfLastWord {

    public static void main(String[] args) {
        LengthOfLastWord lengthOfLastWord = new LengthOfLastWord();
        System.out.println(lengthOfLastWord.lengthOfLastWord("Hello World"));
        System.out.println(lengthOfLastWord.lengthOfLastWord("a "));
        System.out.println(lengthOfLastWord.lengthOfLastWord("b   a    "));
    }

    public int lengthOfLastWord(String s) {
        if (s == null || s.length() == 0) {
            return 0;
        }
        int lastLength = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            if (s.charAt(i) != ' ') {
                lastLength++;
            } else if (lastLength == 0){
                continue;
            } else {
                break;
            }
        }
        return lastLength;
    }
}



```

## 分析

极简题，没什么可说的。只需要注意连续空格即可。例如："b   a    " 返回 1。