---
layout: post
title: "LeetCode[Algorithms] Two Sum"
modified:
categories:
excerpt: LeetCode [Two Sum] by OneCoder
tags: [leetcode, algorithms, two sum]
image:
  feature:
thread_key: 1867
date: 2015-09-06T09:35:45
---
Given an array of integers, find two numbers such that they add up to a specific target number.
The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.
You may assume that each input would have exactly one solution.<br />
**Input:** numbers={2, 7, 11, 15}, target=9<br />
**Output:** index1=1, index2=2

{% highlight java %}
package com.coderli.leetcode.algorithms;

import java.util.HashMap;
import java.util.Map;

/**
 * Given an array of integers, find two numbers such that they add up to a specific target number.
 * <p>
 * The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.
 * <p>
 * You may assume that each input would have exactly one solution.
 * <p>
 * <p>
 * Input: numbers={2, 7, 11, 15}, target=9 <br/>
 * Output: index1=1, index2=2
 * <p>
 *
 * @author li.hzh
 * @date 2015-08-26 21:49
 */
public class TwoSum {

    public static void main(String[] args) {
        int nums[] = {-2, -7, 11, 15};
        int target = -9;
        Solution solution = new TwoSum().new Solution();
        SolutionTwo solutionTwo = new TwoSum().new SolutionTwo();
        int result[] = solution.twoSum(nums, target);
        System.out.println("index1=" + result[0] + ", index2=" + result[1]);
        result = solutionTwo.twoSum(nums, target);
        System.out.println("index1=" + result[0] + ", index2=" + result[1]);
    }


    /**
     * 最简单的O(n2)的解法
     */
    public class Solution {
        public int[] twoSum(int[] nums, int target) {
            int[] output = new int[2];
            int length = nums.length;
            for (int i = 0; i < length - 1; i++) {
                for (int j = i + 1; j < length; j++) {
                    if (nums[i] + nums[j] == target) {
                        if (i <= j) {
                            output[0] = i + 1;
                            output[1] = j + 1;
                        } else {
                            output[0] = j + 1;
                            output[1] = i + 1;
                        }
                    }
                }
            }
            return output;
        }
    }

    /**
     * O(n2) runtime, O(1) space – Brute force:
     * <p>
     * The brute force approach is simple. Loop through each element x and find if there is another value that equals to target – x. As finding another value requires looping through the rest of array, its runtime complexity is O(n2).
     * <p>
     * O(n) runtime, O(n) space – Hash table:
     * <p>
     * We could reduce the runtime complexity of looking up a value to O(1) using a hash map that maps a value to its index.
     */
    public class SolutionTwo {
        public int[] twoSum(int[] nums, int target) {
            Map map = new HashMap();
            int[] output = new int[2];
            int length = nums.length;
            for (int i = 0; i < length; i++) {
                int j = target - nums[i];
                if (map.containsKey(j)) {
                    int index = (int) map.get(j);
                    if (index < i) {
                        output[0] = index + 1;
                        output[1] = i + 1;
                    } else {
                        output[0] = i + 1;
                        output[1] = index + 1;
                    }
                    return output;
                }
                map.put(nums[i], i);
            }
            return null;
        }
    }
}
{% endhighlight %}
总结：以空间换时间，解决以前关于HashMap的时间复杂度的误区，查询了HashMap实现相关的文章。
参考：[http://it.deepinmind.com/%E6%80%A7%E8%83%BD/2014/04/24/hashmap-performance-in-java-8.html](http://it.deepinmind.com/%E6%80%A7%E8%83%BD/2014/04/24/hashmap-performance-in-java-8.html "http://it.deepinmind.com/%E6%80%A7%E8%83%BD/2014/04/24/hashmap-performance-in-java-8.html")

