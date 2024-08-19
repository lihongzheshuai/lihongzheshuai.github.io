---
title: LeetCode Maximum Subarray
tags: [LeetCode,Java]
date: 2017-11-06 14:33:24 +0800
comments: true
author: onecoder
---
# Problem

Find the contiguous subarray within an array (containing at least one number) which has the largest sum.

For example, given the array [-2,1,-3,4,-1,2,1,-5,4],
the contiguous subarray [4,-1,2,1] has the largest sum = 6.

click to show more practice.

More practice:
If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.


题目的意思是求一个数组，最大子序列的和。 并且，额外要求，在O(n)算法之外，可以尝试用分治法解决该问题。


<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Find the contiguous subarray within an array (containing at least one number) which has the largest sum.
 * <p>
 * For example, given the array [-2,1,-3,4,-1,2,1,-5,4],
 * the contiguous subarray [4,-1,2,1] has the largest sum = 6.
 *
 * @author OneCoder 2017-10-31 23:41
 */
public class MaximumSubarray {

    public static void main(String[] args) {
        MaximumSubarray maximumSubarray = new MaximumSubarray();
        System.out.println(maximumSubarray.maxSubArray(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4}));
        System.out.println(maximumSubarray.maxSubArray(new int[]{-2, -1}));
        System.out.println(maximumSubarray.maxSubArray(new int[]{1, -3, 2}));
        System.out.println(maximumSubarray.maxSubArray(new int[]{1, -1, -2, 2}));
        System.out.println(maximumSubarray.maxSubArrayByDC(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4}));
        System.out.println(maximumSubarray.maxSubArrayByDC(new int[]{-2, -1}));
        System.out.println(maximumSubarray.maxSubArrayByDC(new int[]{1, -3, 2}));
        System.out.println(maximumSubarray.maxSubArrayByDC(new int[]{1, -1, -2, 2}));
    }

    public int maxSubArray(int[] nums) {
        if (nums.length == 0) {
            return 0;
        }
        int maxResult = nums[0];
        int tempSum = maxResult;
        for (int i = 1; i < nums.length; i++) {
            if (tempSum <= 0) {
                tempSum = nums[i];
            } else {
                tempSum = tempSum + nums[i];
            }
            if (tempSum > maxResult) {
                maxResult = tempSum;
            }
        }
        return maxResult;
    }

    public int maxSubArrayByDC(int[] nums) {
        if (nums.length == 0) {
            return 0;
        }
        return findMaxSubArray(nums, 0, nums.length - 1);

    }

    private int findMaxSubArray(int[] nums, int from, int to) {
        if (from == to) {
            return nums[from];
        }
        int mid = from + (to - from) / 2;
        int maxLeft = findMaxSubArray(nums, from, mid);
        int maxRight = findMaxSubArray(nums, mid + 1, to);

        int midLeftMax = nums[mid];
        int midLeftTempSum = midLeftMax;
        for (int i = mid -1; i >= from; i--) {
            midLeftTempSum += nums[i];
            if (midLeftMax < midLeftTempSum) {
                midLeftMax = midLeftTempSum;
            }
        }

        int midRightMax = nums[mid];
        int midRightTempSum = midRightMax;
        for (int i = mid + 1; i <= to; i++) {
            midRightTempSum += nums[i];
            if (midRightMax < midRightTempSum) {
                midRightMax = midRightTempSum;
            }
        }

        int midMax = midLeftMax + midRightMax - nums[mid];
        if (maxLeft >= maxRight && maxLeft >= midMax) {
            return maxLeft;
        } else if (maxRight > midMax) {
            return maxRight;
        } else {
            return midMax;
        }
    }
}


```

## 分析

解法1是一个线性解法，好处是效率够快，不足就是丢失最大子序列的位置信息，最后得到的仅仅是个最大值。

解法2，就是题目要求尝试的分治解法。即把子序列可能存在位置分三种情况考虑，左、右和横跨中点。
对于左和右，可以递归解决。横跨的简单计算即可。