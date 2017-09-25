---
layout: post
title: Callable vs Runnable - Runners间的“争论”
date: 2012-09-25 21:32 +0800
author: onecoder
comments: true
tags: [翻译]
thread_key: 1155
---
<p>
	看到一篇通过模拟Runnable和Callable对话的方式，形象的讲述Java中Runnable和Callable区别的文章，遂决定翻译过来加深印象与大家分享。</p>
<p>
	英文原文地址：<a href="http://java.dzone.com/articles/callable-vs-runnable-brawl">http://java.dzone.com/articles/callable-vs-runnable-brawl</a></p>

<strong>Runnable: </strong>我是多线程里的Yoda大师。(OneCoder注：I am the Yoda of multithreading.&nbsp;)。一段时间以来，我是Java中开发并行程序的唯一手段。（不算lang.Thread）记得我拥有的酷酷的方法run吧。不幸的是，他没有返回值。

<strong>Callable:</strong> 我一个Runnable, 更好更酷一点。我有一个令人惊叹的方法，叫做call。它能返回我工作的结果。call方法的返回类型是泛型的并且返回结果可以通过Future取到。现在，我已经超越了你，Runnable。

<strong>Runnable：</strong>好吧好吧。不过，事实上是，你的存在仅仅是为了填补我设计上的空白而已。比方说，我的run方法不会抛出Exception异常，如果你的任务想要抛出一个异常的话，你仅仅可以抛出Runtime异常。

<strong>Callable：</strong>我同意。我确实是站在你的肩膀上。毫无疑问，call方法抛出一个Exception异常，使得一个任务抛出一个校验过的异常给调用者。

Runnable API：

```java
void    run() d
```

Callable API:

```java
V     call() throws Exception
```


差异中的统一

FutureTask是一个有意思的类，它的构造函数既可以接受Runnable也可以接受Callable。因为FutureTask实现了Runnable接口，它可以确保的通过Exexutor.execute方法调用。要记住，Executor.executer方法仅仅接受Runnable类型的参数。我仍然需要特别的指出为什么某些人本想以为executer方法没有返回值不能返回结果。

厚脸皮从Javadoc中拷贝如下：

```java
Executor executor= &hellip;

FutureTask<String> future =

   new FutureTask<String>(new Callable<String>() {
     public String call() {
       &hellip; do your thing&hellip;

    }});

executor.execute(future);
```

