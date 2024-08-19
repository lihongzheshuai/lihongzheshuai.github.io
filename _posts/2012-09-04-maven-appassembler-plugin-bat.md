---
layout: post
title: 利用Maven插件打包产生可运行bat文件
date: 2012-09-04 23:02 +0800
author: onecoder
comments: true
tags: [Maven]
categories: [Java技术研究]
thread_key: 1131
---
其实是一个很简单的技巧，就是利用**Maven**的**appassembler-maven-plugin**插件，就可以实现自动打包可运行的脚本，还可以跨平台。（Windows/linux）

首先在pom.xml文件的build节点下配置插件：	

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>appassembler-maven-plugin</artifactId>
    <version>1.1.1</version>
	<configuration>
	<repositoryLayout>flat</repositoryLayout>
	<repositoryName>lib</repositoryName>
	<configurationSourceDirectory>src/main/resources/conf</configurationSourceDirectory>
	<!-- Set the target configuration directory to be used in the bin scripts -->
	<configurationDirectory>conf</configurationDirectory>
	<!-- Copy the contents from &quot;/src/main/config&quot; to the target configuration 
	directory in the assembled application -->
	<copyConfigurationDirectory>true</copyConfigurationDirectory>
	<!-- Include the target configuration directory in the beginning of 
		the classpath declaration in the bin scripts -->
	<includeConfigurationDirectoryInClasspath>true</includeConfigurationDirectoryInClasspath>
	<!-- prefix all bin files with &quot;mycompany&quot; -->
	<binPrefix>startup</binPrefix>
	<!-- set alternative assemble directory -->
	<assembleDirectory>${project.build.directory}/server</assembleDirectory>
	<!-- Extra JVM arguments that will be included in the bin scripts -->
	<extraJvmArguments>-Xms768m -Xmx768m -XX:PermSize=128m
						-XX:MaxPermSize=256m -XX:NewSize=192m -XX:MaxNewSize=384m
	</extraJvmArguments>
	<!-- Generate bin scripts for windows and unix pr default -->
	<platforms>
	<platform>windows</platform>
	<platform>unix</platform>
	</platforms>
	<programs>
	<program>
	<mainClass>com.coderli.onecoder.server.HypervisorServer</mainClass>
	<name>startup</name>
	</program>
	</programs>
	</configuration>
</plugin>
```

然后选择你要编译的工程，**右键**->**maven build**... 命令如下图：

![](/images/oldposts/ogPHi.jpg)

然后Run一下：

![](/images/oldposts/HaQ6M.jpg)

一个可执行的脚本文件就生成好了。**startup.bat**是**windows**下的，**startup.sh**是**linux**下的。具体参数，可以参考我上面给出的配置，也可以自己研究一下插件的配置。