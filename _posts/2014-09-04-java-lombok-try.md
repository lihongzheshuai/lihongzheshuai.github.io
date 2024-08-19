---
layout: post
title: 点滴积累 Lombok  实用且有想法的jar
date: 2014-09-04 00:27 +0800
author: onecoder
comments: true
tags: [Lombok]
categories: [Java技术研究]
thread_key: 1800
---
<p>
	官网：<a href="http://projectlombok.org/">http://projectlombok.org/</a></p>
<p>
	通过官网的视频，可以看到Lombok可以帮助我们节约很多机械而繁琐的代码。例如在写Pojo类或者Log的时候。写段代码体会一下：</p>
<p>
	Gradle依赖配置：</p>

```groovy
'org.projectlombok:lombok:1.14.4'
```

<p>
	验证代码：</p>

```java
package com.coderli.lombok;

import lombok.Data;
import lombok.extern.java.Log;

/**
* Lombok 工具jar 测试类
*
* @author OneCoder
* @date 2014年9月3日 下午10:48:12
* @website http://www.coderli.com
*/
@Log
@Data
public class LombokTest {
   
     private String name;
     private int count;
   
     public static void main(String[] args) {
          log.info(&quot;Print log with Lombok&quot;);
     }
}
```

<p>
	可以看到，代码中没有声明log对象，我们却是可以直接使用。这就是Lombok的作用。在类生配置了@Log注解，类中就可以直接使用log对象。</p>
<p>
	当然，如果想在Eclipse不提示编译错误，首先自然是用把Lombok安装到eclipse中。双击下载好的jar即可安装。</p>
<p>
	同样@Data注解，就表明该类是一个model类。会自动给属性增加get/set 方法。节约代码。在Eclipse中按F4，查看该类的Type Hierarchy，可以看到每个属性get set方法已经存在。</p>
<p>
	OneCoder查了一下他的实现原理，应该利用AST，抽象语法树实现的。具体的我也不是很了解这方面的东西。有空研究一下。有两篇文章有比较详细的介绍：</p>
<p>
	<a href="https://www.ibm.com/developerworks/cn/java/j-lombok/">https://www.ibm.com/developerworks/cn/java/j-lombok/</a><br />
	<a href="http://openjdk.java.net/groups/compiler/doc/compilation-overview/index.html">http://openjdk.java.net/groups/compiler/doc/compilation-overview/index.html</a></p>
<p>
	Lombok的更多功能，大家可以自己体会一下。确实是个很有想法的项目。佩服。</p>
<p>
	太晚了，休息了。晚安。</p>
