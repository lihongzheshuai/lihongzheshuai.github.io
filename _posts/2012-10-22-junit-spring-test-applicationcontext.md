---
layout: post
title: SpringTest框架JUnit单元测试用例获取ApplicationContext实例的方法
date: 2012-10-22 10:51 +0800
author: onecoder
comments: true
tags: [JUnit]
categories: [Java技术研究]
thread_key: 1196
---
JUnit单元测试用例中使用Spring框架，之前我的使用方式很直接。

```java
/**
 * 用于需要用到Spring的测试用例基类
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "/spring/applicationContext.xml" })
public class SpringTest {}
```

在测试的过程中，有人提到，想要获取ApplicationContext实例。于是，添加了对ApplicationContext的注入。

```java
/**
 * 用于需要用到Spring的测试用例基类
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "/spring/applicationContext.xml" })
public class SpringTest {

@Autowired
protected ApplicationContext ctx;
```

其实，Spring中早已直接提供了更加方便使用的基类：AbstractJUnit4SpringContextTests。修改代码如下：

```java
/**
 * 用于需要用到Spring的测试用例基类
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
@ContextConfiguration(locations = { "/spring/applicationContext.xml" })
public class SpringTest extends AbstractJUnit4SpringContextTests {

public <T> T getBean(Class<T> type) {
return applicationContext.getBean(type);
}

public Object getBean(String beanName) {
return applicationContext.getBean(beanName);
}

protected ApplicationContext getContext() {
return applicationContext;
}

}
```

代码也简洁多了。

现在想想，你想要的常用功能，一般人家都能想到了。做之前，不妨先查查有没有现成可用的工具吧：）

