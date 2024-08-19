---
title: LeetCode  Maximum Depth of Binary Tree
tags: [LeetCode,Java]
categories: [算法学习]
date: 2017-11-15 00:10:24 +0800
comments: true
author: onecode
---
# Problem

Given a binary tree, find its maximum depth.

The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

求二叉树的最大深度

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

/**
 * Given a binary tree, find its maximum depth.
 * <p>
 * The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
 *
 * @author OneCoder 2017-11-14 23:20
 */
public class MaximumDepthOfBinaryTree {

    public static void main(String[] args) {
        MaximumDepthOfBinaryTree maximumDepthOfBinaryTree = new MaximumDepthOfBinaryTree();
        TreeNode tree = maximumDepthOfBinaryTree.new TreeNode(1);
        TreeNode subNodeLeft = maximumDepthOfBinaryTree.new TreeNode(2);
        TreeNode subNodeRight = maximumDepthOfBinaryTree.new TreeNode(2);
        subNodeLeft.left = maximumDepthOfBinaryTree.new TreeNode(3);
        subNodeLeft.right = maximumDepthOfBinaryTree.new TreeNode(4);
        subNodeRight.left = maximumDepthOfBinaryTree.new TreeNode(4);
        subNodeRight.right = maximumDepthOfBinaryTree.new TreeNode(3);
        tree.left = subNodeLeft;
        tree.right = subNodeRight;
        System.out.println(maximumDepthOfBinaryTree.maxDepth(tree));
    }


    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int maxLeft = maxDepth(root.left);
        int maxRight = maxDepth(root.right);
        int maxChild = maxLeft >= maxRight ? maxLeft : maxRight;
        return maxChild + 1;
    }

    public class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;

        TreeNode(int x) {
            val = x;
        }
    }
}

```

## 分析

很容易想到递归。得到子树的最大深度，然后+1即可。本质应该也属于动态规划问题。