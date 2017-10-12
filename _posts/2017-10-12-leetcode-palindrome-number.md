---
layout: post
title: LeetCode  Palindrome Number
tags: [LeetCode,Java]
date: 2017-10-12 13:38:24 +0800
comments: true
author: onecoder
thread_key: 1915
---
# Problem

Determine whether an integer is a palindrome. Do this without extra space.

即返回一个数是否是回数。例如：1，1221，12321是回数，负数不是回数。题目特别提醒，不要使用额外的空间，即不要考虑转换成String来处理。

# Java 实现

``` java

/**
 * Determine whether an integer is a palindrome. Do this without extra space.
 *
 * @author li.hzh 2017-10-12
 */
public class PalindromeNumber {

    public static void main(String[] args) {
        PalindromeNumber palindromeNumber = new PalindromeNumber();
        System.out.println(palindromeNumber.isPalindrome(123));
        System.out.println(palindromeNumber.isPalindrome(12321));
        System.out.println(palindromeNumber.isPalindrome(10));
        System.out.println(palindromeNumber.isPalindrome(1));
        System.out.println(palindromeNumber.isPalindrome(11));
        System.out.println(palindromeNumber.isPalindrome(1221));
    }

    public boolean isPalindrome(int x) {
        if (x < 0 || (x != 0 && x % 10 == 0)) {
            return false;
        }
        int temp = 0;
        while (x > temp) {
            temp = temp * 10 + x % 10;
            x = x / 10;
        }
        return temp / 10 == x || temp == x;
    }

}

```

## 分析

参考reverse integer的思想，先排除掉负数和以0为结尾的数。然后，对x依次取尾数，构造一个新数。最后的判断，前面是针对奇数位的情况，后面是针对偶数位的情况。
例如：
12321 ： 1232  - 1  -> 123 - 12 -> 12 - 123 。  
1221：122 - 1 -> 12 - 12 。

由于只检查了数字的1/2长度，因此不用考虑溢出情况。

