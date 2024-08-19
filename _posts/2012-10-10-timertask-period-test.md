---
layout: post
title: Java Timer任务执行消耗事件大于执行周期问题验证
date: 2012-10-10 15:51 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究,JDK]
thread_key: 1170
---
<p>
	其实是一个不值得一提的小问题，不过既然验证了，就拿出来分享一下吧。</p>
<div>
	<a href="http://www.coderli.com">OneCoder</a>在要做一个周期性的任务，Timer即可实现，不过考虑到有可能在一个周期内，任务可能没有结束，不知道Timer的处理方式，是直接启动下一个，还是等待完成，还是可配置的。于是<a href="http://www.coderli.com">OneCoder</a>进行了一个简单的验证：</div>
	
```java
/**
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
public class TimerMain {

	/**
	 * JDK Timer类测试类。主要测试在一个Timer周期内，线程未结束时，timer的处理情况。
	 * 
	 * @param args
	 * @author lihzh
	 * @alia OneCoder
	 */
	public static void main(String[] args) {
		TimerTask timerTask = new TimerTask() {
			@Override
			public void run() {
				try {
					System.out.println(Thread.currentThread().getName());
					Thread.sleep(1000 * 5);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		};
		Timer timer = new Timer();
		
		timer.scheduleAtFixedRate(timerTask, 0, 1000);
	}
}
```

<p>
	结论也很简单，下一个任务会等待上一个任务执行完成再启动。也算合理。</p>