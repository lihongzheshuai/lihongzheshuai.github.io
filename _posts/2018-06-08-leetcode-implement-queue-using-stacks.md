---
title: LeetCode Implement Queue Using Stacks
tags: [LeetCode,Python]
categories: [算法学习]
date: 2018-06-08 09:51:24 +0800
comments: true
author: onecode
---
# Problem

Implement the following operations of a queue using stacks.

```
push(x) -- Push element x to the back of queue.
pop() -- Removes the element from in front of queue.
peek() -- Get the front element.
empty() -- Return whether the queue is empty.
```

Example:

```
MyQueue queue = new MyQueue();

queue.push(1);
queue.push(2);  
queue.peek();  // returns 1
queue.pop();   // returns 1
queue.empty(); // returns false
```

Notes:

You must use only standard operations of a stack -- which means only push to top, peek/pop from top, size, and is empty operations are valid.
Depending on your language, stack may not be supported natively. You may simulate a stack by using a list or deque (double-ended queue), as long as you use only standard operations of a stack.
You may assume that all operations are valid (for example, no pop or peek operations will be called on an empty queue).false


即用stack来实现queue

<!--break-->

# Python3

``` python
# Implement the following operations of a queue using stacks.
#
# push(x) -- Push element x to the back of queue.
# pop() -- Removes the element from in front of queue.
# peek() -- Get the front element.
# empty() -- Return whether the queue is empty.
# Example:
#
# MyQueue queue = new MyQueue();
#
# queue.push(1);
# queue.push(2);
# queue.peek();  // returns 1
# queue.pop();   // returns 1
# queue.empty(); // returns false
# Notes:
#
# You must use only standard operations of a stack -- which means only push to top, peek/pop from top, size, and is
# empty operations are valid.
# Depending on your language, stack may not be supported natively. You may simulate a stack by using a list or
# deque (double-ended queue), as long as you use only standard operations of a stack.
# You may assume that all operations are valid (for example, no pop or peek operations will be called on an empty queue).

class MyQueue:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self._data = []
        self._temp_stack = []

    def push(self, x):
        """
        Push element x to the back of queue.
        :type x: int
        :rtype: void
        """
        self._data.append(x)

    def pop(self):
        """
        Removes the element from in front of queue and returns that element.
        :rtype: int
        """
        if len(self._temp_stack) == 0:
            while len(self._data) != 0:
                self._temp_stack.append(self._data.pop())
        return self._temp_stack.pop()

    def peek(self):
        """
        Get the front element.
        :rtype: int
        """
        if len(self._temp_stack) == 0:
            while len(self._data) != 0:
                self._temp_stack.append(self._data.pop())
        return self._temp_stack[-1]

    def empty(self):
        """
        Returns whether the queue is empty.
        :rtype: bool
        """
        return len(self._data) == 0 and len(self._temp_stack) == 0

# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
```

## 分析

无话可说……