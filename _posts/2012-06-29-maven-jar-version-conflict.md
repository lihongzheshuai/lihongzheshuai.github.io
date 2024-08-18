---
layout: post
title: Maven 解决Jar包版本冲突
date: 2012-06-29 21:42 +0800
author: onecoder
comments: true
tags: [Maven]
thread_key: 716
---
今天遇到一个小问题。在使用**apache-commons-codec**包进行编码/解码的时候，用到了**Base64**类的**decodeBase64(String base64String)**方法，这个方法在**1.4**版中才提供。而我们的工程中对codec存在两个间接的依赖，一个依赖**1.2**版本，一个依赖1.4版本，打包后，只有1.2版本，所以会报找不到该方法的错误。

这个问题其实很好解决。在依赖1.2版本的项目上，排除对codec的间接依赖即可。如：

```xml
		<dependency>
          <!-- 你直接依赖的Jar包-->
			<groupId>AAA</groupId>
			<artifactId>AAA</artifactId>
			<exclusions>
				<exclusion>
                 <!-- 你想排除的间接依赖的Jar包-->
					<artifactId>xxx</artifactId>
					<groupId>xxx</groupId>
				</exclusion>
			</exclusions>
			<version>AAA</version>
		</dependency>
```
