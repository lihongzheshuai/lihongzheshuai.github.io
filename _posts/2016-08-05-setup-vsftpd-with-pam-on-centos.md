---
layout: post
title: CentOS下vsftpd服务配置说明
tags: [Linux]
date: 2016-08-05 09:52:27 +0800
comments: true
author: onecoder
thread_key: 1896
---
项目需要用到分用户的FTP服务器，因此花了一天时间学习了vsftpd服务的搭建和配置说明。记录如下。

<!--break-->

# 安装

```bash
yum install vsftpd ftp
```

# 配置虚拟用户

虚拟用户即可以登录Ftp，不能登录系统。配置原理即开启vsftpd的虚拟用户功能，并配合pam管理用户认证
修改配置文件/etc/vsftpd/vsftpd.conf

```properties
# 关闭匿名访问
anonymous_enable=NO
# 本地用户可访问
local_enable=YES
# 用户不能离开主目录
chroot_local_user=YES
chroot_list_enable=YES
# 开启pam权限管理插件
pam_service_name=vsftpd
#启用虚拟用户
guest_enable=YES
guest_username=ftp
#虚拟用户配置文件路径
user_config_dir=/etc/vsftpd/vuser_conf
#开启PASV模式
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=50000
```

安装Berkeley DB工具，用于PAM模块使用。

```bash
yum install db4 db4-utils
```

创建用户密码文本/etc/vsftpd/vuser_passwd，奇行是用户名，偶行是密码

```text
dps-ftp
dps-ftp
```

## 生成虚拟用户认证的db文件

```bash
db_load -T -t hash -f /etc/vsftpd/vuser_passwd /etc/vsftpd/vuser_passwd.db
```

编辑认证文件/etc/pam.d/vsftpd，内容

```
auth required pam_userdb.so db=/etc/vsftpd/vuser_passwd
account required pam_userdb.so db=/etc/vsftpd/
vuser_passwd
```

创建虚拟用户配置文件

```bash
mkdir /etc/vsftpd/vuser_conf/
vim /etc/vsftpd/vuser_conf/dps-ftp  
```

文件名vuser_passwd里面的账户名
内容如下

```
#虚拟用户根目录,根据实际情况修改
local_root=/root/ftp/dps-ftp  
#可写,否则无法上传文件
write_enable=YES
#掩码
anon_umask=022
anon_world_readable_only=NO
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_other_write_enable=YES
```

注，关于掩码：
umask = 022 时，新建的目录 权限是755，文件的权限是 644

# 后续添加用户方式

1. 在vuser_passwd.txt文件内追加用户名密码。
2. 用db_load重新生成数据库文件
3. 在/etc/vsftpd/vuser_conf/ 创建新用户的配置文件(创建用户目录，给用户目录写和执行全新，修改用户目录路径。)