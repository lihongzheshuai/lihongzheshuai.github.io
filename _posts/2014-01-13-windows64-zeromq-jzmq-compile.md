---
layout: post
title: Windows7 x64下编译ZeroMQ和JZMQ  Java Binding
date: 2014-01-13 15:27
author: onecoder
comments: true
tags: [ZeroMQ]
thread_key: 1619
---
<p>
	首先，先说明的是，OneCoder采用的是使用vs2010的编译方式，zeromq的版本是3.2.4。</p>
<p>
	先编译zeromq3.2.4的源码。双击builds/msvc/ 目录下的msvc.sln导入到VS2010。选择x64位编译器，生成解决方案。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DssB5eQd/SbH9v.jpg" style="height: 436px; width: 630px;" /></p>
<p>
	默认的生成目录是在zeromq-3.2.4\builds\msvc\Release\ 下。</p>
<p>
	然后编译Jzmq，从github上下载源码。<br />
	git clone https://github.com/zeromq/jzmq.git</p>
<p>
	默认master分支的代码在windows好像目录结构不对，所以这里选择的是切换到tag2.2.2的分支。<br />
	同样，打开jzmq目录下，builds\msvs\msvc.sln文件，导入到VS2010中。<br />
	编辑工程属性。选择x64编译环境。编辑VC++工程目录</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DssB6qS3/oQ99R.jpg" style="height: 450px; width: 630px;" /></p>
<p>
	在包含目录中，添加JDK的include目录，JDK include目录中的win32目录以及刚才zeromq目录中的include目录。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DsszrLEF/ympnz.jpg" /></p>
<p>
	在库目录中，添加刚才编译zeromq生成的release目录。</p>
<p style="text-align: center;">
	<img alt="" src="http://onecoder.qiniudn.com/8wuliao/DssB7zMH/TXEcE.jpg" /></p>
<p>
	然后生成解决方案即可。</p>
<p>
	与4.0.3版本编译，会出现异常：</p>
<blockquote>
	<p>
		error C2371: &ldquo;int8_t&rdquo;: 重定义；不同的基类型</p>
</blockquote>
<p>
	可能兼容性还有问题。</p>
<p>
	运行期，只需要依赖编译生成的jzmq.dll和libzmq.dll文件即可。</p>

