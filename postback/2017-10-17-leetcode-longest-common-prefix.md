---
title: LeetCode Longest Common Prefix
layout: post
tags: [LeetCode,Java]
date: 2017-10-17 13:25:24 +0800
comments: true
author: onecoder
thread_key: 1917
---
# Problem

Write a function to find the longest common prefix string amongst an array of strings.

就是找出一个字符串数组中元素，最长的通用前缀。例如：{"ab","abc","abd"}，答案是 "ab"。

<!--break-->

# Java 实现

``` java

package com.coderli.leetcode.algorithms.easy;

import java.util.Arrays;

/**
 * Write a function to find the longest common prefix string amongst an array of strings.
 *
 * @author li.hzh
 */
public class LongestCommonPrefix {

    public static void main(String[] args) {
        LongestCommonPrefix longestCommonPrefix = new LongestCommonPrefix();
        System.out.println(longestCommonPrefix.longestCommonPrefix(new String[]{"a"}));
        System.out.println(longestCommonPrefix.longestCommonPrefix(new String[]{"a", "ab", "abc"}));
        System.out.println(longestCommonPrefix.longestCommonPrefix(new String[]{"abc", "ab", "abc"}));
        System.out.println(longestCommonPrefix.longestCommonPrefix(new String[]{"abd", "ab", "abc"}));
        System.out.println(longestCommonPrefix.longestCommonPrefix(new String[]{"a", "b", "c"}));
    }

    public String longestCommonPrefix(String[] strs) {
        if (strs.length == 0) {
            return "";
        }
        if (strs.length == 1) {
            return strs[0];
        }
        String result = strs[0];
        for (int i = 1; i < strs.length; i++) {
            String currentStr = strs[i];
            int findLength = Math.min(result.length(), currentStr.length());
            int commonLength = 0;
            for (int j = 0; j < findLength; j++) {
                char charInResult = result.charAt(j);
                char charInCurrent = currentStr.charAt(j);
                if (charInResult == charInCurrent) {
                    commonLength++;
                } else {
                    break;
                }
            }
            result = result.substring(0,commonLength);
        }
        return result;
    }

    public String longestCommonPrefixBySortFirst(String[] strs) {
        if (strs.length == 0) {
            return "";
        }
        if (strs.length == 1) {
            return strs[0];
        }
        Arrays.sort(strs);
        String first = strs[0];
        String second = strs[strs.length - 1];
        String result = first;
        int commonLength = 0;
        for (int j = 0; j < first.length(); j++) {
            char charInFirst = result.charAt(j);
            char charInSecond = second.charAt(j);
            if (charInFirst == charInSecond) {
                commonLength++;
            } else {
                break;
            }
        }
        result = result.substring(0,commonLength);
        return result;
    }

}



```

## 分析

这里提供了两个解法。第一个解法**longestCommonPrefix**，应该最容易被想到的解法。就是直接暴力的遍历数组元素，拿每个元素跟当前结果做前缀比较。找出最新的最大前缀。输出结果。需要注意处理一下边界值就ok。

提供第二个解法**longestCommonPrefixBySortFirst**是因为，第一个解法测试虽然通过，但效率不高。因为考虑优化性能，减少遍历。因此采用先排序再比较的做法。这样只需要拿排序后的数组的第一位和最后一位比较即可。减少一次遍历，但是增加了一次排序损耗。不过快排一般来说是O（nlgn）的，而后一次的遍历，遍历的只是数组最短长度元素的长度，因此提升了一些效率。

最后，我也查看一下提交里效率较高解法，主要的优化在于前缀计算上。参考代码如下：

```java

public String longestCommonPrefix(String[] strs) {
    if (strs.length == 0) return "";
    String prefix = strs[0];
    for (int i = 1; i < strs.length; i++)
        while (strs[i].indexOf(prefix) != 0) {
            prefix = prefix.substring(0, prefix.length() - 1);
            if (prefix.isEmpty()) return "";
        }        
    return prefix;
}

```