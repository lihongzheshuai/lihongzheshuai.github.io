---
title: LeetCodeClimbing Stairs
tags: [LeetCode,Java]
date: 2017-11-09 09:48:24 +0800
comments: true
author: onecode
---
# Problem

You are climbing a stair case. It takes n steps to reach to the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Note: Given n will be a positive integer.


Example 1:

Input: 2
Output:  2
Explanation:  There are two ways to climb to the top.

1. 1 step + 1 step
2. 2 steps
Example 2:

Input: 3
Output:  3
Explanation:  There are three ways to climb to the top.

1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

再经典不过的爬楼梯问题。每次只能上1或2级台阶，问n级台阶，多少种走法。


<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * ou are climbing a stair case. It takes n steps to reach to the top.
 * <p>
 * Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
 * <p>
 * Note: Given n will be a positive integer.
 * <p>
 * <p>
 * Example 1:
 * <p>
 * Input: 2
 * Output:  2
 * Explanation:  There are two ways to climb to the top.
 * <p>
 * 1. 1 step + 1 step
 * 2. 2 steps
 * Example 2:
 * <p>
 * Input: 3
 * Output:  3
 * Explanation:  There are three ways to climb to the top.
 * <p>
 * 1. 1 step + 1 step + 1 step
 * 2. 1 step + 2 steps
 * 3. 2 steps + 1 step
 *
 * @author OneCoder 2017-11-08 22:03
 */
public class ClimbingStairs {

    public static void main(String[] args) {
        String s = "a" + "b" + "c" + "d";
        ClimbingStairs climbingStairs = new ClimbingStairs();
        System.out.println(climbingStairs.climbStairsWithRecursion(3));
        System.out.println(climbingStairs.climbStairsWithRecursion(10));
        System.out.println(climbingStairs.climbStairsWithRecursion(44));
        System.out.println(climbingStairs.climbStairs(44));
    }

    public int climbStairsWithRecursion(int n) {
        if (n == 1) {
            return 1;
        } else if (n == 2) {
            return 2;
        } else {
            return climbStairsWithRecursion(n - 1) + climbStairsWithRecursion(n - 2);
        }
    }

    public int climbStairs(int n) {
        if (n == 1) {
            return 1;
        }
        int prev = 1;
        int cur = 2;
        for (int i = 3; i <= n; i++) {
            int temp = cur;
            cur += prev;
            prev = temp;
        }
        return cur;
    }
}


```

## 分析

典型的动态规划思路。因为只能爬1或2级台阶。所以，爬到n阶，最后一步只能是n-1阶走一步，或者n-2阶，走2步。因此n阶的走法=n-1阶走法+n-2阶走法。依次类推。

最简单的写法，就是递归了。不过时间超时。改成一个递推写法，就好了。
