---
layout: post
title: Java小故事 我许你一个未来 Future
date: 2012-07-26 21:41 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究,JDK]
thread_key: 999
---
还是梳理代码，频频到**Future**这个字眼，很自然的让我想到了未来。

还是那对男孩和女孩，女孩问男孩，你会娶我吗？男孩说，一定会，等我为你盖好一栋美丽的房子……

```java
/**
 * Java小故事 我许你一个未来 Future
 * <p>
 * 还是那对男孩和女孩，女孩问男孩，你会娶我吗？<br>
 * 男孩说，一定会，等我为你盖好一栋美丽的房子……
 * 
 * @author lihzh
 * @alia OneCoder
 * @Blog http://www.coderli.com
 * @date 2012-7-26 下午8:44:58
 */
public class PromiseUAFuture {

	/**
	 * @author lihzh
	 * @throws ExecutionException
	 * @throws InterruptedException
	 * @alia OneCoder
	 * @date 2012-7-26 下午8:44:58
	 */
	public static void main(String[] args) throws InterruptedException, ExecutionException {
		// 我许你一个未来
		Future<BeautifulHouse> future = Executors.newSingleThreadExecutor().submit(new Boy());
		while (!future.isDone()) {
			System.out.println("Sorry baby, the house is not ok.");
		}
		System.out.println(future.get());
	}

	public static class Boy implements Callable<BeautifulHouse> {
		@Override
		public BeautifulHouse call() throws Exception {
			Thread.sleep(5000);
			return new BeautifulHouse();
		}

	}

	public static class BeautifulHouse {
		@Override
		public String toString() {
			return "This is a beautiful house.";
		}
	}
}
```