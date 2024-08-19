---
title: LeetCode Intersection of Two Linked List
tags: [LeetCode,Python]
categories: [算法学习]
date: 2017-12-15 10:45:24 +0800
comments: true
author: onecode
---
# Problem

Write a program to find the node at which the intersection of two singly linked lists begins.


For example, the following two linked lists:

```
A:          a1 → a2
                   ↘
                     c1 → c2 → c3
                   ↗            
B:     b1 → b2 → b3
```

begin to intersect at node c1.


Notes:

If the two linked lists have no intersection at all, return null.
The linked lists must retain their original structure after the function returns.
You may assume there are no cycles anywhere in the entire linked structure.
Your code should preferably run in O(n) time and use only O(1) memory.

即找到两个链表相交的第一个元素。要求不改变链表结构，O（n)时间， O(1)内存

<!--break-->

# Python 实现

``` python

# Write a program to find the node at which the intersection of two singly linked lists begins.
#
#
# For example, the following two linked lists:
#
# A:          a1 → a2
#                    ↘
#                      c1 → c2 → c3
#                    ↗
# B:     b1 → b2 → b3
# begin to intersect at node c1.
#
#
# Notes:
#
# If the two linked lists have no intersection at all, return null.
# The linked lists must retain their original structure after the function returns.
# You may assume there are no cycles anywhere in the entire linked structure.
# Your code should preferably run in O(n) time and use only O(1) memory.

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

# author li.hzh
class Solution(object):
    def getIntersectionNode(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """
        if not headA or not headB:
            return None
        count_a = count_b = 1
        point_a = headA
        point_b = headB
        while point_a.next is not None:
            point_a = point_a.next
            count_a += 1
        while point_b.next is not None:
            point_b = point_b.next
            count_b += 1
        sub_num = 0
        long = short = None
        if count_a >= count_b:
            sub_num = count_a - count_b
            long = headA
            short = headB
        else:
            sub_num = count_b - count_a
            long = headB
            short = headA
        for i in range(sub_num):
            long = long.next
        while long is not short:
            long = long.next
            short = short.next
        return long

    def getIntersectionNode_II(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """
        # 考虑一个有趣的事实，设链表A = a + c（公共部分），B = b + c(公共部分）
        # 那么如果AB相接，到达c需要a + c + b步，同样BA相接，需要b + c + a 步，二者相等，因此有代码：
        point_a, point_b = headA, headB
        if not point_a or not point_b:
            return None
        while point_a is not point_b:
            point_a = point_a.next if point_a is not None else headB
            point_b = point_b.next if point_b is not None else headA
        return point_a


```

## 分析

这里我做了两个实现，第一个是比较直白的。就是先计算两个链表的长短，去掉长出的部分，剩下一样长。然后两个指针开始遍历链表，找到相等的元素即可。

第二个实现的的原理已经写在注释上了，其实开始我就考虑首尾相接的解法。不过愚蠢的当环来处理，即映射到[Linked List CycleII][1]那道题上，时间超时了。一道Easy题，怎么可能会那么复杂。改进后，好多了。


  [1]: http://www.coderli.com/linked-list-cycle-ii/