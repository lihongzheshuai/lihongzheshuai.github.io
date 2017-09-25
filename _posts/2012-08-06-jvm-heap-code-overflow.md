---
layout: post
title: JVM运行时数据区详解-Heap堆(优化配置、代码样例)
date: 2012-08-06 12:19 +0800
author: onecoder
comments: true
tags: [JVM]
thread_key: 1043
---
在Java虚拟机中，堆（**Heap**）是可供各条线程共享的运行时内存区域，也是供所有类实例和数组对象分配内存的区域。

**Java**堆在虚拟机启动的时候就被创建，它存储了被自动内存管理系统（**Automatic Storage Management System**，也即是常说的"**Garbage Collector**（垃圾收集器）"）所管理的各种对象，这些受管理的对象无需，也无法显式地被销毁。本规范中所描述的Java虚拟机并未假设采用什么具体的技术去实现自动内存管理系统。虚拟机实现者可以根据系统的实际需要来选择自动内存管理技术。**Java**堆的容量可以是固定大小的，也可以随着程序执行的需求动态扩展，并在不需要过多空间时自动收缩。**Java**堆所使用的内存不需要保证是连续的。


堆内存分为三部分：

**永久存储区**		

永久存储区是一个常驻内存区域，用于存放**JDK** 自身所携带的**Class**,**Interface** 的元数据，也就是说它存储的是运行环境必须的类信息，被装载进此区域的数据是不会被垃圾回收器回收掉的。关闭JVM 才会释放此区域所占用的内存

**Young Generation Space 新生区**

新生区是类的诞生、成长、消亡的区域，一个类在这里产生，应用，最后被垃圾回收器收集，结束生命。新生区又分为两部分： 伊甸区（**Eden space**）和幸存者区（**Survivor pace**），所有的类都是在伊甸区被new 出来的。幸存区有两个： 0 区（**Survivor 0 space**）和1 区（**Survivor 1 space**）。

当伊甸园的空间用完时，程序又需要创建对象，JVM 的垃圾回收器将对伊甸园区进行垃圾回收，将伊甸园区中的不再被其他对象所引用的对象进行销毁。然后将伊甸园中的剩余对象移动到幸存0区。若幸存0 区也满了，再对该区进行垃圾回收，然后移动到1 区。那如果1 区也满了呢？再移动到养老区。

**Tenure generation space养老区**

养老区用于保存从新生区筛选出来的**JAVA** 对象，一般池对象都在这个区域活跃。 三个区的示意图如下：

![](/images/post/jvm-heap/heap.png)

**Method Area** 方法区是被所有线程共享，该区域保存所有字段和方法字节码，以及一些特殊方法如构造函数，接口代码也在此定义。

**PC Register** 程序计数器, 每个线程都有一个程序计数器，就是一个指针，指向方法区中的方法字节码，由执行引擎读取下一条指令。

**Native Method Stack** 本地方法栈，**Java**虚拟机实现应当提供给程序员或者最终用户调节**Java**堆初始容量的手段，对于可以动态扩展和收缩**Java**堆来说，则应当提供调节其最大、最小容量的手段。

Java堆可能发生如下异常情况，如果实际所需的堆超过了自动内存管理系统能提供的最大容量，那Java虚拟机将会抛出一个**OutOfMemoryError**异常。同样通过代码来理解一下

```java
        /**
	 * 循环创建新对象，构造<p>java.lang.OutOfMemoryError: Java heap space</p>异常
	 * 
	 * @author lihzh
	 * @alia OneCoder
	 * @blog http://www.coderli.com
	 */
	private static void getHeapOutOfMemoryError() {
		int count = 0;
		List list = new LinkedList<>();
		for (;;) {
			System.out.println(count++);
			list.add(new Object());
		}
	}
```

不停的创建新的对象，来使堆内存溢出。启动参数设置：**-Xmx2m**

运行结果：

```
178702
178703
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
```

大概17w左右开始内存溢出。增大参数看看效果，**-Xmx10m**

```
305677
305678
305679
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
```

由此可见，通过设置**-Xmx**参数，可以调整**JVM**中堆的大小，从而可以在内存中保存更多的对象。

再看看另一种**OutOfMemoryError**:j**ava.lang.OutOfMemoryError: PermGen space**。同样是，通过代码构造一个PermGen space的异常。（**OneCoder**认为，你会构造出异常，自然就会慢慢理解这个异常是怎么产生的，什么参数会对这个有影响。）

由于**PermGen space**一般发生在预加载类的过程中，所以OneCoder这里利用tomcat启动来进行测试。设置Tomcat 启动参数为：

```
-server -XX:MaxPermSize=2m -XX:PermSize=2m
```

运行结果

```
java.lang.OutOfMemoryError: PermGen space
		at sun.misc.URLClassPath$JarLoader$1.run(URLClassPath.java:608)
```

果然发生P**ermGen space**异常。如果你逐渐放大该配置，会发现报错的时机逐渐推后，也就是可以加载更多的类。**OneCoder**给**tomcat**指定一个合理的值比如： 

```
-server -XX:MaxPermSize=64m -XX:PermSize=64m
```

程序即可重新启动了。	

你也可以多做一些试验，验证你的想法，所谓实践出真知。

概念参考：

- Java虚拟机规范
- 慢慢琢磨JVM