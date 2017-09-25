---
layout: post
title: 增强Spring测试框架的beforeClass和afterClass功能
date: 2012-10-12 13:34 +0800
author: onecoder
comments: true
tags: [Junit]
thread_key: 1179
---
<p>
	<a href="http://www.coderli.com">OneCoder</a>正巧在规划JUnit单元测试用例编写的问题，就发现了一篇分享JUnit使用技巧的文章，也到了&ldquo;每周一译&rdquo;的时间了，学习+翻译，一石二鸟。</p>
<div>
	怎样能让类的实例的方法能有想JUnit中BeforeClass一样的功能。</div>
<div>
	&nbsp;</div>
<div>
	JUnit允许我们在类的级别给方法设置属性，以使其在所有的测试用例执行之前或者之后执行。然而，在设计的时候，他们仅支持在静态方法上设置@BeforeClass和@AfterClass注解。例如如下简单样例给出的JUnit的一个典型的设置：</div>

```java
package deng.junitdemo;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

public class DemoTest {

    @Test
    public void testOne() {
        System.out.println("Normal test method #1.");
    }

    @Test
    public void testTwo() {
        System.out.println("Normal test method #2.");
    }

    @BeforeClass
    public static void beforeClassSetup() {
        System.out.println("A static method setup before class.");
    }

    @AfterClass
    public static void afterClassSetup() {
        System.out.println("A static method setup after class.");
    }
}
```

上述代码输出如下：
<div>
	<blockquote>
		<div>
			A static method setup before class.</div>
		<div>
			Normal test method #1.</div>
		<div>
			Normal test method #2.</div>
		<div>
			A static method setup after class.</div>
	</blockquote>
</div>
<div>
	这种使用方式在大多数情况下是没什么问题的，不过有些时候你会想使用非静态方法来完成设置。稍后我详细总结一些非静态方法的用例场景。对现在而言，我们先来看看如何用JUnit解决这个棘手的问题。</div>
<div>
	我们可以通过让我们的测试用例实现一个Listener接口，该接口提供了before和after回调，我们还需要让JUnit探测到我们的Listener以调用我们的方法。解决方案如下：</div>

```java
package deng.junitdemo;

import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(InstanceTestClassRunner.class)
public class Demo2Test implements InstanceTestClassListener {

    @Test
    public void testOne() {
        System.out.println("Normal test method #1");
    }

    @Test
    public void testTwo() {
        System.out.println("Normal test method #2");
    }

    @Override
    public void beforeClassSetup() {
        System.out.println("An instance method setup before class.");
    }

    @Override
    public void afterClassSetup() {
        System.out.println("An instance method setup after class.");
    }
}
```

<div>
	根据之前的介绍，Listern定义很简单，如下：</div>

```java
package deng.junitdemo;

public interface InstanceTestClassListener {
    void beforeClassSetup();
    void afterClassSetup();
}
```

我们下一步的任务就是提供一个JUnit的runner实现类来触发我们的设置方法。

```java
package deng.junitdemo;

import org.junit.runner.notification.RunNotifier;
import org.junit.runners.BlockJUnit4ClassRunner;
import org.junit.runners.model.InitializationError;

public class InstanceTestClassRunner extends BlockJUnit4ClassRunner {

    private InstanceTestClassListener InstanceSetupListener;

    public InstanceTestClassRunner(Class<?> klass) throws InitializationError {
        super(klass);
    }

    @Override
    protected Object createTest() throws Exception {
        Object test = super.createTest();
        // Note that JUnit4 will call this createTest() multiple times for each
        // test method, so we need to ensure to call "beforeClassSetup" only once.
        if (test instanceof InstanceTestClassListener &amp;&amp; InstanceSetupListener == null) {
            InstanceSetupListener = (InstanceTestClassListener) test;
            InstanceSetupListener.beforeClassSetup();
        }
        return test;
    }

    @Override
    public void run(RunNotifier notifier) {
        super.run(notifier);
        if (InstanceSetupListener != null)
            InstanceSetupListener.afterClassSetup();
    }
}
```

现在，我们都准备就绪了。如果我们执行上述测试用例，将返回类似的结果，不过现在我们使用的非静态方法。
<div>
	<blockquote>
		<div>
			An instance method setup before class.</div>
		<div>
			Normal test method #1</div>
		<div>
			Normal test method #2</div>
		<div>
			An instance method setup after class.</div>
	</blockquote>
</div>
<div>
	一个具体的使用场景：使用Spring的测试框架。</div>
<div>
	&nbsp;</div>
<div>
	现在，让我来介绍一个使用上述方法真实的场景。如果你使用Spring的测试框架，你会使用类似的方式去设置测试用例，你的测试方法会作为类的实例的一个方法固定的注入其中。</div>

```java
package deng.junitdemo.spring;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertThat;

import java.util.List;

import javax.annotation.Resource;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration
public class SpringDemoTest {

    @Resource(name="myList")
    private List<String> myList;

    @Test
    public void testMyListInjection() {
        assertThat(myList.size(), is(2));
    }
}
```
<div>
	&nbsp;</div>
<div>
	你还需要在相同的包下有Spring的xml配置文件。</div>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
     <bean id="myList" class="java.util.ArrayList">
        <constructor-arg>
            <list>
                <value>one</value>
                <value>two</value>
            </list>
        </constructor-arg>
     </bean>
</beans>
```
<div>
	&nbsp;</div>
<div>
	特别注意这个类的实例的List<String> myList属性。当运行JUnit测试用例的时候，这个属性会被Spring注入给实例，并且可以被这个类的任何测试方法使用。然而，如果你想某些代码仅仅设置一次并且获取Spring注入属性的引用，你就很不幸了。这是因为JUnit的@BeforeClass强制要求你的方法是静态的，同时，如果你的属性也是静态的，Spring的注入将无法运行。</div>

这里，如果你经常使用Spring，你应该知道Spring的测试框架已经提供了一个处理这种场景的方式。下面的代码就是通过Spring来处理类级别设置的方式：

```java
package deng.junitdemo.spring;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertThat;

import java.util.List;

import javax.annotation.Resource;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.TestContext;
import org.springframework.test.context.TestExecutionListeners;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.support.AbstractTestExecutionListener;
import org.springframework.test.context.support.DependencyInjectionTestExecutionListener;

@RunWith(SpringJUnit4ClassRunner.class)
@TestExecutionListeners(listeners = {
        DependencyInjectionTestExecutionListener.class, 
        SpringDemo2Test.class})
@ContextConfiguration
public class SpringDemo2Test extends AbstractTestExecutionListener {

    @Resource(name="myList")
    private List<String> myList;

    @Test
    public void testMyListInjection() {
        assertThat(myList.size(), is(2));
    }

    @Override
    public void afterTestClass(TestContext testContext) {
        List<?> list = testContext.getApplicationContext().getBean("myList", List.class);
        assertThat((String)list.get(0), is("one"));
    }

    @Override
    public void beforeTestClass(TestContext testContext) {
        List<?> list = testContext.getApplicationContext().getBean("myList", List.class);
        assertThat((String)list.get(1), is("two"));
    }
}
```

可以看到，Spring提供了@TestExecutionListeners注解让你可以去编写任意的Listener，在其中，你可以获得对TestContext的引用，TestContext中包含了ApplicationContext，可以获得对注入属性的引用。这确实行得通，但是却不够优雅。它要求你必须去查找指定的bean，尽管你注入的属性已经准备就绪。但是你却无法使用它，除非你通过TestContext参数去获取。</div>
<div>
	&nbsp;</div>
<div>
	现在，如果你可以把这两种解决方案融合一下，我们会看到一个更漂亮测试用例设置。</div>

```java
package deng.junitdemo.spring;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertThat;

import java.util.List;

import javax.annotation.Resource;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;

import deng.junitdemo.InstanceTestClassListener;

@RunWith(SpringInstanceTestClassRunner.class)
@ContextConfiguration
public class SpringDemo3Test implements InstanceTestClassListener {

    @Resource(name="myList")
    private List<String> myList;

    @Test
    public void testMyListInjection() {
        assertThat(myList.size(), is(2));
    }

    @Override
    public void beforeClassSetup() {
        assertThat((String)myList.get(0), is("one"));
    }

    @Override
    public void afterClassSetup() {
        assertThat((String)myList.get(1), is("two"));
    }
}
```

JUnit仅允许你使用一个Runner，所以我们必须扩展Spring的版本来插入我们之前做的工作：

```java
package deng.junitdemo.spring;

import org.junit.runner.notification.RunNotifier;
import org.junit.runners.model.InitializationError;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import deng.junitdemo.InstanceTestClassListener;

public class SpringInstanceTestClassRunner extends SpringJUnit4ClassRunner {

    private InstanceTestClassListener InstanceSetupListener;

    public SpringInstanceTestClassRunner(Class<?> clazz) throws InitializationError {
        super(clazz);
    }

    @Override
    protected Object createTest() throws Exception {
        Object test = super.createTest();
        // Note that JUnit4 will call this createTest() multiple times for each
        // test method, so we need to ensure to call "beforeClassSetup" only once.
        if (test instanceof InstanceTestClassListener &amp;&amp; InstanceSetupListener == null) {
            InstanceSetupListener = (InstanceTestClassListener) test;
            InstanceSetupListener.beforeClassSetup();
        }
        return test;
    }

    @Override
    public void run(RunNotifier notifier) {
        super.run(notifier);
        if (InstanceSetupListener != null)
            InstanceSetupListener.afterClassSetup();
    }
}
```

执行测试用例，会得到以下输出：
<div>
	<blockquote>
		<div>
			12:58:48 main INFO &nbsp;org.springframework.test.context.support.AbstractContextLoader:139 | Detected default resource location "classpath:/deng/junitdemo/spring/SpringDemo3Test-context.xml" for test class [deng.junitdemo.spring.SpringDemo3Test].</div>
		<div>
			12:58:48 main INFO &nbsp;org.springframework.test.context.support.DelegatingSmartContextLoader:148 | GenericXmlContextLoader detected default locations for context configuration [ContextConfigurationAttributes@74b23210 declaringClass = &#39;deng.junitdemo.spring.SpringDemo3Test&#39;, locations = &#39;{classpath:/deng/junitdemo/spring/SpringDemo3Test-context.xml}&#39;, classes = &#39;{}&#39;, inheritLocations = true, contextLoaderClass = &#39;org.springframework.test.context.ContextLoader&#39;].</div>
		<div>
			12:58:48 main INFO &nbsp;org.springframework.test.context.support.AnnotationConfigContextLoader:150 | Could not detect default configuration classes for test class [deng.junitdemo.spring.SpringDemo3Test]: SpringDemo3Test does not declare any static, non-private, non-final, inner classes annotated with @Configuration.</div>
		<div>
			12:58:48 main INFO &nbsp;org.springframework.test.context.TestContextManager:185 | @TestExecutionListeners is not present for class [class deng.junitdemo.spring.SpringDemo3Test]: using defaults.</div>
		<div>
			12:58:48 main INFO &nbsp;org.springframework.beans.factory.xml.XmlBeanDefinitionReader:315 | Loading XML bean definitions from class path resource [deng/junitdemo/spring/SpringDemo3Test-context.xml]</div>
		<div>
			12:58:48 main INFO &nbsp;org.springframework.context.support.GenericApplicationContext:500 | Refreshing org.springframework.context.support.GenericApplicationContext@44c9d92c: startup date [Sat Sep 29 12:58:48 EDT 2012]; root of context hierarchy</div>
		<div>
			12:58:49 main INFO &nbsp;org.springframework.beans.factory.support.DefaultListableBeanFactory:581 | Pre-instantiating singletons in org.springframework.beans.factory.support.DefaultListableBeanFactory@73c6641: defining beans [myList,org.springframework.context.annotation.internalConfigurationAnnotationProcessor,org.springframework.context.annotation.internalAutowiredAnnotationProcessor,org.springframework.context.annotation.internalRequiredAnnotationProcessor,org.springframework.context.annotation.internalCommonAnnotationProcessor,org.springframework.context.annotation.ConfigurationClassPostProcessor$ImportAwareBeanPostProcessor#0]; root of factory hierarchy</div>
		<div>
			12:58:49 Thread-1 INFO &nbsp;org.springframework.context.support.GenericApplicationContext:1025 | Closing org.springframework.context.support.GenericApplicationContext@44c9d92c: startup date [Sat Sep 29 12:58:48 EDT 2012]; root of context hierarchy</div>
		<div>
			12:58:49 Thread-1 INFO &nbsp;org.springframework.beans.factory.support.DefaultListableBeanFactory:433 | Destroying singletons in org.springframework.beans.factory.support.DefaultListableBeanFactory@73c6641: defining beans [myList,org.springframework.context.annotation.internalConfigurationAnnotationProcessor,org.springframework.context.annotation.internalAutowiredAnnotationProcessor,org.springframework.context.annotation.internalRequiredAnnotationProcessor,org.springframework.context.annotation.internalCommonAnnotationProcessor,org.springframework.context.annotation.ConfigurationClassPostProcessor$ImportAwareBeanPostProcessor#0]; root of factory hierarchy</div>
	</blockquote>
</div>
<div>
	显然，这些输出没什么可关注的，但是测试用例会全部通过。关键在于，现在我们有一个更加优雅的方式去完成类级别的before和after测试方法的设置，并且他们可以是用类的实例的方法同时还支持Spring的注入。</div>

原文地址：<a href="http://java.dzone.com/articles/enhancing-spring-test">http://java.dzone.com/articles/enhancing-spring-test</a>

