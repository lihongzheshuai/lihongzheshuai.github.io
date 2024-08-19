---
title: LeetCode Linked List Cycle
tags: [LeetCode,Python]
categories: [算法学习]
date: 2017-12-12 13:45:24 +0800
comments: true
author: onecode
---
# Problem

Given a linked list, determine if it has a cycle in it.

Follow up:
Can you solve it without using extra space?

判断一个链表中是否存在 环，不开辟额外的空间

<!--break-->

# Python 实现

``` python

# Given a linked list, determine if it has a cycle in it.
#
# Follow up:
# Can you solve it without using extra space?

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution(object):
    def hasCycle(self, head):
        """
        :type head: ListNode
        :rtype: bool
        """
        if head is None:
            return False
        slow, faster = head, head.next
        while faster is not None:
            slow = slow.next
            if faster.next is not None:
                faster = faster.next.next
            else:
                return False
            if slow is faster:
                return True
        return False

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


head = ListNode(1)
two = ListNode(2)
two.next = head
head.next = two

print(Solution().hasCycle(head))

```

## 分析

题目要求不适用额外的内存空间。所以，其实我想到两个办法，一个是判断该节点是否被访问过。可以把所有访问过的节点，都变成head节点，这样，当你.next又访问到head节点时，那说明有环。（因为访问到了之前访问过的节点。）不过，我并没有采用这个方法，因为它改变了链表数据，不具备实际作用。

既然是环，就采用了追击的办法，两个指针，一个快（2步），一慢（1步），如果是环，则总会追上。效率O(n)。