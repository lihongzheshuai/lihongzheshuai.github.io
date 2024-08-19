---
layout: post
title: "博客从wordpress迁移到Github.io、GitCafe"
modified:
categories: 
excerpt: 最近博客([www.coderli.com](www.coderli.com)) 被几个流氓IP爬的厉害，流量超标。促使我萌生了将博客迁移到github.io的想法。整个迁移过程OneCoder之前也是不熟悉的，不过思路是清晰的。
tags: [jekyll, blog, gitcafe, github.io]
image:
  feature:
thread_key: 1863
date: 2014-12-12T15:18:51+08:00
---

最近博客([www.coderli.com](http://www.coderli.com)) 被几个流氓IP爬的厉害，流量超标。促使我萌生了将博客迁移到github.io的想法。整个迁移过程OneCoder之前也是不熟悉的，不过思路是清晰的。

1、 如何在github.io/GitCafe上建立页面。
github.io就是原github的page功能。建立的方式很简单。首先你需要有一个Github帐号，然后在你的github帐号下建立一个名为：
yourusername.github.io的库（repository）即可。
以后，你只需要往该库上传静态html页面即可通过地址：http://yourusername.github.io 进行访问。默认地址(如：
http://lihongzheshuai.github.io)打开的是该库根目录下的index.html页面。
Gitcafe只需要建立一个同名的库，并创建一个gitcafe-pages分支即可。
鉴于国内对Github访问速度和稳定性的问题，OneCoder决定把域名绑定到GitCafe提供的pages服务上：）。

2、 利用Jekyll搭建Blog
上面介绍的只是如何在github.io存放和浏览独立页面。离搭建一个独立的Blog还有距离。目前在Github上搭建blog最流行的工具就是Jekyll了。
Mac上安装Jekyll：
通过rubygem命令，gem install jekyll
不过在国内的用户可能需要先切换到淘宝的gem源，切换方式参考：
[http://ruby.taobao.org/](http://ruby.taobao.org/)

安装成功后需要配置Jekyll，
可参考：
[http://jekyllrb.com/docs/quickstart/](http://jekyllrb.com/docs/quickstart/)
和
[http://www.ruanyifeng.com/blog/2012/08/blogging_with_jekyll.html](http://www.ruanyifeng.com/blog/2012/08/blogging_with_jekyll.html)
后面文章中的配置方式是手动的可能有些老，不过你可以学习他介绍的Jekyll各种配置。

一些好看的Jekyll模版：
[http://jekyllthemes.org/](http://jekyllthemes.org/)
原理很简单，其实只要把Jekyll生成的所有目录结构同步到Github即可。各个目录结构的介绍可以参考Jekyll的官方文档。
[http://jekyllcn.com/docs/structure/](http://jekyllcn.com/docs/structure/)
我们只需要将文章放到_posts文件夹下即可。

3、将文章从wordpress迁移数据到github.io、GitCafe

数据分两部分，文章数据和评论。
1、文章导出
通过wordpress的后台-》工具->导出功能，将所有的文章导出为xml文件。
2、转成.md文件(markdown)
这里由于OneCoder是在windows环境下进行的这部操作，所以使用的工具是：
[https://github.com/theaob/wpXml2Jekyll](https://github.com/theaob/wpXml2Jekyll)
其他工具可以参考官方的介绍：
[http://jekyllcn.com/docs/migrations/](http://jekyllcn.com/docs/migrations/)

4、评论迁移
由于OneCoder使用的是多说评论框，所以需要在新站点把thread_key同步过来。这工作正在慢慢的进行中。。很痛苦。对于没有迁移过来的文章，是暂时关闭评论了。开放评论的都是同步好key的文章和新文章。

5、域名绑定
参考gitcafe的说明即可。

6、用octopress写博客
[http://octopress.org/docs/blogging/](http://octopress.org/docs/blogging/)
安卓部署参考：
[http://octopress.org/docs/setup/](http://octopress.org/docs/setup/)

时间仓促，OneCoder只是草草的把文章迁移了过来很多文章的格式，甚至图片都无法显示。没办法，300多篇文章，只能一个一个慢慢修改了。

PS：友链部分，OneCoder会抽空修改模版，统一添加进去。