---
layout: post
title: 选择排序 - Java实现
date: 2012-05-30 23:00 +0800
author: onecoder
comments: true
tags: [Java, 排序, 算法]
categories: [算法学习]
thread_key: 184
---
```java
/**
 * "选择排序"，《算法导论》习题2.2-2 
 * Consider sorting n numbers stored in array A by first
 * finding the smallest element of A and exchanging it with the element in A[1].
 * Then find the second smallest element of A, and exchange it with A[2].
 * Continue in this manner for the first n - 1 elements of A. Write pseudocode
 * for this algorithm, which is known as selection sort . What loop invariant
 * does this algorithm maintain? Why does it need to run for only the first n -
 * 1 elements, rather than for all n elements? Give the best-case and worst-
 * case running times of selection sort in θ- notation. 
 * 伪代码：
 * 	for i <- 1 to length[A]-1
 * 		key <- A[i]
 * 		index <- i
 * 		for j <- 2 to length[A]
 * 			key = key < A[j] ? key : A[j];
			index = key < A[j] ? index : j;
 * 		A[index] = A[i];
		A[i] = key;	
 * @author lihzh(OneCoder)
 * @OneCoder-Blog http://www.coderli.com
 */
public class SelectionSort {
	
	private static int[] input = new int[] { 2, 1, 5, 4, 9, 8, 6, 7, 10, 3 };

	public static void main(String[] args) {
		for (int i=0; i<input.length-1; i++) {//复杂度：n
			int key = input[i];
			int index = i;
			//比较当前值和下一个值的关系，记录下较小值的值和索引数，用于交换。
			for (int j=i+1; j<input.length; j++) {//复杂度：1+2+...+(n-1)=θ(n^2)
				key = key < input[j] ? key : input[j];
				index = key < input[j] ? index : j;
			}
			input[index] = input[i];
			input[i] = key;
		}
		/*
		 * 复杂度分析：
		 * 最坏情况下，复杂度为：n*n=n^2(若略微精确的计算即为：n-1+1+2+...+n-1=(2+n)*(n-1)/2,
		 * 所以复杂度仍为n^2。
		 * 最优情况下，由于不论原数组是否排序好，均需要全部遍历以确定当前的最小值，所以复杂度不变仍未n^2。
		 * 
		 */
		//打印数组
		printArray();
	}
	
	private static void printArray() {
		for (int i : input) {
			System.out.print(i + " ");
		}
	}

}

```
