---
layout: post
title: Windows下Libvirt Java API使用教程 - 开发环境部署
date: 2012-06-19 22:17
author: onecoder
comments: true
tags: [Libvirt]
categories: [Java技术研究,Libvirt]
thread_key: 613
---
 <a href="http://libvirt.org/" target="\_blank">**Libvirt**</a>是一个优秀的虚拟化环境管理的工具包。核心用c实现，不过提供了不同语言的调用API。官网的简介如下：

> libvirt is:
> 
- A toolkit to interact with the virtualization capabilities of recent versions of Linux (and other OSes), see our  <a target="_blank" href="http://libvirt.org/goals.html" >project goals</a> for details.
- Free software available under the  <a target="_blank" href="http://www.opensource.org/licenses/lgpl-license.html">GNU Lesser General Public License</a>.
- A long term stable C API
- A set of bindings for common languages
- A  <a target="_blank" href="http://libvirt.org/CIM/">CIM provider</a> for the DMTF virtualization schema
- A  <a target="_blank" href="http://libvirt.org/qpid/">QMF agent</a> for the AMQP/QPid messaging system
> 
> libvirt supports:
> 
- The <a target="_blank" href="http://libvirt.org/drvqemu.html">KVM/QEMU</a> Linux hypervisor
- The  <a target="_blank" href="http://libvirt.org/drvxen.html">Xen</a> hypervisor on Linux and Solaris hosts.		
- The  <a target="_blank" href="http://libvirt.org/drvlxc.html">LXC</a> Linux container system
- The  <a target="_blank" href="http://libvirt.org/drvopenvz.html">OpenVZ</a> Linux container system
- The  <a target="_blank" href="http://libvirt.org/drvuml.html">User Mode Linux</a> paravirtualized kernel
- The  <a target="_blank" href="http://libvirt.org/drvvbox.html">VirtualBox</a> hypervisor
- The  <a target="_blank" href="http://libvirt.org/drvesx.html">VMware ESX and GSX</a> hypervisors
- The  <a target="_blank" href="http://libvirt.org/drvvmware.html">VMware Workstation and Player</a> hypervisors
- The  <a target="_blank" href="http://libvirt.org/drvhyperv.html">Microsoft Hyper-V</a> hypervisor
- Virtual networks using bridging, NAT, VEPA and VN-LINK.
- Storage on IDE/SCSI/USB disks, FibreChannel, LVM, iSCSI, NFS and filesystems

> libvirt provides:
> 		
- Remote management using TLS encryption and x509 certificates	
- Remote management authenticating with Kerberos and SASL
- Local access control using PolicyKit	
- Zero-conf discovery using Avahi multicast-DNS
- Management of virtual machines, virtual networks and storage
- Portable client API for Linux, Solaris and Windows
	
由于我只是一个简单而纯粹的Java程序员，所以自然只能依赖于libvirt的Java binding api。

作为一个源码控，我选择下载源码的方式验证使用，git仓库：

- git clone git://libvirt.org/libvirt-java.git 

笔者下载源码后，直接构建了Eclipse的工程，当然你也可以用源码编译(**ant**)出一份jar来依赖：

```sh
cd libvirt-java
ant build
```

http://www.libvirt.org/maven2/ 没有Maven？可以直接从Maven库中下载Jar包,如
<a href="http://www.libvirt.org/maven2/org/libvirt/libvirt/" target="_blank">http://www.libvirt.org/maven2/org/libvirt/libvirt/</a>

这么多途径，相信你总可以搞到一份libvirt的源码或者Jar了吧。

由于**libvirt**的核心都是c写的，Java API只是帮助你封装了对动态链接库(dll)文件的本地调用，所以现在应该做的是安装dll文件。libvirt官网提供了自行编译dll文件的脚本：

> The easiest way is to use the msys_setup script, developed by Matthias Bolte. This is actively developed and kept current with libvirt releases, 
> <a target="\_blank" href="https://github.com/photron/msys\_setup">https://github.com/photron/msys\_setup</a> 

不过笔者并没有尝试该种方式，因为libvirt官网也提供了windows下的安装包:	

> A windows installation package is in development. An experimental version is available here:
> <a target="_blank" href="http://libvirt.org/sources/win32_experimental/Libvirt-0.8.8-0.exe">http://libvirt.org/sources/win32_experimental/Libvirt-0.8.8-0.exe</a>
It is not production ready.(注：其并不是已经发布的产品)

该安装包中不仅包含了需要的dll文件，还提供了一个方便好用的virsh-shell 命令行工具，通过命令可以调用libvirt的所有接口(查看，管理虚拟机等。)，对于我们的开发调试是非常有帮助的。

![](/images/post/windows-libvirt/libvirt-cmd.jpg)

安装完成后，想让Java API找到dll文件，还需要指定jna路径，有两种方式，一种是直接设置系统环境变量：

![](/images/post/windows-libvirt/jna-system-environment.jpg)

另一种是可在程序中动态指定，笔者选择了后者，比较灵活简单，编写测试代码如下

```java
public void testGetXenVMs() {
		try {
- System.setProperty("jna.library.path", "D:/Git-Repo/git/libvirt-java/libvirt-java/src/test/java/kubi/coder/");
- Connect conn = new Connect("xen+tcp://10.4.55.203/");
- System.out.println(conn.nodeInfo().cores);
- for (String name : conn.listDefinedDomains()) {
- 	System.out.println(name);
- 	if (name != null) {
- 		Domain domain = conn.domainLookupByName(name);
- 		System.out.println(domain.getMaxMemory());
- 		System.out.println(domain.getUUIDString());
- 		System.out.println(domain.getInfo().maxMem);
- 		System.out.println(domain.getInfo().state);
- 		System.out.println(conn.listDomains().length);
- 	}
- }
		} catch (LibvirtException e) {
- e.printStackTrace();
		}
	}
```

是不是还是找不到dll？报异常

> Exception in thread "main" java.lang.UnsatisfiedLinkError: Unable to load library 'virt'

原来他是搜索叫**virt**的**dll**文件。		

查看源码

```java
Libvirt INSTANCE = (Libvirt) Native.loadLibrary("virt", Libvirt.class);
```

原来如此，将**libvirt-0.dll**改名为**virt.dll**。结果终于出来了。

> 注：libvirt的Java API封装的比较直观，上手很容易，其入口就是Connect 这个连接类，获取连接后，即可对虚拟机环境进行查看和管理操作。笔者后续会奉上Java API详细使用介绍。

