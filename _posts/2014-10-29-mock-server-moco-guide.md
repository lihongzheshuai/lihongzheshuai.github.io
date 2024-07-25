---
layout: post
title: Mock Server- Moco  使用指南
date: 2014-10-29 12:04 +0800
author: onecoder
comments: true
tags: [Moco]
thread_key: 1843
---
项目里需要使用Mock Server(Mock Server是做什么的，您可以Google一下)，这也是我个人比较喜欢的做法。这里我们选择的是Moco，OneCoder其实也没用过，所以就先学习一下。
官方地址：https://github.com/dreamhead/moc

Moco服务端就是一个独立的jar包。通过命令(针对0.9.2版本)：
<blockquote>java -jar moco-runner-&lt;version&gt;-standalone.jar start -p 12306 -c ***.json</blockquote>
即可启动服务。其中12306是任意指定的端口号。foo.json是需要加载的配置文件名。&lt;version&gt; 是你下载的Moco的版本号，当前最新版为0.9.2。

<img class="aligncenter" src="/images/oldposts/start-moco.png" alt="" width="674" height="437" />

上图中，启动信息之外的信息，是通过浏览器访问地址:http://localhost:12306后，控制台输出的信息。此时的配置文件如下：
<blockquote>
<div>[
{
"response" :
{
"text" : "Hello, Moco"
}
}
]</div></blockquote>
剩下的任务就是构造自己项目的配置文件了。这部分内容的详细文档在：<a href="https://github.com/dreamhead/moco/blob/master/moco-doc/apis.md">https://github.com/dreamhead/moco/blob/master/moco-doc/apis.md</a>

值得一提的是，Moco支持动态加载配置文件，所以无论你是修改还是添加配置文件都是不需要重启服务的。这点非常方便。

关于配置文件，这里OneCoder介绍几个关键的部分：
Moco支持在全局的配置文件中引入其他配置文件，这样就可以分服务定义配置文件，便于管理。例如你有两个项目Boy和Girl项目需要使用同一个Mock Server，那么可以分别定义boy.json和girl.json配置文件，然后在全局文件中引入即可：
全局配置如下：
<blockquote>
<div>[
{
"context": "/boy",
"include": "boy.json"
},
{
"context": "/girl",
"include": "girl.json"
}
]</div></blockquote>
在boy.json和girl.json中分别定义:
<div>
<blockquote>
<div>//boy</div>
<div>[
{
"request" : {
"uri" : "/hello"
},
"response" : {
"text" : "I am a boy."
}
}
]</div>
<div>//girl</div>
<div>[
{
"request" : {
"uri" : "/hello"
},
"response" : {
"text" : "I am a girl."
}
}
]</div></blockquote>
</div>
注意，此时需要通过参数-g在加载全局配置文件。即：
<blockquote>java -jar moco-runner-&lt;version&gt;-standalone.jar start -p 12306 -g onecoder.json</blockquote>
否则配置文件解析会报错。这里容易忽略。

启动成功后，我们分别通过http://localhost:12306/girl/hello 和 http://localhost:12306/boy/hello 访问服务，便可得到对应的reponse结果。
其实全局文件的引入方式还有直接include等，不过OneCoder觉得context这种方式应该比较常用，管理起来也比较方便。

接下来要关注的就是每个模块内的配置文件本身了。基本的request/response已经见过了。request里自然有很多带参数的，配置如下：
<blockquote>
<div>{
"request" : {
"uri" : "/getBoy",
"queries":
{
"name":"onecoder"
}
},
"response" : {
"text" : "Hey."
}
}</div></blockquote>
上述配置匹配的url即为：http://localhost:12306/boy/getBoy?name=onecoder，返回值即为: Hey.

也就是说，使用这种方式你需要在开发期有固定的测试参数和参数值。

对于rest风格的url，Moco支持正则匹配。
<blockquote>
<div>{
"request":
{
"uri":
{
"match": "/searchboy/\\w+"
}
},
"response":
{
"text": "Find a boy."
}
}</div></blockquote>
此时，访问http://localhost:12306/boy/searchboy/*** 结尾加任何参数均可匹配到。

除了Get外，Post，Put，Delete等请求模式自然是支持的：
<div>
<blockquote>
<pre>{
  "request" :
    {
      "method" : "post",
      "forms" :
        {
          "name" : "onecoder"
        }
    },
  "response" : 
    {
      "text" : "Hi."
    }}</pre>
</blockquote>
</div>
当然，对于Header、Cookies等请求信息的配置也是支持的。官方文档介绍的也很清除，这里着重说一下template功能。上面介绍了对于带参数的请求参数，请求参数的值和返回值都是固定的，这自然太过死板。好在从0.8版本开始，Moco提供了template功能，可以动态的返回一些参数值。例如：
<div>
<blockquote>
<div>[</div>
<div>    {
<div>    "request": {</div>
<div>             "uri": "/template"</div>
<div>                   },</div>
<div>    "response": {</div>
<div>           "text": {</div>
<div>               "template": "${req.queries['name']}"</div>
</div>
<div>               }</div>
<div>                     }</div>
<div>        }</div></blockquote>
<div>
<blockquote>
<div>]</div></blockquote>
</div>
</div>
此时通过url：http://localhost:12306/template?name=onecoder 访问，则会返回onecoder。

这样就可以通过template这种方式灵活的返回一些值。

最后，再介绍一个redirect
<blockquote>
<div>{
"request" :
{
"uri" : "/redirect"
},
"redirectTo" : "http://www.coderli.com"
}</div></blockquote>
用过浏览器访问对应的地址，就会跳转到我的博客了，哈哈。
更多的配置方式，这里就不一一介绍了。真的可以看文档就搞定了。总体来说，场景覆盖的还是很全的，但是总觉得respone的配置不够灵活，通过修改源码我们可以扩展一下自己想要的方式。这部分只能有空再看了：）
