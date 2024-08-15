---
layout: post
title: RESTful 接口规范
date: 2012-09-30 08:56 +0800
author: onecoder
comments: true
tags: [Restful]
thread_key: 1164
---
<a href="http://www.coder.com">OneCoder</a>最近一直在使用Restful API，最近正好看到一篇自定义restful接口规范的&ldquo;抛砖引玉&rdquo;得的文章，索性翻译一下，与大家分享。
原文地址：<a href="http://java.dzone.com/articles/restful-standard-resolved">http://java.dzone.com/articles/restful-standard-resolved</a>

最近，我正在使用RESTfull的方式构建一个web服务。尽管现在有很多的一般的指导和提示告诉你如何定义restful接口，但是却没有一个明确的标准或大家都接受的schema定义去遵循。

在网上获取了一些信息后，我打算打破这一局面：）我打算分享一下我定义的规则和结构，并且很希望能得到一些反馈来帮助我完善这个规则，所以，不要犹豫，请毫无留情给我指出错误和毛病吧。</div>

<div>
	高级别的模式是：</div>
<div>
	http(s)://server.com/app-name/{version}/{domain}/{rest-convention}</div>

这里，{version}代表api的版本信息。{domain}是一个你可以用来定义任何技术的区域(例如：安全-允许指定的用户可以访问这个区域。)或者业务上的原因。(例如：同样的功能在同一个前缀之下。)

<div>
	{rest-convention} 代表这个域(domain)下，约定的rest接口集合。</div>

<div>
	<strong>单资源(&nbsp;singular-resourceX&nbsp;)</strong></div>
<div>
	url样例：order/&nbsp; (order即指那个单独的资源X)</div>
<ul>
	<li>
		GET - 返回一个新的order</li>
	<li>
		POST- 创建一个新的order，从post请求携带的内容获取值。</li>
</ul>

<div>
	<strong>单资源带id(singular-resourceX/{id}&nbsp;)</strong></div>
<div>
	URL样例：order/1 ( order即指那个单独的资源X&nbsp;)</div>
<ul>
	<li>
		GET - 返回id是1的order</li>
	<li>
		DELETE - 删除id是1的order</li>
	<li>
		PUT - 更新id是1的order，order的值从请求的内容体中获取。</li>
</ul>

<div>
	<strong>复数资源(plural-resourceX/)</strong></div>
<div>
	URL样例:orders/</div>
<ul>
	<li>
		GET - 返回所有orders</li>
</ul>

<div>
	<strong>复数资源查找(plural-resourceX/search)</strong></div>
<div>
	URL样例：orders/search?name=123</div>
<ul>
	<li>
		GET - 返回所有满足查询条件的order资源。(实例查询，无关联) - order名字等于123的。</li>
</ul>

<div>
	<strong>复数资源查找(plural-resourceX/searchByXXX)</strong></div>
<div>
	URL样例：orders/searchByItems?name=ipad</div>
<ul>
	<li>
		GET - 将返回所有满足自定义查询的orders - 获取所有与items名字是ipad相关联的orders。</li>
</ul>

<div>
	<strong>单数资源(singular-resourceX/{id}/pluralY)</strong></div>
<div>
	URL样例：order/1/items/ (这里order即为资源X，items是复数资源Y)</div>
<ul>
	<li>
		GET - 将返回所有与order id 是1关联的items。</li>
</ul>

<div>
	<strong>singular-resourceX/{id}/singular-resourceY/</strong></div>
<div>
	URL样例：order/1/item/</div>
<ul>
	<li>
		GET - 返回一个瞬时的新的与order id是1关联的item实例。</li>
	<li>
		POST - 创建一个与order id 是1关联的item实例。Item的值从post请求体中获取。</li>
</ul>

<div>
	<strong>singular-resourceX/{id}/singular-resourceY/{id}/singular-resourceZ/</strong></div>
<div>
	URL样例：order/1/item/2/package/</div>
<ul>
	<li>
		GET - 返回一个瞬时的新的与item2和order1关联的package实例。</li>
	<li>
		POST - 创建一个新的与item 2和order1关联的package实例，package的值从post请求体中获得。</li>
</ul>

<div>
	上面的规则可以在继续递归下去，并且复数资源后面永远不会再跟随负数资源。</div>
<div>
	总结几个关键点，来更清晰的表述规则。</div>
<div>
	<ul>
		<li>
			在使用复数资源的时候，返回的是最后一个复数资源使用的实例。</li>
		<li>
			在使用单个资源的时候，返回的是最后一个但是资源使用的实例。</li>
		<li>
			查询的时候，返回的是最后一个复数实体使用的实例(们)。</li>
	</ul>
</div>
<div>
	希望你的关注能帮助我完整这个结构并解决你可能偶然遇到的问题。</div>

<div>
	在下一篇文章里，在这个结构完善之后，我将会一些技术上的样例如何在Spring MVC3.1中，使用它。</div>

<div>
	<a href="http://www.coder.com">OneCoder</a>注：<a href="http://www.coder.com">OneCoder</a>只做翻译，不代表统一文中观点，Rest URL的定义本来也算是一个仁者见仁智者见智的事情。该文下面的评论中，就有人发表的不同的观点。</div>