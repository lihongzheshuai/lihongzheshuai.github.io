---
layout: post
title: 自定义xsd文件及使用
date: 2014-04-02 23:55 +0800
author: onecoder
comments: true
tags: [XML]
thread_key: 1633
---
<p>
	需要规范用户开发并行计算任务的配置文件的格式，自然考虑定义任务配置的xsd文件。对于xsd的介绍可以参考：<br />
	http://www.w3school.com.cn/schema/schema_example.asp<br />
	这里，<a href="http://www.coderli.com">OneCoder</a>给出想要定义的XML文件的格式以及根据该格式定义出的xsd文件。供大家参考。其实整个定义过程还是很简单的。</p>
<p>
	定义后的xsd文件如下(省略冗余的配置项)：</p>

```xml
<?xml version="1.0" encoding= "UTF-8"?>
<xsd:schema xmlns= "http://www.coderli.com/shurnim" xmlns:xsd= "http://www.w3.org/2001/XMLSchema"
     targetNamespace="http://www.coderli.com/shurnim" elementFormDefault="qualified" >
     <xsd:simpleType name ="IDType">
           <xsd:restriction base ="xsd:string">
               <xsd:pattern value= "[\w,\-,_]{1,32}"></xsd:pattern >
           </xsd:restriction >
     </xsd:simpleType >
     <!-- 定义类型 -->
     <xsd:complexType name ="jobType">
           <xsd:sequence >
               <xsd:element name ="jobId" type="IDType">
                    <xsd:annotation >
                         <xsd:documentation ><![CDATA[任务ID，唯一区别一个并行计算任务，必须唯一 ]]></xsd:documentation >
                    </xsd:annotation >
               </xsd:element >
               <xsd:element name ="jobName" type= "xsd:string" minOccurs ="0">
                    <xsd:annotation >
                         <xsd:documentation ><![CDATA[任务名称，可选 ]]></xsd:documentation >
                    </xsd:annotation >
               </xsd:element >
             </xsd:sequence >
     </xsd:complexType >
     <!-- 定义类型 -->
     <xsd:complexType name ="jobBundleType">
           <xsd:sequence >
               <xsd:element name ="job" maxOccurs= "unbounded" type="jobType" >
               </xsd:element >
           </xsd:sequence >
           <xsd:attribute name ="bundleName" type= "IDType"></xsd:attribute >
     </xsd:complexType >


     <xsd:element name ="jobBundle" type="jobBundleType">
     </xsd:element >
</xsd:schema>
```

<p>
	对应的xml文件即为：</p>

```xml
<?xml version="1.0" encoding= "UTF-8"?>
<jobBundle bundleName= "sldfjlaksd" xmlns= "http://www.coderli.com/shurnim"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.coderli.com/shurnim pc-3.0.xsd">
     <job >
           <jobId >df-asd_asdf238-sdf_adf</ jobId>
           <distributorClassName ></distributorClassName >
     </job >
</jobBundle>
```

<p>
	通过对比xml和xsd文件其实可以很容易的学会xsd的定义规则。定义元素，区分基本数据类型和"复杂"的可嵌套的数据类型。基本数据类型支持校验，校验又支持正则等等。这些基础的知识在w3cschool上都有。这里稍微绕一点的知识可能就是xml的命名空间了。这个网上介绍的文章也很多，可以参考：http://www.cnblogs.com/martin-chen/archive/2011/02/24/xml-studynote-namespace.html</p>
<p>
	xml引用xsd的方式有多种，上面的文章里也有介绍。引用本地xsd的时候是配置的路径，相对自己所在的文件夹开始的。</p>
<p>
	注意一点，就在eclipse里开发xsd的时候，我是一遍开发一遍在xml中进行测试的。这个时候每修改一处xsd，需要重新打开xml才能重新加载。这一个小问题，却让OneCoder吃了不少苦头。最后才&ldquo;幡然醒悟&rdquo;。</p>
<p>
	最后，附上利用xsd校验xml和解析xml头中引用的xsd文件的Java代码。既然定义了，就要合理的利用：</p>

```java
package com.coderli.schema;


import java.io.InputStream;
import java.net.URL;


import javax.xml.transform.Source;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;


import org.dom4j.io.OutputFormat;
import org.dom4j.io.XMLWriter;
import org.dom4j.util.XMLErrorHandler;
import org.xml.sax.SAXException;


/**
* @author lihzh
* @date 2014年4月2日 下午2:34:08
*/
public class JobConfigXMLValidateTest {


     public static void main(String args[]) throws SAXException {
           validateXMLByXSD();
     }


     /**
      *
      * @throws SAXException
      * @author lihzh
      * @date 2014年4月2日 下午4:25:39
      */
     public static void validateXMLByXSD() throws SAXException {
          String xmlFileName = "com/coderli/schema/shurnim.xml" ;
          String xsdFileName = "com/coderli/schema/shurnim.xsd" ;
           // 建立schema工厂
          SchemaFactory schemaFactory = SchemaFactory
                    . newInstance("http://www.w3.org/2001/XMLSchema");
           // 建立验证文档文件对象，利用此文件对象所封装的文件进行schema验证
          URL schemaFile = JobConfigXMLValidateTest. class.getClassLoader()
                   .getResource(xsdFileName);
           // 利用schema工厂，接收验证文档文件对象生成Schema对象
          Schema schema = schemaFactory.newSchema(schemaFile);
           // 通过Schema产生针对于此Schema的验证器，利用schenaFile进行验证
          Validator validator = schema.newValidator();
           // 创建默认的XML错误处理器
          XMLErrorHandler errorHandler = new XMLErrorHandler();
          validator.setErrorHandler(errorHandler);
           // 得到验证的数据源
          InputStream xmlStream = JobConfigXMLValidateTest. class.getClassLoader()
                   .getResourceAsStream(xmlFileName);
          Source source = new StreamSource(xmlStream);
           // 开始验证，成功输出success!!!，失败输出fail
           try {
              validator.validate(source);
              XMLWriter writer = new XMLWriter(OutputFormat.createPrettyPrint());
               // 如果错误信息不为空，说明校验失败，打印错误信息
               if (errorHandler.getErrors().hasContent()) {
                   System. out.println( "XML文件通过XSD文件校验失败！" );
                   writer.write(errorHandler.getErrors());
              } else {
                   System. out.println( "Good! XML文件通过XSD文件校验成功！" );
              }
              ;
          } catch (Exception ex) {
              ex.printStackTrace();
          }
     }
}
```

<p>
	当不合法的时候，打印信息如下：(例如设置jobId为：asdfa23##4)</p>
<p>
	XML文件通过XSD文件校验失败！</p>
<blockquote>
	<p>
		<errors>
		&nbsp; <error column="28" line="6">cvc-pattern-valid: Value &#39;asdfa23##4&#39; is not facet-valid with respect to pattern &#39;[\w,\-,_]{1,32}&#39; for type &#39;IDType&#39;.</error><br />
		&nbsp; <error column="28" line="6">cvc-type.3.1.3: The value &#39;asdfa23##4&#39; of element &#39;jobID&#39; is not valid.</error><br />
		</errors></p>
</blockquote>
<p>
	读取xml中引用的xsd信息的代码：</p>

```java
SAXReader saxReader = new SAXReader();
               Document document = saxReader.read(configFile);
               Element root = document.getRootElement();
               QName qName = new QName("schemaLocation", new Namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance"));
               Attribute xsdAddr = root.attribute(qName);
               System.out.println(xsdAddr.getText());
```