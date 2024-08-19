---
layout: post
title: Windows下Libvirt Java API使用教程(二)- 接口使用说明
date: 2012-06-21 23:05 +0800
author: onecoder
comments: true
tags: [Libvirt]
categories: [Java技术研究,Libvirt]
thread_key: 624
---
介绍完<a href="http://www.coderli.com/windows-libvirt-one" target="/_blank">libvirt Java API的部署工作</a>，接下来我们就介绍一下接口的使用和代码样例。

**libvirt**的管理单位是单个主机，所以探测和监控接口所能获取的信息的最大范围也是主机。所以先从主机入手，验证libvirt接口。主机（libvirt所在管理节点）探测相关接口验证代码如下：

```java
   @Before
	public void init() {
		System.setProperty("jna.library.path",
				"D:/Git-Repo/git/libvirt-java/libvirt-java/src/test/java/kubi/coder/");
		try {
			xenConn = new Connect("xen+tcp://10.4.55.203/");
			// system代表拥有系统权限/session是用户权限
			kvmConn = new Connect("qemu+tcp://10.4.54.10/system");
		} catch (LibvirtException e) {
			e.printStackTrace();
		}
	}

	/**
	 * 主机信息探测接口验证，验证可以获取的主机属性和监控指标，分别考虑Xen环境和KVM环境
	 * 
	 * 
	 * @author lihzh
	 * @date 2012-5-15 下午1:28:00
	 */
	@Test
	public void testDetectHost() {
		// KVM
		doDetectHost(kvmConn);
		// XEN
		doDetectHost(xenConn);
	}

	/**
	 * 执行探测主机测试函数
	 * 
	 * @param conn
	 * @author lihzh
	 * @date 2012-5-15 下午1:37:37
	 */
	private void doDetectHost(Connect conn) {
		try {
			// Returns the free memory for the connection
			// System.out.println("FreeMemory: " + conn.getFreeMemory());// 不支持
			
			// Returns the system hostname on which the hypervisor is running.
			// (the result of the gethostname(2) system call)
			// If we are connected to a remote system,
			// then this returns the hostname of the remote system
			System.out.println("Host name: " + conn.getHostName());
			// Gets the name of the Hypervisor software used.
			System.out.println("Type: " + conn.getType());
			// Gets the version level of the Hypervisor running. This may work
			// only with hypervisor call, i.e. with priviledged access to the
			// hypervisor, not with a Read-Only connection. If the version can't
			// be extracted by lack of capacities returns 0.
			// Returns:
			// major * 1,000,000 + minor * 1,000 + release
			System.out.println(conn.getVersion());

			NodeInfo nodeInfo = conn.nodeInfo();
			System.out.println("the number of active CPUs: " + nodeInfo.cpus);
			System.out.println("number of core per socket: " + nodeInfo.cores);
			System.out.println("memory size in kilobytes: " + nodeInfo.memory);
			System.out.println("expected CPU frequency: " + nodeInfo.mhz);
			System.out.println("string indicating the CPU model: "
					+ nodeInfo.model);
			System.out.println("the number of NUMA cell, 1 for uniform: "
					+ nodeInfo.nodes);
			System.out.println("number of CPU socket per node: "
					+ nodeInfo.sockets);
			System.out.println("number of threads per core: "
					+ nodeInfo.threads);
			System.out
					.println("the total number of CPUs supported but not necessarily active in the host.: "
							+ nodeInfo.maxCpus());

			// for (String interName : conn.listInterfaces()) {
			// System.out.println(interName);
			// } 不支持

			// Provides the list of names of defined interfaces on this host

			// for (String interName : conn.listDefinedInterfaces()) {
			// System.out.println(interName);
			// } // 不支持

			// Lists the active networks.
			for (String networkName : conn.listNetworks()) {
				System.out.println("Network name: " + networkName);
			}

			// Lists the names of the network filters
			for (String networkFilterName : conn.listNetworkFilters()) {
				System.out.println("Network filter name: " + networkFilterName);
			}

			System.out.println(conn.getCapabilities());
		} catch (LibvirtException e) {
			e.printStackTrace();
		}
	}
```

分别在KVM和XEN环境下测试了libvirt接口，测试结果如下：

```xml
Host name: s5410
Type: QEMU
9001
the number of active CPUs: 64
number of core per socket: 8
memory size in kilobytes: 49444896
expected CPU frequency: 2131
string indicating the CPU model: x86_64
the number of NUMA cell, 1 for uniform: 1
number of CPU socket per node: 4
number of threads per core: 2
the total number of CPUs supported but not necessarily active in the host.: 64
Network name: hello
Network name: default
Network filter name: no-other-l2-traffic
Network filter name: allow-dhcp
Network filter name: allow-dhcp-server
Network filter name: no-other-rarp-traffic
Network filter name: no-mac-spoofing
Network filter name: qemu-announce-self-rarp
Network filter name: clean-traffic
Network filter name: no-arp-spoofing
Network filter name: allow-ipv4
Network filter name: no-ip-spoofing
Network filter name: qemu-announce-self
Network filter name: allow-arp
Network filter name: no-mac-broadcast
Network filter name: allow-incoming-ipv4
Network filter name: no-ip-multicast
<capabilities>

  <host>
    <uuid>30b940dd-f79a-21a2-82d5-ddc1b1b4a7e4</uuid>
    <cpu>
      <arch>x86_64</arch>
      <model>core2duo</model>
      <topology sockets='4' cores='8' threads='2'/>
      <feature name='lahf_lm'/>
      <feature name='rdtscp'/>
      <feature name='pdpe1gb'/>
      <feature name='popcnt'/>
      <feature name='x2apic'/>
      <feature name='sse4.2'/>
      <feature name='sse4.1'/>
      <feature name='dca'/>
      <feature name='xtpr'/>
      <feature name='cx16'/>
      <feature name='tm2'/>
      <feature name='est'/>
      <feature name='vmx'/>
      <feature name='ds_cpl'/>
      <feature name='pbe'/>
      <feature name='tm'/>
      <feature name='ht'/>
      <feature name='ss'/>
      <feature name='acpi'/>
      <feature name='ds'/>
    </cpu>
    <migration_features>
      <live/>
      <uri_transports>
        <uri_transport>tcp</uri_transport>
      </uri_transports>
    </migration_features>
  </host>

  <guest>
    <os_type>hvm</os_type>
    <arch name='i686'>
      <wordsize>32</wordsize>
      <emulator>/usr/libexec/qemu-kvm</emulator>
      <machine>rhel5.4.0</machine>
      <machine canonical='rhel5.4.0'>pc</machine>
      <machine>rhel5.4.4</machine>
      <machine>rhel5.5.0</machine>
      <machine>rhel5.6.0</machine>
      <domain type='qemu'>
      </domain>
      <domain type='kvm'>
        <emulator>/usr/libexec/qemu-kvm</emulator>
      </domain>
    </arch>
    <features>
      <cpuselection/>
      <pae/>
      <nonpae/>
      <acpi default='on' toggle='yes'/>
      <apic default='on' toggle='no'/>
    </features>
  </guest>

  <guest>
    <os_type>hvm</os_type>
    <arch name='x86_64'>
      <wordsize>64</wordsize>
      <emulator>/usr/libexec/qemu-kvm</emulator>
      <machine>rhel5.4.0</machine>
      <machine canonical='rhel5.4.0'>pc</machine>
      <machine>rhel5.4.4</machine>
      <machine>rhel5.5.0</machine>
      <machine>rhel5.6.0</machine>
      <domain type='qemu'>
      </domain>
      <domain type='kvm'>
        <emulator>/usr/libexec/qemu-kvm</emulator>
      </domain>
    </arch>
    <features>
      <cpuselection/>
      <acpi default='on' toggle='yes'/>
      <apic default='on' toggle='no'/>
    </features>
  </guest>

</capabilities>

Host name: s55203
Type: Xen
3001000
the number of active CPUs: 32
number of core per socket: 8
memory size in kilobytes: 50276352
expected CPU frequency: 1995
string indicating the CPU model: x86_64
the number of NUMA cell, 1 for uniform: 1
number of CPU socket per node: 2
number of threads per core: 2
the total number of CPUs supported but not necessarily active in the host.: 32
Network name: default
Network filter name: allow-dhcp-server
Network filter name: qemu-announce-self-rarp
Network filter name: no-arp-spoofing
Network filter name: allow-arp
Network filter name: no-ip-multicast
Network filter name: no-other-rarp-traffic
Network filter name: allow-incoming-ipv4
Network filter name: no-mac-spoofing
Network filter name: allow-ipv4
Network filter name: no-ip-spoofing
Network filter name: clean-traffic
Network filter name: qemu-announce-self
Network filter name: no-other-l2-traffic
Network filter name: allow-dhcp
Network filter name: no-mac-broadcast
<capabilities>

  <host>
    <cpu>
      <arch>x86_64</arch>
      <features>
        <vmx/>
      </features>
    </cpu>
    <migration_features>
      <live/>
      <uri_transports>
        <uri_transport>xenmigr</uri_transport>
      </uri_transports>
    </migration_features>
  </host>

  <guest>
    <os_type>xen</os_type>
    <arch name='x86_64'>
      <wordsize>64</wordsize>
      <emulator>/usr/lib64/xen/bin/qemu-dm</emulator>
      <machine>xenpv</machine>
      <domain type='xen'>
      </domain>
    </arch>
  </guest>

  <guest>
    <os_type>xen</os_type>
    <arch name='i686'>
      <wordsize>32</wordsize>
      <emulator>/usr/lib64/xen/bin/qemu-dm</emulator>
      <machine>xenpv</machine>
      <domain type='xen'>
      </domain>
    </arch>
    <features>
      <pae/>
    </features>
  </guest>

  <guest>
    <os_type>hvm</os_type>
    <arch name='i686'>
      <wordsize>32</wordsize>
      <emulator>/usr/lib64/xen/bin/qemu-dm</emulator>
      <loader>/usr/lib/xen/boot/hvmloader</loader>
      <machine>xenfv</machine>
      <domain type='xen'>
      </domain>
    </arch>
    <features>
      <pae/>
      <nonpae/>
      <acpi default='on' toggle='yes'/>
      <apic default='on' toggle='yes'/>
    </features>
  </guest>

  <guest>
    <os_type>hvm</os_type>
    <arch name='x86_64'>
      <wordsize>64</wordsize>
      <emulator>/usr/lib64/xen/bin/qemu-dm</emulator>
      <loader>/usr/lib/xen/boot/hvmloader</loader>
      <machine>xenfv</machine>
      <domain type='xen'>
      </domain>
    </arch>
    <features>
      <acpi default='on' toggle='yes'/>
      <apic default='on' toggle='yes'/>
    </features>
  </guest>

</capabilities>
```

> - 注1：标注不支持的，是在当前环境当前libvirt版本下，运行会报：
***unsupported in sys interface***的接口。
> - 注2：名词解释
	- **hvm**:gives similar information but when running a 32 bit OS fully virtualized with Xen using the hvm support。
	- **numa**：For processors that support hyperthreading, this is the number of hyperthreads
they have per core.  On a machine that doesn't support hyperthreading, this
will be 1.

说实话，这么多信息中，笔者关注的不多，有很多甚至说不出其代表的含义，笔者关注只是cpu的个数，核心数，内存总量等直观信息。有就足以。

看完了主机，再看看虚拟机。一个虚拟化环境中的核心资源自然是虚拟机，所以其属性和信息也自然多很多，上测试代码：

```java
/**
	 * 测试探测虚拟机接口
	 * 
	 * @author lihzh
	 * @date 2012-5-16 上午11:14:20
	 */
	@Test
	public void testDetectDomains() {
		// KVM
		doDetectDomains(kvmConn);
		// XEN
		doDetectDomains(xenConn);
	}

        /**
	 * 执行探测虚拟机测试函数
	 * 
	 * @param conn
	 * @author lihzh
	 * @date 2012-5-16 上午11:15:27
	 */
	private void doDetectDomains(Connect conn) {
		try {
			// Lists the active domains.(列出所有处于启动(激活)状态的虚拟机的id)
			for (int activeDomId : conn.listDomains()) {
				System.out.println("Active vm id: " + activeDomId);
				// 根据Id，探测各个虚拟机的详细信息
				Domain domain = conn.domainLookupByID(activeDomId);
				// Gets the hypervisor ID number for the domain
				System.out.println("Domain id: " + domain.getID());
				// Gets the public name for this domain
				System.out.println("Domain name: " + domain.getName());
				// Gets the type of domain operation system.
				System.out.println("Domain os type: " + domain.getOSType());
				// Gets the UUID for this domain as string.
				System.out.println("Domain uuid: " + domain.getUUIDString());
				// Retrieve the maximum amount of physical memory allocated to a
				// domain.
				System.out.println("Domain max memory: "
						+ domain.getMaxMemory());
				// Provides the maximum number of virtual CPUs supported for the
				// guest VM. If the guest is inactive, this is basically the
				// same as virConnectGetMaxVcpus. If the guest is running this
				// will reflect the maximum number of virtual CPUs the guest was
				// booted with.
				System.out.println("Domain max vcpu: " + domain.getMaxVcpus());
				// Provides an XML description of the domain. The description
				// may be
				// reused later to relaunch the domain with createLinux().
				System.out.println("Domain xml description: "
						+ domain.getXMLDesc(0));
				System.out.println("Domain maxMen allowed: "
						+ domain.getInfo().maxMem);
				System.out.println("Domain memory: " + domain.getInfo().memory);
				// domain.getJobInfo()
				// 不支持
				System.out.println("Domain state: " + domain.getInfo().state);
				// Provides a boolean value indicating whether the network is
				// configured to be automatically started when the host machine
				// boots.
				System.out.println("Domain network autostart: "
						+ domain.getAutostart());
				// Extracts information about virtual CPUs of this domain
				for (VcpuInfo vcpuInfo : domain.getVcpusInfo()) {
					System.out.println("cpu: " + vcpuInfo.cpu);
					System.out.println("cpu time: " + vcpuInfo.cpuTime);
					System.out.println("cpu number: " + vcpuInfo.number);
					System.out.println("cpu state: " + vcpuInfo.state);
				}
			
				// 如果是KVM环境
				if (conn.getURI().startsWith("qemu")) {
					// This function returns block device (disk) stats for block
					// devices attached to the domain
					DomainBlockInfo blockInfo = domain
							.blockInfo("/opt/awcloud/instance/admin/"
									+ domain.getName() + "/disk");
					System.out.println("Disk Capacity: "
							+ blockInfo.getCapacity());
					System.out.println("Disk allocation: "
							+ blockInfo.getAllocation());
					System.out.println("Disk physical: "
							+ blockInfo.getPhysical());

					DomainBlockStats blockStats = domain.blockStats("vda");
					// 磁盘读取请求总数
					System.out.println("read request num: " + blockStats.rd_req);
					// 磁盘读取总bytes数
					System.out.println("read request num: " + blockStats.rd_bytes);
					// 磁盘写入请求总数
					System.out.println("read request num: " + blockStats.wr_req);
					// 磁盘写入总bytes数
					System.out.println("read request num: " + blockStats.wr_bytes);
				}

			}
			
			// 列出所有停止态的虚拟机
			for (String name : conn.listDefinedDomains()) {
				System.out.println("Inactive domain name: " + name);
			}

		} catch (LibvirtException e) {
			e.printStackTrace();
		}
	}

```

循环较多，摘取部分测试结果如下：

```xml
Active vm id: 53
Domain id: 53
Domain name: i-546A099E
Domain os type: hvm
Domain uuid: e608560a-2c03-8e48-2e60-d0d01693f530
Domain max memory: 147456
Domain max vcpu: 1
Domain xml description: <domain type='xen' id='53'>
  <name>i-546A099E</name>
  <uuid>e608560a-2c03-8e48-2e60-d0d01693f530</uuid>
  <memory>131072</memory>
  <currentMemory>131072</currentMemory>
  <vcpu>1</vcpu>
  <os>
    <type>hvm</type>
    <loader>/usr/lib/xen/boot/hvmloader</loader>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
    <emulator>/usr/lib64/xen/bin/qemu-dm</emulator>
    <disk type='file' device='disk'>
      <driver name='file'/>
      <source file='/opt/awcloud/instance/admin/i-546A099E/disk'/>
      <target dev='hda' bus='ide'/>
    </disk>
    <disk type='file' device='disk'>
      <driver name='file'/>
      <source file='/opt/awcloud/instance/admin/i-546A099E/disk2'/>
      <target dev='hdb' bus='ide'/>
    </disk>
    <interface type='bridge'>
      <mac address='d0:0d:54:6a:09:9e'/>
      <source bridge='xenbr0'/>
      <script path='vif-bridge'/>
      <target dev='vif53.0'/>
    </interface>
    <serial type='file'>
      <source path='/opt/awcloud/instance/admin/i-546A099E/console.log'/>
      <target port='0'/>
    </serial>
    <console type='file'>
      <source path='/opt/awcloud/instance/admin/i-546A099E/console.log'/>
      <target port='0'/>
    </console>
    <input type='tablet' bus='usb'/>
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='17237' autoport='no'/>
  </devices>
</domain>

Domain maxMen allowed: 147456
Domain memory: 139140
Domain state: VIR_DOMAIN_BLOCKED
Domain network autostart: false
cpu: 31
cpu time: 2225977676675
cpu number: 0
cpu state: VIR_VCPU_BLOCKED
Domain network autostart: false
Inactive domain name: i-46A70811
Inactive domain name: i-38C20705
Inactive domain name: i-498E09B2
Inactive domain name: null
Inactive domain name: null
Inactive domain name: null
Inactive domain name: null
Inactive domain name: null
```

结果分析：
结果中基本包含了一个虚拟机组成的全部元素信息。如果你想做一个监控系统，你可以发现这里有

- 虚拟机的名字
- 虚拟机的Id
- 虚拟机的内存大小
- 虚拟CPU个数
- 虚拟机磁盘文件信息，磁盘文件的大小。甚至包括log等信息。
- 虚拟磁盘读写速率。
- 虚拟机网络设备信息。Mac地址，设备类型等。
- 虚拟机网卡读写速率。

基本可以满足一个监控系统的需求。
解释一下上面的测试代码。libvirt Java API的入口基本都是通过**Connect**这个类，也就是首先建立与被管理主机之间的连接

```java
Connect kvmConn = new Connect("qemu+tcp://10.4.54.10/system");
```

然后通过该连接获取信息：

```java
conn.listDomains()
```

一个接口的如果需要接受参数：

```java
conn.domainLookupByID(activeDomId)
```

肯定可以从其他的接口返回中找到答案：

```
for (int activeDomId : conn.listDomains())
```

只是有的获取的直接，有可能需要解析xml格式的返回值来获取需要参数值。比如：**disk**的**path**和**interface**的**path**。
最后再简单介绍一下管控接口：

```java
  /**
	 * 测试虚拟机的简单操作
	 * 
	 * @author lihzh
	 * @date 2012-5-16 下午3:35:43
	 */
	@Test
	public void testControlVM() {
		try {
			Domain domain = kvmConn.domainLookupByID(8);
			System.out.println("Domain state: " + domain.getInfo().state);
			domain.suspend();
			System.out.println("Domain state: " + domain.getInfo().state);
			for (int i = 0; i < 5; i++) {
				System.out.println("wait for: " + (5 - i));
				Thread.sleep(1000);
			}
			System.out.println("Resume vm.");
			domain.resume();
			System.out.println("Domain state: " + domain.getInfo().state);
		} catch (LibvirtException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
```

该用例主要测试了虚拟机的挂起和恢复操作。这类操作是比较简单的（因为无需参数）。一个复杂系统肯定需要包括虚拟机创建等操作。libvirt主要通过xml表述来创建资源，首先需要生成被创建虚拟机的完整描述，然后传递给创建的方法即可。描述的格式？呵呵，自然是上面测试结果给出的数据了。有兴趣的，大家可以自己尝试一下。libvirt的文档，还不完善，不过对于创建这样重要的功能，还是给出了说明。大家也可以下载官方的手册作为参考。

好了，相对于**VMware**、**Xenserver**等虚拟化平台的SDK，libvirt的Java API还是比较简单的，上手很快，结构很简单。当然，功能上可能还是有所欠缺，信息量上，没有其他的那么充足。基于XML的方式操作资源，减少了接口的个数，使调用更直接，但是对开发人员却增加了困难。不过仍不失为一个不错的虚拟机环境操作的API，尤其是针对KVM/XEN的环境来说，可谓不二的选择。