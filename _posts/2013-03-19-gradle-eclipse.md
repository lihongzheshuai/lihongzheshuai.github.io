---
layout: post
title: Gradle初试
date: 2013-03-19 22:07 +0800
author: onecoder
comments: true
tags: [Gradle]
categories: [Java技术研究]
thread_key: 1414
---
<p>
	Gradle是什么就不多说了，跟Maven是同类型的工具。Spring和Hibernate都早已经迁移了过来。官网地址：<a href="http://www.gradle.org">http://www.gradle.org</a>。最新稳定版为1.4</p>
<p>
	Gradle Eclipse Plugin是spring的sts支持的。安装之：</p>
<blockquote>
	<p>
		Installing Gradle Tooling from update site<br />
		Alternatively you can install from update sites. The following update sites are available:</p>
	<p>
		&nbsp;&nbsp; * http://dist.springsource.com/snapshot/TOOLS/nightly/gradle (latest development snapshot)<br />
		&nbsp;&nbsp; * http://dist.springsource.com/milestone/TOOLS/gradle (latest milestone build.)<br />
		&nbsp;&nbsp; * http://dist.springsource.com/release/TOOLS/gradle (latest release)</p>
</blockquote>
<p>
	Gradle的配置文件脚本是groovy语法的，Eclipse插件也安装之</p>
<blockquote>
	<p>
		http://dist.springsource.org/release/GRECLIPSE/e4.2/</p>
</blockquote>
<p>
	将工程转换为Gradle工程。</p>
<p>
	然后编辑，配置文件即可。Gradle吸引人的地方就是文档相当的完善，对于一般使用者，最常用的就是依赖管理功能，文档地址：<a href="http://www.gradle.org/docs/current/userguide/artifact_dependencies_tutorial.html">http://www.gradle.org/docs/current/userguide/artifact_dependencies_tutorial.html</a></p>
<p>
	根据文档，先配置Gradle环境，</p>
<p>
	PATH=D:\Develop Software\gradle-1.4\bin</p>
<p>
	这里是为了能够在命令行中使用gradle。对于Eclipse 插件来说，其默认下载是使用的是1.2版本，如果强制指定我们下载的1.4版本，在某些操作的时候会报错。</p>
<p>
	可编辑gradle.bat(.sh)文件，设置JVM参数。</p>
<p>
	我们就在Eclipse中尝试gradle，通过configure-&gt;convert to gradle project，将工程变为Gradle管理的工程。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/OqHZL.jpg" style="width: 630px; height: 139px;" /></p>
<p>
	然后编写build.gradle配置文件。</p>
<p>
	&nbsp;</p>

```groovy
apply plugin: 'java'
group='onecoder'
version='1.0'
repositories {
mavenCentral()
mavenRepo url: "https://oss.sonatype.org/content/repositories/opensymphony-releases"
mavenRepo url: "http://dev.anyframejava.org/maven/repo"
}
sourceSets {
main
}
dependencies {
compile "io.netty:netty:3.6.3.Final"
compile "ch.qos.logback:logback-core:1.0.7"
compile "org.slf4j:slf4j-api:1.7.3"
compile "javax.mail:mail:1.4.4"
compile "org.apache.httpcomponents:httpclient:4.2.2"
compile "org.hyperic:sigar:1.6.4"
compile "net.sourceforge.groboutils:groboutils-core:5"
}
```

<br />
<p>
	然后fresh all一下，即可自动下载依赖了。相对pom.xml来说，配置文件看起来确实清晰简单多了。这里有很多配置，OneCoder还没有弄清楚，这里只是简单的试用，并且把个人联系的工程迁移了过来。细节问题，留待以后使用中慢慢研究吧。<br />
	&nbsp;</p>

