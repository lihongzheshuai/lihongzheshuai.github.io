---
title: LeetCode Valid Phone Number
tags: [LeetCode, Bash]
date: 2017-12-28 17:26:24 +0800
comments: true
author: onecode
---
# Problem

Given a text file file.txt that contains list of phone numbers (one per line), write a one liner bash script to print all valid phone numbers.

You may assume that a valid phone number must appear in one of the following two formats: (xxx) xxx-xxxx or xxx-xxx-xxxx. (x means a digit)

You may also assume each line in the text file must not contain leading or trailing white spaces.

For example, assume that file.txt has the following content:

```
987-123-4567
123 456 7890
(123) 456-7890
```
Your script should output the following valid phone numbers:
```
987-123-4567
(123) 456-7890
```
即从文件中找到合法的电话号码。又进入bash题区了。

<!--break-->

# Bash

``` bash
grep -P '^(\d{3}-|\(\d{3}\) )\d{3}-\d{4}$' file.txt
```


## 分析

没啥可说的，正则题而已。唯一需要注意的是，这里用的是\d ，所以需要-P支持。