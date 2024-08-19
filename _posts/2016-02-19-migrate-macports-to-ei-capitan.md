---
layout: post
title: "MacPorts 迁移至 EI Capitan"
date: 2016-02-19 13:58:12 +0800
comments: true
tags: [Mac]
categories: [知识扩展]
thread_key: 1872
---
老版本的MacPorts在EI Capitan下有兼容性问题。今天运行报错如下：

> Error: Current platform "darwin 15" does not match expected platform "darwin 14"
> Error: If you upgraded your OS, please follow the migration instructions: https://trac.macports.org/wiki/Migration
> OS platform mismatch
>     while executing
> "mportinit ui_options global_options global_variations"
> Error: /opt/local/bin/port: Failed to initialize MacPorts, OS platform mismatch

搜索解决方案：
[http://stackoverflow.com/questions/31483432/how-do-i-remove-macports-on-an-unsupported-os-i-e-el-capitan-public-beta](http://stackoverflow.com/questions/31483432/how-do-i-remove-macports-on-an-unsupported-os-i-e-el-capitan-public-beta)

参考之进行重新安装，依次执行命令：

{% highlight bash %}
xcode-select —install
xcodebuild -license
{% endhighlight %}

从官网下载安装包：
[https://www.macports.org/install.php](https://www.macports.org/install.php)

直接利用安装包安装即可。

![](/images/post/macports-install.png)

![](/images/post/macports-version.png)