---
layout: post
title: Hibernate4.0源码下载和编译教程
date: 2012-06-06 23:27 +0800
author: onecoder
comments: true
tags: [Hibernate]
thread_key: 320
---
废话不多说，直接进入主题。首先是下载源码，跟spring一样，hibernate也采用git管理。

- git://github.com/hibernate/hibernate-orm.git 

下载后，hiberante同样也是采用了gradle进行编译，所以同样同之前说的spring的编译， 参考阅读：

- <a href="http://www.coderli.com/springframework-source-compile/" target="_blank">《SpringFramework3 源码下载和编译教程》</a>

在源码的根目录执行： 

```sh
gradlew.bat assemble 
```

> 可跳过测试，否则执行gradlew.bat build的过程中，遇到test出错会报错退出。

本以为会顺利结束，没想到又报错了。是符号无法识别转换的错误。在网上搜索了一番，这个跟系统的区域设置有关。需要改为：***英语（英国）***。我试了英语（美国）居然还是报错。。。 

> PS：区域设置在控制面板中。 

再此编译，终于成功。 最后，一样执行

```sh
gradlew.bat eclipse 
```

生成eclipse工程，导入，ok大功告成！ 

PS：不知道为什么hiberante编译出来的***core***和***test***工程会有循环依赖。我手动取消了core对test工程依赖，改为引用了build出来的test工程的jar包，解决问题。不知道大家是否遇到这样的问题。
