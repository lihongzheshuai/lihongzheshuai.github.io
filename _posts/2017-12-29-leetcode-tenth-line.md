---
title: LeetCode Tenth Line
tags: [LeetCode, Bash]
date: 2017-12-29 13:07:24 +0800
comments: true
author: onecode
---
# Problem

How would you print just the 10th line of a file?

For example, assume that file.txt has the following content:

```
Line 1
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
```
Your script should output the tenth line, which is:
```
Line 10
```
即输出第十行，又是bash题。

<!--break-->

# Bash

``` bash
sed -n 10p file.txt
```


## 分析

没什么可说的。题目要求3种以上解法。不过对于bash题，暂时以学习了解为主。