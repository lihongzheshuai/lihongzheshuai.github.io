---
layout: post
title: 利用堆合并数组- Java实现
date: 2012-05-30 22:07 +0800
author: onecoder
comments: true
tags: [Java, 排序, 算法]
categories: [算法学习]
thread_key: 178
---
```java
/**
 * 《算法导论》习题6.5-8: Give an θ(nlgk)-time algorithm to merge k sorted lists into
 * one sorted list, where n is the total number of elements in all the input
 * lists. (Hint: Use a min-heap for k-way merging.) 
 * @author lihzh(OneCoder)
 * @OneCoder-Blog http://www.coderli.com
 */
public class Exercice658 {

	// 给定3（k=3）个已排好序的数组，这里考虑简单情况，
	// 即所有数组包含的元素个数一致。
	// 注：因为已实现MaxHeapify算法，所以此处用最大到小排好序的数组举例
	private static int[] arrayOne = new int[] { 7, 4, 3, 1 };
	private static int[] arrayTwo = new int[] { 10, 9, 5, 2 };
	private static int[] arrayThree = new int[] { 12, 11, 8, 6 };
	
	// 已排好序中的数组中，元素的个数
	private static int length = arrayOne.length;
	// 已排好序的数组的个数
	private static int k = 3;
	// 所有数组中元素的总个数
	private static int n = length * k;
	// 合并后输出数组
	private static int[] output = new int[n];
	
	public static void main(String[] args) {
		mergeSortedArrays();
		// 打印数组
		printArray();
	}

	/**
	 * 合并已排序的数组，利用<code>;PriorityQueue</code>;中 的insert和extractMax算法实现
	 * 复杂度分析：
	 * 根据当前实现，复杂度应该为：θ(nk)，并不满足题意。
	 * 但是所用思路，与习题参考中的思路一致，参考原文如下：
	 * Given k sorted lists with a total of n elements show how to merge them in O(n lg k) time. Insert
	 * all k elements a position 1 from each list into a heap. Use EXTRACT-MAX to obtain the rst element
	 * of the merged list. Insert element at position 2 from the list where the largest element originally
	 * came from into the heap. Continuing in this fashion yields the desired algorithm. Clearly the
	 * running time is θ(n lg k).
	 * 差异之处在于，当从堆中取出一个元素之后，需要知道这个元素原来所属数组，这里也需要去判断，这里耗时K。另外，在插入的时候，
	 * 也需要判断
	 */
	private static void mergeSortedArrays() {
		
		// 利用前面实现的优先级队列中的方法，构造一个容量为k=3的堆
		PriorityQueue priQueue = new PriorityQueue(k);
		int count = 0;
		//用于保存各数组当前插入元素索引位的数组
		int[] indexArray = new int[k];
		int arrayChoice = 0;
		//初始情况，向堆中插入各数组首位元素
		//复杂度：θ(klgk)
		priQueue.insert(arrayOne[0]);
		priQueue.insert(arrayTwo[0]);
		priQueue.insert(arrayThree[0]);
		for (int i = 0; i < n; i++) {// 该循环复杂度：θ(n)
			// 取出当前最大值，复杂度θ(lgk)
			int value = priQueue.extractMax();
			count++;
			// 赋值
			output[n-count] = value;
			// 判断当前取出的最大元素所在数组，硬编码：(疑惑：复杂度θ(k),因为最差会进行k次比较，此处如何优化)
			if (value == arrayOne[indexArray[0]]) {
				arrayChoice = 0;
			} else if (value == arrayTwo[indexArray[1]]) {
				arrayChoice = 1;
			} else {
				arrayChoice = 2;
			}
			// 相应的索引位+1
			indexArray[arrayChoice]++;
			// 向堆中插入元素,如果备选数组中还有元素，则继续从该数组选取(疑惑：采用switch语句，复杂度是否降到θ(lgk)以下)
			// 根据:http://hi.baidu.com/software_one/blog/item/254990dfd96aee205982ddcb.html 中介绍，似乎可以。
			// 望高手指导！
			switch (arrayChoice) {
			case 0 :
				if (indexArray[0] < length) {
					priQueue.insert(arrayOne[indexArray[0]]);
				}
				break;
			case 1 :
				if (indexArray[1] < length) {
					priQueue.insert(arrayTwo[indexArray[1]]);
				}
				break;
			case 2 :
				if (indexArray[2] < length) {
					priQueue.insert(arrayThree[indexArray[2]]);
				} 
				break;
			}
		}
	}

	private static void printArray() {
		for (int i : output) {
			System.out.print(i + " ");
		}
	}
}
```

