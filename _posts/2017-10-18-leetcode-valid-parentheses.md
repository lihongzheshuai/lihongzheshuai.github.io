---
title: LeetCode Valid Parentheses
tags: [LeetCode,Java]
date: 2017-10-18 12:59:24 +0800
comments: true
author: onecoder
thread_key: 1918
---
# Problem

Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.

即判断一个只包含括号的字符串，是不是合法的。

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
 * <p>
 * The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.
 *
 * @author li.hzh 2017-10-18
 */
public class ValidParentheses {

    public static void main(String[] args) {
        ValidParentheses validParentheses = new ValidParentheses();
        System.out.println(validParentheses.isValid("()[]{}"));
        System.out.println(validParentheses.isValid("([)]"));
    }

    public boolean isValid(String s) {
        if (s.length() % 2 != 0) {
            return false;
        }
        if (s.length() == 0) {
            return true;
        }
        char[] stack = new char[s.length()];
        int lastIndex = 0;
        for (int i = 0; i < s.length(); i++) {
            char currentChar = s.charAt(i);
            if (currentChar == '(' || currentChar == '[' || currentChar == '{') {
                stack[lastIndex] = currentChar;
                lastIndex++;
                continue;
            } else {
                if (lastIndex == 0) {
                    return false;
                }
                char lastValue = stack[lastIndex - 1];
                lastIndex--;
                if (currentChar == ')') {
                    if (lastValue != '(') {
                        return false;
                    }
                } else if (currentChar == ']') {
                    if (lastValue != '[') {
                        return false;
                    }
                } else {
                    if (lastValue != '{') {
                        return false;
                    }
                }
            }
        }
        if (lastIndex != 0) {
            return false;
        }
        return true;
    }
}

```

## 分析

因为要配对的，首先先pass掉长度是奇数的输入。剩下的输入，如果是左括号，则放入栈中。如果是右括号，从栈里取出最后一个元素进行配对。如果配对则继续。不配对，则说明字符串不合法。