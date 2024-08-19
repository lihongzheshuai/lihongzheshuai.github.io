---
layout: post
title: Eclipse4.2+Tomcat7+Maven3+Servlet3.0 J2EE工程配置说明
date: 2012-09-29 09:16 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究]
thread_key: 1161
---
<a href="http://www.coderli.com">OneCoder</a>准备自己慢慢写点东西，把离散的知识点汇总一下。给出的版本没什么特别的含义，只是<a href="http://www.coderli.com">OneCoder</a>目前使用的环境而已。
	<ul>
		<li>
			IDE:Eclipse4.2 JUNO。</li>
		<li>
			应用服务器：Tomcat7.0.30（Servlet3.0）</li>
		<li>
			项目构建工具： Maven 3.0.4</li>
		<li>
			JDK版本：1.7.07</li>
		<li>
			日志组件：logback最新版</li>
		<li>
			单元测试框架：Junit</li>
	</ul>
	<div>
		为什么都用最新版本？因为<a href="http://www.coderli.com">OneCoder</a>是个新版控呵呵。</div>
	<div>
		为了以后管理方便，先建一个全局的parent工程，统一控制jar包依赖的版本。然后新建一个Maven管理的Web工程，parent指定为<a href="https://code.google.com/p/onecoder/">onecoder-parent</a>工程。</div>

Parent pom.xml配置样例：(主要是版本变量定义，依赖包设置和编译级别设置)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>onecoder-parent</groupId>
	<artifactId>onecoder-parent</artifactId>
	<version>0.1</version>
	<packaging>pom</packaging>
	<properties>
		<logback.version>1.0.7</logback.version>
		<slf4j.version>1.7.1</slf4j.version>
		<junit.version>4.10</junit.version>
	</properties>
	<dependencyManagement>
		<dependencies>
			<dependency>
				<groupId>junit</groupId>
				<artifactId>junit</artifactId>
				<version>${junit.version}</version>
				<scope>test</scope>
			</dependency>
			<dependency>
				<groupId>org.slf4j</groupId>
				<artifactId>slf4j-api</artifactId>
				<version>${slf4j.version}</version>
			</dependency>
			<dependency>
				<groupId>ch.qos.logback</groupId>
				<artifactId>logback-core</artifactId>
				<version>${logback.version}</version>
			</dependency>
			<dependency>
				<groupId>ch.qos.logback</groupId>
				<artifactId>logback-classic</artifactId>
				<version>${logback.version}</version>
			</dependency>
		</dependencies>
	</dependencyManagement>
	<build>
		<pluginManagement>
			<plugins>
				<plugin>
					<groupId>org.apache.maven.plugins</groupId>
					<artifactId>maven-compiler-plugin</artifactId>
					<version>2.3.2</version>
					<configuration>
						<verbose>true</verbose>
						<fork>true</fork>
						<executable>${JAVA_HOME}/bin/javac</executable>
						<compilerVersion>1.7</compilerVersion>
						<source>1.7</source>
						<target>1.7</target>
					</configuration>
				</plugin>

				<plugin>
					<groupId>org.apache.maven.plugins</groupId>
					<artifactId>maven-surefire-plugin</artifactId>
					<version>2.7.2</version>
				</plugin>
			</plugins>
		</pluginManagement>
	</build>
</project>
```
	
logback的简要配置：

```xml
<configuration>  
  <appender name="console" class="ch.qos.logback.core.ConsoleAppender">  
    <encoder  class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">  
      <pattern>%d{yyyy/MM/dd-HH:mm:ss} %level [%thread] %C - %msg%n</pattern>  
    </encoder >  
  </appender>  
  
  <root level="INFO">  
    <appender-ref ref="console" />  
  </root>  
</configuration>  
```

<p>
	扔到src/main/resources下。</p>
<p style="text-align: center; ">
	<img alt="" src="/images/oldposts/9wt4N.jpg" /></p>
<p>
	&nbsp;</p>
<div>
	如果你此时不知所措，不放直接扔到Tomcat下启动一下，看报什么错，就知道缺什么了。解决错误的过程，可以学到很多东西。</div>

接下来应该写Servlet了。Servlet3.0的一大亮点就是支持注解配置。所以你会发现没有了web.xml配置文件。Servlet写起来也很简单。

```java
/**
 * Servlet3.0 Servlet使用样例
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
@WebServlet(name = "FirstServlet", urlPatterns = { "/firstservlet"})
public class FirstServlet extends HttpServlet {

	private static final long serialVersionUID = 3038754482452604279L;
	private static final Logger log = LoggerFactory.getLogger(FirstServlet.class);

        @Override
	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		PrintWriter out = response.getWriter();
		log.info("This is log");
		out.println("hello,world...");
		out.close();
	}
}
```

<div>
	一个简单的Servlet就写好了。</div>

运行一下？等等。我们知道一个web工程运行时依赖的jar包是需要放到WEB-INF/lib下的，这里明显看到lib下空的，并且我们的jar包是通过Maven管理的，难道要手动拷贝过去吗？<a href="http://www.coderli.com">OneCoder</a>以前还真干过这样的啥事，甚至还自己开发了脚本，做所谓的&ldquo;一键自动化&rdquo;工作。其实Eclipse里已经帮你做好了。在工程的Properties配置项里的Deployment Assembly配置里，配好Maven的依赖和部署即可，如图：

<div style="text-align: center; ">
	<img alt="" src="/images/oldposts/e1swU.jpg" /></div>

<div>
	此时再运行一下，log正常输出，说明jar依赖过来了，一切都ok了。</div>
<div style="text-align: center; ">
	<img alt="" src="/images/oldposts/ddymn.jpg" /></div>
<div>
	剩下的就是你想用什么框架就引入什么了。<a href="http://www.coderli.com">OneCoder</a>会一遍配置，一遍简要的说明一下。</div>

