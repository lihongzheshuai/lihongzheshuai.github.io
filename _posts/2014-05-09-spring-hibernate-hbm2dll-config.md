---
layout: post
title: Spring集成Hibernate注解配置 无hibernate.cfg.xml文件，自动生成表配置
date: 2014-05-09 13:59 +0800
author: onecoder
comments: true
tags: [Spring,Hibernate]
categories: [Java技术研究]
thread_key: 1643
---
<p>
	本以为一个无足挂齿的小问题，没想到还折腾了一下。遂记录一下。主要搜索出的结果排名靠前的大多是在hibernate.cfg.xml中的配置方式。与我的环境不符。正确配置方式如下。已测试。</p>

```xml
<bean id= "sessionFactory"
           class= "org.springframework.orm.hibernate3.annotation.AnnotationSessionFactoryBean" >
           <property name ="dataSource">
               <ref bean ="dataSource" />
           </property >
           <property name ="packagesToScan" value= "xxx.xxx" />
           <property name ="hibernateProperties">
               <props >
                    <prop key= "hibernate.hbm2ddl.auto">create</prop >
               </props >
               <!-- <value>hibernate.hbm2ddl.auto=create</value> -->
           </property >
     </bean >
```

<p>
	注：注释掉的配置value配置方式和prop配置方式，均有效。<br />
	&nbsp;</p>

