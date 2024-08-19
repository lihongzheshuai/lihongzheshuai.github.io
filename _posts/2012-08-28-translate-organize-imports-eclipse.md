---
layout: post
title: 在Eclipse中管理Java类引用的技巧
date: 2012-08-28 20:45 +0800
author: onecoder
comments: true
tags: [Eclipse]
categories: [翻译, 知识扩展]
thread_key: 1111
---
今天，我学到了一个在Eclipse中管理引用的小技巧。当然，你可以在单个文件中用Ctrl+shift+O去移除未使用的引用。但是，如果你想移除很多类的无用的引用你该如何去做，比如移除整个包下的类？

很简单，在包浏览(Package Exporler)视图下，右击你想要修改的包，然后依次选择source -&gt; Organize imports，它将自动分析该包下的所有文件，然后移除无用的引用。

还有一个更加巧妙的技巧可以让你在保存文件的时候自动管理类引用。启用该功能，你需要进行如下配置，进入：&nbsp;<strong>Windows -&gt; Preferences -&gt; Java -&gt; Editor -&gt; Save Actions</strong>。然后选择 <strong>Perform the selected action on save -&gt; Organize imports</strong>。如此设置后，当你保存一个Java文件时，Eclipse将会自动的管理去掉无效的引用。

OneCoder翻译

英文原文地址：&nbsp;<a href="http://java.dzone.com/articles/organize-imports-eclipse">http://java.dzone.com/articles/organize-imports-eclipse</a>