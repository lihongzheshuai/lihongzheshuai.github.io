---
layout: post
title: MacOS10.9 下 ZeroMQ4.0.3和Java Binding安装部署
date: 2014-01-10 21:04 +0800
author: onecoder
comments: true
tags: [ZeroMQ]
thread_key: 1616
---
<p>
	ZeroMQ是什么可以自己去官网了解。<br />
	<a href="http://zeromq.org/">http://zeromq.org/</a></p>
<p>
	Mac下，对于安装了brew的朋友，很简单了。<br />
	首先安装zeromq</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
brew install zeromq
</pre>
<p>
	如果报错，很可能是因为没有安装命令行编译工具。可以通过xcode命令安装</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
xcode-select --install
</pre>
<p>
	安装成功后，即可正常编译zeromq了。</p>
<p>
	对于自己手动编译的朋友，也不麻烦。首先还是要保证安装了命令行编译工具，同上通过xcode-select安装。然后解压zeromq。然后进入目录，执行：</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
./configure
make
make install
</pre>
<p>
	然后安装jzmq，java binding<br />
	通过github下载源码<br />
	git clone https://github.com/zeromq/jzmq.git<br />
	然后依次执行</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
./autogen.sh
./configure
make
make install
</pre>
<p>
	即可在/usr/local/share/java 目录下编译出zmq.jar。</p>
<p>
	注：<br />
	如果报错：<br />
	checking whether the C compiler works&hellip; no<br />
	可以执行：</p>
<pre class="brush:bash;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
export CC=/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc
CPP=&#39;/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc -E&#39;
</pre>
<p>
	&nbsp;</p>

