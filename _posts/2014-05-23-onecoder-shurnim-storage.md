---
layout: post
title: OneCoder的shurnim-storage项目
date: 2014-05-23 00:03 +0800
author: onecoder
comments: true
tags: [随笔]
categories: [随笔]
thread_key: 1659
---
<h1>
	shurnim-storage</h1>
<p>
	<img alt="" src="/images/oldposts/rEBO.jpg" style="width: 180px; height: 180px;" /></p>
<h3>
	背景介绍</h3>
<p>
	Shurnim，是我和我老婆曾经养过的一只仓鼠的名字。</p>
<p>
	shurnim-storage，是一个插件式云存储/网盘同步管理工具。是在参加又拍云开发大赛的过程中设计并开发。</p>
<p>
	项目介绍<br />
	shurnim-storage 的设计初衷是给大家提供一个可方便扩展的云存储/网盘同步工具。分后端接口和前端UI界面两部分。</p>
<p>
	<br />
	由于目前各种云存储和网盘系统层出不穷，单一工具往往支持支持某几个特定存储之间的同步，如又拍云到七牛云存储的同步工具，此时如若想同步到其他存则可能需要新的工具，给用户带来不便。shurnim-storage 正是为了解决此问题而设计的。<br />
	在shurnim-storage中，用户使用的固定的统一的后端接口。而所有云存储/网盘API的支持则是以插件的形式部署到系统中的。如此，如果用户想要一个从又拍云到Dropbox的同步工具，则只需要在原有基础上，增加Dropbox的插件，即可实现互通，方便快捷。</p>
<p>
	<br />
	同时，后端统一接口的设计也考虑到界面开发的需求，可直接通过后端提供的接口开发具有上述扩展功能的云存储UI工具。</p>
<p>
	<br />
	目前，后端整体框架的核心部分已经基本开发完成。只需逐步补充后端接口和插件开发接口的定义即可。但由于个人时间和能力所限，UI部分没有开发，有兴趣的同学可以一试。</p>
<h3>
	获取代码</h3>
<p>
	&nbsp;&nbsp; * GitHub项目主页:<a href="https://github.com/lihongzheshuai/shurnim-storage" target="_blank"> https://github.com/lihongzheshuai/shurnim-storage</a><br />
	&nbsp;&nbsp; * OSChina项目主页: <a href="http://git.oschina.net/onecoder/shurnim-storage" target="_blank">http://git.oschina.net/onecoder/shurnim-storage</a></p>
<p>
	<span style="color:#ff0000;">GitHub上的会持续更新。欢迎任何形式的fork。</span></p>
<p>
	另外你也可以通过OSChina的Maven库获取依赖，或者自己编译jar包。</p>
<p>
	maven</p>
<p>
	<br />
	加入OSC仓库</p>

```xml
				<repositories>
            		<repository>
            			<id>nexus</id>
            			<name>local private nexus</name>
            			<url>http://maven.oschina.net/content/groups/public/</url>
            			<releases>
            				<enabled>true</enabled>
            			</releases>
            			<snapshots>
            				<enabled>false</enabled>
            			</snapshots>
            		</repository>
            	</repositories>
```

<p>
	<br />
	加入依赖</p>

```xml
<dependency>
			  <groupId>com.coderli</groupId>
			  <artifactId>shurnim-storage</artifactId>
 			  <version>0.1-alpha</version>
			</dependency>
```

<p>
	项目采用Gradle管理依赖，可通过gradle编译Jar</p>
<p>
	在项目目录执行</p>

```groovy
gradle jar
```

<h3>
	最后</h3>
<p>
	时间仓促，功能简陋，望您包涵。OneCoder(Blog:http://www.coderli.com)特别希望看到该项目对您哪怕一点点的帮助。任意的意见和建议，欢迎随意与我沟通,联系方式：</p>
<p>
	&nbsp;&nbsp; * Email: wushikezuo@gmail.com<br />
	&nbsp;&nbsp; * QQ:57959968<br />
	&nbsp;&nbsp; * Blog:OneCoder<br />
	&nbsp;</p>

