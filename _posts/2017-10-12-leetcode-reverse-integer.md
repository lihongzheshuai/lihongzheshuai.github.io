---
layout: post
title: LeetCode  Reverse Integer
tags: [LeetCode,Java]
date: 2017-10-12 13:29:24 +0800
comments: true
author: onecoder
thread_key: 1914
---
# Problem

Reverse digits of an integer.

Example1: x = 123, return 321
Example2: x = -123, return -321

Note:
The input is assumed to be a 32-bit signed integer. Your function should return 0 when the reversed integer overflows.

即返回一个数的逆序数。

# Java 实现

``` java

/**
 * Reverse digits of an integer.
 * <p>
 * Example1: x = 123, return 321
 * Example2: x = -123, return -321
 *
 * @author li.hzh
 * @date 2017-10-11 22:07
 */
public class ReverseInteger {
    
    public static void main(String[] args) {
        int x = 123;
        int y = -321;
        int z = 1000000003;
        ReverseInteger instance = new ReverseInteger();
        System.out.println(instance.reverse(x));
        System.out.println(instance.reverse(y));
        System.out.println(instance.reverse(z));
    }
    
    public int reverse(int x) {
        int result = 0;
        int tempResult = 0;
        while (x != 0) {
            int remainder = x % 10;
            result = result * 10 + remainder;
            if ((result - remainder) / 10 != tempResult) {
                return 0;
            }
            tempResult = result;
            x = x / 10;
        }
        return result;
    }
    
}

```

## 分析

reverse中为具体实现，上面是简单的测试用例。通过一次除以10 取余来依次从后至前得到末尾数，构造逆序数。通过

```java
if ((result - remainder) / 10 != tempResult) {
                return 0;
				}
```

逆计算来判断整数是否溢出。


