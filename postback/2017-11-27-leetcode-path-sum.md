---
title: LeetCode Path Sum
tags: [LeetCode,Python]
date: 2017-11-27 17:10:24 +0800
comments: true
author: onecode
---
# Problem

Given a binary tree and a sum, determine if the tree has a root-to-leaf path such that adding up all the values along the path equals the given sum.

For example:
Given the below binary tree and sum = 22,
 
 ```
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \      \
        7    2      1
```
 
return true, as there exist a root-to-leaf path 5->4->11->2 which sum is 22.

```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
```

<!--break-->

# Python 实现

``` python

'''
Given a binary tree and a sum, determine if the tree has a root-to-leaf path such that adding up all the values along the path equals the given sum.

For example:
Given the below binary tree and sum = 22,
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \      \
        7    2      1
return true, as there exist a root-to-leaf path 5->4->11->2 which sum is 22.
'''
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def hasPathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: bool
        """
        if root == None:
            return False
        leftValue = sum - root.val
        if root.left == None and root.right == None and leftValue == 0:
            return True
        return self.hasPathSum(root.left, leftValue) or self.hasPathSum(root.right, leftValue)


```

## 分析

还是递归的思路。子树有满足减去当前节点值的和即可。
