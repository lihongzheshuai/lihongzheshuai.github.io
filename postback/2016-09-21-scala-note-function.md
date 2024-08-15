---
layout: post
title: Scala学习笔记 - 函数
tags: [Scala]
date: 2016-09-21 16:36:32 +0800
comments: true
author: onecoder
thread_key: 1900
---
Scala做为支持函数式编程的语言，函数自然是其核心的特性，因此笔者对函数部分的学习自然会更加认真细致一些。但也仅仅是基础部分。

<!--break-->

# 函数基础

先看一段代码：

```scala
package com.coderli.scala.lab

class FuntionDemo {
  /**
    * 函数声明
    *
    * @param a
    * @param b
    * @return
    */

def sum(a: Int, b: Int): Int = {
  return Function.singleSum(a, b);
}
}

/**
  * @author li.hzh
  * @date 2016-09-20 16:54
  */
object Function {

  def main(args: Array[String]) {
    // 单例函数调用
    singleInstance();
    // 函数实例方式调用
    println("求和: " + new FuntionDemo().sum(1, 2));
    // 伴生函数
    println("伴生求和: " + new Function().sum(2, 3));
  }

  def singleInstance(): Unit = {
    println("单例函数。")
  }

  private def singleSum(a: Int, b: Int): Int = {
    return a + b;
  }
}

class Function {
  val c = 100;

  // 直接调用伴生函数,私有成员亦可访问
  def sum(a: Int, b: Int): Int = {
    return Function.singleSum(a, b);
  }
}
```

这段代码包含关于scala函数若干知识点。

## 函数声明和调用

跟Java一样，函数都需要有参数和返回值。遵循scala一贯的语法，类型在后，变量在前，之间用冒号分割。
以def sum(a: Int, b: Int): Int = {} 函数为例。
sum是函数名，a,b是两个Int型的参数。最后的:Int是返回值。然后就是一个奇怪的等号=（我总是忘记），大括号里是方法体。

## 单例、伴生对象

scala中没有static关键字，网上说这更面相对象（不是很能反应过来）。于是，scala里的单例的实现方式就是通过object关键字声明一个“类”，这个类里定义的方法，都是可以直接调用（或者说通过类名调用）的。例如类FuntionDemo里的sum方法调用object Function里的sum函数。

传统的通过类的实例调用函数跟Java没太大区别，这里不再赘述。

伴生对象（Companion Object）是scala里的新概念，即与类名(class)相同的object声明。即上述代码里的object Function和class Function。class Function即我们传统的类，而前面刚刚介绍过，scala通过object的方式实现单例。所以，我理解通过伴生对象把单例方法和普通类方法分开编写，是代码节奏。从scala语法层面，二者内部的私有变量都是可以互相访问的，从字节码实现层面，scala把二者融合在一起。文章http://dreamhead.blogbus.com/logs/60217908.html有较为详细的分析。必须承认的是，由于初学scala，笔者对此特性还只是有肤浅的了解，随着使用的深入，希望可以加深理解。

# 函数参数和高阶函数

继续说scala函数，scala作为支持函数式编程的语言，自然支持将函数作为参数传递，并可控在任意时刻求值。例如：

```scala
def printTime(a: Long, t: => Long): Unit = {
  println("Out time value: " + a);
  Thread.sleep(2000L);
  println("Out time value: " + a);
  println("Inner time value: " + t);
}

def time(): Long = {
  println("获取时间")
  return System.nanoTime();
}
```

调用

```scala
printTime(time(), time());
```

函数printTime里，第二个参数t就是接受一个返回值为Long类型的函数作为参数，函数参数t可以在printTime方法体内任意时刻被调用。上述代码输出结果为：

> 获取时间  
Out time value: 5111365327821  
Out time value: 5111365327821  
获取时间  
Inner time value: 5113371789992  
> 

可见，第二个time是在方法体内调用时求值的，这也是函数式编程的一大重要特性。而printTime这个使用其他函数的函数，我理解就是scala里的高阶函数。（如果我理解错了，请告诉我。）

# 指定参数名调用

scala支持在函数调用时，指定参数名传值，而不是必须严格按照函数参数定义顺序传值，例如：

```scala
def paramOrder(a: Int, b: Int): Unit = {
  println("a: " + a);
  println("b: " + b);
}
```

调用：

```
paramOrder(1, 2);
paramOrder(b = 1, a = 2);
```

两次调用，分别输出：

> 
a: 1  
b: 2  
a: 2  
b: 1  
> 

# 可变长参数

可变长参数在Java里也有支持，语法是参数名后加... ，在Scala里变成了*，本质是一样的，可变参数都转换为数组操作。例如：

```scala
def varArgs(strs: String*): Unit = {
  for (a: String <- strs) {
    println(a);
  }
}
```

调用

```scala
varArgs("One", "Two", "Three");
```

输出

> 
One  
Two  
Three
> 

# 默认参数值

scala支持在函数定义时，给函数默认参数分配默认值，当调用者未显示个参数赋值时，使用定义时的默认值。例如：

```scala
def defaultValueParam(a: Int = 5, b: Int = 7): Unit = {
  println("a: " + a);
  println("b: " + b);
}
```

调用者

```scala
defaultValueParam(3);
defaultValueParam(b = 3);
```

输出：

> 
a: 3  
b: 7  
a: 5  
b: 3  
> 

# 内嵌函数

scala支持在函数中定义函数。即局部函数

```scala
def innerFunction(a: Int): Int = {
  def inner(i: Int, result: Int): Int = {
    if (i == 1) {
      return result;
    } else {
      return inner(i - 1, result * i)
    }
  }
  return inner(a, 1);
}
```

调用

```scala
println("阶乘: " + innerFunction(3));
```

# 匿名函数

匿名函数可以大幅简化代码，把函数定义赋值给变量，随意传递。为函数式编程服务。匿名函数语法很简单符号=>左边是参数，右边是方法体。例如：

```scala
val fun1 = (x: Int) => 2 + x;
println("调用匿名函数: " + fun1(4));
```

必须承认是，由于没有实战经验，笔者目前对匿名函数的理解还仅仅停留在语法层面。离灵活使用感觉都还有记录，姑且先了解有这个特性，至少能读懂别人的代码再说吧。

# 偏应用函数

没有去查这个翻译的英文原文是什么，姑且就这么用吧。看一段代码：

```scala
val date = new Date;
val dateLog = log(date, _: String);
dateLog("Msg One");
dateLog("Msg Two");

def log(date: Date, msg: String) = {
  println(date + "---" + msg + "---.");
}
```

输出：

> 
Wed Sep 21 16:03:35 CST 2016---Msg One---.  
Wed Sep 21 16:03:35 CST 2016---Msg Two---.
> 

上述代码含义是，对于log函数里的日期类型，因为我们在调用的时候需要传入同一个值，为了避免繁琐，又定义了一个dateLog偏应用函数，给date赋予相同的值，对于变化的日志信息参数，用_保留。然后调用dateLog函数传入信息即可。

# 函数柯里化（Currying）

柯里化(Currying)指的是将原来接受两个参数的函数变成新的接受一个参数的函数的过程。新的函数返回一个以原有第二个参数为参数的函数。看一段代码吧：

之间我们定义的函数：

```scala
def singleSum(a: Int, b: Int): Int = {
  return a + b;
}
```

柯里化后变成

```scala
def singleSum(a: Int)(b: Int): Int = {
  return a + b;
}
```

调用方式变成

```scala
println(singleSumCurrying(1)(2))
val sumOne = singleSumCurrying(1)(_);
println(sumOne)
val result = sumOne(2);
println(result)
```

实际上是将对两个参数的函数的一次调用变成对两个一个参数函数的两次调用。具体解释可参见：[http://www.runoob.com/scala/currying-functions.html](http://www.runoob.com/scala/currying-functions.html)

至于为什么要函数柯里化，这个笔者看了一篇文章：[https://gist.github.com/jcouyang/b56a830cd55bd230049f](https://gist.github.com/jcouyang/b56a830cd55bd230049f) 。看的时候角儿将的挺好，但是过后就忘了，没有实战，理解太浅。

很多概念，在实战中才能加深理解，比如函数式编程的思想，看一遍理解一遍，理解一遍忘一遍。多写写也许就好了。

其实在写这篇笔记的时候，我已经将scala的基础语法看完了。剩下的部分不再整理详细的笔记了，因为大多是一些相同概念下语法上的区别。并且，笔者理解太浅，实在也讲不出什么值得分享的东西，也就不浪费自己的时间了。下一步在应用中提高自己。

scala基础语法具体可见：[http://www.runoob.com/scala/scala-tutorial.html](http://www.runoob.com/scala/scala-tutorial.html)