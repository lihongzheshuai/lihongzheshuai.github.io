---
title: LeetCode  Valid Palindrome
tags: [LeetCode,Python]
date: 2017-12-06 23:20:24 +0800
comments: true
author: onecode
---
# Problem

Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

For example,
"A man, a plan, a canal: Panama" is a palindrome.
"race a car" is not a palindrome.

Note:
Have you consider that the string might be empty? This is a good question to ask during an interview.

For the purpose of this problem, we define empty string as valid palindrome.

即判断一个字符串的字符部分是不是回环字符串。即出去非字母，数字以外的字符，剩下的部分满足正反相同。
<!--break-->

# Python实现

``` python?linenums

'''
Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

For example,
"A man, a plan, a canal: Panama" is a palindrome.
"race a car" is not a palindrome.

Note:
Have you consider that the string might be empty? This is a good question to ask during an interview.

For the purpose of this problem, we define empty string as valid palindrome.
'''

# author li.hzh

class Solution:
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        if len(s) == 0:
            return True
        front_index, end_index = 0, len(s) - 1
        while front_index < end_index:
            if not s[front_index].isalnum():
                front_index += 1
                continue
            if not s[end_index].isalnum():
                end_index -= 1
                continue
            if s[front_index].lower() != s[end_index].lower():
                return False
            else:
                front_index += 1
                end_index -= 1
        return True


print(Solution().isPalindrome("A man, a plan, a canal: Panama"))
print(Solution().isPalindrome("race a car"))
```

## 分析

很直接的思路，首尾两个指针，依次过滤字符进行判断。有不相等即返回False。

还有一个思路，代码很简单。先用正则去掉所有的非字母数字的字符，然后判断原字符串与逆序的字符串相等即可。该思路用python的re包实现非常简单。

```python?linenums
class Solution:
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        import re
        s = re.sub(r'[^A-Za-z0-9]', '', s).lower()
        return s == s[::-1]

```