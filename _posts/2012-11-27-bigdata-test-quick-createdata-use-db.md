---
layout: post
title: 海量数据测试，利用数据库查询拷贝快速构造测试数据
date: 2012-11-27 17:19 +0800
author: onecoder
comments: true
tags: [Hive]
categories: [大数据]
thread_key: 1251
---
这也是<a href="http://www.coderli.com">OneCoder</a>在数据测试过程中遇到的问题，不一定有多少普试性，但是也许可以解决你的问题。

海量数据测试，数据导入一般是非常耗时的过程。<a href="http://www.coderli.com">OneCoder</a>这里面对大约2T左右数据的导入问题，头疼不已，时间有限。本来准备的方式是将事先生成好的数据文件导入HBase中，这里有两个比较耗时的过程，put到hdfs和import到HBase中，昨天测试5G数据导入到HBase中，居然用了20min。如此估算，不能忍。

交流中，获知可以考虑先导入部分数据，然后利用这部分数据，在数据库中查询出来，然后修改比如时间字段的值，然后在合并入表中。这样，利用一天的数据，就可以构造出2、4，8，16天的数据。效率会高出很多。

当然，如果你的测试是基于真实的业务数据的，那么这种方式不适合你。如果你是构造的数据，那么可以尝试一下这种方式。<a href="http://www.coderli.com">OneCoder</a>基于MySQL写了一个自动化的代码，作为参考。真实海量数据的一般可能是基于Hive的，只要修改链接串和可能少量的SQL语句即可。

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * 用于在MySQL中数据翻倍复制
 * 
 * @author OneCoder(OneCoder)
 * @date 2012-11-27 下午3:28:16
 * @Blog http://www.coderli.com
 */
public class MySQLDataCopy {

	private static final int COPY_COUNT = 9;
	private static final long ONE_DAY_MILLISECOND = 3600 *24 *1000L;
	private static final String SQL_CREATE_TABLE_ONE = "CREATE TABLE metric_t1 AS SELECT * FROM metric;";
	private static final String SQL_CREATE_TABLE_TWO = "CREATE TABLE metric_t2 AS SELECT * FROM metric LIMIT 1;";
	private static final String SQL_DELETE_DATA_TABLE_TWO = "DELETE FROM metric_t2;";
	private static final String SQL_INSERT_DATA_TABLE_TWO_PREFIX = "INSERT INTO metric_t2 SELECT cpu, id, recordtime + ";
	private static final String SQL_INSERT_DATA_TABLE_TWO_MIDDLE = " AS recordtime, CONCAT(id,\"_\",recordtime + ";
	private static final String SQL_INSERT_DATA_TABLE_TWO_PRSTFIX = ") AS rowkey FROM metric;";
	private static final String SQL_DELETE_DATA = "DELETE FROM metric;";
	private static final String SQL_INSERT_DATA = "INSERT INTO metric SELECT * FROM (SELECT * FROM metric_t1 UNION ALL SELECT * FROM metric_t2) tmp;";
	private static final String SQL_DROP_TABLE_ONE = "DROP TABLE metric_t1;";
	private static final String SQL_DROP_TABLE_TWO = "DROP TABLE metric_t2;";
	
	

	static {
		try {
			Class.forName("com.mysql.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
	}

	/**
	 * @param args
	 * @author OneCoder(OneCoder)
	 * @throws SQLException
	 * @date 2012-11-27 下午3:28:16
	 */
	public static void main(String[] args) throws SQLException {
		Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/test", "root",
				"root");
		int times = 1;
		for (int i = 1; i <= COPY_COUNT; i++) {
			System.out.println("Begin to copy: " + i +" time");
			conn.createStatement().execute(SQL_CREATE_TABLE_ONE);
			System.out.println("Create table t1 finished");
			conn.createStatement().execute(SQL_CREATE_TABLE_TWO);
			System.out.println("Create table t2 finished");
			conn.createStatement().execute(SQL_DELETE_DATA_TABLE_TWO);
			System.out.println("Delete table t2 data");
			conn.createStatement().execute(createInsertDataToTableTwoSQL(times));
			System.out.println("Insert into table t2 new data.");
			conn.createStatement().execute(SQL_DELETE_DATA);
			System.out.println("Delete table metric data");
			conn.createStatement().execute(SQL_INSERT_DATA);
			System.out.println("Insert new data into metric");
			conn.createStatement().execute(SQL_DROP_TABLE_ONE);
			System.out.println("Drop table t1");
			conn.createStatement().execute(SQL_DROP_TABLE_TWO);
			System.out.println("Drop table t1");
			times *= 2;
		}
	}

	private static String createInsertDataToTableTwoSQL(int count) {
		long addNum = count * ONE_DAY_MILLISECOND;
		StringBuilder sbuilder = new StringBuilder();
		sbuilder.append(SQL_INSERT_DATA_TABLE_TWO_PREFIX).append(addNum)
				.append(SQL_INSERT_DATA_TABLE_TWO_MIDDLE).append(addNum)
				.append(SQL_INSERT_DATA_TABLE_TWO_PRSTFIX);
		return sbuilder.toString();
	}

}
```

初学者，请勿见笑，多多指教：）

