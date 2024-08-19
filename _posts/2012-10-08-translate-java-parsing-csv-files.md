---
layout: post
title: Java 解析CSV文件
date: 2012-10-08 15:25 +0800
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究,JDK]
thread_key: 1170
---
<p>
	十一匆匆的就过去了，OneCoder过的也是有点恍惚。不知道都做了什么，心却有点散。做一篇翻译，权当收收心，找找感觉吧。</p>
<div>
	原文地址:<a href="http://www.markhneedham.com/blog/2012/09/23/java-parsing-csv-files/">http://www.markhneedham.com/blog/2012/09/23/java-parsing-csv-files/</a>&nbsp;&nbsp;</div>
<div>
	&nbsp;</div>
<div>
	在之前发布的博文里我提到，我最近正在把一些neo4j数据加载的代码从Ruby迁移到Java，因此作为这个过程中的一步，我需要解析一些CSV文件。</div>
<div>
	&nbsp;</div>
<div>
	在Ruby中，我使用<a href="http://fastercsv.rubyforge.org/">FasterCSV</a>进行解析。<a href="http://fastercsv.rubyforge.org/">FasterCSV</a>已经是Ruby1.9中的标准的CSV库。但是，我必须用Java代码去解析CSV文件，所以我不知道该用什么库。</div>
<div>
	&nbsp;</div>
<div>
	我需要一个可以解析用逗号分割的文件内容的库，这里逗号还有可能是其中某部分的一个值。我认为这是任何CSV解析库的最普通标准的特性，不过通过google，我找到了OpenCSV。</div>
<div>
	&nbsp;</div>
<div>
	在这里可以下载到<a href="http://downloads.sourceforge.net/project/opencsv/opencsv/2.3/opencsv-2.3-src-with-libs.tar.gz?r=&amp;ts=1348439616&amp;use_mirror=ignum">OpenCSV</a>，到目前为止它做的还不错。</div>
<div>
	&nbsp;</div>
<div>
	下面是我使用的一个例子：</div>

```java
String filePath = "/Users/mneedham/data/awesome-csv-file.csv";
CSVReader reader = new CSVReader(new FileReader(filePath), ',');

List<String[]> csvEntries = reader.readAll();
Iterator<String[]> iterator = csvEntries.iterator();

while (iterator.hasNext()) {
    String[] row = iterator.next();
    System.out.println("field 1: " + row[0]);
}
```

在它的项目<a href="http://opencsv.sourceforge.net/">主页</a>中有更多使用场景的莉子。