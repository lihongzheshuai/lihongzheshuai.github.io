---
title: LeetCode Minimum Depth of Binary Tree
tags: [LeetCode,Python]
date: 2017-11-27 16:28:24 +0800
comments: true
author: onecode
---
# Problem

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

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

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Given a binary tree, find its minimum depth.
# The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
class Solution:
    def minDepth(self, root):
        if root == None:
            return 0
        minLeft = minRight = 1
        hasLeft = hasRight = False
        if root.left != None:
            minLeft = self.minDepth(root.left) + 1
            hasLeft = True
        if root.right != None:
            minRight = self.minDepth(root.right) + 1
            hasRight = True
        if not hasLeft:
            return minRight
        if not hasRight:
            return minLeft
        if minLeft <= minRight:
            return minLeft
        else:
            return minRight


tree = TreeNode(1)
tree.left = TreeNode(1)
treeFirstRight = TreeNode(1)
treeSecondLeft = TreeNode(1)
treeFirstRight.left = treeSecondLeft
# tree.right = treeFirstRight
print(Solution().minDepth(tree))

```

## 分析

显然递归是最容易想到的解决办法，每层的最小深度叠加出来就是最终的最小深度。

PS: 在学习Python，所以常用的Python解问题。

