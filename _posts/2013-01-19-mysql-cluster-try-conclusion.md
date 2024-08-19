---
layout: post
title: MySQL Cluster 初用初测小结
date: 2013-01-19 09:29 +0800
author: onecoder
comments: true
tags: [MySQL]
categories: [知识扩展]
thread_key: 1296
---
<p>
	基于上篇搭建的环境，验证一些基本功能和性能需求。这里先说一下功能使用的问题。<a href="http://www.coderli.com">OneCoder</a>也是第一次用。摸索着来，仅做一个记录。</p>
<p>
	从部署图就可知道，对数据库的请求操作发生在SQL节点上。为了达到试验效果，这里又追加了一个sql节点。现在集群环境如下：</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/6Gr6u.jpg" style="width: 632px; height: 209px;" /></p>
<p>
	在追加的过程中，发现MySQL Cluster对启动顺序要求严格，在没考虑热部署方案的情况下，必须停止了所有节点，重新按照management-&gt;data-&gt;sql的顺序启动节点。</p>
<p>
	现在测试对表的创建和修改的自动同步：</p>
<p>
	在任意SQL节点执行：（这里选择44.200节点）</p>
<pre class="brush:sql;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
create table bigdata_cluster(id int primary key, name varchar(20)) engine=ndbcluster default charset utf8;
</pre>
<p>
	创建表，注意表的引擎一定要指定ndbcluster，在201节点查看</p>
<pre class="brush:sql;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
show tables;</pre>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/1S4y1.jpg" style="width: 635px; height: 400px;" /></p>
<p>
	发现已经可以同步查询了。其实本来底层data节点对上层就是透明的，自然可以查到。多sql节点，就可以起到负载均衡的效果。</p>
<p>
	调整表和数据插入，都跟传统的MySQL方式相同，不再赘述，同样也是可以做到实时同步的，这里也测过了。下面通过JDBC代码测试下API操作的效果，同时也想灌入100w的数据，进行一下效率测试和对比。</p>
<p>
	在测试前，OneCoder先用SQLyog工具，测试了一下数据库远端访问权限，发现果然没有。在一个节点grant all了一下以后，却发现另一个节点仍然无法访问，搜索才知，原来MySQL Cluster的用户权限默认不是共享的，进行如下设置，在mysql终端执行：</p>
<pre class="brush:sql;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
mysql&gt; SOURCE /usr/local/mysql/share/ndb_dist_priv.sql;
mysql&gt; CALL mysql.mysql_cluster_move_privileges();
</pre>

即可完成权限共享，现在在一个终端设置的权限就是集群共享的了。在用SQLYog测试，果然均可以链接了。下面开始开发JDBC链接MySQL的代码：</p>

```java
/**
  * 向数据库中插入数据
  *
  * @param conn
  * @param totalRowCount
  * @param perRowCount
  * @param tableName
  * @author lihzh(OneCoder)
  * @throws SQLException
  * @date 2013-1-17 下午1:57:10
  */
private void insertDataToTable(Connection conn, String tableName,
long totalRowCount, long perRowCount) throws SQLException {
conn.setAutoCommit(false);
long start = System.currentTimeMillis();
String sql = "insert into " + tableName + " VALUES(?,?,?)";
System.out.println("Begin to prepare statement.");
PreparedStatement statement = conn.prepareStatement(sql);
for (int j = 0; j < TOTAL_ROW_COUNT / BATCH_ROW_COUNT; j++) {
long batchStart = System.currentTimeMillis();
for (int i = 0; i < BATCH_ROW_COUNT; i++) {
long id = j * BATCH_ROW_COUNT + i;
String name_pre = String.valueOf(id);
statement.setLong(1, id);
statement.setString(2, name_pre);
statement.setString(3, name_pre);
statement.addBatch();
}
System.out.println("It's up to batch count: " + BATCH_ROW_COUNT);
statement.executeBatch();
conn.commit();
long batchEnd = System.currentTimeMillis();
System.out.println("Batch data commit finished. Time cost: " + (batchEnd - batchStart));
}
long end = System.currentTimeMillis();
System.out.println("All data insert finished. Total time cost: " + (end - start));
}
```

<p>
	开始设置BATCH_ROW_COUNT为5w，结果报错：</p>
<blockquote>
	<p>
		java.sql.BatchUpdateException: Got temporary error 233 'Out of operation records in transaction coordinator (increase MaxNoOfConcurrentOperations)' from NDBCLUSTER</p>
</blockquote>
<p>
	意思比较明显，超过了<strong>MaxNoOfConcurrentOperations</strong>设置的值。该值默认为：32768。你可以通过修改config.ini里的配置改变默认值。不过有人提到，修改该值的同事，你也需要修改</p>
<p>
	MaxNoOfLocalOperations的值，并且建议后者的值超过前者值10%左右（1.1倍）。</p>
<p>
	这里为了避免麻烦，我们直接将代码的里预设值调小到2w，再运行代码。</p>
<blockquote>
	<p>
		Begin to prepare statement.<br />
		It's up to batch count: 20000<br />
		Batch data commit finished. Time cost: 20483<br />
		It's up to batch count: 20000<br />
		Batch data commit finished. Time cost: 19768<br />
		It's up to batch count: 20000<br />
		Batch data commit finished. Time cost: 20136<br />
		It's up to batch count: 20000<br />
		Batch data commit finished. Time cost: 19958<br />
		&hellip;&hellip;.<br />
		java.sql.BatchUpdateException: The table 'bigdata_cluster' is full</p>
</blockquote>
<p>
	无语&hellip;&hellip;表满了。共写入了88w条数据。每次batch写入时间稳定。再测试条件查询耗时：</p>

```java
/**
  * 查询特定的一个或者一组数据，打印查询耗时
  *
  * @param conn
  * @param tableName
  * @author lihzh
  * @throws SQLException
  * @date 2013-1-17 下午4:46:20
  */
private void searchData(Connection conn, String tableName) throws SQLException {
long start = System.currentTimeMillis();
String sql = "select * from " + tableName + " where name = ?";
PreparedStatement statement = conn.prepareStatement(sql);
statement.setString(1, "300");
ResultSet resultSet = statement.executeQuery();
resultSet.first();
System.out.println("Name is: " + resultSet.getObject("name"));
long end = System.currentTimeMillis();
System.out.println("Query one row from 88w record cost time: " + (end - start));
}
```

<p>
	通过另一个sql节点，根据没有索引的name字段查询耗时约1.4s，有索引的id查询耗时20ms左右。</p>
<p>
	再新建一个表，发现什么数据再也无法写入，看来是数据节点全局容量限制导致的。修改config.ini文件中的</p>
<blockquote>
	<p>
		DataMemory=80M&nbsp;&nbsp;&nbsp; # How much memory to allocate for data storage<br />
		IndexMemory=18M&nbsp;&nbsp; # How much memory to allocate for index storage<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # For DataMemory and IndexMemory, we have used the<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # default values. Since the "world" database takes up<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # only about 500KB, this should be more than enough for<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # this example Cluster setup.</p>
</blockquote>
<p>
	分别改为1400和384M。重启集群。再通过</p>
<pre class="brush:shell;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
ndb_mgm&gt; all report memoryusage
</pre>
<p>
	命令查看使用情况，</p>
<p style="text-align: center;">
	<img alt="" src="/images/oldposts/P9btE.jpg" style="width: 533px; height: 90px;" /></p>
<p>
	似乎恢复了正常。再向新表写入数据，成功。</p>
<p>
	测试删除数据，又遇到提示：</p>
<blockquote>
	<p>
		ERROR 1297 (HY000): Got temporary error 233 'Out of operation records in transaction coordinator (increase MaxNoOfConcurrentOperations)' from NDBCLUSTER</p>
</blockquote>
<p>
	看来真的得调整<strong>MaxNoOfConcurrentOperations</strong>参数的大小了。根据虚拟机内存情况（据说1约需要1kb内存。因此10w，大约100m内存），调整如下：</p>
<blockquote>
	<p>
		MaxNoOfConcurrentOperations=300000<br />
		MaxNoOfLocalOperations=330000</p>
</blockquote>
<p>
	重启，测试删除11w数据，通过。同时，再次测试向新表写入100w条数据，以20w为一组，也顺利通过了。</p>
<blockquote>
	<p>
		It's up to batch count: 200000<br />
		Batch data commit finished. Time cost: 268642<br />
		It's up to batch count: 200000<br />
		Batch data commit finished. Time cost: 241301<br />
		It's up to batch count: 200000<br />
		Batch data commit finished. Time cost: 209329<br />
		It's up to batch count: 200000<br />
		Batch data commit finished. Time cost: 207634<br />
		It's up to batch count: 200000<br />
		Batch data commit finished. Time cost: 241746<br />
		All data insert finished. Total time cost: 1168703</p>
</blockquote>
<p>
	目前的使用情况大致如此，接下来<a href="http://www.coderli.com">OneCoder</a>打算测试一下集群节点添加和数据自动分区读写情况。等有了结论在与大家分享。<br /></p>
