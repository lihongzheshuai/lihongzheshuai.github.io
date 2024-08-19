---
layout: post
title: MySQL 用户并发数限制问题解决
date: 2013-03-15 17:35 +0800
author: onecoder
comments: true
tags: [MySQL]
categories: [知识扩展]
thread_key: 1397
---
<p>
	对MySQL进行并发测试过程中遇到的一个小问题，记录一下。</p>
<p>
	用mysqlslap进行并发访问测试，在1024线程的时候报错：</p>
<blockquote>
	<p>
		bin/mysqlslap: Error when connecting to server: 1135 Can&#39;t create a new thread (errno 11); if you are not out of available memory, you can consult the manual for a possible OS-dependent bug</p>
</blockquote>
<p>
	Linux系统的open files数已经修改。当然仍然报错。ulimit -a命令，可查看当前系统限制情况</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/nlHDT.jpg" style="width: 392px; height: 259px;" /></p>
<p>
	<strong>max user processes = 1024</strong></p>
<br />
<p>
	通过ulimit -u 10000命令修改当前session的限制值，然后重启MySQL，问题解决。如果你想使此值永久生效，可配置在/etc/profile 中。</p>