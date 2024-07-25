---
layout: post
title: MacOS下纯shell模式Github使用简介
date: 2013-02-18 09:30 +0800
author: onecoder
comments: true
tags: [git]
thread_key: 1326
---
<p>
	为了同步在MacOS下和Windows下编写的C++练习代码，同时也想多学一些命令行的操作，<a href="http://www.coderli.com">OneCoder</a>决定鼓捣一下Mac OS X下的Git代码管理，抛弃以往完全依赖工具界面的操作方式，完全采用shell的操作模式，加深理解。</p>
<p>
	首先从Github上下载了Git的Mac版，安装。执行：</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
$&gt;git
</pre>
<p>
	即可验证是否安装成功。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/1470vC.jpg" style="height: 628px; width: 630px;" /></p>
<p>
	根据Git设计理念，我们先创建一个本地库。进入想要创建Git仓库的目录。</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
$&gt;git init</pre>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/9Dz6Z.jpg" style="width: 630px; height: 39px;" /></p>
<p>
	然后像Git仓库中添加文件，利用git add命令。git add支持各种模糊匹配模式，将当前目标下的所有文件添加如git仓库执行。</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
$&gt;git add .
</pre>
<p>
	即可。<br />
	然后执行：</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
$&gt;git commit
</pre>
<p>
	输入备注后，提交入本地git仓库。通过git log可以查看到此次提交的日志信息。<br />
	如果我们对文件进行了修改，再通过</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
$&gt;git status
</pre>
<p>
	命令便可以查看到变化的文件。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/PcJyh.jpg" style="width: 630px; height: 182px;" /></p>
<p>
	上图在文件修改后，已经执行<strong>git add &lt;file&gt;</strong>命令后的效果，再次<strong>git commit</strong>即可提交修改。</p>
<p>
	不过一般情况下，我们使用代码管理的很重要的理由是需要代码同步，这里我们以GitHub作为远端托管仓库。先在GitHub上创建一个git仓库，然后通过</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
$&gt;git clone
</pre>
<p>
	命令拷贝到本地。<br />
	将代码文件放在git仓库目录下，执行前面的操作本地commit代码。然后执行</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
$&gt;git push
</pre>
<p>
	即可将本地代码推送到远端。</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/Hvd09.jpg" style="width: 630px; height: 206px;" /></p>
<p>
	此时如果需要异地同步下载代码，只需要<strong>git pull</strong>到本地即可。<strong>git pull</strong>本身就是集成了下载和merge两个命令，即会自动和你本地的代码合并的。如果只下载不合并的话，则可使用<strong>git fetch</strong>命令。</p>
<p>
	git的其他使用细节，<a href="http://www.coderli.com">OneCoder</a>也需要慢慢摸索，这里也不再介绍。至少至此，我们的代码是已经可以成功提交到远端仓库之上了，并且也初步熟悉了一下git的命令行操作，对我来说也算是略有收获了。</p>

