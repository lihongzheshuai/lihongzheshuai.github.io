---
layout: post
title: Maven库中.lastUpdated文件自动清除工具
date: 2012-06-26 21:43 +0800
author: onecoder
comments: true
tags: [Maven]
categories: [Java技术研究]
thread_key: 695
---

最近开发过程中，在更新**maven**库时，如果网络问不定或者是一些自己手动安装到本地maven库的jar包，在中心库找不到对应的jar，会生成一些**.lastUpdated**文件，会导致m2e工具无法找到依赖的jar包，从而提示编译错误。

对于该问题，我也没有找到很好的解决方案，只能手动删除一下lastUpdated文件。文件多时十分繁琐。网上看到别人的解决方案也有利用命令行命令，匹配文件扩展名批量删除的。命令行不会，于是就写了几行代码用于删除.lastUpdated文件。如有其他直接的解决方案，望不吝赐教，写代码实属无奈之举。

```java
public class DelLastUpdated { 
 
    private static PropertyHelper propHelper = new PropertyHelper("config"); 
    private static final String KEY_MAVEN_REPO = "maven.repo"; 
    private static final String MAVEN_REPO_PATH = propHelper 
            .getValue(KEY_MAVEN_REPO); 
    private static final String FILE_SUFFIX = "lastUpdated"; 
    private static final Log _log = LogFactory.getLog(DelLastUpdated.class); 
 
    /** 
     * @param args 
     */ 
    public static void main(String[] args) { 
        File mavenRep = new File(MAVEN_REPO_PATH); 
        if (!mavenRep.exists()) { 
            _log.warn("Maven repos is not exist."); 
            return; 
        } 
        File[] files = mavenRep.listFiles((FilenameFilter) FileFilterUtils 
                .directoryFileFilter()); 
        delFileRecr(files,null); 
        _log.info("Clean lastUpdated files finished."); 
    } 
 
    private static void delFileRecr(File[] dirs, File[] files) { 
        if (dirs != null && dirs.length &gt; 0) { 
            for(File dir: dirs){ 
                File[] childDir = dir.listFiles((FilenameFilter) FileFilterUtils 
                .directoryFileFilter()); 
                File[] childFiles = dir.listFiles((FilenameFilter) FileFilterUtils 
                .suffixFileFilter(FILE_SUFFIX)); 
                delFileRecr(childDir,childFiles); 
            } 
        } 
        if(files!=null&&files.length&gt;0){ 
            for(File file: files){ 
                if(file.delete()){ 
                    _log.info("File: ["+file.getName()+"] has been deleted."); 
                } 
            } 
        } 
    } 
 
} 
```

配置文件：**config.properties**

```properties
maven.repo=D:\\.m2\\repository 
```

源码下载地址：
	
- svn:<a href="https://svn.code.sf.net/p/maventools/code/trunk/maven-tools" target="\_blank">https://svn.code.sf.net/p/maventools/code/trunk/maven-tools</a>

工程里还包括一个批量安装jar包到本地maven库的工具。以后再另外介绍。