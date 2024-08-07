---
layout: post
title: 为Jekyll站添加“相关文章"功能
date: 2024-08-07 10:47 +0800
author: onecoder
comments: true
tags: [Jekyll]
categories: [Jekyll]
---
想为本博客添加**相关文章**功能，因为本站是通过Jekyll搭建的静态站，所以首先想到通过Jekyll相关插件解决，没想到搜遍全网居然未找到可用的插件，无奈最后手敲实现，以下记录折腾过程。

<!--more-->

## 一、插件方案

搜索Jekyll**相关文章**功能插件，最常见下面几种：

### jekyll-related-posts

Gem安装时报错如下：

```bash
Resolving dependencies...
Could not find compatible versions

Because every version of jekyll-related-posts depends on jekyll ~> 3.0
  and Gemfile depends on jekyll ~> 4.3.3,
  jekyll-related-posts cannot be used.
So, because Gemfile depends on jekyll-related-posts >= 0,
  version solving has failed.
```

该插件只支持jekyll 3.x版本，我目前使用的是4.3.3版本，不兼容，放弃。

### jekyll-advanced-search 和 jekyll-recommend

Gem安装时报错如下：

```bash
Fetching gem metadata from https://rubygems.org/.........
Could not find gem 'jekyll-advanced-search' in rubygems repository
https://rubygems.org/ or installed locally.
```

和

```bash
Fetching gem metadata from https://rubygems.org/.........
Could not find gem 'jekyll-recommend' in rubygems repository
https://rubygems.org/ or installed locally.
```

根本找不到相应插件，怀疑是不是AI编出来骗我的，放弃。

### jekyll-algolia

这个折腾时间最漫长。先说一下Algolia， [Algolia](https://www.algolia.com/)是一个功能强大的搜索即服务（Search as a Service）平台，它提供了快速、可靠和高度可定制的搜索功能。Algolia 主要用于网站和应用程序中的搜索和发现功能。该方案即是利用该服务能力，未网站增加相关搜索功能（具体效果未见到）。

#### 1. 注册Algolia

登录网站注册即可，不赘述，注册后你会得到你`Application ID`、`Search API Key`和`Write API Key`，用于后续接口调用，保管好。但显然他是一个收费服务，具体收费点没研究。

#### 2. 安装Algolia插件

插件官方地址为[https://github.com/algolia/jekyll-algolia?tab=readme-ov-file](https://github.com/algolia/jekyll-algolia?tab=readme-ov-file)，是的他已经废弃了，并且官方描述也是支持Jekyll3.x版本，不过并没有说不支持4.x版本，所以我继续试试。（仅为好奇，废弃的东西我也不打算继续使用）

在Gemfile中添加

```ruby
group :jekyll_plugins do
  gem 'jekyll-algolia', '~> 1.0'
end
```

然后执行

```bash
bundle install
```

安装插件。插件的作用是本地生成你的网站数据，传递给Algolia用于检索索引。所以解下来就需要执行命令生成并上传数据。执行前需要先设置`ALGOLIA_API_KEY`环境变量，值为你的`Write API Key`，切勿泄露。对于PowerShell而言，命令如下：

```ps
 $env:ALGOLIA_API_KEY="Your Write API Key"
```

然后执行

```bash
bundle exec jekyll algolia
```

开始生成数据，很快的，我们就遇到了限制文章大小的问题：

```text
Processing site...
       Jekyll Feed: Generating feed for posts
Rendering to HTML (100%) |=====================================================|
Extracting records (100%) |====================================================|
[✗ Error] Record is too big

The jekyll-algolia plugin detected that one of your records exceeds the 10.00 Kb
record size limit.
```

解决办法自然是有，但真的无力再折腾下去了，毕竟插件都废弃了。如果你的文章没有超过10Kb限制，可能你已经成功了。

## 二、自编码方案

插件不行，就手写一个吧，简单搜索发现也不复杂。Jekyll网站是基于Liquid模板语言，核心代码如下：

{% raw %}
```Liquid
<h2>相关文章</h2>
  <ul>
    {% assign related_posts = "" | split: "" %}
    {% for tag in page.tags %}
      {% assign related_posts = related_posts | concat: site.posts | where: "tags", tag %}
    {% endfor %}
    {% assign related_posts = related_posts | uniq | where_exp: "post", "post.url != page.url" %}
    {% for post in related_posts limit: 6 %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
```
{% endraw %}

逻辑就是根据文章上打的tag，将tag相同的文章（排除当前文章）放到一起，然后输出到一个列表中。列表的多少通过limit控制，这里设置的是6个。

将上述放到文章页合适位置，即可实现相关文章的效果。当然为了便于管理，推荐你将其封装成一个小的模板页，然后通过include引入到合适的位置。例如，将代码放入post-recommended.html页，然后引入：

{% raw %}
```Liquid
 {% include _macro/post-recommended.html %}
```
{% endraw %}

最终效果如下：

![](/images/post/recommended-posts/posts-relate.png)

至此，折腾完成。