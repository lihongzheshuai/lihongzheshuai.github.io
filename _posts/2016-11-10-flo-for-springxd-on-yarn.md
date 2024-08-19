---
layout: post
title: On Yarn模式下 Spring Flo for SpringXD UI部署
tags: [Spring]
categories: [Java技术研究]
date: 2016-11-10 11:16:33 +0800
comments: true
author: onecoder
thread_key: 1904
---
配置Spring Flo可在SpringXD的admin-ui页面提供拖拽式的组合job的定义。

从Pivotal官方下载Flo for XD 1.0.1版本
[https://network.pivotal.io/products/p-spring-flo](https://network.pivotal.io/products/p-spring-flo)

<!--break-->

解压flo-spring-xd-admin-ui-client-1.3.1.RELEASE.zip

```bash
unzip flo-spring-xd-admin-ui-client-1.3.1.RELEASE.zip
```

将解压后的jar放到lib目录下替换原来的spring-xd-admin-ui-client-1.3.1.RELEASE.jar文件

```bash
zip -r spring-xd-1.3.1.RELEASE-yarn/spring-xd-yarn-1.3.1.RELEASE.zip lib/spring-xd-admin-ui-client-1.3.1.RELEASE.jar
```

重新发布

```bash
bin/xd-yarn push
```

如果存在已有服务，需要先kill掉

```bash
bin/xd-yarn kill -a ${appId}
```

其中appid可通过命令查询

```bash
bin/xd-yarn submitted
```

提交

```bash
bin/xd-yarn submit
```

通过浏览器访问admin-ui，Flo出现了

![](/images/post/flo-for-springxd-on-yarn/flo-for-xd.png)