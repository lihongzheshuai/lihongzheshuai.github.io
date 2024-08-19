---
layout: post
title: 插入排序 - Java实现
date: 2012-05-30 22:40 +0800
author: onecoder
comments: true
tags: [Java, Java 排序, 算法导论]
thread_key: 181
---
```java
/**
 *  "插入排序 "，对少量元素进行排序的有效算法。
 *  《算法导论》原文摘要：
 * Insertion sort works the way many people sort a hand
 * of playing cards. We start with an empty left hand and the cards face down on
 * the table. We then remove one card at a time from the table and insert it
 * into the correct position in the left hand. To find the correct position for
 * a card, we compare it with each of the cards already in the hand, from right
 * to left, as illustrated in Figure 2.1. At all times, the cards held in the
 * left hand are sorted, and these cards were originally the top cards of the
 * pile on the table. 
 * 伪代码如下： 
 * for j<- 2 to length[A] 
 * 	do key <- A[j] 
 * 		>Insert A[j] into the sorted sequence A[1..j-1] （>符号代表后面的部分是注释）
 * 		i <- j-1 
 * 		while i>0 and A[i]>key 
 * 			do A[i+1] <- A[i] 
 * 			i <- i-1 
 * 		A[i+1] <- key 
 * 算法复杂度：n^2
 * @author lihzh(OneCoder)
 * @OneCoder-Blog http://www.coderli.com
 */
public class InsertionSort {

	private static int[] input = new int[] { 2, 1, 5, 4, 9, 8, 6, 7, 10, 3 };

	public static void main(String[] args) {
		//从数组第二个元素开始排序，因为第一个元素本身肯定是已经排好序的
		for (int j = 1; j < input.length; j++) {// 复杂度 n
			int key = input[j];
			int i = j - 1;
			//依次跟之前的元素进行比较，如果发现比前面的原素小，则交换位置，最终完成排序。
			while (i >= 0 && input[i] > key) {//复杂度：1+2+...+(n-1)=&Theta;(n^2)
				input[i + 1] = input[i];
				input[i] = key;
				i--;
			}
		}
		/*
		 * 所以最终复杂度为n*n=n^2。最优情况下（即都已经排列好的情况下），第二个n=1， 所以在最优情况下，复杂度为n。
		 */
		// 打印数组
		printArray();
	}

	private static void printArray() {
		for (int i : input) {
			System.out.print(i + " ");
		}
	}
}
```

