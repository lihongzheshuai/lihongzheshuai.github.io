---
layout: post
title: MMM （Multi-Master Replication Manager for MySQL）MySQL集群简介
date: 2013-01-05 09:43
author: onecoder
comments: true
categories: [BigData, Cluster, MMM, mysql, 集群]
---
<p>
	<a href="http://www.coderli.com">OneCoder</a>最近在关注一些基于MySQL的数据库集群方案。不过目前只是一些表面的搜集和粗浅的了解，还没有亲身试用。</p>
<p>
	这次我们了解的是：Multi-Master Replication Manager for MySQL，官网地址：<a href="http://mysql-mmm.org/">http://mysql-mmm.org/</a><br />
	&nbsp;<br />
	<strong>MMM简介：</strong></p>
<p>
	MMM(<strong>M</strong>ulti-<strong>M</strong>aster Replication <strong>M</strong>anager for MySQL，多主控复制管理MySQL集群)&nbsp; 是一组主-主配置复制的可监控/故障恢复的灵活的MySQL集群。<br />
	MMM同样可以读取有任意数量从节点的负载均衡的主/从配置，因此您可以利用它来在一组服务器之间根据他们是否有复制滞后来移动虚拟IP。</p>
<p>
	<br />
	<strong>一些典型用例：</strong></p>
<p>
	<em>双节点配置：</em></p>
<p style="text-align: center; ">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CxGOVHTF/j3g2R.png" /></p>
<br />
<p>
	在双节点主-主配置中，MMM使用5个IP，每个节点有一个永久不变的IP，2个只读IP和一个写IP。后三个IP根据节点的可用情况进行迁移。</p>
<p>
	通常情况下（没有复制失败，没有复制延迟等），活动的主节点有两个IP（读和写），备用主有一个读IP。在失效的情况下，读写都会迁移到可用节点。</p>
<p>
	<em>双主 + 一/多从节点：</em></p>
<p style="text-align: center; ">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/CxGOW4jO/w4oAN.png" /></p>
<p>
	<strong>部署需求</strong></p>
<p>
	对于在有N个服务器节点的MySQL上来部署MMM来说，你需要：</p>
<p>
	<em>n + 1 个主机</em></p>
<p>
	每个MySQL需要需要个主机(n个); MMM 监控一个主机。</p>
<p>
	<br />
	<em>2 * (n + 1) 个IP</em><br />
	每个主机一个IP(n+1个，同上); 写节点一个IP; 每个主机一个读节点，需要n个ip。</p>
<p>
	<em>监控用户</em><br />
	一个拥有REPLICATION CLIENT 权限的MySQL用户，用于MMM 监控。</p>
<p>
	<em>代理用户</em><br />
	一个拥有 SUPER, REPLICATION CLIENT, PROCESS 权限的MySQL用户，用于MMM代理。</p>
<p>
	<em>复制用户</em><br />
	一个拥有 REPLICATION SLAVE 权限的MySQL用户用于复制。</p>
<p>
	<em>工具用户</em><br />
	一个拥有 SUPER, REPLICATION CLIENT, RELOAD 权限的MySQL用户，用于MMM 工具。</p>

