---
layout: post
title: Java面试题 实现单例模式
date: 2014-08-12 15:22 +0800
author: onecoder
comments: true
tags: [Java]
thread_key: 1793
---
<p>
	好久没有更新博客了，<a href="http://www.coderli.com">OneCoder</a>没挂，只是儿子出生，忙了一个多月。生活节奏有点小乱。这期间也抽空换了份工作，坚持技术路线不动摇。So，抓紧调整一下状态，继续读书，写码。</p>
<p>
	面试题系列，是<a href="http://www.coderli.com">OneCoder</a>早就打算学习的方向。为以后打基础，主要是学习《剑指Offer》和《编程之美》这两本书。iOS的单排第二季也会在近期开始，效仿马克思的学习方式，撸累了iOS的时候，做两道题，调剂一下。</p>
<p>
	不过，这次是从面试题先开始的，因为恰好<a href="http://www.coderli.com">OneCoder</a>之前在准备面试的时候，看到了这个问题。早就想总结一下，分享给大家。结果一直拖到现在。</p>
<p>
	进入正题，Singleton模式是什么，这里不解释，直接上代码。这里分享了5种写法，并附上了评论。有好有坏，大家自行理解。</p>
<br />

```java
package com.coderli.interview;

/**
* 常见面试题：实现单例模式 <br>
* 《剑指offer》，第二章，面试题2 <br>
* 这里给出五种写法和对应的评论
*
* @author lihzh
* @date 2014年8月12日 上午11:10:13
*/
public class Singleton {
      /**
      * 写法一 <br>
      * 最直接的初级写法，忽略了对多线程并发的考虑。 <br>
      * 不推荐
      *
      * @author OneCoder
      * @blog http://www.coderli.com
      * @date 2014年8月12日 上午11:46:58
      */
      static class SingletonOne {

           // 私有化构造函数是必须的
           private SingletonOne() {
          }
           static SingletonOne instance = null;

           static SingletonOne getInstance() {
               if ( instance == null) {
                    instance = new SingletonOne();
              }
               return instance;
          }
     }
      /**
      * 写法二 <br>
      * 考虑到多线程并发的情况，加锁控制。 <br>
      * 功能正确，但是效率不高，每次获取实例都需要先获取锁。 <br>
      * 不推荐
      *
      * @author OneCoder
      * @blog http://www.coderli.com
      * @date 2014年8月12日 下午12:01:59
      */
      static class SingletonTwo {

           // 私有化构造函数是必须的
           private SingletonTwo() {
          }
           static SingletonTwo instance = null;

           static synchronized SingletonTwo getInstance() {
               if ( instance == null) {
                    instance = new SingletonTwo();
              }
               return instance;
          }
     }
      /**
      * 写法三 <br>
      * 考虑到多线程并发的情况，加锁控制。 <br>
      * 同时考虑到效率问题，进行二次判断，只在需要创建新实例的时候加锁。获取的时候无锁 <br>
      * 勉强过关
      *
      *
      * @author OneCoder
      * @blog http://www.coderli.com
      * @date 2014年8月12日 下午12:01:59
      */
      static class SingletonThree {

           // 私有化构造函数是必须的
           private SingletonThree() {
          }
           static SingletonThree instance = null;
           static byte[] lock = new byte[0];

           static SingletonThree getInstance() {
               if ( instance == null) {
                    synchronized ( lock) {
                         if ( instance == null) {
                              instance = new SingletonThree();
                        }
                   }
              }
               return instance;
          }
     }
      /**
      * 写法四 <br>
      * 考虑到多线程并发的情况，利用Java执行原理，静态方法执行一次 <br>
      * 无锁，效率高 <br>
      * 缺点：无论使用与否，都预先初始化完成。浪费资源。 <br>
      * 推荐写法的一种
      *
      *
      * @author OneCoder
      * @blog http://www.coderli.com
      * @date 2014年8月12日 下午12:01:59
      */
      static class SingletonFour {

           // 私有化构造函数是必须的
           private SingletonFour() {
          }
           static SingletonFour instance = new SingletonFour();

           static SingletonFour getInstance() {
               return instance;
          }
     }
    
      /**
      * 写法四 <br>
      * 考虑到多线程并发的情况，通过内部类实现按序初始化，且无锁 <br>
      * 最推荐的写法
      *
      *
      * @author OneCoder
      * @blog http://www.coderli.com
      * @date 2014年8月12日 下午12:01:59
      */
      static class SingletonFive {
         
           static class Inner {
               static SingletonFive new_instance = new SingletonFive();
          }
           // 私有化构造函数是必须的
           private SingletonFive() {
          }

           static SingletonFive getInstance() {
               return Inner. new_instance;
          }
     }

}
```