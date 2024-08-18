---
layout: post
title: Scala学习笔记-基础语法
tags: [Scala]
date: 2016-09-20 16:30:10 +0800
comments: true
author: onecoder
thread_key: 1899
---
上手学习Scala语言。先熟悉一下语法。对于Scala笔者也是完全的新手，对scala的设计思想和实现原理没有太多了解。错误在所难免，还望发现后不吝指教。

<!--break-->

# Hello World

基础环境配置直接利用IntelliJ提供的Scala插件，会自动下载Scala开发包并配置好开发环境。直接从我们熟悉的“Hello world”开始对Scala的认知过程。

```scala
/**
  * Scala 基础语法
  *
  * @author li.hzh
  * @date 2016-09-14 23:37
  */
object SyntaxBasis {
  def main(args: Array[String]): Unit = {
    println("Hello world");
  }
}
```

这里def main(args: Array[String]) 是一切scala程序的入口。

# 换行符

与Java相同，scala同样用分号;作为换行符，但不是必须的。一行只有一个语句的时候可以省略分号。不过笔者还是习惯都加上分号。如：
def main(args: Array[String]): Unit = {
  println("Hello world");
  println("不用写分号")
  println("必须写分号"); println("因为有这句。")
}

详情参考：[http://www.runoob.com/scala/scala-basic-syntax.html](http://www.runoob.com/scala/scala-basic-syntax.html)

# 数据类型

与Java有较大区别，没有Java中的基本数据类型，只有int等基本数据类型的包装类。一切皆对象。scala继承关系图

![](/images/post/scala-syntax/scala-extends.png)

其中Unit等同于Java中的void，所以我们的main函数代码里有个Unit的返回值。Nothing是一切对象的子类。Any是一切对象的基类。Null代表空值或者空引用。AnyRef是一切引用对象的超类。通过代码来理解一下。

```scala
package com.coderli.scala.lab

/**
  * Scala 数据类型
  *
  * @author li.hzh
  * @date 2016-09-20 11:21
  */
object DataType {

  def main(args: Array[String]) {
    val aInt: Int = 2147483647
    val aLong: Long = 9223372036854775807L;
    val aFloat: Float = 3.2F;
    val aDouble: Double = 3.2;
    val aString: String = "Single Line String";
    val mString: String =
      """Multiple Lines String
         Line One
         Line Two
         Line Three
      """;
    println("a Int : " + aInt);
    println("a Long: " + aLong);
    println("a Float: " + aFloat);
    println("a Double: " + aDouble);
    println("Single Line String: " + aString);
    println("Multiple Lines String: " + mString);
    // 因为一切皆对象,所以可以直接进行API调用
    println(aDouble.-(2));
    // 验证数据类型继承关系
    println(aDouble.isInstanceOf[Double]);
    println(aDouble.isInstanceOf[Any]);
    println(aString.isInstanceOf[AnyRef]);
    println(aString.isInstanceOf[String]);
  }

}
```

与Java的几个区别

- 变量声明类型在后，变量名在前，中间用冒号: 分隔，挺别扭。
- 字符串类型多了一个三引号，可直接写换行的字符串。
- 数据类型都是对象，可以直接调用封装的方法，与其他类型同等对待，不用再区分所谓的基本数据类型。
- 最后通过几个isInstanceOf函数，验证一下上面的继承关系图。

上述代码输出结果如下：

> a Int : 2147483647  
> a Long: 9223372036854775807  
> a Float: 3.2  
> a Double: 3.2  
> Single Line String: Single Line String  
> Multiple Lines String: Multiple Lines String  
>          Line One  
>          Line Two  
>          Line Three  
> 
> 1.2000000000000002  
> true  
> true  
> true  
> true  

详情参考：[http://www.runoob.com/scala/scala-data-types.html](http://www.runoob.com/scala/scala-data-types.html)

# 变量和常量

```scala
/**
  * 变量和常量
  *
  * @author li.hzh
  * @date 2016-09-20 13:56
  */
object ValAndVar {
  def main(args: Array[String]) {
    // 常量用val声明, 值不可修改。相当于final,此处省略了类型声明, 利用了Scala的类型推断
    val a = 1;
    var b = "String";
    b = "StringChange";
    println(b)
  }

}
```

如果省略类型声明，则必须在声明时给予初始化值，以进行类型推断。不能修改常量值，否则会编译错误。

详情参考：[http://www.runoob.com/scala/scala-variables.html](http://www.runoob.com/scala/scala-variables.html)

# 访问修饰符

scala里**private**和**protected**的作用域都比Java更严格，private修饰的成员，仅可以在类内访问，外部类亦不可以访问。protected修饰的成员，仅子类可访问，同包不可。

这里重点关注scala提供的作用域保护的特性。

```scala
package com.coderli.scala.lab

import com.coderli.scala.lab.access.Demo

/**
  * 访问修饰符
  *
  * @author li.hzh
  * @date 2016-09-20 14:29
  */
object AccessModifier {

  def main(args: Array[String]) {
    new Demo().printDemo();
  }

}

package access {

  private[lab] class Demo {

    def printDemo(): Unit = {
      println("Print Demo");
    }

  }

}
```

Demo类声明为，对除了lab包内的类以外的类均不可访问。因此可以在lab包里AccessModifier的main函数里访问。如果仅仅声明为private class Demo, 则会提示无法访问，编译错误。这个特性在项目中隔离内外部代码访问上很有用处。

访问作用域修饰可使用private和protected。（效果相同？）
详情参考：[http://www.runoob.com/scala/scala-access-modifiers.html](http://www.runoob.com/scala/scala-access-modifiers.html)

运算符和条件控制语句与Java基本相同，略。
详情参考：
[http://www.runoob.com/scala/scala-operators.html](http://www.runoob.com/scala/scala-operators.html)
[http://www.runoob.com/scala/scala-if-else.html](http://www.runoob.com/scala/scala-if-else.html)

# 循环

scala里for循环的写法和特性上有比较明显的变化

```scala
/**
  * @author li.hzh
  * @date 2016-09-20 14:53
  */
object Loop {

  def main(args: Array[String]) {
    var i = 0;
    for (i <- 1 to 10) {
      println("Value of i: " + i);
    }
    var j = 0;
    for (i <- 1 to 3; j <- 1 until 3) {
      println("Value of i: " + i);
      println("Value of j: " + j);
    }

    val evenResult = for (i <- 1 to 10 if i % 2 == 0
    ) yield i;
    println(evenResult)
    for (i <- evenResult) {
      println(i)
    }
  }
}
```

第一个就是普通的for循环输出从1-10 的数字

> Value of i: 1  
> Value of i: 2  
> Value of i: 3  
> Value of i: 4  
> Value of i: 5  
> Value of i: 6  
> Value of i: 7  
> Value of i: 8  
> Value of i: 9  
> Value of i: 10  

第二个实际相当于Java中的二层循环。输出所有可能的组合结果，有个细微的区别，对于变量j，使用了**until**代替**to**，所以j的取值范围不包括3。

> Value of i: 1  
> Value of j: 1  
> Value of i: 1  
> Value of j: 2  
> Value of i: 2  
> Value of j: 1  
> Value of i: 2  
> Value of j: 2  
> Value of i: 3  
> Value of j: 1  
> Value of i: 3  
> Value of j: 2  

第三个循环是Java没有的特性，yield，对于满足if条件的变量保存起来，存入返回值的数组。因此输出为：

> 2  
> 4  
> 6  
> 8  
> 10  

函数部分是scala的核心，包含的特性较多，scala号称多范式语言支持函数式编程，，笔者准备在下篇文章里单独介绍。