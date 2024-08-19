---
layout: post
title: Spring Framework 4.0 迁移指南 （官方文档翻译）
date: 2013-12-14 12:46 +0800
author: onecoder
comments: true
tags: [Spring, 翻译]
categories: [Java技术研究]
thread_key: 1578
---
看到Spring Framework4.0发布的消息，看了下new future，<a href="http://www.coderli.com">OneCoder</a>很喜欢spring这种追&ldquo;时髦&rdquo;的风格，groovy脚本配置和Java8都支持了。顺便就翻译了一下官方的迁移指南。对一般使用来说，迁移没什么难度。替换依赖基本就可以了。

如果想要了解Sping Framework4.0.0的新特性，可以参考官方文档中的：New Features and Enhancements in Spring Framework 4.0

## 环境依赖要求：

Spring Framework4.0 需要Java SE 6 或以上的版本。（特别强调，最低版本实际为2008年发布的JDK6 update 10）。如果你从老版本的Java环境中迁移，你至少需要升级到最近的JDK6版本。推荐使用Java7和8，Java8 的稳定开发者预览状态会一致持续到2014年3月，OpenJDK8 进入最终版为止。

如果你在 Java EE 服务器部署Spring应用，你需要确认你的应用支持Java EE 6及以上的版本。这其中，特别需要注意的是满足JPA2.0和Servlet3.0规范。这个意思其实是说，你仍然可以把你的Spring Framework4.0的应用部署在只支持Servlet2.5规范的容器中。（如。Google App Engine, WebSphere 7, WebLogic 10.3），只是Spring4中一些基于Servlet3.0的特性将会无效。

## 依赖升级

Spring Framework4.0 声明了下列(可选)依赖的最低版本:

### 规范
<ul>
<li>Servlet 3.0 (2.5 支持部署)</li>
	<li>
		JPA 2.0</li>
	<li>
		Bean Validation 1.0</li>
	<li>
		JSF 2.0</li>
	<li>
		JCache 1.0 PFD</li>
	<li>
		JDO 3.0</li>
</ul>

### 容器
<ul>
	<li>
		Tomcat 6.0.30</li>
	<li>
		Jetty 7.3</li>
	<li>
		JBoss AS 6.0</li>
	<li>
		GlassFish 3.1</li>
	<li>
		Oracle WebLogic 10.3.4 (with JPA 2.0 patch applied)</li>
	<li>
		IBM WebSphere 7.0.0.9 (with JPA 2.0 feature pack installed)</li>
</ul>

### 库
<ul>
	<li>
		Hibernate Validator 4.3</li>
	<li>
		Hibernate 3.6 (推荐4.2 )</li>
	<li>
		EhCache 2.1 (推荐2.5)</li>
	<li>
		<Quartz 1.8 (推荐2.2 )</li>
	<li>
		Jackson 1.8 (推荐2.2 )</li>
	<li>
		Groovy 1.8 (推荐2.2)</li>
	<li>
		Joda-Time 2.0 (推荐2.3)</span></li>
	<li>
		Hessian 4.0</li>
	<li>
		XStream 1.4</li>
	<li>
		Apache POI 3.5</li>
</ul>

### 废弃的代码

下列的类和方法在Spring Framework4.0中被废弃。这些代码未来将会被移除，所以请检查javadoc并迁移至推荐的写法：
 
#### Jackson v1

所有Jackson v1支持的被废弃，以支持Jacksonv2:
<ul>
	<li>
		MappingJacksonMessageConverter</li>
	<li>
		JacksonObjectMapperFactoryBean</li>
	<li>
		MappingJacksonHttpMessageConverter</li>
</ul>

#### 泛型：

GenericTypeResolver中的许多方法都被废弃了。新的ResolvableType类提供了对GeneriTypeResolver和GenericCollectionTypeResolver类中废弃方法的替换：

<ul>
	<li>
	GenericTypeResolver.getTargetType(MethodParameter methodParam)</li>
	<li>
		GenericTypeResolver.resolveType(Type genericType, Map&lt;TypeVariable, Type&gt; map)</li>
	<li>
		GenericTypeResolver.getTypeVariableMap(Class&lt;?&gt; clazz)</li>
</ul>

#### Burlap

Burlap不再在开发包下，并且将在以后完全不再提供支持。
<ul>
	<li>
		BurlapClientInterceptor</li>
	<li>
		BurlapExporter</li>
	<li>
		BurlapProxyFactoryBean</li>
	<li>
		BurlapServiceExporter</li>
	<li>
		SimpleBurlapServiceExporter</li>
</ul>

#### 过时的JBoss类

下面的类由于不在当前JBoss释放版中而被废弃：</span></p>
<ul>
	<li>
		JBossWorkManagerTaskExecutor</li>
	<li>
		JBossWorkManagerUtils</li>
</ul>

#### 其他废弃

<ul>
	<li>	AbstractJaxWsServiceExporter.setWebServiceFeatures(Object[] webServiceFeatures)</li>
	<li>JaxWsPortClientInterceptor.setWebServiceFeatures(Object[] webServiceFeatures)</span></li>
	<li>
		DefaultKeyGenerator</li>
</ul>

### 默认的缓存key生成器</span><br />

Spring使用的默认的KeyGenerator实现，由原来的DefaultKeyGenerator变为SimpleKeyGenerator。新的生成器不会再有key冲突并且基本不太可能使一个缓存的方法返回错误的结果。如果仍想使用之前的key策略，你需要配置使用废弃的DefaultKeyGenerator或者创建一个自定义的KeyGenerator实现。

### MVC 命名空间

Spring MVC的命名空间XSD已经升级，以正确使用一对属性。当升级到spring-mvc-4.0.xsd后，你应该分别用 enable-matrix-variables 和ignore-default-model-on-redirect respectively 来替换原来的enableMatrixVariables 和ignoreDefaultModelOnRedirect 属性。