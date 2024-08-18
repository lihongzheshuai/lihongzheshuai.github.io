---
layout: post
title: JZMQ环境变量配置说明 ZeroMQ Java Binding
date: 2014-01-24 17:18 +0800
author: onecoder
comments: true
tags: [ZeroMQ]
thread_key: 1627
---
<p>
	在考虑使用ZeroMQ时，灵活夸平台使用的问题。除了要在编译不同平台的版本，还需要在不同的平台下，进行相应的环境变量的配置。简要说明一下：<br />
	首先，对于JNI调用来说，不论什么平台都需要指定本地动态链接库的位置，指向包含动态链接库的文件夹：</p>

```bash
-Djava.library.path=XXX
```

<p>
	不过光这样是不够的，因为底层C/C++ 库之间也需要知道彼此的位置，这就需要指定库的地址：<br />
	<br />
	Windows，配置path环境变量</p>

```bash
set path=%path%;XXX
```

<p>
	Linux，配置LD_LIBRARY_PATH环境变量</p>

```bash
export LD_LIBRARY_PATH=XXX
```

<p>
	基本就ok了。还有一点略微奇怪的是，在OneCoder这里，windows下需要两个dll文件。jzmq.dl和libzmq.dll，但是在linux下核心文件虽然还是两个libjzmq.so和libzmq.so和libzmq.so.3文件(这里，我使用的是ZeroMQ3.2.4的源码编译)。否则总会报找不到libzmq.so.3这个文件的错误。不知道具体原因。<br />
	&nbsp;</p>

