---
layout: post
title: Eclipse使用技巧 - 自定义JavaDoc注解和代码模版，提升开发效率和规范性
date: 2012-06-02 21:46 +0800
author: onecoder
comments: true
tags: [Eclipse, Javadoc, Java]
categories: [Java技术研究,Eclipse]
thread_key: 268
---
项目中对于注释和代码规范的要求往往是毕比较严格的，如果全靠手动完成效率低，还难以保证保证的规范。幸好Eclipse给我们提供了自定义代码模版的功能。

先说一下Java代码注释模版，它是指这里的配置：

![](/images/post/eclipse-javadoc/1codetemplate.jpg)

是不是跟你的不一样，多了**@author**和**@date**。恩，这是我自定义过的注释模版。效果是在给方法用/**注释内容*/，注释的时候，会生成如下形式的代码：

![](/images/post/eclipse-javadoc/2code.jpg)

***${tags}***是生成@param，@return这些结果。其余的应该不用我多说了。

定义这样的模版很简单，在刚才的位置，点Edit，按照如下的输入即可：

![](/images/post/eclipse-javadoc/3javadoctemplate.jpg)

这就够了？当然不是，如果在之前的方法忘记了***@date***时间注释，要怎么补上？直接用**@** + 代码辅助？是不是找不到***@date*** 标签？呵呵，当然，这个***@date***其实是我自定义的。定义的位置在这里：

![](/images/post/eclipse-javadoc/4templates.jpg)

赶紧New一个 ***@date***标签吧。

![](/images/post/eclipse-javadoc/5newdate.jpg)

注：Pattern中 ***@date***字符为手动填写。后面两个变量为Eclipse内部提供的。

保存看看效果？

![](/images/post/eclipse-javadoc/6result.png)

***@date*** 出现了吧

是不是还想扩展Insert Variable里的内容？笔者也研究了一番，找到了这个

- [《Eclipse使用技巧 &ndash; 自定义注释模板变量》](http://www.coderli.com/eclipse-template-variable/)

不过考虑到操作性价比，笔者并未尝试，有兴趣的朋友可以研究一下，欢迎交流。