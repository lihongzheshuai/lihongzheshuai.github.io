---
title: LeetCode Path Sum II
tags: [LeetCode,Python]
date: 2017-11-30 09:08:24 +0800
comments: true
author: onecode
---
# Problem

Given a binary tree and a sum, find all root-to-leaf paths where each path's sum equals the given sum.

For example:
Given the below binary tree and sum = 22,
 
 ```
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
```
 
return

```
[
   [5,4,11,2],
   [5,8,4,5]
]
```
即[Path Sum][1]问题的进一步，不仅仅是判断是否存在路径，而是找出所有的路径。

<!--break-->

# Python 实现

``` python

'''
Given a binary tree and a sum, find all root-to-leaf paths where each path's sum equals the given sum.

For example:
Given the below binary tree and sum = 22,
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
return
[
   [5,4,11,2],
   [5,8,4,5]
]
'''


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

# author li.hzh 2017-11-29 23:34
class Solution:
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype:
         List[List[int]]
        """
        result = []
        if root is None:
            return result
        cur_val = root.val
        sub_sum = sum - cur_val
        if root.left is None and root.right is None and sub_sum == 0:
            return [[cur_val]]
        left_result = []
        if root.left is not None:
            left_result = self.pathSum(root.left, sub_sum)
        if root.right is not None:
            left_result.extend(self.pathSum(root.right, sub_sum))
        for path in left_result:
            path.insert(0, cur_val)
            result.append(path)
        return result


from my.leetcode.TreeNode import TreeNode

tree = TreeNode(1)
one_left = TreeNode(2)
one_right = TreeNode(2)
tree.left = one_left
tree.right = one_right
one_left.left = TreeNode(3)
one_left.right = TreeNode(3)
one_right.left = TreeNode(3)
one_right.right = TreeNode(3)
print(Solution().pathSum(tree, 6))

```

## 分析

思路依然是递归，只是这次把路径保存起来即可。


  [1]: http://www.coderli.com/leetcode-path-sum/