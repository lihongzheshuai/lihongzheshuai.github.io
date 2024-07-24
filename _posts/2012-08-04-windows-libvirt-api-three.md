---
layout: post
title: Windows下Libvirt Java API使用教程(三)- TLS认证访问和动态连接文件依赖
date: 2012-08-04 23:39 +0800
author: onecoder
comments: true
tags: [Libvirt]
thread_key: 1041
---
突兀的出来一个**libvirt**的教程三，您可能会觉得奇怪，其实这是**OneCoder**以前写的一个小系列教程，原来发在**51cto**的博客上，前两篇已经发了过来，考虑到完整性，就把第三篇也发过来。前两篇地址：
	
- 《<a href="http://www.coderli.com/windows-libvirt-one/" target="\_blank">Windows下Libvirt Java API使用教程 (一) 开发环境部署</a>》
- 《<a href="http://www.coderli.com/windows-libvirt-api-two/" target="\_blank">Windows下Libvirt Java API使用教程(二) 接口使用说明</a>》

之前已经介绍过了libvirt api的上手使用方式，这里再补充一些细节问题。

# TLS安全认证访问：

之前我们给出的例子都是直接用**tcp**访问的，这就需要被访问的服务器开放**tcp**访问的端口，也就是说，任何机器只要知道了服务器的**ip**，都是可以访问上面的**libvirt**接口的。这是十分危险的，在生产环境中是不可取的。

所以，**libvirt**支持基于**tls**认证的安全访问协议。连接格式如下：

```	
qemu+tls://10.4.54.10
或者
qemu://10.4.54.10(因为默认就是走tls的)
```

要想正常访问，必须在客户端和服务端配置证书，下面就介绍一个这个配置过程。
	
1. 首先自然是证书生成工具的安装。**libvirt**官方推荐的工具是：**GnuTLS**。不过可惜，官网给出的地然居然不正确。**GnuTLS**项目，官网地址如下：

- <a href="http://www.gnu.org/software/gnutls/manual/html_node/" target="\_blank">http://www.gnu.org/software/gnutls/manual/html_node/</a>
	
下载页面为：

- <a href="http://www.gnu.org/software/gnutls/download.html" target="\_blank">http://www.gnu.org/software/gnutls/download.html</a>
	
这里介绍的windows环境下配置，所以进入页面：

- <a href="http://homes.esat.kuleuven.be/~nikos/gnutls-win32/" target="\_blank">http://homes.esat.kuleuven.be/~nikos/gnutls-win32/</a>

下载即可。

2. 解压下载的工具。通过命令行进入**\bin**目录(或者将该**bin**目录配置到环境变量的**path**即可在任意路径访问)：

![](/images/oldposts/GyTui.jpg)

3. 首先为你的证书生成私钥：

> Create a private key for your CA:

```bat
certtool --generate-privkey > cakey.pem
```

![](/images/oldposts/15v6oh.jpg)

然后，为你证书进行自签名。

> and self-sign it by creating a file with the signature details called ca.info containing:</p>
	
```bat
cn = Name of your organization
ca
certsigningkey

certtool --generate-self-signed --load-privkey cakey.pem   --template ca.info --outfile cacert.pem (Y)
```

先在当前路径下创建一个叫**ca.info**的文件，里面写上如上第一段内容，

![](/images/oldposts/dcm8W.jpg)

然后执行第二段引用所示命令：
	
![](/images/oldposts/gnutls-bat-console.jpg)	
报错。这下头疼了。。笔者翻箱倒柜，翻江倒海找了一通。。实在没有找到答案。。。考虑到证书的制作过程中没有与机器相关的信息，所以，决定求助笔者非常不熟悉的**linux**。掏出**putty**，登录，重新执行上面第一个命令。生成私钥：

![](/images/oldposts/nT1dV.jpg)

然后同样按照上面的方式进行签名，果然轻松成功！	

![](/images/oldposts/cMkws.jpg)

此时已经可以删除**ca.info**文件了。继续生成证书，接下来开始生成服务端私钥：

```bash
certtool --generate-privkey > serverkey.pem
```

![](/images/oldposts/nT1dV.jpg)

然后签名：

```bash
certtool --generate-certificate --load-privkey serverkey.pem  --load-ca-certificate cacert.pem --load-ca-privkey cakey.pem --template server.info --outfile servercert.pem
```

同样是依靠一个叫做**server.info**的文件。先创建改文件，写入如下格式内容：

```
organization = Name of your organization
cn = oirase
tlswwwserver
encryptionkey
signingkey
```

这里只有cn这个属性需要注意，他应该是当前主机的主机名：（

> only the CN field matters, which as explained above must be the server&#39;s hostname）- (The CN must match the hostname which clients will be using to connect to the server. In the example below, clients will be connecting to the server using a URI of xen://oirase/, so the CN must be &quot;oirase&quot;.)

如果不知道主机名，用ip当然也是可以的。那么你的访问就是通过IP访问了。：）	

![](/images/oldposts/Obxaz.jpg)

成功。

将服务端证书拷贝服务器的相应位置：

<blockquote>
	<p>
		Finally we have two files to install:</p>
	<p>
		serverkey.pem is the server&#39;s private key which should be copied to the server only as /etc/pki/libvirt/private/serverkey.pem.<br />
		servercert.pem is the server&#39;s certificate which can be installed on the server as /etc/pki/libvirt/servercert.pem.</p>
</blockquote>

最后是客户端的证书，过程类似，这里只列出主要过程和命令：

1、创建私钥:


```bash
certtool --generate-privkey > clientkey.pem
```

2、创建client.info模版文件:

```
country = GB
state = London
locality = London
organization = Red Hat
cn = client1
tlswwwclient
encryptionkey
signingkey
```

然后签名:

```bash
certtool --generate-certificate --load-privkey clientkey.pem \
  --load-ca-certificate cacert.pem --load-ca-privkey cakey.pem \
  --template client.info --outfile clientcert.pem
```

3、拷贝证书到客户端的指定位置（**linux**）:

```bash
cp clientkey.pem /etc/pki/libvirt/private/clientkey.pem
cp clientcert.pem /etc/pki/libvirt/clientcert.pem
```

其中**client.info**中国家等信息可根据你的情况指定。

至此，需要的证书已经都准备好了。证书有了，服务端也部署了。但是**windows**的客户端不知道该部署到什么地方？因为网上的说明给出的都是**linux**文件路径，没说**windows**下的情况。不过笔者相信**libvirt**的错误日志：）于是：

![](/images/oldposts/mDDtR.jpg)

怎么样，位置有了吧。赶紧拷贝过去试试。</p>

有的同学可能发现，这里只给出了一个位置，我们有三个证书呢。别急，你看这个路径，比照网上给出的**linux**的路径格式：

<table>
	<tbody>
		<tr>
			<th>
				Location</th>
			<th>
				Machine</th>
			<th>
				Description</th>
			<th>
				Required fields</th>
		</tr>
		<tr>
			<td>
				/etc/pki/CA/cacert.pem</td>
			<td>
				Installed on all clients and servers</td>
			<td>
				CA&#39;s certificate (<a href="http://libvirt.org/remote.html#Remote_TLS_CA">more info</a>)</td>
			<td>
				n/a</td>
		</tr>
		<tr>
			<td>
				/etc/pki/libvirt/ private/serverkey.pem</td>
			<td>
				Installed on the server</td>
			<td>
				Server&#39;s private key (<a href="http://libvirt.org/remote.html#Remote_TLS_server_certificates">more info</a>)</td>
			<td>
				n/a</td>
		</tr>
		<tr>
			<td>
				/etc/pki/libvirt/ servercert.pem</td>
			<td>
				Installed on the server</td>
			<td>
				Server&#39;s certificate signed by the CA. (<a href="http://libvirt.org/remote.html#Remote_TLS_server_certificates">more info</a>)</td>
			<td>
				CommonName (CN) must be the hostname of the server as it is seen by clients.</td>
		</tr>
		<tr>
			<td>
				/etc/pki/libvirt/ private/clientkey.pem</td>
			<td>
				Installed on the client</td>
			<td>
				Client&#39;s private key. (<a href="http://libvirt.org/remote.html#Remote_TLS_client_certificates">more info</a>)</td>
			<td>
				n/a</td>
		</tr>
		<tr>
			<td>
				/etc/pki/libvirt/ clientcert.pem</td>
			<td>
				Installed on the client</td>
			<td>
				Client&#39;s certificate signed by the CA (<a href="http://libvirt.org/remote.html#Remote_TLS_client_certificates">more info</a>)</td>
			<td>
				Distinguished Name (DN) can be checked against an access control list (tls_allowed_dn_list).</td>
		</tr>
	</tbody>
</table>

其实基本已经可以猜出**windows**下的目录组织了。**linux**在的**/etc**目录，就想当于我们这里的**..\libvirt**目录，子目录的组织相同即可。

没猜出来也不用担心，最多我们复制一个证书尝试一次，错误信息会依次告诉你所有的路径的：）

再访问一下，成功~

![](/images/oldposts/5WsWD.jpg)

补充说明一下关于动态链接文件的问题:

之前介绍的时候，笔者只提到说调用**libvirt Java api**需要一个**virt.dll**文件，这个文件笔者是拷贝的**libvirt-0.dll**文件改名而来，然后访问成功。

笔者后来发现，原来**libvirt** 安装目录的bin文件夹下的所有文件，其实都是该**dll**文件的依赖文件，当笔者将其他文件删除或转义的时候，依然会报找不到**virt.dll**文件的错误。所以，如果调用**libvirt** **Java API**开发，可以将所有的**dll**拷贝到一个指定位置，然后指定**jna.library.path**到该位置即可。