---
layout: post
title: MySQL Cluster写入效率测试
date: 2013-02-27 23:10 +0800
author: onecoder
comments: true
tags: [MySQL]
thread_key: 1358
---
<p>
	MySQL Cluster使用到目前为止遇到渴望得到答案的问题，也是直接影响使用的问题就是MySQL Cluster的写入效率问题和Cluster是否适合大数据存储、如何配置存储的问题。</p>

<!--break-->

<p>
	在之前的测试中MySQL Cluster的写入效率一直不佳，这也是直接影响能否使用MySQL Cluster的关键。现在我们来仔细测试一下。使用的环境略有变化。</p>
<p>
	Data节点的内存扩展为4G。</p>
<p>
	集群配置如下：</p>
<pre class="brush:plain;first-line:1;pad-line-numbers:true;highlight:null;collapse:false;">
[ndbd default]

# Options affecting ndbd processes on all data nodes:

NoOfReplicas=2    # Number of replicas

DataMemory=2000M    # How much memory to allocate for data storage

IndexMemory=300M   # How much memory to allocate for index storage

                  # For DataMemory and IndexMemory, we have used the

                  # default values. Since the "world" database takes up

                  # only about 500KB, this should be more than enough for

                  # this example Cluster setup.

MaxNoOfConcurrentOperations=1200000

MaxNoOfLocalOperations=1320000
</pre>
<p>
	测试代码如下：</p>

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
      * @date 2013 -1 -17 下午1:57:10
      */
     private void insertDataToTable(Connection conn, String tableName,
                 long totalRowCount, long perRowCount, long startIndex)
                 throws SQLException {
           conn.setAutoCommit( false);
           String sql = "insert into " + tableName + " VALUES(?,?,?)";
           System. out.println( "Begin to prepare statement.");
           PreparedStatement statement = conn.prepareStatement(sql);
            long sum = 0L;
            for ( int j = 0; j < TOTAL_ROW_COUNT / BATCH_ROW_COUNT; j++) {
                 long batchStart = System. currentTimeMillis();
                 for ( int i = 0; i < BATCH_ROW_COUNT; i++) {
                      long id = j * BATCH_ROW_COUNT + i + startIndex;
                     String name_pre = String. valueOf(id);
                     statement.setLong(1, id);
                     statement.setString(2, name_pre);
                     statement.setString(3, name_pre);
                     statement.addBatch();
                }
                System. out.println( "It's up to batch count: " + BATCH_ROW_COUNT);
                statement.executeBatch();
                conn.commit();
                 long batchEnd = System. currentTimeMillis();
                 long cost = batchEnd - batchStart;
                System. out.println( "Batch data commit finished. Time cost: "
                           + cost);
                sum += cost;
           }
           System. out.println( "All data insert finished. Total time cost: "
                     + sum);
           System. out.println( "Avg cost: "
                     + sum/5);
     }

```

<p>
	分下列情景进行写入测试。</p>
<p>
	数据加载、写入在内存中时，在独立的新库、新表中一次写入100，1000，10000，50000条记录，分别记录其耗时情况。（5次平均）</p>
<blockquote>
	<p>
		100：260ms</p>
	<p>
		1000：1940ms</p>
	<p>
		10000：17683ms(12000-17000)</p>
	<p>
		50000： 93308、94730、90162、94849、162848</p>
</blockquote>
<p>
	与普通单点MySQL写入效率进行对比（2G内存）</p>
<blockquote>
	<p>
		100：182ms<br />
		1000：1624ms<br />
		10000：14946ms<br />
		50000：84438ms</p>
</blockquote>
<p>
	<strong>&nbsp; &nbsp; 双线程并发写入测试</strong></p>
<p>
	由于只有两个SQL节点，所以这里只采用双线程写入的方法进行测试。代码上采用了简单的硬编码</p>

```java
/**
      * 多线程并行写入测试
      *
      * @author lihzh(OneCoder)
      * @blog http://www.coderli.com
      * @date 2013 -2 -27 下午3:39:56
      */
     private void parallelInsert() {
            final long start = System. currentTimeMillis();
           Thread t1 = new Thread( new Runnable() {
                 @Override
                 public void run() {
                      try {
                           Connection conn = getConnection(DB_IPADDRESS, DB_PORT,
                                      DB_NAME, DB_USER, DB_PASSOWRD);
                           MySQLClusterDataMachine dataMachine = new MySQLClusterDataMachine();
                           dataMachine.insertDataToTable(conn, TABLE_NAME_DATAHOUSE,
                                     500, 100, 0);
                            long end1 = System.currentTimeMillis();
                           System. out.println( "Thread 1 cost: " + (end1 - start));
                     } catch (SQLException e) {
                           e.printStackTrace();
                     }
                }
           });


           Thread t2 = new Thread( new Runnable() {
                 @Override
                 public void run() {
                      try {
                           Connection conn = getConnection(DB_IPADDRESS_TWO, DB_PORT,
                                      DB_NAME, DB_USER, DB_PASSOWRD);
                           MySQLClusterDataMachine dataMachine = new MySQLClusterDataMachine();
                           dataMachine.insertDataToTable(conn, TABLE_NAME_DATAHOUSE,
                                     500, 100, 500);
                            long end2 = System.currentTimeMillis();
                           System. out.println( "Thread 2 cost: " + (end2 - start));
                     } catch (SQLException e) {
                           e.printStackTrace();
                     }
                }
           });
           t1.start();
           t2.start();
     }
```

<p>
	测试结果：</p>
<p>
<!--?xml version="1.0" encoding="UTF-8" standalone="no"?--></p>
<table border="1" cellpadding="2" cellspacing="0" style="font-family: Arial; " width="100%">
	<tbody>
		<tr>
			<td valign="top">
				(总条数/每次)</td>
			<td valign="top">
				线程1（总/平均- 各写一半数据）</td>
			<td valign="top">
				线程2</td>
			<td valign="top">
				并行总耗时</td>
			<td valign="top">
				单线程单点</td>
		</tr>
		<tr>
			<td valign="top">
				1000/100</td>
			<td valign="top">
				985/197</td>
			<td valign="top">
				1005/201</td>
			<td valign="top">
				1005/201</td>
			<td valign="top">
				2264/226</td>
		</tr>
		<tr>
			<td valign="top">
				10000/1000</td>
			<td valign="top">
				9223/1836</td>
			<td valign="top">
				9297/1850</td>
			<td valign="top">
				9297/1850</td>
			<td valign="top">
				19405/1940</td>
		</tr>
		<tr>
			<td valign="top">
				100000/10000</td>
			<td valign="top">
				121425/12136</td>
			<td valign="top">
				122081/12201</td>
			<td valign="top">
				121425/12136</td>
			<td valign="top">
				148518/14851<br />
				&nbsp;</td>
		</tr>
	</tbody>
</table>
<p>
	从结果可以看出，在10000条以下批量写入的情况下，SQL节点的处理能力是集群的瓶颈，双线程双SQL写入相较单线程单节点效率可提升一倍。但是当批量写入数据达到一定数量级，这种效率的提升就不那么明显了，应该是集群中的其他位置也产生了瓶颈。</p>
<p>
	注：由于各自测试环境的差异，测试数据仅可做内部比较，不可外部横向对比。仅供参考。</p>
<p>
	写入测试，要做的还很多，不过暂时告一段落。大数据存储和查询测试，随后进行。</p>