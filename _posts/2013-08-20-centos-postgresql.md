---
layout: post
title: CentOS下 PostgreSQL部署记录
date: 2013-08-20 21:05 +0800
author: onecoder
comments: true
tags: [PostgreSQL]
categories: [知识扩展]
thread_key: 1489
---
MySQL License收费的问题越来越现实了。PostgreSQL成了最好的替代方案。

部署环境：CentOS6.3 x64。PostgreSQL版本：9.2.4-1。

CentOS的Develop包模式行可能已经带了PostgreSQL数据库，不过版本较老，这里还是要全新部署一个。官网提供了很多的部署方式，这里笔者选择的是命令行交互的离线安装包的方式，因为可以脱离网络和操作系统UI进行安装，比较贴近生产环境。

离线包下载地址：

* [http://community.openscg.com/se/postgresql/packages.jsp](http://community.openscg.com/se/postgresql/packages.jsp)

下载好对应操作系统的包，赋予执行权限，执行即可完成安装。安装期间会交互的让你设置一些默认的存放目录，如果没有特殊要求，默认回车即可。

安装很快即可完成。

**启动数据库**

不能使用root用户启动，需要使用安装时新创建的用户，默认为postgres。

```bash
bin>postgres -D data
```

-D 为指定配置文件和数据存放目录。该目录须存在且包含postgres.conf配置文件。按照上面的方式安装后，只要指定为安装目录下的data文件夹即可。

如果不存在，则需要初始化该目录。

```bash
>initdb -D 目录
```

如果需要远程连接访问该数据库，需要修改**pg_hba.conf**文件，给指定的主机和ip开发访问权限。其实影响访问的还有**postgresql.conf**中的配置，不过默认是开放了权限的。

<img alt="" src="/images/oldposts/KjsPD.jpg" style="width: 630px; height: 461px;" />

启动后可通过

```bash
>psql
```

客户端连接到数据库，查看数据库信息。具体命令可通过help查看。

<img alt="" src="/images/oldposts/Z650t.jpg" style="width: 630px; height: 459px;" />

