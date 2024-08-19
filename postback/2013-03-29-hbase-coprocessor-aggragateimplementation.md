---
layout: post
title: HBase 利用Coprocessor实现聚合函数
date: 2013-03-29 20:53 +0800
author: onecoder
comments: true
tags: [HBase]
thread_key: 1427
---
<p>
	HBase默认不支持聚合函数（sum,avg等）。可利用HBase的coprocessor特性实现。这样做的好处是利用regionserver在服务端进行运算。效率高，避免客户端取回大量数据，占用网络带宽，消耗大量内存等。</p>
<p>
	实现方式：</p>
<p>
	利用HBase提供的endPoint类型的AggregateImplementation Coprocess，配合AggregationClient访问客户端实现RegionServer端的集合计算。AggregationClient访问代码如下：</p>

```java
aggregationClient.avg(Bytes. toBytes("TableName"), ci, scan);
```

<p>
	scan即为要计算列的查询条件。这里有一个ColumnInterperter类型的参数ci。即列解释器，用于解析列中的值。HBase默认提供了LongColumnInterpreter。而我要处理的值是double类型的，所以先实现了一个DoubleColumnInterpreter。（从JIRA上看Doulbe类型的解释器好像正在开发中）。ColumnInterpreter接口的实现会在AggregateImplementation</p>

```java
/**
* Double类型的列解释器实现
*
 * @author OneCoder
*/
public class DoubleColumnInterpreter implements
           ColumnInterpreter<Double, Double> {

     @Override
     public void write(DataOutput out) throws IOException {


     }

     @Override
     public void readFields(DataInput in) throws IOException {


     }

     @Override
     public Double getValue( byte[] colFamily, byte[] colQualifier, KeyValue kv)
                 throws IOException {
            if (kv == null)
                 return null;
            // 临时解决方案，如果采用Bytes.toDouble(kv.getValue())会报错，偏移量大于总长度。
            // toDouble(getBuffer(), getValueOffset)，偏移量也不对。
            return Double. valueOf(new String(kv.getValue()));
     }


     @Override
     public Double add(Double l1, Double l2) {
            if (l1 == null ^ l2 == null) {
                 return l1 == null ? l2 : l1;
           } else if (l1 == null) {
                 return null;
           }
            return l1 + l2;
     }

     @Override
     public Double getMaxValue() {
            // TODO Auto-generated method stub
            return null;
     }


     @Override
     public Double getMinValue() {
            // TODO Auto-generated method stub
            return null;
     }

     @Override
     public Double multiply(Double o1, Double o2) {
            if (o1 == null ^ o2 == null) {
                 return o1 == null ? o2 : o1;
           } else if (o1 == null) {
                 return null;
           }
            return o1 * o2;
     }


     @Override
     public Double increment(Double o) {
            // TODO Auto-generated method stub
            return null;
     }

     @Override
     public Double castToReturnType(Double o) {
            return o.doubleValue();
     }


     @Override
     public int compare(Double l1, Double l2) {
            if (l1 == null ^ l2 == null) {
                 return l1 == null ? -1 : 1; // either of one is null.
           } else if (l1 == null)
                 return 0; // both are null
            return l1.compareTo(l2); // natural ordering.
     }


     @Override
     public double divideForAvg(Double o, Long l) {
            return (o == null || l == null) ? Double. NaN : (o.doubleValue() / l
                     .doubleValue());
     }
}
```

<p>
	导出jar包上传到HBase Region节点的lib下。然后配置RegionServer的Coprocessor。在服务端hbase-site.xml中，增加</p>

```xml
<property>
            <name >hbase.coprocessor.region.classes </name >
           <value >org.apache.hadoop.hbase.coprocessor.AggregateImplementation </value >
 </property >    
```

<p>
	重启服务，使配置和jar生效。然后调用AggregationClient中提供的avg, max等聚合函数，即可在region端计算出结果，返回。</p>

