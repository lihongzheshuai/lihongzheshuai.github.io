---
layout: post
title: 用16G内存在Java Map中处理30亿对象
date: 2012-11-12 14:26 +0800
author: onecoder
comments: true
tags: [Java]
thread_key: 1217
---
在一个下雨的夜晚，我在思考Java中内存管理的问题，以及Java集合对内存使用的效率情况。我做了一个简单的实验，测试在16G内存条件下，Java的Map可以插入多少对象。

这个试验的目的是为了得出集合的内部上限。所以，我决定使用很小的key和value。所有的测试，都是在64w位linux环境下进行的，操作系统是ubuntu12.04。JVM版本为Oracle Java 1.7.0_09-bo5 (HotSpot 23.5-b02)。在这个JVM中，压缩指针(compressed pointers(-XX:+UseCompressedOops))的选项是默认打开的。

首先是简单的针对java.util.TreeMap的测试。不停向其中插入数字，直到其抛出内存溢出异常。JVM的设置是**-xmx15G**

```java
import java.util.*; 
Map m = new TreeMap();
for(long counter=0;;counter++){
  m.put(counter,"");
  if(counter%1000000==0) System.out.println(""+counter);
}
```

这个用例插入了1 7200 0000条数据。在接近结束的时候，由于高负荷的GC插入效率开始降低。第二次，我用HashMap代替TreeMap，这次插入了182 000 000条数据。

Java默认的集合并不是最高效利用内存的。所以，这回我们尝试最后化内存的测试。我选择了MapDB中的LongHashMap，其使用原始的long key并且对封装的内存占用进行了优化。JVM的设置仍然是**-Xmx15G**。

```java
import org.mapdb.*
LongMap m = new LongHashMap();    
for(long counter=0;;counter++){
  m.put(counter,"");
  if(counter%1000000==0) System.out.println(""+counter);
}
```

这次，计数器停止在了276 000 000。同样，在插入接近结束的时候，速度开始减慢。看起来这是基于堆的结合的限制所在。垃圾回收带来了瓶颈 。

现在是时候祭出杀手锏了:-)。我们可以采用非基于堆的方式存储，这样GC就不会发现我们的数据。我来介绍一下MapDB，它提供了基于数据库引擎的并发同步的TreeMap和HashMap。它提供了多样化的存储方式，其中一个就是非堆内存的方式。(声明：我是MapDB的作者)。

现在，让我们再跑一下之前的用例，这次采用的是非堆的Map。首先是配置并打开数据库，它打开的直接基于内存存储并且关闭事物的模式。接下来的代码是在这个db中创建一个新的map。

```java
import org.mapdb.*

DB db = DBMaker
   .newDirectMemoryDB()
   .transactionDisable()
   .make();

Map m = db.getTreeMap("test");
for(long counter=0;;counter++){
  m.put(counter,"");
  if(counter%1000000==0) System.out.println(""+counter);
}
```

这是非堆的Map，所以我们需要不同的JVM配置： **-XX:MaxDirectMemorySize=15G -Xmx128M**。这次测试在达到980 000 000条记录的时候出现内存溢出。

但是，MapDB还可以优化。之前样例的问题在于记录的破碎分散，b-tree的节点每次插入都要调整它的容量。变通的方案是，将b-tree的节点在其插入前短暂的缓存起来。这使得记录的分散降到最低。所以，我们来改变一下DB的配置：

```java
DB db = DBMaker
     .newDirectMemoryDB()
     .transactionDisable()
     .asyncFlushDelay(100)
     .make();

Map m = db.getTreeMap("test");   
```

这次记录数达到了 1 738 000 000。速度也是达到了惊人的31分钟完成了17亿数据的插入。

MapDB还能继续优化。我们把b-tree的节点容量从32提升到120并且打开透明(OneCoder理解为对用户不可见的)压缩：

```java
DB db = DBMaker
            .newDirectMemoryDB()
            .transactionDisable()
            .asyncFlushDelay(100)
            .compressionEnable()
            .make();

   Map m = db.createTreeMap("test",120, false, null, null, null);
```

这个用例在大约3 315 000 000条记录时出现内存溢出。由于压缩，他的速度 有所降低，不过还是在几个小时内完成。我还可以进行一些优化(自定义序列化等等) ，使得数据量达到大约40亿。

也许你好奇所有这些记录是怎么存储的。答案就是，delta-key压缩。(<a href="http://www.coderli.com">OneCoder</a>注：不知如何翻译)。当然，向B-Tree插入已经排好序的递增key是最佳的使用场景，并且MapDB也对此进行了一些小小的 优化。最差的情形就是key是随机的.

后续更新：很多朋友对压缩有一些困惑。在这些用例中，Delta-key 压缩默认都是启用的。在下面的用例中，我又额外开启了zlib方式的压缩：

```java
DB db = DBMaker
            .newDirectMemoryDB()
            .transactionDisable()
            .asyncFlushDelay(100)
            .make();

    Map m = db.getTreeMap("test");

    Random r = new Random();
    for(long counter=0;;counter++){
        m.put(r.nextLong(),"");
        if(counter%1000000==0) System.out.println(""+counter);
    }
```

即使在随机序列情况下，MapDB也可以存储652 000 000条记录，大概4倍于基于堆的集合。

这个简单的试验没有太多的目的。这仅仅是我对MapDB的一种优化。也许，更多的惊喜在于插入效率确实不错并且MapDB可以抗衡基于内存的集合。

原文地址：<a href="http://kotek.net/blog/3G_map">http://kotek.net/blog/3G_map</a>

<a href="http://www.coderli.com">OneCoder</a>注：<a href="http://www.coderli.com">OneCoder</a>仅做翻译，顺便了解一下知识，关于本文，下面的评论中也存在一定的争议，大家可以自行关注。此文，权当开阔视野，不是也很好么。
