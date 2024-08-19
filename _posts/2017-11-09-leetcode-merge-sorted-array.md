---
title: LeetCode  Merge Sorted Array
tags: [LeetCode,Java]
categories: [算法学习]
date: 2017-11-09 23:48:24 +0800
comments: true
author: onecode
---
# Problem

Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.

Note:
You may assume that nums1 has enough space (size that is greater or equal to m + n) to hold additional elements from nums2. The number of elements initialized in nums1 and nums2 are m and n respectively.

合并两个已排序的数组为一个新的排好序的数组。

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

import java.util.stream.IntStream;

/**
 * Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.
 * <p>
 * Note:
 * You may assume that nums1 has enough space (size that is greater or equal to m + n) to hold additional elements
 * from nums2. The number of elements initialized in nums1 and nums2 are m and n respectively.
 *
 * @author OneCoder 2017-11-09 22:58
 */
public class MergeSortedArray {

    public static void main(String[] args) {
        MergeSortedArray mergeSortedArray = new MergeSortedArray();
        int[] nums1 = new int[]{1, 3, 5, 7, 0, 0, 0};
        int[] nums2 = new int[]{2, 4, 6};
        mergeSortedArray.merge(nums1, 4, nums2, 3);
        IntStream.of(nums1).forEach(System.out::print);
    }

    public void merge(int[] nums1, int m, int[] nums2, int n) {
        while (m > 0 && n > 0) {
            if (nums1[m - 1] >= nums2[n - 1]) {
                nums1[n + m - 1] = nums1[m - 1];
                m--;
            } else {
                nums1[n + m - 1] = nums2[n - 1];
                n--;
            }
        }
        if (m == 0) {
            while (n > 0) {
                nums1[n - 1] = nums2[n - 1];
                n--;
            }
        }
    }

}

```

## 分析

排序数组合并，因为题目给出nums1足够大，因此从后往前放置元素可简单将元素放入最终位置。