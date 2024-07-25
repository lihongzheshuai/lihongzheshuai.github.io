---
layout: post
title: Hessian4.0.7+Spring3.2.2文件上传
date: 2013-07-04 22:00 +0800
author: onecoder
comments: true
tags: [Spring]
thread_key: 1465
---
<p>
	最近用Hessian4.0.7做文件上传，先给出自己做试验的样例代码，写在tomcat7下，采用servlet3.0，配置代码如下：</p>

```java
**
 * 基于Servlet3.0的，相当于以前<b>web.xml</b>配置文件的配置类
 * 
 * @author OneCoder
 * @Blog http://www.coderli.com
 * @date 2012-9-30 下午1:16:59
 */
publicclass DefaultWebApplicationInitializer implements
WebApplicationInitializer {

@Override
publicvoid onStartup(ServletContext appContext) throws ServletException {
AnnotationConfigWebApplicationContext rootContext = new AnnotationConfigWebApplicationContext();
rootContext.register(DefaultAppConfig.class);

appContext.addListener(new ContextLoaderListener(rootContext));
ServletRegistration.Dynamic hessianServlet = appContext.addServlet("hessian", new HessianServlet());
hessianServlet.addMapping("/hessian");
hessianServlet.setInitParameter("service-class", HessianFileUploader.class.getName());
//ServletRegistration.Dynamic dispatcher = appContext.addServlet(
//"dispatcher", new DispatcherServlet(rootContext));
//dispatcher.setLoadOnStartup(1);
//dispatcher.addMapping("/");
//// Spring Security 过滤器配置
//FilterRegistration.Dynamic securityFilter = appContext.addFilter(
//"springSecurityFilterChain", DelegatingFilterProxy.class);
//securityFilter.addMappingForUrlPatterns(null, false, "/*");
}}
```

<p>
	定义接口，并在服务端实现，Hessian4.0开始支持流作为参数传递，以前则采用byte[]方式传递：</p>

```java
public interface FileUploader {

void uplaodFile(String fileName，InputStream is);

}


public class HessianFileUploader implements FileUploader {

@Override
publicvoid uplaodFile(String fileName，InputStream is) {
try {
OutputStream out = new FileOutputStream("/Users/apple/Desktop/" + fileName);
int nLength = 0;
byte[] bData = newbyte[1024];
while (-1 != (nLength = is.read(bData))) {
out.write(bData, 0, nLength);
}
out.close();
} catch (FileNotFoundException e) {
e.printStackTrace();
} catch (IOException e) {
e.printStackTrace();
} finally {
try {
is.close();
} catch (IOException e) {
e.printStackTrace();}}
}

}
```

<p class="p1">
	客户端调用：</p>

```java
public class FileUploaderTest {
private FileUploader uploader;
private HessianProxyFactory factory = new HessianProxyFactory();
@Test publicvoid testFileUploader() throws FileNotFoundException, MalformedURLException {
uploader = (FileUploader) factory.create(FileUploader.class, "http://localhost:8080/onecoder-shurnim/hessian");
InputStream is = new FileInputStream("/Users/apple/git/onecoder-java/onecoder-shurnim/src/main/resources/logback.xml"); uploader.uplaodFile(is, "logback.xml"); }
 
}
```

<p>
	很简单方便。这里曾遇到一个奇怪的问题，如果接口的参数顺序调换，即InputStream在前则会报错：</p>
<blockquote>
	<p>
		com.caucho.hessian.io.HessianProtocolException: uplaodFile: expected string at 0x3c (<)</p>
</blockquote>
<p>
	Hessian协议没有深入研究，不知道是不是一个约定或是要求。开发时需要注意。</p>
<p>
	如果集成spring，只需将servlet交由spring的代理里即可，修改配置即可：</p>

```xml
<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN//EN" "http://www.springframework.org/dtd/spring-beans.dtd"> 
<beans>         
<bean id="defaultHandlerMapping" class="org.springframework.web.servlet.handler.BeanNameUrlHandlerMapping"/>        
 <bean id="fileUploader" class="com.coderli.shurnim.file.HessianFileUploader"/>         
<bean name="/hello" class="org.springframework.remoting.caucho.HessianServiceExporter">                 
     <property name="service" ref="fileUploader"/> 
                <property name="serviceInterface" value="com.coderli.shurnim.file.FileUploader"/>        
 </bean> 
</beans>
```

<p class="p1">
	亲测spring3.2.2+Hessian4.0.7可用。文件内容保存完整。</p>
<p class="p1" style="text-align: center;">
	&nbsp; &nbsp;&nbsp;<img alt="" src="/images/oldposts/K9Jh4.jpg" style="width: 630px; height: 516px;" /></p>

