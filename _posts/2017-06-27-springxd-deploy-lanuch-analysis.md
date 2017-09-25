---
layout: post
title: SpringXD 任务、启动消息通信代码流程分析
tags: [SpringXD]
date: 2017-06-27 10:29:18 +0800
comments: true
author: onecoder
thread_key: 1908
---
# 通信流程概括

* 任务部署时，xd-admin和container之间通过zookeeper的节点监听通信。container监听zk deployment节点，执行部署。同事绑定kafka message consumer和reactor subscriber。
* 任务启动时，xd-admin和container通过kafka通信。container端消费到kafka的message，然后通过reactor的事件机制转发处理。

<!--break-->

![](/images/post/xd-deploy-launch/job-deploy-launch.png)