---
title: LeetCode Isomorphic Strings
tags: [LeetCode,Python]
categories: [算法学习]
date: 2018-05-17 23:18:24 +0800
comments: true
author: onecode
---

# Problem

Given two strings s and t, determine if they are isomorphic.

Two strings are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character but a character may map to itself.

**Example 1:**
```
Input: s = "egg", t = "add"
Output: true
```

**Example 2:**
```
Input: s = "foo", t = "bar"
Output: false
```

**Example 3:**
```
Input: s = "paper", t = "title"
Output: true
```

**Note:**
You may assume both s and t have the same length.

**同构字符串：**

给定两个字符串 s 和 t，判断它们是否是同构的。

如果 s 中的字符可以被替换得到 t ，那么这两个字符串是同构的。

所有出现的字符都必须用另一个字符替换，同时保留字符的顺序。两个字符不能映射到同一个字符上，但字符可以映射自己本身。

<!--break-->

**示例 1:**

```
输入: s = "egg", t = "add"
输出: true
```

**示例 2:**
```
输入: s = "foo", t = "bar"
输出: false
```

**示例 3:**
```
输入: s = "paper", t = "title"
输出: true
```

**说明:**
你可以假设 s 和 t 具有相同的长度。

# Python3

```python
class Solution:
    def isIsomorphic(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        temp_s_t_map = {}
        temp_t_s_map = {}
        for idx in range(len(s)):
            if temp_s_t_map.get(s[idx]) is None and temp_t_s_map.get(t[idx]) is None:
                temp_s_t_map[s[idx]] = t[idx]
                temp_t_s_map[t[idx]] = s[idx]
            elif temp_s_t_map.get(s[idx]) is not t[idx] or temp_t_s_map.get(t[idx]) is not s[idx]:
                return False
        return True


s = Solution()
print(s.isIsomorphic("egg","add"))
print(s.isIsomorphic("foo","bar"))
print(s.isIsomorphic("paper","title"))
print(s.isIsomorphic("ab","aa"))
```

# 解析

利用map里保存已经出现的字符串。判断已有映射是否一致。不一致则为False。