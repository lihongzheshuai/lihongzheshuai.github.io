---
layout: post
title: 教你快速写出多线程Junit单元测试用例 - GroboUtils
date: 2012-06-13 13:17 +0800
author: onecoder
comments: true
tags: [Groboutils, JUnit]
categories: [Java技术研究]
thread_key: 439
---

写过Junit单元测试的同学应该会有感觉，Junit本身是不支持普通的多线程测试的，这是因为Junit的底层实现上，是用System.exit退出用例执行的。JVM都终止了，在测试线程启动的其他线程自然也无法执行。JunitCore代码如下

```java
/**

* Run the tests contained in the classes named in the <code>args</code>.

* If all tests run successfully, exit with a status of 0. Otherwise exit with a status of 1.

* Write feedback while tests are running and write

* stack traces for all failed tests after the tests all complete.

* @param args names of classes in which to find tests to run

*/

public static void main(String... args) {

runMainAndExit(new RealSystem(), args);

}

/**

* Do not use. Testing purposes only.

* @param system

*/

public static void runMainAndExit(JUnitSystem system, String... args) {

Result result= new JUnitCore().runMain(system, args);

system.exit(result.wasSuccessful() ? 0 : 1);

}
```

RealSystem：

```java
public void exit(int code) {

System.exit(code);

}
```

所以要想编写多线程Junit测试用例，就必须让主线程等待所有子线程执行完成后再退出。想到的办法自然是Thread中的join方法。话又说回来，这样一个简单而又典型的需求，难道会没有第三方的包支持么？通过google，笔者很快就找到了GroboUtils这个Junit多线程测试的开源的第三方的工具包。
			
- GroboUtils官网如下：<a href="http://groboutils.sourceforge.net/" target="_blank">http://groboutils.sourceforge.net/</a>
- 下载页面：<a href="http://groboutils.sourceforge.net/downloads.html" target="_blank">http://groboutils.sourceforge.net/downloads.html</a>


Maven依赖方式：

```xml
<dependency>

<groupId>net.sourceforge.groboutils</groupId>

<artifactId>groboutils-core</artifactId>

<version>5</version>

</dependency>
```
			
>注：需要第三方库支持：Repository url https://oss.sonatype.org/content/repositories/opensymphony-releases

依赖好Jar包后就可以编写多线程测试用例了。上手很简单：

```java
/**

* 多线程测试用例

*

* @author lihzh(One Coder)

* @date 2012-6-12 下午9:18:11

* @blog http://www.coderli.com

*/

@Test

public void MultiRequestsTest() {

// 构造一个Runner

TestRunnable runner = new TestRunnable() {

@Override

public void runTest() throws Throwable {

// 测试内容

}

};

int runnerCount = 100;

//Rnner数组，想当于并发多少个。

TestRunnable[] trs = new TestRunnable[runnerCount];

for (int i = 0; i < runnerCount; i++) {

trs[i] = runner;

}

// 用于执行多线程测试用例的Runner，将前面定义的单个Runner组成的数组传入

MultiThreadedTestRunner mttr = new MultiThreadedTestRunner(trs);

try {

// 开发并发执行数组里定义的内容

mttr.runTestRunnables();

} catch (Throwable e) {

e.printStackTrace();

}

}
```
		
执行一下，看看效果。怎么样，你的Junit也可以执行多线程测试用例了吧：）。