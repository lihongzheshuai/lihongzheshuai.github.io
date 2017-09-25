---
layout: post
title: Eclipse小技巧 增加JVM参数显示状态条
date: 2012-08-01 21:15 +0800
author: onecoder
comments: true
tags: [Eclipse]
thread_key: 1024
---
动手来为你的**Eclipse**增加一个能显示当前**Eclipse**使用的**JVM**配置的工具条吧。简单的很。

![](http://onecoder.qiniudn.com/8wuliao/C9QumDdk/uVp7a.jpg)

在eclipse根目录下建立一个文件，文件名options,不要加后缀直接保存，文件内容

```properties
org.eclipse.ui/perf/showHeapStatus=true
```

![](http://onecoder.qiniudn.com/8wuliao/C9Qun4SJ/ZlXDP.jpg)

修改eclipse目录下的eclipse.ini文件，在文件起始部分添加如下内容：

```text
-debug
options
-vm
javaw.exe
```

![](http://onecoder.qiniudn.com/8wuliao/C9QumOB6/x4STk.jpg)

重启即可。

