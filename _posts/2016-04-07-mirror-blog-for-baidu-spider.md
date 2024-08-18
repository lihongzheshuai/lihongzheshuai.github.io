---
layout: post
title: 镜像博客站点解决百度Spider无法爬取Github Pages问题
tags: [github,spider,百度]
date: 2016-04-07 23:09:33 +0800
comments: true
thread_key: 1887
---
最近，不知是因为哪根筋的问题，我突然去百度统计关注了一下博客的访问情况。意外的发现博客的访问量较之以前大减，而且几乎看不到来自百度搜索的访问。我意识到，这应该我博客的百度索引出现了问题。去百度站长工具查询索引量，果然不出所料

![](/images/post/mirrorblog-for-baiduspider/1baiduindex.png)

从3月7日开始，索引量瞬间归零。我努力的回忆当时发生了什么。突然想起我的一篇日记<a href="http://www.coderli.com/migrate-blog-again-and-new-house-property/" target="_blank">《20160302 博客再次迁移和房产证办理》</a>。该日记写在3月2日的，也就是说在3月2日左右，我把博客从Gitcafe迁移到Github。之前在Gitcafe的时候，百度索引一直是正常的。从Gitcafe迁移出去是因为Gitcafe被coding.net收购了，服务也全部迁移到coding.net了，而当时提供的迁移工具用的很不友好，也没快速找到pages服务的迁移办法，就索性直接迁到Github了，这是后话了。

于是，我上网搜索了一下Github百度索引变为零的原因，这才知道原来Github早已屏蔽百度Spider的爬取，原因似乎是因为百度Spider爬取给Github造成的压力过大，影响到正常服务。也怪我自己居然连这个都不知道。出于好奇，我还是用Chrome的***User-Agent Switcher***工具模拟百度Spider访问了一下Github，果然如此。

![](/images/post/mirrorblog-for-baiduspider/2user-agent-switcher.png)

原因找到了，剩下就是找解决问题的办法了。靠谱的办法基本有两个，一个是利用CDN加速，一个利用镜像站。其实本质原理都是一样的，就是让百度Spider访问到非Github服务提供的页面，自然就解决了Github封禁百度Spider的问题。由于我的域名一直没有做备案，所以国内的CDN服务（如又拍云等）基本都无法使用，所有只有采用镜像站的方法。

镜像站办法可用的最关键点是***DNSPod***提供的智能DNS功能。

![](/images/post/mirrorblog-for-baiduspider/3dnspod.png)

DNSPod支持根据不同的线路配置不同的规则，而其中有条线路类型就是百度。因此，我们可以将来自百度Spider的请求分发到非Github的镜像站上，用户的请求分发到原始的Github服务。这里，OneCoder采用的镜像站就是前面提到的coding.net提供的pages服务。我把百度线路的CNAME值都指向了coding.net的pages服务地址，默认线路指向Github的pages服务。通过百度站长工具里的抓取诊断功能查看，一切终于恢复了正常。

![](/images/post/mirrorblog-for-baiduspider/4spiderchecker.png)

你可能会问：“为什么不直接用coding.net的服务？”这个问题就有点尴尬了，经历了Gitcafe的收购事件，对国内这种新出现的平台少了许多底气，另外在试用coding.net服务的过程中，对服务的稳定性和正确性也产生了一些疑问，所以暂且只能用做镜像站了。