---
title: LeetCode Merge Two Sorted Lists
tags: [LeetCode,Java]
categories: [算法学习]
date: 2017-10-19 14:49:24 +0800
comments: true
author: onecoder
thread_key: 1919
---
# Problem

Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the nodes of the first two lists.

即合并两个已经排好序的链表。并且要求返回的新链表是由原两个链表元素组合而成的。链表的结构定义也已经固定给出：

```java
public class ListNode {
        int val;
        ListNode next;

        ListNode(int x) {
            val = x;
        }
    }
```

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;


/**
 * Merge two sorted linked lists and return it as a new list.
 * The new list should be made by splicing together the nodes of the first two lists.
 *
 * @author li.hzh 2017-10-19
 */
public class MergeTwoSortedLists {

    public static void main(String[] args) {
        MergeTwoSortedLists mergeTwoSortedLists = new MergeTwoSortedLists();
        ListNode first = mergeTwoSortedLists.new ListNode(1);
        first.next = mergeTwoSortedLists.new ListNode(3);
        ListNode second = mergeTwoSortedLists.new ListNode(2);
        second.next = mergeTwoSortedLists.new ListNode(4);
//        print(mergeTwoSortedLists.mergeTwoLists(first, second));
        print(mergeTwoSortedLists.mergeTwoListsWithRecursion(first, second));
    }


    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        if (l1 == null) {
            return l2;
        }
        if (l2 == null) {
            return l1;
        }
        ListNode firstNode = null;
        ListNode lastNode = null;
        if (l1.val >= l2.val) {
            lastNode = firstNode = l2;
            l2 = l2.next;
        } else {
            lastNode = firstNode = l1;
            l1 = l1.next;
        }
        while (l1 != null || l2 != null) {
            if (l1 == null) {
                lastNode.next = l2;
                break;
            }
            if (l2 == null) {
                lastNode.next = l1;
                break;
            }
            if (l1.val >= l2.val) {
                lastNode.next = l2;
                l2 = l2.next;
                lastNode = lastNode.next;
            } else {
                lastNode.next = l1;
                l1 = l1.next;
                lastNode = lastNode.next;
            }
        }
        return firstNode;
    }

    public ListNode mergeTwoListsWithRecursion(ListNode l1, ListNode l2) {
        if (l1 == null) {
            return l2;
        }
        if (l2 == null) {
            return l1;
        }
        ListNode firstNode = null;
        if (l1.val >= l2.val) {
            firstNode = l2;
            firstNode.next = mergeTwoListsWithRecursion(l1, l2.next);
        } else {
            firstNode = l1;
            firstNode.next = mergeTwoListsWithRecursion(l1.next, l2);
        }
        return firstNode;
    }

    public class ListNode {
        int val;
        ListNode next;

        ListNode(int x) {
            val = x;
        }
    }

    private static void print(ListNode list) {
        while (list != null) {
            System.out.println(list.val);
            list = list.next;
        }
    }
}

```

## 分析

解法**mergeTwoLists**，采用的循环的方式，该思路比较直接，首先处理队列为**NULL**的边界情况。对于两个链表都不为NULL时，循环比较两个链表当前元素的值大小，将结果链表的最后一个元素.next指向值小的节点，然后该节点后移。直到有一个链表没有后续元素，即可把另一链表的所有剩下元素移过来即可。

解法**mergeTwoListsWithRecursion**，利用递归做了进一步优化和代码简化。在每层递归中，算出当前节点，然后后移继续计算，将当前节点.next指向递归计算出的结果即可最终构造出完成的链表。