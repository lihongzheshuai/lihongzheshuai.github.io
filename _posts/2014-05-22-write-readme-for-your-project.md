---
layout: post
title: 为项目编写Readme.MD文件
date: 2014-05-22 00:27 +0800
author: onecoder
comments: true
tags: [Markdown]
thread_key: 1653
---
<p>
	了解一个项目，恐怕首先都是通过其Readme文件了解信息。如果你以为Readme文件都是随便写写的那你就错了。github，oschina git gitcafe的代码托管平台上的项目的Readme.MD文件都是有其特有的语法的。称之为Markdown语法。基本规则如下：</p>
<blockquote>
	<p>
		Markdown 语法速查表<br />
		1 标题与文字格式<br />
		标题<br />
		# 这是 H1 &lt;一级标题&gt;<br />
		## 这是 H2 &lt;二级标题&gt;<br />
		###### 这是 H6 &lt;六级标题&gt;<br />
		文字格式<br />
		**这是文字粗体格式**<br />
		*这是文字斜体格式*<br />
		~~在文字上添加删除线~~<br />
		2 列表<br />
		无序列表<br />
		* 项目1<br />
		* 项目2<br />
		* 项目3<br />
		有序列表<br />
		1. 项目1<br />
		2. 项目2<br />
		3. 项目3<br />
		&nbsp;&nbsp; * 项目1<br />
		&nbsp;&nbsp; * 项目2<br />
		3 其它<br />
		图片<br />
		![图片名称](http://gitcafe.com/image.png)<br />
		链接<br />
		[链接名称](http://gitcafe.com)<br />
		引用<br />
		&gt; 第一行引用文字<br />
		&gt; 第二行引用文字<br />
		水平线<br />
		***<br />
		代码<br />
		`&lt;hello world&gt;`<br />
		代码块高亮<br />
		```ruby<br />
		&nbsp; def add(a, b)<br />
		&nbsp; &nbsp; return a + b<br />
		&nbsp; end<br />
		```<br />
		表格<br />
		&nbsp; 表头&nbsp; | 表头<br />
		&nbsp; ------------- | -------------<br />
		&nbsp;单元格内容&nbsp; | 单元格内容<br />
		&nbsp;单元格内容l&nbsp; | 单元格内容</p>
</blockquote>
<p>
	如果直接记语法，那似乎困难了些。这里OneCoder推荐两个Markdown的编辑器。</p>
<p>
	在线编辑器：stackedit<br />
	网址：<a href="https://stackedit.io/">https://stackedit.io/</a></p>
<p>
	Mac下离线编辑器Mou<br />
	下载地址：<a href="http://mouapp.com/">http://mouapp.com/</a></p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DLZvaeXh/RFZ89.jpg" style="width: 700px; height: 501px;" /></p>
<p>
	<br />
	OneCoder这里使用的是后者为自己的shurnim-storage项目写Readme。至于这个项目是什么，见Readme文档，OneCoder也会在另外的博文做一些补充说明。成品Readme如下：</p>
<blockquote>
	<p>
		# shurnim-storage</p>
	<p>
		![Shurnim icon](http://onecoder.qiniudn.com/8wuliao/DLPii2Jx/rEBO.jpg)</p>
	<p>
		## 目录<br />
		* [背景介绍](#背景介绍)<br />
		* [项目介绍](#项目介绍)<br />
		* [使用说明](#使用说明)<br />
		&nbsp; * [获取代码](#获取代码)<br />
		&nbsp; * [开发插件](#开发插件)<br />
		&nbsp; * [使用ShurnimStorage接口](#使用ShurnimStorage接口)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * [接口介绍](#接口介绍)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * [使用样例](#使用样例)<br />
		* [其他](#其他)</p>
	<p>
		&lt;a name=&quot;背景介绍&quot;&gt;&lt;/a&gt;<br />
		## 背景介绍</p>
	<p>
		*Shurnim*，是我和我老婆曾经养过的一只仓鼠的名字。&lt;br/&gt;<br />
		*shurnim-storage*，是一个插件式云存储/网盘同步管理工具。是在参加又拍云开发大赛的过程中设计并开发。</p>
	<p>
		&lt;a name=&quot;项目介绍&quot;&gt;&lt;/a&gt;<br />
		## 项目介绍</p>
	<p>
		*shurnim-storage* 的设计初衷是给大家提供一个可方便扩展的云存储/网盘同步工具。分后端接口和前端UI界面两部分。&lt;br&gt;</p>
	<p>
		由于目前各种云存储和网盘系统层出不穷，单一工具往往支持支持某几个特定存储之间的同步，如**又拍云**到**七牛云存储**的同步工具，此时如若想同步到其他存则可能需要新的工具，给用户带来不便。*shurnim-storage*&nbsp; 正是为了解决此问题而设计的。</p>
	<p>
		在*shurnim-storage*中，用户使用的固定的统一的后端接口。而所有云存储/网盘API的支持则是以插件的形式部署到系统中的。如此，如果用户想要一个从**又拍云**到**Dropbox**的同步工具，则只需要在原有基础上，增加**Dropbox**的插件，即可实现互通，方便快捷。&lt;br/&gt;</p>
	<p>
		同时，后端统一接口的设计也考虑到界面开发的需求，可直接通过后端提供的接口开发具有上述扩展功能的云存储UI工具。&lt;br&gt;</p>
	<p>
		目前，后端整体框架的核心部分已经基本开发完成。只需逐步补充后端接口和插件开发接口的定义即可。但由于个人时间和能力所限，UI部分没有开发，有兴趣的同学可以一试。</p>
	<p>
		&lt;a name=&quot;使用说明&quot;&gt;&lt;/a&gt;<br />
		## 使用说明</p>
	<p>
		&lt;a name=&quot;获取代码&quot;&gt;&lt;/a&gt;<br />
		### 获取代码</p>
	<p>
		* gitcafe项目主页: &lt;https://gitcafe.com/onecoder/shurnim-storage-for-UPYUN&gt;<br />
		* OSChina项目主页: &lt;http://git.oschina.net/onecoder/shurnim-storage&gt;&lt;br&gt;<br />
		OSChina上的会持续更新。</p>
	<p>
		另外你也可以通过OSChina的Maven库获取依赖，或者自己编译jar包。</p>
	<p>
		* maven</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; 1. 加入OSC仓库<br />
		&nbsp;&nbsp;&nbsp;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;repositories&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;repository&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;id&gt;nexus&lt;/id&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;name&gt;local private nexus&lt;/name&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;url&gt;http://maven.oschina.net/content/groups/public/&lt;/url&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;releases&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;enabled&gt;true&lt;/enabled&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/releases&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;snapshots&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;enabled&gt;false&lt;/enabled&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/snapshots&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/repository&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/repositories&gt;</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; 2. 加入依赖<br />
		&nbsp;&nbsp;&nbsp;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;dependency&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;groupId&gt;com.coderli&lt;/groupId&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;artifactId&gt;shurnim-storage&lt;/artifactId&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;version&gt;0.1-alpha&lt;/version&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/dependency&gt;<br />
		* Gradle 编译Jar</p>
	<p>
		在项目目录执行<br />
		&nbsp;&nbsp;&nbsp;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; gradle jar<br />
		&nbsp;&nbsp;&nbsp;<br />
		&lt;a name=&quot;开发插件&quot;&gt;&lt;/a&gt;<br />
		### 开发插件</p>
	<p>
		在*shurnim-storage*中，插件就像一块一块的积木，不但支撑着框架的功能，也是框架可扩展性的基石。开发一个插件，仅需两步：</p>
	<p>
		1. 实现PluginAPI接口</p>
	<p>
		```<br />
		package com.coderli.shurnim.storage.plugin;</p>
	<p>
		import java.io.File;<br />
		import java.util.List;</p>
	<p>
		import com.coderli.shurnim.storage.plugin.model.Resource;</p>
	<p>
		/**<br />
		* 各种云存储插件需要实现的通用接口<br />
		*<br />
		* @author OneCoder<br />
		* @date 2014年4月22日 下午9:43:41<br />
		* @website http://www.coderli.com<br />
		*/<br />
		public interface PluginAPI {</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 初始化接口<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年5月19日 下午10:47:40<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; void init();</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 获取子资源列表<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param parentPath<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @return<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年4月24日 下午11:29:14<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; List&lt;Resource&gt; getChildResources(String parentPath);</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 下载特定的资源<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param parentPath<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 目录路径<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param name<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 资源名称<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param storePath<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 下载资源保存路径<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @return<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年4月24日 下午11:30:19<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; Resource downloadResource(String parentPath, String name, String storePath);</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 创建文件夹<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param path<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 文件夹路径<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param auto<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 是否自动创建父目录<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @return<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年5月15日 下午10:10:04<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; boolean mkdir(String path, boolean auto);</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 上传资源<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param parentPath<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 父目录路径<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param name<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 资源名称<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param uploadFile<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 待上传的本地文件<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @return<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年5月15日 下午10:40:13<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; boolean uploadResource(String parentPath, String name, File uploadFile);<br />
		}<br />
		```</p>
	<p>
		目前插件的接口列表仅为同步资源设计，如果想要支持更多操作(如删除，查找等)，可扩展该接口定义。&lt;br/&gt;&lt;br/&gt;<br />
		接口中，所有的参数和返回值均为*shurnim-storage*框架中定义的通用模型。因此，您在开发插件过程中需要将特定SDK中的模型转换成接口中提供的模型。&lt;br/&gt;&lt;br/&gt;<br />
		插件实现类只要与*shurnim-storage*工程在同一个classpath即可使用。您既可以直接在源码工程中开发插件，就如工程里提供的*upyun*和*qiniu*插件一样，也可以作为独立工程开发，打成jar，放置在同一个classpath下。&lt;br/&gt;&lt;br/&gt;<br />
		*upyun*插件样例(功能不完整):</p>
	<p>
		```&nbsp;&nbsp;<br />
		package com.coderli.shurnim.storage.upyun.plugin;</p>
	<p>
		import java.io.File;<br />
		import java.util.List;</p>
	<p>
		import com.coderli.shurnim.storage.plugin.AbstractPluginAPI;<br />
		import com.coderli.shurnim.storage.plugin.model.Resource;<br />
		import com.coderli.shurnim.storage.plugin.model.Resource.Type;<br />
		import com.coderli.shurnim.storage.upyun.api.UpYun;</p>
	<p>
		public class UpYunPlugin extends AbstractPluginAPI {</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; private UpYun upyun;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; private String username;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; private String password;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; private String bucketName;</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public UpYun getUpyun() {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return upyun;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public void setUpyun(UpYun upyun) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; this.upyun = upyun;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public String getUsername() {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return username;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public void setUsername(String username) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; this.username = username;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public String getPassword() {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return password;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public void setPassword(String password) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; this.password = password;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public String getBucketName() {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return bucketName;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; public void setBucketName(String bucketName) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; this.bucketName = bucketName;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /*<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * (non-Javadoc)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @see<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * com.coderli.shurnim.storage.plugin.PluginAPI#getChildResources(java.lang<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * .String)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; @Override<br />
		&nbsp;&nbsp;&nbsp;&nbsp; public List&lt;Resource&gt; getChildResources(String parentPath) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return null;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /*<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * (non-Javadoc)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @see<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * com.coderli.shurnim.storage.plugin.PluginAPI#downloadResource(java.lang<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * .String, java.lang.String, java.lang.String)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; @Override<br />
		&nbsp;&nbsp;&nbsp;&nbsp; public Resource downloadResource(String parentPath, String name,<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; String storePath) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; File storeFile = new File(storePath);<br />
		//&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if (!storeFile.exists()) {<br />
		//&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; try {<br />
		//&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; storeFile.createNewFile();<br />
		//&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; } catch (IOException e) {<br />
		//&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; e.printStackTrace();<br />
		//&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br />
		//&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; String filePath = getFullPath(parentPath, name);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; upyun.readDir(&quot;/api&quot;);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if (upyun.readFile(filePath, storeFile)) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Resource result = new Resource();<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; result.setName(name);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; result.setPath(parentPath);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; result.setType(Type.FILE);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; result.setLocalFile(storeFile);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return result;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return null;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; String getFullPath(String parentPath, String name) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if (!parentPath.endsWith(File.separator)) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; parentPath = parentPath + File.separator;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return parentPath + name;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /*<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * (non-Javadoc)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @see com.coderli.shurnim.storage.plugin.PluginAPI#mkdir(java.lang.String,<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * boolean)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; @Override<br />
		&nbsp;&nbsp;&nbsp;&nbsp; public boolean mkdir(String path, boolean auto) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // TODO Auto-generated method stub<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return false;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /*<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * (non-Javadoc)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @see<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * com.coderli.shurnim.storage.plugin.PluginAPI#uploadResource(java.lang<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * .String, java.lang.String, java.io.File)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; @Override<br />
		&nbsp;&nbsp;&nbsp;&nbsp; public boolean uploadResource(String parentPath, String name,<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; File uploadFile) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // TODO Auto-generated method stub<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return false;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /*<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * (non-Javadoc)<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @see com.coderli.shurnim.storage.plugin.AbstractPluginAPI#init()<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; @Override<br />
		&nbsp;&nbsp;&nbsp;&nbsp; public void init() {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; upyun = new UpYun(bucketName, username, password);<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		}<br />
		```</p>
	<p>
		<br />
		2. 编写插件配置文件</p>
	<p>
		```<br />
		&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;<br />
		&lt;plugin&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; &lt;id&gt;qiniu&lt;/id&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; &lt;name&gt;七牛云存储&lt;/name&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; &lt;api&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;className&gt;com.coderli.shurnim.storage.qiniu.QiniuPlugin&lt;/className&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;params&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;param name=&quot;access_key&quot; displayName=&quot;ACCESS_KEY&quot;&gt;EjREKHI_GFXbQzyrKdVhhXrIRyj3fRC1s9UmZPZO<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/param&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;param name=&quot;secret_key&quot; displayName=&quot;SECRET_KEY&quot;&gt;88NofFWUvkfJ6T6rGRxlDSZOQxWkIxY2IsFIXJLX<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/param&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;param name=&quot;bucketName&quot; displayName=&quot;空间名&quot;&gt;onecoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/param&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;/params&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp; &lt;/api&gt;<br />
		&lt;/plugin&gt;<br />
		```<br />
		&nbsp;&nbsp; * **id** 为该插件在*shurnim-storage*框架下的唯一标识，不可重复，必填。<br />
		&nbsp;&nbsp;&nbsp; * **name** 为显示值，为UI开发提供可供显示的有语义的值。<br />
		&nbsp;&nbsp;&nbsp; * **className** 为插件接口实现类的完整路径。必填<br />
		&nbsp;&nbsp;&nbsp; * **params/param** 为插件需要用户配置的参数列表。其中<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * *name* 代表参数名，需要与接口实现类中的参数名严格一致，且必须有相应的set方法的格式要求严格，即set+首字母大写的参数名。例如:setAccess_key(String arg); 目前只支持*String*类型的参数。<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * *displayName* 为参数显示名，同样是为了UI开发的考虑，方便用户开发出可根据参数列表动态显示的UI界面。<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 参数的值可以直接配置在配置文件中，也可以在运行期动态赋值。直接配置值，对于直接使用后端接口来说较为方便。对于UI开发来说，运行期动态赋值更为合理。&lt;br/&gt;&lt;/br&gt;</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; 在使用源码工程时，插件配置文件统一放置在工程的*plugins*目录下。你也可以统一放置在任何位置。此时，在构造后端接口实例时，需要告知接口该位置。<br />
		&nbsp;&nbsp;&nbsp;<br />
		&lt;a name=&quot;使用ShurnimStorage接口&quot;&gt;&lt;/a&gt;<br />
		### 使用*ShurnimStorage*接口</p>
	<p>
		&lt;a name=&quot;接口介绍&quot;&gt;&lt;/a&gt;<br />
		#### 接口介绍</p>
	<p>
		**ShurnimStorage**接口是*shurinm-storage*框架全局的也是唯一的接口，目前定义如</p>
	<p>
		```<br />
		package com.coderli.shurnim.storage;</p>
	<p>
		import java.util.List;<br />
		import java.util.Map;</p>
	<p>
		import com.coderli.shurnim.storage.plugin.model.Plugin;<br />
		import com.coderli.shurnim.storage.plugin.model.Resource;</p>
	<p>
		/**<br />
		* 后台模块的全局接口&lt;br&gt;<br />
		* 通过该接口使用后台的全部功能。&lt;br&gt;<br />
		* 使用方式:&lt;br&gt;<br />
		* &lt;li&gt;<br />
		* 1.先通过{@link #getSupportedPlugins()}方法获取所有支持的平台/插件列表。 &lt;li&gt;<br />
		* 2.将列表中返回的ID传入对应的接口参数中，进行对应的平台的相关操作。&lt;br&gt;<br />
		* 需要注意的是，不同平台的插件需要给不同的参数赋值，该值可以直接配置在配置文件中。&lt;br&gt;<br />
		* 也可以在运行期动态赋值。(会覆盖配置文件中的值。)&lt;br&gt;<br />
		*<br />
		* 参数列表的设计，方便UI开发人员动态的根据参数列表生成可填写的控件。并给参数赋值。增强了可扩展性。<br />
		*<br />
		* @author OneCoder<br />
		* @date 2014年4月22日 下午9:21:58<br />
		* @website http://www.coderli.com<br />
		*/<br />
		public interface ShurnimStorage {</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 获取当前支持的插件列表&lt;br&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 没有支持的插件的时候可能返回null<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @return<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年5月7日 下午8:53:25<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; List&lt;Plugin&gt; getSupportedPlugins();</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 给指定的插件的对应参数赋值&lt;br&gt;<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 此处赋值会覆盖配置文件中的默认值<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param pluginId<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 插件ID<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param paramsKV<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 参数键值对<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年5月9日 上午12:41:53<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; void setParamValues(String pluginId, Map&lt;String, String&gt; paramsKV);</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 获取插件对应目录下的资源列表<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param pluginId<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 插件ID<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param path<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 指定路径<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @return<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年5月11日 上午8:52:00<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; List&lt;Resource&gt; getResources(String pluginId, String path);</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; /**<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * 同步资源<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param fromPluginId<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 待同步的插件Id<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param toPluginIds<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 目标插件Id<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @param resource<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 待同步的资源<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @return 同步结果<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @author OneCoder<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * @date 2014年5月11日 上午11:41:24<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; */<br />
		&nbsp;&nbsp;&nbsp;&nbsp; boolean sycnResource(String fromPluginId, String toPluginId,<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Resource resource) throws Exception;<br />
		}<br />
		```&nbsp;&nbsp;&nbsp;&nbsp;</p>
	<p>
		当前接口实际仅包含了获取资源列表*getResources*和同步资源*sycnResource*功能，*getSupportedPlugins*和*setParamValues*实际为辅助接口，在UI开发时较为有用。&lt;br/&gt;&lt;br/&gt;<br />
		同样，您也可以扩展开发该接口增加更多的您喜欢的特性。例如，同时删除给定存储上的文件。当然，这需要插件接口的配合支持。&lt;br/&gt;&lt;br/&gt;</p>
	<p>
		这里，*sycnResource*设计成插件间一对一的形式，是考虑到获取同步是否成功的结果的需求。如果您想开发一次同步到多个存储的功能，建议您重新开发您自己的接口实现类，因为默认实现会多次下次资源(每次同步后删除)，造成网络资源的浪费。</p>
	<p>
		接口的默认实现类是: **DefaultShurnimStorageImpl**</p>
	<p>
		&lt;a name=&quot;使用样例&quot;&gt;&lt;/a&gt;<br />
		#### 使用样例<br />
		```&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br />
		package com.coderli.shurnim.test.shurnimstorage;</p>
	<p>
		import org.junit.Assert;<br />
		import org.junit.BeforeClass;<br />
		import org.junit.Test;</p>
	<p>
		import com.coderli.shurnim.storage.DefaultShurnimStorageImpl;<br />
		import com.coderli.shurnim.storage.ShurnimStorage;<br />
		import com.coderli.shurnim.storage.plugin.model.Resource;<br />
		import com.coderli.shurnim.storage.plugin.model.Resource.Type;</p>
	<p>
		/**<br />
		* 全局接口测试类&lt;br&gt;<br />
		* 时间有限，目前仅作整体接口测试。细粒度的单元测试，随开发补充。<br />
		*<br />
		* @author OneCoder<br />
		* @date 2014年5月19日 下午10:50:27<br />
		* @website http://www.coderli.com<br />
		*/<br />
		public class ShurnimStorageTest {</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; private static ShurnimStorage shurnim;</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; @BeforeClass<br />
		&nbsp;&nbsp;&nbsp;&nbsp; public static void init() {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; shurnim = new DefaultShurnimStorageImpl(<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &quot;/Users/apple/git/shurnim-storage-for-UPYUN/plugins&quot;);<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }</p>
	<p>
		&nbsp;&nbsp;&nbsp;&nbsp; @Test<br />
		&nbsp;&nbsp;&nbsp;&nbsp; public void testSycnResource() {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Resource syncResource = new Resource();<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; syncResource.setPath(&quot;/api&quot;);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; syncResource.setName(&quot;api.html&quot;);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; syncResource.setType(Type.FILE);<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; try {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Assert.assertTrue(shurnim.sycnResource(&quot;upyun&quot;, &quot;qiniu&quot;,<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; syncResource));<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; } catch (Exception e) {<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; e.printStackTrace();<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; }<br />
		&nbsp;&nbsp;&nbsp;&nbsp; }<br />
		}<br />
		```<br />
		&lt;a name=&quot;其他&quot;&gt;&lt;/a&gt;<br />
		## 其他</p>
	<p>
		时间仓促，功能简陋，望您包涵。OneCoder(Blog:[http://www.coderli.com](http://www.coderli.com))特别希望看到该项目对您哪怕一点点的帮助。任意的意见和建议，欢迎随意与我沟通,联系方式：</p>
	<p>
		* Email: &lt;wushikezuo@gmail.com&gt;<br />
		* QQ:57959968<br />
		* Blog:[OneCoder](http://www.coderli.com)</p>
	<p>
		项目的Bug和改进点，可在OSChina上以issue的方式直接提交给我。</p>
</blockquote>
<p>
	效果预览：</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DLZwwEM3/YRDQc.jpg" style="width: 700px; height: 436px;" /></p>

