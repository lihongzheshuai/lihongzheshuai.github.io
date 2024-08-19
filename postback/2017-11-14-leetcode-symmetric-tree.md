---
title: LeetCode Symmetric Tree
tags: [LeetCode,Java]
date: 2017-11-14 10:12:24 +0800
comments: true
author: onecode
---
# Problem

Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).

For example, this binary tree [1,2,2,3,4,4,3] is symmetric:

```
   1
   / \
  2   2
 / \ / \
3  4 4  3
```
But the following [1,2,2,null,3,null,3] is not:

```
  1
   / \
  2   2
   \   \
   3    3
```
Note:
Bonus points if you could solve it both recursively and iteratively.

判断一个tree是不是自对称的。建议采用递推和递归两种解法。

```java
public class TreeNode {
        int val;
        SymmetricTree.TreeNode left;
        SymmetricTree.TreeNode right;

        TreeNode(int x) {
            val = x;
        }
    }
```

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

import java.util.Stack;

/**
 * Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).
 * <p>
 * For example, this binary tree [1,2,2,3,4,4,3] is symmetric:
 * <p>
 * 1
 * / \
 * 2   2
 * / \ / \
 * 3  4 4  3
 * But the following [1,2,2,null,3,null,3] is not:
 * 1
 * / \
 * 2   2
 * \   \
 * 3    3
 * Note:
 * Bonus points if you could solve it both recursively and iteratively.
 *
 * @author OneCoder 2017-11-11 21:27
 */
public class SymmetricTree {

    public static void main(String[] args) {
        SymmetricTree symmetricTree = new SymmetricTree();
        SymmetricTree.TreeNode tree = symmetricTree.new TreeNode(1);
        SymmetricTree.TreeNode subNodeLeft = symmetricTree.new TreeNode(2);
        SymmetricTree.TreeNode subNodeRight = symmetricTree.new TreeNode(2);
        subNodeLeft.left = symmetricTree.new TreeNode(3);
        subNodeLeft.right = symmetricTree.new TreeNode(4);
        subNodeRight.left = symmetricTree.new TreeNode(4);
        subNodeRight.right = symmetricTree.new TreeNode(3);
        tree.left = subNodeLeft;
        tree.right = subNodeRight;
        System.out.println(symmetricTree.isSymmetric(tree));
    }


    public boolean isSymmetric(TreeNode root) {
        if (root == null) {
            return true;
        }
        Stack<TreeNode> leftStack = new Stack<>();
        Stack<TreeNode> rightStack = new Stack<>();
        leftStack.push(root.left);
        rightStack.push(root.right);
        while (!leftStack.isEmpty() && !rightStack.isEmpty()) {
            TreeNode leftSide = leftStack.pop();
            TreeNode rightSide = rightStack.pop();
            if (leftSide == null && rightSide == null) {
                continue;
            }
            if (leftSide == null || rightSide == null) {
                return false;
            }
            if (leftSide.val != rightSide.val) {
                return false;
            }
            leftStack.push(leftSide.right);
            leftStack.push(leftSide.left);
            rightStack.push(rightSide.left);
            rightStack.push(rightSide.right);
        }
        return leftStack.isEmpty() && rightStack.isEmpty();
    }

    // recursively
    public boolean isSymmetricRecursively(TreeNode root) {
        if (root == null) {
            return true;
        }
        return compare(root.left, root.right);
    }

    private boolean compare(TreeNode leftSide, TreeNode rightSide) {
        if (leftSide == null && rightSide == null) {
            return true;
        }
        if (leftSide == null || rightSide == null) {
            return false;
        }
        if (leftSide.val != rightSide.val) {
            return false;
        }
        return compare(leftSide.left, rightSide.right) && compare(leftSide.right, rightSide.left);
    }

    public class TreeNode {
        int val;
        SymmetricTree.TreeNode left;
        SymmetricTree.TreeNode right;

        TreeNode(int x) {
            val = x;
        }
    }

}


```

## 分析

递归似乎没什么好解释的。即左左=右右，左右=右左。

递推，就跟树的遍历一样，借助一个栈即可。

