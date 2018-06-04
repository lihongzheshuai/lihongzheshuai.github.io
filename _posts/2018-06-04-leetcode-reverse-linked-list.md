---
title: LeetCode Reverse Linked List
tags: [LeetCode,Python]
date: 2018-06-04 23:29:24 +0800
comments: true
author: onecode
---
# Problem

Reverse a singly linked list.

Example:

```
Input: 1->2->3->4->5->NULL
Output: 5->4->3->2->1->NULL
```

Follow up:

A linked list can be reversed either iteratively or recursively. Could you implement both?

即反转链表，建议采用递归和迭代两种方式。

<!--break-->

# Python3

``` python
# Reverse a singly linked list.
#
# Example:
#
# Input: 1->2->3->4->5->NULL
# Output: 5->4->3->2->1->NULL
#
# Follow up:
#
# A linked list can be reversed either iteratively or recursively. Could you implement both?

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# 迭代法
class SolutionIteratively:
    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        pre_node = None
        while head is not None:
            pre_node, head.next, head = head, pre_node, head.next
        return pre_node


# 递归法
class SolutionRecursively:
    def reverseTail(self, cur, pre=None):
        if not cur:
            return pre
        temp_node = cur.next
        cur.next = pre
        return self.reverseTail(temp_node, cur)

    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        return self.reverseTail(head)


node_5 = ListNode(5)
node_4 = ListNode(4)
node_4.next = node_5
node_3 = ListNode(3)
node_3.next = node_4
node_2 = ListNode(2)
node_2.next = node_3
node_1 = ListNode(1)
node_1.next = node_2

solution = SolutionIteratively()
result = solution.reverseList(node_1)
print(result)

result_rec = SolutionRecursively().reverseList(node_5)
print(result_rec)

```

## 分析

迭代法中，只需要在遍历链表时重新构造链表即可。  
递归法中，将开头的元素放置末位后，只需要将剩余的链表反序即可，如此构造一个递归函数。