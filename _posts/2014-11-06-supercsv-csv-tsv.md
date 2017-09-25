---
layout: post
title: 利用supercsv读写CSV、TSV文件
date: 2014-11-06 16:33 +0800
author: onecoder
comments: true
tags: [Java]
thread_key: 1849
---
先简单介绍下CSV和TSV文件的区别：
<blockquote>TSV ，Tab-separated values的缩写，即制表符分隔值。关于TSV标准，参考：<a href="http://en.wikipedia.org/wiki/Tab-separated_values">http://en.wikipedia.org/wiki/Tab-separated_values</a>
CSV，Comma-separated values，即逗号分隔值。关于CSV标准，参考：<a href="http://en.wikipedia.org/wiki/Comma-separated_values">http://en.wikipedia.org/wiki/Comma-separated_values</a></blockquote>
项目需要把原有的tsv文件数据整理一下形成更方便使用的新tsv文件（加几列）。涉及到tsv文件的读写。其实自己实现也是很简单的功能，不过正好有现成的工具包supercsv，就拿来用用试试。
官网地址：<a href="http://supercsv.sourceforge.net/index.html">http://supercsv.sourceforge.net/index.html</a>

文档可以说是清晰明了，网上其实也有不少用supercsv解析csv文件的例子，不过从tsv和csv的区别就可以看出，完全一套代码是可以解决的，只要换个分隔符就好饿了。supercsv里，也确实做到了。 先附上官网的例子：<a href="http://supercsv.sourceforge.net/examples_reading.html">http://supercsv.sourceforge.net/examples_reading.html</a>
待解析的csv文件：
<blockquote>customerNo,firstName,lastName,birthDate,mailingAddress,married,numberOfKids,favouriteQuote,email,loyaltyPoints
1,John,Dunbar,13/06/1945,"1600 Amphitheatre Parkway
Mountain View, CA 94043
United States",,,"""May the Force be with you."" - Star Wars",jdunbar@gmail.com,0
2,Bob,Down,25/02/1919,"1601 Willow Rd.
Menlo Park, CA 94025
United States",Y,0,"""Frankly, my dear, I don't give a damn."" - Gone With The Wind",bobdown@hotmail.com,123456
3,Alice,Wunderland,08/08/1985,"One Microsoft Way
Redmond, WA 98052-6399
United States",Y,0,"""Play it, Sam. Play ""As Time Goes By."""" - Casablanca",throughthelookingglass@yahoo.com,2255887799
4,Bill,Jobs,10/07/1973,"2701 San Tomas Expressway
Santa Clara, CA 95050
United States",Y,3,"""You've got to ask yourself one question: ""Do I feel lucky?"" Well, do ya, punk?"" - Dirty Harry",billy34@hotmail.com,36</blockquote>
利用MapReader方式解析的代码：

```java
/**
 * An example of reading using CsvMapReader.
 */private static void readWithCsvMapReader() throws Exception {
        
        ICsvMapReader mapReader = null;
        try {
                mapReader = new CsvMapReader(new FileReader(CSV_FILENAME), CsvPreference.STANDARD_PREFERENCE);
                
                // the header columns are used as the keys to the Map
                final String[] header = mapReader.getHeader(true);
                final CellProcessor[] processors = getProcessors();
                
                Map&lt;String, Object&gt; customerMap;
                while( (customerMap = mapReader.read(header, processors)) != null ) {
                        System.out.println(String.format("lineNo=%s, rowNo=%s, customerMap=%s", mapReader.getLineNumber(),
                                mapReader.getRowNumber(), customerMap));
                }
                
        }
        finally {
                if( mapReader != null ) {
                        mapReader.close();
                }
        }}

/**
 * Sets up the processors used for the examples. There are 10 CSV columns, so 10 processors are defined. Empty
 * columns are read as null (hence the NotNull() for mandatory columns).
 * 
 * @return the cell processors
 */private static CellProcessor[] getProcessors() {
        
        final String emailRegex = "[a-z0-9\\._]+@[a-z0-9\\.]+"; // just an example, not very robust!
        StrRegEx.registerMessage(emailRegex, "must be a valid email address");
        
        final CellProcessor[] processors = new CellProcessor[] { 
                new UniqueHashCode(), // customerNo (must be unique)
                new NotNull(), // firstName
                new NotNull(), // lastName
                new ParseDate("dd/MM/yyyy"), // birthDate
                new NotNull(), // mailingAddress
                new Optional(new ParseBool()), // married
                new Optional(new ParseInt()), // numberOfKids
                new NotNull(), // favouriteQuote
                new StrRegEx(emailRegex), // email
                new LMinMax(0L, LMinMax.MAX_LONG) // loyaltyPoints
        };
        
        return processors;}
```

样例的代码恐怕清楚的不能再清楚了。只需要解释一点，分隔符是通过CsvPreference.STANDARD_PREFERENCE设定的。如果想要解析TSV文件，只需要将这里换成CsvPreference TAB_PREFERENCE即可。

附个源码吧：

```java
/**
      * Ready to use configuration that should cover 99% of all usages.
      */
      public static final CsvPreference STANDARD_PREFERENCE = new CsvPreference.Builder('"' , ',',"\r\n").build();
     
      /**
      * Ready to use configuration for Windows Excel exported CSV files.
      */
      public static final CsvPreference EXCEL_PREFERENCE = new CsvPreference.Builder('"' , ',' , "\n").build();
     
      /**
      * Ready to use configuration for north European excel CSV files (columns are separated by ";" instead of ",")
      */
      public static final CsvPreference EXCEL_NORTH_EUROPE_PREFERENCE = new CsvPreference.Builder('"' , ';' , "\n" ).build();
     
      /**
      * Ready to use configuration for tab -delimited files.
      */
      public static final CsvPreference TAB_PREFERENCE = new CsvPreference.Builder( '"', '\t', "\n").build();
```