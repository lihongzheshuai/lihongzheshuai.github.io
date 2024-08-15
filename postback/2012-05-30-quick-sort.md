---
layout: post
title: 快速排序 - Java实现
date: 2012-05-30 21:47 +0800
author: onecoder
comments: true
tags: [Java, 排序, 快速排序, 算法导论]
thread_key: 173
---
```java
/**
 * 快速排序，《算法导论》第七章
 * @author lihzh(OneCoder)
 * @OneCoder-Blog http://www.coderli.com
 */
public class QuickSort {
	
	//待排数组
	private static int[] input = new int[] { 2, 1, 5, 4, 9, 8, 6, 7, 10, 3 };

	public static void main(String[] args) {
		//快速排序
		quickSort(input, 0, input.length - 1);
		//打印数组
		printArray();
	}
	
	/**
	 * 快速排序，伪代码：
	 * QUICKSORT(A, p, r)
	 * 1 if p < r
	 * 2 	then q → PARTITION(A, p, r)
	 * 3 		QUICKSORT(A, p, q - 1)
	 * 4 		QUICKSORT(A, q + 1, r)
	 * 
	 * PARTITION(A, p, r)
	 * 1 x → A[r]
	 * 2 i → p - 1
	 * 3 for j → p to r - 1
	 * 4 	do if A[j] <= x
	 * 5 		then i → i + 1
	 * 6 			exchange A[i] ⟷ A[j]
	 * 7 exchange A[i + 1] ⟷ A[r]
	 * 8 return i + 1
	 * 复杂度，最坏情况下：θ(n^2)
	 * 一般平衡情况：θ(nlgn)
	 * @param array 待排数组
	 * @param from 起始位置
	 * @param to 终止位置
	 */
	private static void quickSort(int[] array, int from, int to) {
		if (from < to) {
			int temp = array[to];
			int i = from - 1;
			for (int j = from; j < to; j++) {
				if (array[j] <= temp) {
					i++;
					int tempValue = array[j];
					array[j] = array[i];
					array[i] = tempValue;
				}
			}
			array[to] = array[i+1];
			array[i+1] = temp;
			quickSort(array, from, i);
			quickSort(array, i + 1, to);
		}
	}

	private static void printArray() {
		for (int i : input) {
			System.out.print(i + &quot; &quot;);
		}
	}
}
```

