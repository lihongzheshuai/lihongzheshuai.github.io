---
title: LeetCode Remove Element
tags: [LeetCode,Java]
date: 2017-10-26 13:47:24 +0800
comments: true
author: onecoder
---
# Problem

Given an array and a value, remove all instances of that value in place and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

The order of elements can be changed. It doesn't matter what you leave beyond the new length.

Example:
Given input array nums = [3,2,2,3], val = 3

Your function should return length = 2, with the first two elements of nums being 2.


跟从排好序的队列出移除重复元素问题类似。从给定的队列中移除给定的元素。最后，都需要把剩余的有效元素放在队列的开头，可以理解为同一个问题。


<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Given an array and a value, remove all instances of that value in place and return the new length.
 * <p>
 * Do not allocate extra space for another array, you must do this in place with constant memory.
 * <p>
 * The order of elements can be changed. It doesn't matter what you leave beyond the new length.
 * <p>
 * Example:
 * Given input array nums = [3,2,2,3], val = 3
 * <p>
 * Your function should return length = 2, with the first two elements of nums being 2.
 *
 * @author li.hzh 2017-10-26
 */
public class RemoveElement {

    public static void main(String[] args) {
        RemoveElement removeElement = new RemoveElement();
        System.out.println(removeElement.removeElement(new int[]{}, 3));
        System.out.println(removeElement.removeElement(new int[]{2, 3, 3, 2}, 3));
        System.out.println(removeElement.removeElementByAddCount(new int[]{2, 3, 3, 2, 4, 1}, 3));
    }

    public int removeElement(int[] nums, int val) {
        int result = nums.length;
        for (int i = nums.length - 1; i >= 0; i--) {
            if (nums[i] == val) {
                result--;
                int temp = nums[result];
                nums[result] = val;
                nums[i] = temp;
            }
        }
        return result;
    }

    public int removeElementByAddCount(int[] nums, int val) {
        int result = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != val) {
                nums[result++] = nums[i];
            }
        }
        return result;
    }
}

```

## 分析

这里给出两个解法，**removeElementByAddCount**，是从前往后遍历，跟[remove duplicates from sorted array/][1] 问题解法思路一致了。

**removeElement** 解法，则是从后往前遍历，遇到给定值的元素，交换一下位置即可。


[1]: http://www.coderli.com/leetcode-remove-duplicates-from-sorted-array/