---
layout: post
title: Docker下搭建DNS服务器dnsmasq
tags: [docker]
date: 2016-04-15 14:52:42 +0800
comments: true
thread_key: 1889
---
为方便Hadoop集群管理，决定利用docker环境手动搭建一个DNS服务器。

### 1. 配置容器

选择**andyshinn/dnsmasq**的docker镜像，2.75版本。执行命令

```sh
docker run -d -p 53:53/tcp -p 53:53/udp --cap-add=NET_ADMIN --name dns-server andyshinn/dnsmasq:2.75
```

本以为顺利完成，结果报错：

> docker: Error response from daemon: failed to create endpoint dns-server on network bridge: Error starting userland proxy: listen tcp 0.0.0.0:53: bind: address already in use.

dns服务默认是用的53端口被占用了。查看本机端口占用情况：

```sh
netstat -lnp|grep 53
```

发现在宿主机器上有一个**dnsmasq**服务。google一番了解到，原来是**ubuntu**默认安装了**dnsmasq-base**服务。官网提到：

> Note that the package "dnsmasq" interferes with Network Manager which can use "dnsmasq-base" to provide DHCP services when sharing an internet connection. Therefore, if you use network manager (fine in simple set-ups only), then install dnsmasq-base, but not dnsmasq. If you have a more complicated set-up, uninstall network manager, use dnsmasq, or similar software (bind9, dhcpd, etc), and configure things by hand.

通过kill 停掉该服务。再次执行上述命令，通过

```sh
docker ps
```

查看，容器启动成功。

![](/images/post/docker-dnsmasq/start-container.png)

### 2. 配置DNS服务

进入容器

```sh
docker exec -it dns-server /bin/sh
```

首先配置上行的真正的dns服务器地址，毕竟你只是个本地代理，不了解外部规则。创建文件：

```sh
vi /etc/resolv.dnsmasq
```

添加内容：

```text
nameserver 114.114.114.114
nameserver 8.8.8.8
```

配置本地解析规则，这才是我们的真实目的。新建配置文件

```sh
vi /etc/dnsmasqhosts
```

添加解析规则

```text
172.20.2.14 master
172.20.2.15 slave15
172.20.2.16 slave16
```

修改dnsmasq配置文件，指定使用上述两个我们自定义的配置文件

```sh
vi /etc/dnsmasq.conf
```

修改下述两个配置

```text
resolv-file=/etc/resolv.dnsmasq
addn-hosts=/etc/dnsmasqhosts
```

回到宿主，重启dns-server容器服务。

```sh
docker restart dns-server
```

通过本机验证

修改本机dns服务器地址：

![](/images/post/docker-dnsmasq/config-dns.png)

通过dig命令查看

```sh
dig master
```

![](/images/post/docker-dnsmasq/dig-console.png)

一切如愿。