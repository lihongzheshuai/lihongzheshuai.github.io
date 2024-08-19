---
title: LeetCode Convert Sorted Array to Binary Search Tree
tags: [LeetCode,Java]
date: 2017-11-23 16:38:24 +0800
comments: true
author: onecode
---
# Problem

Given an array where elements are sorted in ascending order, convert it to a height balanced BST.

```java
public class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;

        TreeNode(int x) {
            val = x;
        }
    }
```

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Given an array where elements are sorted in ascending order, convert it to a height balanced BST.
 *
 * @author li.hzh 2017-11-16 11:51
 */
public class ConvertSortedArrayToBinarySearchTree {

    public static void main(String[] args) {
        ConvertSortedArrayToBinarySearchTree convert = new ConvertSortedArrayToBinarySearchTree();
        printTreeMidOrder(convert.sortedArrayToBST(new int[]{2, 3, 4, 5, 7, 8, 9}));
        printTreeMidOrder(convert.sortedArrayToBST(new int[]{0}));
        printTreeMidOrder(convert.sortedArrayToBST(new int[]{1, 3}));
        printTreeMidOrder(convert.sortedArrayToBST(new int[]{-1,0, 1, 2}));
    }

    public TreeNode sortedArrayToBST(int[] nums) {
        if (nums == null || nums.length == 0) {
            return null;
        }
        if (nums.length == 1) {
            return new TreeNode(nums[0]);
        }
        int left = 0;
        int right = nums.length - 1;
        return sortedArrayToBST(left, right, nums);
    }

    private TreeNode sortedArrayToBST(int from, int to, int[] nums) {
        if (from == to) {
            return new TreeNode(nums[from]);
        }
        int mid = from + (to - from) / 2;
        TreeNode node = new TreeNode(nums[mid]);
        if (mid > from) {
            node.left = sortedArrayToBST(from, mid - 1, nums);
        }
        if (mid < to) {
            node.right = sortedArrayToBST(mid + 1, to, nums);
        }
        return node;
    }

    public class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;

        TreeNode(int x) {
            val = x;
        }
    }

    private static void printTreeMidOrder(TreeNode node) {
        if (node == null) {
            return;
        }
        if (node.left != null) {
            printTreeMidOrder(node.left);
        }
        System.out.print(node.val + " ");
        if (node.right != null) {
            printTreeMidOrder(node.right);
        }

    }
}


```

## 分析

二叉树的处理，首先想到递归。剩下就好处理了。

