---
layout: post
title: Servlet3.0下基于注解的SpringMVC3.1配置-完全零配置文件
date: 2012-10-15 09:54 +0800
author: onecoder
comments: true
tags: [Spring]
categories: [Java技术研究,Spring]
thread_key: 1183
---
<p>
	Spring3.1.x系列的一个新特性就是支持了Servlet3.0规范，基于注解的方式配置SpringMVC框架。官方文档描述如下：</p>
<blockquote>
	<div>
		<div>
			<div>
				<h3>
					3.1.10&nbsp;Support for Servlet 3 code-based configuration of Servlet Container</h3>
			</div>
		</div>
	</div>
	<p>
		The new&nbsp;WebApplicationInitializer&nbsp;builds atop Servlet 3.0&#39;s&nbsp;ServletContainerInitializer&nbsp;support to provide a programmatic alternative to the traditional web.xml.</p>
	<div>
		<ul type="disc">
			<li>
				<p>
					See org.springframework.web.WebApplicationInitializer Javadoc</p>
			</li>
			<li>
				<p>
					<a href="http://bit.ly/lrDHja" target="_top">Diff from Spring&#39;s Greenhouse reference application</a>&nbsp;demonstrating migration from web.xml to&nbsp;WebApplicationInitializer</p>
			</li>
		</ul>
	</div>
</blockquote>
<p>
	既然如此，我们就来实现一下。根据WebApplicationInitializer&nbsp;的注释说明，实现该接口即可。</p>

```java
/**
 * 基于Servlet3.0的，相当于以前<b>web.xml</b>配置文件的配置类
 * 
 * @author OneCoder
 * @Blog http://www.coderli.com
 * @date 2012-9-30 下午1:16:59
 */
public class DefaultWebApplicationInitializer implements
		WebApplicationInitializer {

	@Override
	public void onStartup(ServletContext appContext)
			throws ServletException {
		AnnotationConfigWebApplicationContext rootContext = new AnnotationConfigWebApplicationContext();
		rootContext.register(DefaultAppConfig.class);

		appContext.addListener(new ContextLoaderListener(rootContext));

		ServletRegistration.Dynamic dispatcher = appContext.addServlet(
				"dispatcher", new DispatcherServlet(rootContext));
		dispatcher.setLoadOnStartup(1);
		dispatcher.addMapping("/");

	}
}
```

<p>
	这里说明一下，根据WebApplicationInitializer&nbsp;类的注释说明(<a href="http://www.coderli.com">OneCoder</a>建议大家多阅读代码注释(Javadoc)，其实也就是API文档。)，其实这里有两种初始化rootContext的方式。一种是利用XmlWebApplicationContext，即Spring的配置是通过传统的Xml的方式配置的。另一种就是这里用到的AnnotationConfigWebApplicationContext&nbsp;，即Spring的配置也是通过注解的方式。这里，我们既然说了是完全零配置文件，那么我就采用第二种方式。利用新建的配置类，配置注解的方式，完成配置。</p>

```java
/**
 * Spring3.1基于注解的配置类， 用于代替原来的<b>applicationContext.xml</b>配置文件
 * 
 * @author lihzh
 * @date 2012-10-12 下午4:23:13
 */
@Configuration
@ComponentScan(basePackages = "com.coderli.shurnim.*.biz")
public class DefaultAppConfig {

}
```

<p>
	可以看到，基本原有在配置文件里的配置，这里都提供的相应的注解与之对应。这里我们仅仅配置的包扫描的根路径，用于SpringMVC配置的扫描，以进一步达到零配置文件的效果。在业务包下，写一个MVC的controller类：</p>

```java
/**
 * 用户操作Action类
 * 
 * @author lihzh
 * @date 2012-10-12 下午4:12:54
 */
@Controller
public class UserAction {

	@RequestMapping("/user.do")
	public void test(HttpServletResponse response) throws IOException {
		response.getWriter().write("Hi, u guy.");
	}
}
```

<p>
	启动Tomcat，浏览器访问地址：&nbsp;<a href="file:///C:/Users/lihzh/AppData/Local/youdao/ynote/editor/web/%E5%90%AF%E5%8A%A8Tomcat%EF%BC%8C%E8%AE%BF%E9%97%AE%E5%9C%B0%E5%9D%80%EF%BC%9Ahttp://localhost:8080/onecoder-shurnim/user.do%E3%80%82%E6%80%8E%E4%B9%88">http://localhost:8080/onecoder-shurnim/user.do</a></p>
<div>
	怎么样，OK了吧。看看我们的工程，这回是不是真的一个配置文件都没有。</div>
<div>
	&nbsp;</div>
<div>
	写在最后，<a href="http://www.coderli.com">OneCoder</a>这里只是零配置文件的配置方式，不参与讨论配置文件与注解的优劣问题的争执。我觉得，这就是个人喜好问题。任何东西，有好的一面就有不利的一面，坚持你喜欢的并承担相应后果就好：）</div>

