---
layout: post
title: zTree 上手记录
date: 2014-10-09 16:53 +0800
author: onecoder
comments: true
tags: [zTree]
thread_key: 1827
---
由于工作需要，前端基本瞎的我也需要学习一些前端的知识。第一课就是zTree，因为我要做一个树。

zTree官网为：<a href="http://www.ztree.me/v3/main.php#_zTreeInfo">http://www.ztree.me/v3/main.php#_zTreeInfo</a>

官网下载的包里文档和demo都很全，基本参照样例就可以写出一个自己的树。

zTree依赖jQuery 1.4.1以上的版本。所以，我们需要引入jQuery和zTree的js库以及css文件即可。

zTree支持JSON格式的数据，用zTree生成一个基本树很简单。
<ol>
	<li>给出选项配置。</li>
	<li>给出节点数据(JSON)。</li>
	<li>调用初始化接口。参见下面官方样例：</li>
</ol>

```javascript
var setting = {    };
          var zNodes =[
              { name:"父节点1 - 展开", open:true,
                   children: [
                        { name:"父节点11 - 折叠",
                             children: [
                                  { name:"叶子节点111"},
                                  { name:"叶子节点112"},
                                  { name:"叶子节点113"},
                                  { name:"叶子节点114"}
                             ]},
                        { name:"父节点12 - 折叠",
                             children: [
                                  { name:"叶子节点121"},
                                  { name:"叶子节点122"},
                                  { name:"叶子节点123"},
                                  { name:"叶子节点124"}
                             ]},
                        { name:"父节点13 - 没有子节点", isParent:true}
                   ]},
              { name:"父节点2 - 折叠",
                   children: [
                        { name:"父节点21 - 展开", open:true,
                             children: [
                                  { name:"叶子节点211"},
                                  { name:"叶子节点212"},
                                  { name:"叶子节点213"},
                                  { name:"叶子节点214"}
                             ]},
                        { name:"父节点22 - 折叠",
                             children: [
                                  { name:"叶子节点221"},
                                  { name:"叶子节点222"},
                                  { name:"叶子节点223"},
                                  { name:"叶子节点224"}
                             ]},
                        { name:"父节点23 - 折叠",
                             children: [
                                  { name:"叶子节点231"},
                                  { name:"叶子节点232"},
                                  { name:"叶子节点233"},
                                  { name:"叶子节点234"}
                             ]}
                   ]},
              { name:"父节点3 - 没有子节点", isParent:true}

          ];

          $(document).ready(function(){
              $.fn.zTree.init($("#treeDemo"), setting, zNodes);
          });
```

<img class="aligncenter" src="/images/oldposts/standard-data-zTree.png" alt="" width="225" height="369" />

这里我们使用的是标准的JSON数据格式。而且所有数据都是预先加载好的。在我们的场景中，一般是需要逐层通过ajax懒加载的。在zTree中，只需要在setting中进行适当的配置即可。代码如下：

```xml
<! DOCTYPE html>
< html>
< head>
< meta charset= "UTF-8">
< link rel= "stylesheet" href= "../../css/zTreeStyle/zTreeStyle.css"
      type= "text/css">
< script type= "text/javascript" src= "../../js/jQuery/jquery-2.1.1.js" ></script >
< script type= "text/javascript"
      src= "../../js/zTree/jquery.ztree.core-3.5.js" ></script >
< title> OneCoder zTree Demo</ title>
< SCRIPT type= "text/javascript" >
      var setting = {
          async : {
              enable : true,
              url : "../shurnim/zTree/getData" ,
              autoParam : [ "id"],
              otherParam : {
                    "otherParam" : "zTreeAsyncTest"
              },
              type: "get",
              dataType: "json",
              dataFilter : filter
          }
     };

      function filter(treeId, parentNode, childNodes) {
           if (!childNodes)
               return null;
           for ( var i = 0, l = childNodes.length; i < l; i++) {
              childNodes[i].name = childNodes[i].name.replace(/\.n/g, '.' );
          }
           return childNodes;
     }

     $(document).ready( function() {
          $.fn.zTree.init($( "#ajaxTreeDemo"), setting);
     });
</ SCRIPT>

</ head>
< body>
      <div class = "zTreeDemoBackground left">
           <ul id = "ajaxTreeDemo" class= "ztree"></ ul>
      </div >

</ body>
</ html>
```

这里主要的区别就是在setting中设置了async属性。url即为ajax请求的地址。其他属性可在API文档中查询：http://www.ztree.me/v3/api.php
服务端代码如下：

```java
package com.coderli.springmvc.controller;

import java.io.IOException;

import javax.servlet.http.HttpServletResponse;

import lombok.extern.slf4j.Slf4j;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.coderli.springmvc.model.ZTreeData;
import com.google.gson.Gson;

@Slf4j
@Controller
public class ZTreeDataController {

      @RequestMapping(value = "/zTree/getData", method = RequestMethod.GET )
      @ResponseBody
      public String getTreeData( @RequestParam(required = false) String id,
              HttpServletResponse response) throws IOException {
          ZTreeData rootNode = new ZTreeData( "root");
           rootNode.setOpen( true);
          ZTreeData rChildNodeOne = new ZTreeData("childOne" );
           rootNode.addChild( rChildNodeOne);
           rChildNodeOne.setParent( true);
          Gson gson = new Gson();
          String jsonStr = gson.toJson( rootNode);
           log.debug( "JSON: {}", jsonStr);
           return jsonStr;
     }

}
</pre>
模型代码：
<pre class="brush:java">package com.coderli.springmvc.model;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

@Data
public class ZTreeData {

      private String name;
      // 节点是否展开
      private boolean open;
      // 节点是否是父亲节点
      private boolean isParent;
      private List<ZTreeData> children = new ArrayList<ZTreeData>();;

      public ZTreeData() {
     }

      public ZTreeData(String name) {
           this. name = name;
     }


      public void addChild(ZTreeData child) {
           children.add( child);
     }

}
```

就是根据上面的标准JSON数据格式来构造返回数据。然后zTree就会根据你返回的数据自动生成。从代码里，也可以看出。如果isParent=true，则会认为是父亲节点，在点击展开节点时会再次向后端请求数据。基本上，对于我们来说，至此已够了。

会上手了，深入的使用只要参考官方的API文档即可。
