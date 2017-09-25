---
layout: post
title: Github时区问题 新文章无法显示
tags: [github,time,jekyll]
date: 2016-03-03 13:30:36 +0800
comments: true
thread_key: 1878
---

昨天把博客迁移到Github，本来一切安好。今天就遇到新发的文章在列表上刷不出来，把github的help都快翻烂了，也没找到解决方案，还给github的support发了邮件。。。

偶然在Jekyll官网的3.0升级指南里，看到一个关于时区问题的说明。给头里的date部分加上了+0800是时区标识。

> date: 2016-03-03 13:30:36 +0800

文章奇迹的出现了。。。

把程序也做了相应的修改，还发现了一个关于时间的大Bug。。

希望一切幸运吧……


