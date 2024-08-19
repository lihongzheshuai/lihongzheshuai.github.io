---
layout: post
title: 白话Java - 守护线程
date: 2012-06-25 22:47
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究,JDK]
thread_key: 686
---
关于"白话", 偶然想到的词。目的就是用简洁，明快的语言来告诉您，我所知道的一切。

Java中的线程分两类，用户线程和守护线程。

```java
Thread commonThread = new Thread("Common Thread");
```

这样就是**用户线程**。

```java
Thread daemonThread = new Thread("Daemon Thread");
daemonThread.setDaemon(true);
```

这样就是**守护线程**。

起了"守护"线程这么动听的名字，自然要起到"守护"的作用。就好比男人要守护妹子。守护线程的作用，按照网上的说法是：

> 守护线程则是用来服务用户线程的，如果没有其他用户线程在运行，那么就没有可服务对象，也就没有理由继续下去。

说白了就是妹子没了，男人也就自尽了。分情况写几个例子，一跑便知。

#### 1. 两个妹子 - 互不相干，你挂你的，我挂我的

```java
	/**
	 * 测试两个用户线程的情况
	 * 
	 * @author lihzh(OneCoder)
	 * @date 2012-6-25 下午10:07:16
	 */
	private static void twoCommonThread() {
		String girlOneName = "Girl One";
		Thread girlOne = new Thread(new MyRunner(3000, girlOneName), girlOneName);
		String girlTwoName = "Girl Two";
		Thread girlTwo = new Thread(new MyRunner(5000, girlTwoName), girlTwoName);
		girlOne.start();
		System.out.println(girlOneName + "is starting.");
		girlTwo.start();
		System.out.println(girlTwoName + "is starting");
	}

	private static class MyRunner implements Runnable {
		
		private long sleepPeriod;
		private String threadName;
		
		public MyRunner(long sleepPeriod, String threadName) {
			this.sleepPeriod = sleepPeriod;
			this.threadName = threadName;
		}
		@Override
		public void run() {
			try {
				Thread.sleep(sleepPeriod);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			System.out.println(threadName + " has finished.");
		}
	}
```

![](/images/post/daemon-thread/debug-all-live.png)

开始都活着。

![](/images/post/daemon-thread/debug-one-dead.png)

3秒后，妹子1挂了，妹子2活的好好的，她的寿命是5秒。<br />

#### 2. 一妹子一王子

```java
   /**
	 * 测试一个用户一个守护线程
	 * 
	 * @author lihzh(OneCoder)
	 * @date 2012-6-25 下午10:22:58
	 */
	private static void oneCommonOneDaemonThread() {
		String girlName = "Girl";
		Thread girl = new Thread(new MyRunner(3000, girlName), girlName);
		String princeName = "Prince";
		Thread prince = new Thread(new MyRunner(5000, princeName), princeName);
		girl.start();
		System.out.println(girlName + "is starting.");
		prince.setDaemon(true);
		prince.start();
		System.out.println(prince + "is starting");
	}
```
![](/images/post/daemon-thread/debug-girl-dead-boy.png)

开始快乐的生活着，妹子能活3秒，王子本来能活5秒

![](/images/post/daemon-thread/debug-boy-daemon-dead.png)

但是3秒后，妹子挂了，王子也殉情了。

你可能会问，如果王子活3秒，妹子能活5秒呢。我只能说，虽然你是王子，该挂也得挂，妹子还会找到其他高富帅的，懂？

![](/images/post/daemon-thread/debug-boy-dead-first.png)

看，王子已经挂了。

#### 3. 两个王子

```java
   /**
	 * 测试两个守护线程
	 * 
	 * @author lihzh(OneCoder)
	 * @date 2012-6-25 下午10:29:18
	 */
	private static void twoDaemonThread() {
		String princeOneName = "Prince One";
		Thread princeOne = new Thread(new MyRunner(5000, princeOneName), princeOneName);
		String princeTwoName = "Prince Two";
		Thread princeTwo = new Thread(new MyRunner(3000, princeTwoName), princeTwoName);
		princeOne.setDaemon(true);
		princeOne.start();
		System.out.println(princeOneName + "is starting.");
		princeTwo.setDaemon(true);
		princeTwo.start();
		System.out.println(princeTwoName + "is starting");
	}
```

![](/images/post/daemon-thread/debug-two-boy-dead.png)

我只能说，没有妹子，没有活着的理由，直接就都挂了。

现在，你懂守护线程了吗？