---
layout: post
title: Java小故事 不舍得叫醒女孩的男孩 观察者模式
date: 2012-07-25 20:56 +0800
author: onecoder
comments: true
tags: [Java]
thread_key: 994
---
今天在梳理项目里一些老的代码逻辑和结构的时候，发现了一段观察者的代码。脑海里同时浮现出这样一个故事……

> 有一个女孩和一个男孩，他们在山里迷路了。晚上，他们都精疲力尽。男孩对女孩说，你睡会吧，我看着，有动静我叫你，然而……

```java
/**
 * Java小故事，不舍得叫醒女孩的男孩
 * <p>
 * 有一个女孩和一个男孩，他们在山里迷路了。<br>
 * 晚上，他们都精疲力尽。男孩对女孩说，你睡会吧，我看着，有动静我叫你。<br>
 * 然而……
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class ObserverBoyAndGirlMain {

	/**
	 * @author lihzh
	 * @alia OneCoder
	 */
	public static void main(String[] args) {
		Boy boy = new Boy();
		Girl girl = new Girl();
		// 让女孩监听男孩的消息
		boy.addObserver(girl);
		try {
			// 然而，八个小时过去了，男孩的腿虽然已经被压得麻木了。
			Thread.sleep(8 * 60 * 60 * 1000L);
			// 但是，你舍得叫醒她么？：）
			// boy.wakeupGirl();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	/**
	 * 男孩，观察周围的动静，有问题发出信号
	 * 
	 * @author lihzh
	 * @alia OneCoder
	 */
	public static class Boy extends Observable {
		/**
		 * 叫醒女孩
		 * 
		 * @author lihzh
		 * @alia OneCoder
		 */
		public void wakeupGirl() {
			setChanged();
			notifyObservers("");
		}
	}

	/**
	 * 女孩，睡着了，如果男孩叫她，则会醒来
	 * 
	 * @author lihzh
	 * @alia OneCoder
	 */
	public static class Girl implements Observer {
		@Override
		public void update(Observable o, Object arg) {
			System.out.println("Thank you, I'm up.");
		}
	}
}
```