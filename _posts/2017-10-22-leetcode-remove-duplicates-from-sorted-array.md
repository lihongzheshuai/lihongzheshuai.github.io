---
title: LeetCode  Remove Duplicates from Sorted Array
tags: [LeetCode,Java]
date: 2017-10-22 22:47:24 +0800
comments: true
author: onecoder
---
# Problem

Given a sorted array, remove the duplicates in place such that each element appear only once and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

For example,
Given input array nums = [1,1,2],

Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively. It doesn't matter what you leave beyond the new length.

题目其实包含两部分要求。首先，需要返回一个已排序数组，值不相同的元素的个数。例如：[1,1,2]返回2。这也是题目代码可以自动校验的部分。另一个隐含的要求是，要求不使用新的空间，并且在算出个数n后，将值不相同的元素，依次放置到数组的前N位。

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Given a sorted array, remove the duplicates in place such that each element appear only once and
 * return the new length.
 * <p>
 * Do not allocate extra space for another array, you must do this in place with constant memory.
 * <p>
 * For example,
 * Given input array nums = [1,1,2],
 * <p>
 * Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively.
 * It doesn't matter what you leave beyond the new length.
 *
 * @author li.hzh 2017-10-22 21:24
 */
public class RemoveDuplicatesFromSortedArray {
    
    public static void main(String[] args) {
        RemoveDuplicatesFromSortedArray rdfSortedArray = new RemoveDuplicatesFromSortedArray();
        System.out.println(rdfSortedArray.removeDuplicates(new int[]{1}));
        System.out.println(rdfSortedArray.removeDuplicates(new int[]{1, 1}));
        System.out.println(rdfSortedArray.removeDuplicates(new int[]{1, 1, 2}));
        System.out.println(rdfSortedArray.removeDuplicates(new int[]{1, 1, 2, 2}));
        System.out.println(rdfSortedArray.removeDuplicates(new int[]{1, 1, 1, 2, 2}));
        System.out.println(rdfSortedArray.removeDuplicates(new int[]{1, 1, 2, 2, 3, 3}));
        System.out.println(rdfSortedArray.removeDuplicates(new int[]{1, 2, 2, 3, 4, 4}));
    }
    
    public int removeDuplicates(int[] nums) {
        if (nums == null || nums.length == 0) {
            return 0;
        }
        int compareValue = nums[0];
        int result = 1;
        for (int i = 1; i < nums.length; i++) {
            if (compareValue < nums[i]){
                compareValue = nums[i];
                nums[result] = compareValue;
                result++;
            }
        }
        return result;
    }
    
}

```

## 分析

解法很简单，一次遍历。用变量**compareValue**记录当前比较的值，result为不相同的元素个数。当需要比较的值与当前元素值不相同时，即有新值出现的时候，结果+1，将新值放置到当前不相同元素个数所在的索引位即可。（因为题目不要求，除了不相同的元素之外的元素分配。）