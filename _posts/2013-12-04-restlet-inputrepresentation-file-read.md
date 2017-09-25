---
layout: post
title: Restlet流式读取远端文件内容 InputRepresentation
date: 2013-12-04 21:44 +0800
author: onecoder
comments: true
tags: [Restlet]
thread_key: 1564
---
<p>
	<a href="http://www.coderli.com">OneCoder</a>验证用Restlet做服务，读取远端文件内容功能，编写验证代码。目前测试通过，主要是利用restlet内部提供的InputRepresentation对象，通过ReadableByteChannel，按字节流的方式读取文件内容。代码如下，省略注册服务的部分，只给出服务端和客户端关键代码：<br />
	服务端：</p>

```java
package com.coderli.restlet.file;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;


import org.restlet.representation.InputRepresentation;
import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;


/**
* 文件读取服务端
*
* @author lihzh(OneCoder)
* @date 2013年12月4日 下午4:35:22
* @website http://www.coderli.com
*/
public class MacFile extends ServerResource {


     @Get
     public InputRepresentation readFile() throws FileNotFoundException {
          System. out.println("开始读取文件" );
          File file = new File("/Users/apple/Documents/stockdata/SH600177.TXT" );
          InputStream inputStream = new FileInputStream(file);
          InputRepresentation inputRepresentation = new InputRepresentation(
                   inputStream);
           return inputRepresentation;
     }
}
```

<p>
	客户端：</p>

```java
package com.coderli.restlet.file;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.ReadableByteChannel;


import org.restlet.data.MediaType;
import org.restlet.representation.ReadableRepresentation;
import org.restlet.representation.Representation;
import org.restlet.resource.ClientResource;


/**
* 文件读取，客户端
*
* @author lihzh(OneCoder)
* @date 2013年12月4日 下午4:36:00
*/
public class MacFileClient {


     public static void main(String[] args) throws IOException {
          ClientResource clientResource = new ClientResource(
                    "http://localhost:8182/macFile" );
          Representation rp = clientResource.get(MediaType.ALL );
          ReadableRepresentation rRepresentation = (ReadableRepresentation) rp;
          ReadableByteChannel rbc = rRepresentation.getChannel();
          ByteBuffer bb = ByteBuffer. allocate(1024);
           int index = -1;
           do {
              index = rbc.read(bb);
               if (index <= 0) {
                    break;
              }
              bb.position(0);
               byte[] bytes = new byte[index];
              bb.get(bytes);
              System. out.print(new String(bytes, "gbk"));
              bb.clear();
          } while (index > 0);
     }
}
```

<p>
	需要注意的是，这里客户端实现中的System.out.print部分是由缺陷的，在有汉字的时候，会因为不正确的截断字节数组造成乱码。这里是因为我验证的时候文件只有英文和数组，所以简单的采用此种方式。</p>

