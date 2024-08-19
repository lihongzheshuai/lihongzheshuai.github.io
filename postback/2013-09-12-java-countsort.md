---
layout: post
title: 计数排序Java实现
date: 2013-09-12 12:46 +0800
author: onecoder
comments: true
tags: [Java]
thread_key: 1493
---
计数排序&mdash;&mdash;线性排序算法《算法导论》8.2

```java
package com.coderli.algorithm.arrayandsort;

/**
 * 《算法导论》8.2 计数排序 线性排序算法<br>
 * 
 * <pre>
 * 计数排序假设<b>n个输入元素的每一个都是介于0到k之间的整数。</b>
 * k为某个整数，k = O(n)时。技术排序的运行事件为&Theta;(n)
 * 
 * 
 * @author OneCoder
 * @date 2013年9月11日 下午8:15:00
 * @website http://www.coderli.com
 */
public class CountSort {

	private static int[] sortArray = new int[] { 2, 5, 3, 0, 2, 3, 0, 3, 4, 1};
	private static int k = 6;

	public static void main(String[] args) {
		int[] countArray = new int[k];
		int[] outArray = new int[sortArray.length];
		// 给元数组中的数字计数
		for (int i = 0; i < sortArray.length; i++) {
			countArray[sortArray[i]] = countArray[sortArray[i]] + 1;
		}
		// 计算元素位置
		for (int j = 1; j < k; j++) {
			countArray[j] = countArray[j] + countArray[j - 1];
		}
		// 排序到输出数组
		for (int h = sortArray.length - 1; h >= 0; h--) {
			outArray[countArray[sortArray[h]] - 1] = sortArray[h];
			countArray[sortArray[h]] = countArray[sortArray[h]] - 1;
		}
		// 打印结果
		for (int n : outArray) {
			System.out.print(n + &quot; &quot;);
		}
	}
}

```

