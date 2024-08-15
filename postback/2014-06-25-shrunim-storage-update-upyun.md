---
layout: post
title: 关于Shurnim-storage项目更新和喜获奖
date: 2014-06-25 20:52 +0800
author: onecoder
comments: true
tags: [日记]
thread_key: 1768
---
<p>
	前端时间参加了又拍云存储的开发者大赛，没想到今天公布名单居然得了一等奖，小意外：）</p>
<p>
	shurnim项目介绍：</p>
<p>
	<a href="http://www.coderli.com/onecoder-shurnim-storage">http://www.coderli.com/onecoder-shurnim-storage</a></p>
<p>
	结果公布页如下：<br />
	<a href="https://www.upyun.com/op/dev/showcase.html">https://www.upyun.com/op/dev/showcase.html</a></p>
<p>
	说巧不巧的，这个项目本来一直没有更新，昨天正好我有一个需求，因为购买的又拍图片管家最近要到期了，所以我想把图片都迁移到七牛上。因为七牛现在每个月10g以内都是免费的。所以打算拿来当图床。当然，网站的CDN加速，还是用的又拍的赞助：）</p>
<p>
	考虑到以前发布过的文章中的图片已经有外链地址。所以，而这里二级域名的变化是不可避免的。不过这里有一个好办法，就是如果仅仅前缀二级域名变化的，可以通过在数据执行：</p>

```
UPDATE  `wp_posts` set post_content=replace(post_content,'http://8wuliao.v.yupoo.com/','http://onecoder.qiniudn.com');
```

<p>
	进行全部替换。那么我们只要保持后面的相对路径不变即可。好在七牛这方面比较简单，因为他是key-value式存储，所以你只要把key设置成想要的路径即可，而不要考虑文件的时间存储位置。</p>
<p>
	从又拍导出的图片文件名是用&quot;_&quot;分隔的三段名，而这三段正好是图片访问的相对路径。例如，图片名为：8wuliao_C6UViNqh_YOGEq.jpg，则原始对应的访问路径为：&quot;http://8wuliao.v.yupoo.com/8wuliao/C6UViNqh/YOGEq.jpg&quot;。所以，我们只要把文件名解析成对应的key即可。</p>
<p>
	这里，正好也丰富下shurnim-storage。开发一个本地文件测插件local，后台接口再增加一个批量递归上传的接口。</p>
<p>
	代码已经上传到OSChina的git上了，项目地址：<br />
	<a href="http://git.oschina.net/onecoder/shurnim-storage">http://git.oschina.net/onecoder/shurnim-storage</a></p>
<p>
	不过，由于着急实现功能，这里还有几个OneCoder不是很满意的地方，考虑做一些优化：</p>
<blockquote>
	<p>
		1、给本地插件增加一个类别，这样以后所有的本地化操作插件，在调用download接口式，都不会生成临时文件。也不会删除临时文件。增加选项，是否删除原文件。<br />
		2、不上传子目录的分支尚为TODO状态<br />
		3、支持文件夹、文件名过滤。</p>
</blockquote>
<p>
	慢慢实现，不着急：）</p>