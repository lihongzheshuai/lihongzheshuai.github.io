---
layout: post
title: "LeetCode[Algorithms] Median of Two Sorted Arrays"
modified:
excerpt: LeetCode [Median of Two Sorted Arrays] by OneCoder
tags: [算法,LeetCode]
categories: [算法学习]
thread_key: 1868
date: 2015-09-22T11:54:45
---
There are two sorted arrays nums1 and nums2 of size m and n respectively. Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

{% highlight java %}
package com.coderli.leetcode.algorithms;

/**
 * There are two sorted arrays nums1 and nums2 of size m and n respectively.<br />
 * Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
 *
 * @author li.hzh
 * @date 2015/9/6 10:42
 */
public class MedianOfTwoSortedArrays {

   public static void main(String[] args) {
      Solution solution = new MedianOfTwoSortedArrays().new Solution();
      int[] arrayOne = new int[]{1};
      int[] arrayTwo = new int[]{};
      System.out.println(solution.findMedianSortedArrays(arrayOne, arrayTwo));
   }


   public class Solution {

      public double findMedianSortedArrays(int[] nums1, int[] nums2) {
         int lengthOne = nums1.length;
         int lengthTwo = nums2.length;
         int totalLength = lengthOne + lengthTwo;
         int mid = totalLength / 2;
         if (totalLength % 2 == 1) {
            return findKth(nums1, nums2, mid, 0, lengthOne - 1, 0, lengthTwo -1);
         } else {
            double one = findKth(nums1, nums2, mid, 0, lengthOne - 1, 0, lengthTwo -1);
            double two = findKth(nums1, nums2, mid - 1, 0, lengthOne - 1, 0, lengthTwo -1);
            return (one + two) / 2;
         }
      }

      private int findKth(int A[], int B[], int k,
                     int aStart, int aEnd, int bStart, int bEnd) {

         int aLen = aEnd - aStart + 1;
         int bLen = bEnd - bStart + 1;

         if (aLen == 0)
            return B[bStart + k];
         if (bLen == 0)
            return A[aStart + k];
         if (k == 0)
            return A[aStart] < B[bStart] ? A[aStart] : B[bStart];

         int aMid = aLen * k / (aLen + bLen);
         int bMid = k - aMid - 1;

         aMid = aMid + aStart;
         bMid = bMid + bStart;

         if (A[aMid] > B[bMid]) {
            k = k - (bMid - bStart + 1);
            aEnd = aMid;
            bStart = bMid + 1;
         } else {
            k = k - (aMid - aStart + 1);
            bEnd = bMid;
            aStart = aMid + 1;
         }

         return findKth(A, B, k, aStart, aEnd, bStart, bEnd);
      }
   }
}
{% endhighlight %}

参考：[http://www.programcreek.com/2012/12/leetcode-median-of-two-sorted-arrays-java/](http://www.programcreek.com/2012/12/leetcode-median-of-two-sorted-arrays-java/)
