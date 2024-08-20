---
layout: post
title: Windows下 Apache Http Server+ Tomcat 整合配置
date: 2014-10-30 16:07
author: onecoder
comments: true
tags: [Tomcat]
categories: [知识扩展]
thread_key: 1846
---
可能网上已经有很多教程，这里只是记录OneCoder自己的搭建过程。

需要模拟实际环境进行一些验证工作，这里搭建环境也力图简便。没有自己编译Apache Http Server，而是下载了一个编译好的安装包：[https://mirror.bit.edu.cn/apache//httpd/binaries/win32/httpd-2.2.25-win32-x86-openssl-0.9.8y.msi](https://mirror.bit.edu.cn/apache//httpd/binaries/win32/httpd-2.2.25-win32-x86-openssl-0.9.8y.msi)

与tomcat整合，一般有三种方式 jk,http_proxy和ajp_proxy，这里以jk为例。
需要通过mod_jk模块，可以在这里下载对应的版本：
[https://mirrors.cnnic.cn/apache/tomcat/tomcat-connectors/jk/binaries/windows/](https://mirrors.cnnic.cn/apache/tomcat/tomcat-connectors/jk/binaries/windows/)

解压后放置到apache安装目录中的modules文件夹中。

然后修改httpd.conf中的配置。加入配置：

>LoadModule jk_module modules/mod_jk.so
>JKWorkersFile conf/workers.properties

即加载mod_jk.so模块，配置文件为workers.properties.

接下来配置worker.properties

```properties
workers.tomcat_home=D:\apache-tomcat-6.0.41
ps=/
worker.list=ajp13
worker.ajp13.port=8009
worker.ajp13.host=localhost
worker.ajp13.type=ajp13
```

主要是配置tomcat所在目录，已经ajp协议的端口号版本和地址。

接下来就是告诉apache什么请求交给tomcat来处理。

```text
<VirtualHost>
ServerAdmin localhost
DocumentRoot E:/
ServerName localhost
DirectoryIndex index.html index.htm index.jsp index.action

JkMount /*WEB-INF ajp13
JkMount /*j_spring_security_check ajp13
JkMount /*.action ajp13
JkMount /servlet/* ajp13
JkMount /games/* ajp13
JkMount /*.jsp ajp13
JkMount /*.do ajp13
JkMount /*.action ajp13
</VirtualHost>
```

最后，记得开放访问权限。

>&lt;Directory&gt;
Allow from all
&lt;/Directory&gt;

启动tomcat和apache，一切over。

另外两种方式，配置更简单，可参考：
[https://www.ibm.com/developerworks/cn/opensource/os-lo-apache-tomcat/](https://www.ibm.com/developerworks/cn/opensource/os-lo-apache-tomcat/)
