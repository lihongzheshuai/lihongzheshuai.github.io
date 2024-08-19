---
layout: post
title: "LeetCode[Algorithms] Add Two Numbers"
modified:
excerpt: LeetCode [Add Two Numbers] by OneCoder
tags: [算法,LeetCode]
categories: [算法学习]
thread_key: 1868
date: 2015-09-06T10:00:45
---
You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.<br />

<!--more-->

**Input:** (2 -> 4 -> 3) + (5 -> 6 -> 4)<br />
**Output:** 7 -> 0 -> 8

{% highlight java %}
package com.coderli.leetcode.algorithms;

/**
 * You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
 * <p>
 * Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)<br/>
 * Output: 7 -> 0 -> 8
 * <p>
 *
 * @author li.hzh
 * @date 2015/8/27 08:41
 */
public class AddTwoNumbers {

    public static void main(String[] args) {
        AddTwoNumbers addTwoNumbers = new AddTwoNumbers();
        Solution solution = addTwoNumbers.new Solution();
        ListNode one = addTwoNumbers.createNode(2,3,4,5);
        ListNode two = addTwoNumbers.createNode(4,5,6,7);
        ListNode result = solution.addTwoNumbers(one, two);
        addTwoNumbers.printListNode(result);
    }

    private void printListNode(ListNode node) {
        ListNode cNode = node;
        do {
            System.out.print(cNode.val);
            if (cNode.next != null) {
                System.out.print("->");
            }
            cNode = cNode.next;
        } while (cNode != null);
        System.out.println();
    }

    private ListNode createNode(int... values) {
        ListNode result = new ListNode(values[0]);
        if (values.length > 1) {
            ListNode currentNode = new ListNode(values[1]);
            result.next = currentNode;
            for (int i = 2; i < values.length; i++) {
                currentNode.next = new ListNode(values[i]);
                currentNode = currentNode.next;
            }
        }
        return result;
    }

    /**
     * Definition for singly-linked list.
     * public class ListNode {
     * int val;
     * ListNode next;
     * ListNode(int x) { val = x; }
     * }
     */
    public class Solution {


        public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
            int carryInt = 0;
            ListNode result = null;
            ListNode resultCurrentNode = null;
            ListNode l1Current = l1;
            ListNode l2Current = l2;
            while (l1Current != null || l2Current != null || carryInt == 1) {
                int l1Value = l1Current == null ? 0 : l1Current.val;
                int l2Value = l2Current == null ? 0 : l2Current.val;
                int tempVal = l1Value + l2Value + carryInt;
                if (tempVal > 9) {
                    tempVal = tempVal % 10;
                    carryInt = 1;
                } else {
                    carryInt = 0;
                }
                if (result == null) {
                    resultCurrentNode = result = new ListNode(tempVal);
                } else {
                    resultCurrentNode.next = new ListNode(tempVal);
                    resultCurrentNode = resultCurrentNode.next;
                }
                l1Current = l1Current == null ? null : l1Current.next;
                l2Current = l2Current == null ? null : l2Current.next;
            }
            return result;
        }
    }

    public class ListNode {
        int val;
        ListNode next;

        ListNode(int x) {
            val = x;
        }
    }
}
{% endhighlight %}
