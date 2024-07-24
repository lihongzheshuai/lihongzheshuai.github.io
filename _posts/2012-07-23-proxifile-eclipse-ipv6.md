---
layout: post
title: Eclipse javaw 通过Proxifile代理ipv6协议问题解决
date: 2012-07-23 21:33 +0800
author: onecoder
comments: true
tags: [Eclipse]
thread_key: 985
---
这是一个在比较特殊情况下才会发生的问题。不过却在笔者的身上发生了，既然如此，那就记录一下，也许还有其他朋友也会碰到。

**问题描述**：笔者办公环境使用**Proxifile**全局代码上网，不过对于一些不想走代理的程序和地址进行了过滤。然后笔者发现，**Eclipse**更新不好用了。查看**Proxifile**记录，发现**Eclipse**访问网址，都是通过**ipv6**协议。而**ipv6**似乎**proxifile**无法解析。于是，笔者在**Eclipse**的配置文件,**eclipse.ini**中加入下面一行配置。

```
-vmargs
-Djava.net.preferIPv4Stack=true
```

重启，生效。

然而，问题还没完。笔者最近一直在研究**Netty**。在启动**Netty**服务的时候，发现开始报无法绑定地址的错误。很显然，这也是由于设置**proxifile**代理产生的。（因为之前没有这个问题。），查看日志，还是**ipv6**的问题。这回是**javaw.exe**，走的**ipv6**协议。
一样的解决办法，临时在启动项参数中加入：

```
-Djava.net.preferIPv4Stack=true
```

![](/images/oldposts/11FR3Q.jpg)

问题解决，不过后来笔者有考虑了一下，这样一个一个设置太麻烦了，不如来个全局的，于是笔者在使用的jre上，设置了全局参数。一劳永逸了。：）

![](/images/oldposts/6g8sc.jpg)
