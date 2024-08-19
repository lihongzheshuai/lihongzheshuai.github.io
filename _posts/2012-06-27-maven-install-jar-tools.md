---
layout: post
title: Maven批量安装本地Jar文件小工具
date: 2012-06-27 21:51 +0800
author: onecoder
comments: true
tags: [Maven]
categories: [Java技术研究]
thread_key: 700
---
**Maven** 批量安装本地 Jar文件到本地Maven库小程序。根据自己的需求临时开发完成。

使用方式：

- 在**config.properties**中，配置待安装jar文件的存放路径。
- 安装时**groupId,artifactId,version**等信息，根据jar文件的文件名获得。采用分割"-"的方式，解析出来。所以，推荐jar的文件名中含有两个"-"。例如：**group-artifact-version.jar**。如果为**group-artifactversion.jar**，则**groupId=group，artifactId=version=artifactversion**。

```java
public class Main { 
     
    private static final Log _log = LogFactory.getLog(Main.class); 
    private static PropertyHelper propHelper = new PropertyHelper("config"); 
    private static Runtime _runRuntime = Runtime.getRuntime(); 
    private static boolean isDelete = Boolean.valueOf(propHelper.getValue("delete-installed-jar")); 
    private static boolean isMove = Boolean.valueOf(propHelper.getValue("move-installed-jar")); 
    private static final String KEY_JARPATH = "jar-path"; 
    private static final String KEY_BACKUPPATH = "back-path"; 
    private static final String ENCODE = "gbk"; 
    private static final String INSTALL_PATH = propHelper.getValue(KEY_JARPATH); 
    private static  String CMD_INSTALL_FILE; 
    private static  String CMD_BACKUP_JAR; 
     
    public static void main(String[] args) { 
         
        _log.info("The path of the jars is ["+INSTALL_PATH+"]."); 
        File file = new File(INSTALL_PATH); 
        if(!file.isDirectory()){ 
            _log.warn("The path must be a directory."); 
            return; 
        } 
        FilenameFilter filter = new JarFilter(); 
        File[] jarFiles = file.listFiles(filter); 
        for(File jar: jarFiles){ 
            installJarToMaven(jar); 
            if(isDelete){ 
                _log.info("Delete the original jar file ["+jar.getName()+"]."); 
                jar.delete(); 
            }else{ 
                if(isMove){ 
                    String backupPath = propHelper.getValue(KEY_BACKUPPATH); 
                    backupJar(jar,file,backupPath); 
                } 
            } 
        } 
    } 
 
    private static void backupJar(File jar, File file, String backupPath) { 
        CMD_BACKUP_JAR = "copy "+INSTALL_PATH+File.separator+jar.getName()+" "+backupPath; 
        String[] cmds = new String[]{"cmd", "/C",CMD_BACKUP_JAR}; 
        try { 
            Process process =_runRuntime.exec(cmds,null,file); 
            printResult(process); 
        } catch (IOException e) { 
            e.printStackTrace(); 
        } 
            _log.info("The jar ["+jar.getName()+"]  is backup, it&#39;s will be deleted.\r"); 
            jar.delete(); 
    } 
 
    private static void installJarToMaven(File file) { 
        String fileName = file.getName(); 
        String jarName = getJarName(fileName); 
        String groupId=null; 
        String artifactId=null; 
        String version=null; 
        int groupIndex = jarName.indexOf("-"); 
        if(groupIndex==-1){ 
            version = artifactId = groupId = jarName; 
        }else{ 
            groupId = jarName.substring(0,groupIndex); 
            int versionIndex = jarName.lastIndexOf("-"); 
            if(groupIndex==versionIndex){ 
                version = artifactId = jarName.substring(versionIndex+1,jarName.length()); 
            }else{ 
                artifactId = jarName.substring(groupIndex+1,versionIndex); 
                version = jarName.substring(versionIndex+1,jarName.length()); 
            } 
        } 
        _log.info("Jar ["+jarName+"] will be installed with the groupId="+groupId+" ," 
                +"artifactId="+artifactId+" , version="+version+"."); 
        executeInstall( groupId,  artifactId,  version, file.getPath()); 
    } 
 
    private static void executeInstall(String groupId, String artifactId, 
            String version, String path) { 
        CMD_INSTALL_FILE = createInstallFileCMD( groupId,  artifactId, 
                 version,  path); 
        String[] cmds = new String[]{"cmd", "/C",CMD_INSTALL_FILE}; 
        try { 
            Process process = _runRuntime.exec(cmds); 
            printResult(process); 
        } catch (IOException e) { 
            e.printStackTrace(); 
        } 
    } 
     
    private static void printResult(Process process) throws IOException { 
        InputStream is = process.getInputStream(); 
        BufferedReader br = new BufferedReader(new InputStreamReader(is,ENCODE)); 
        String lineStr; 
        while((lineStr= br.readLine()) !=null){ 
            System.out.println(lineStr); 
        } 
    } 
 
    private static String createInstallFileCMD(String groupId, 
            String artifactId, String version, String path) { 
        StringBuffer sb = new StringBuffer(); 
        sb.append("mvn install:install-file -DgroupId=").append(groupId) 
            .append(" -DartifactId=").append(artifactId) 
            .append(" -Dversion=").append(version) 
            .append(" -Dpackaging=jar") 
            .append(" -Dfile=").append(path); 
        _log.debug(sb.toString()); 
        return sb.toString(); 
    } 
 
    private static String getJarName(String fileName) { 
        int index = fileName.indexOf(".jar"); 
        return fileName.substring(0, index); 
    } 
 
} 
```

```
public class PropertyHelper { 
     
    private ResourceBundle propBundle;  
     
    public PropertyHelper(String bundle){ 
        propBundle = PropertyResourceBundle.getBundle(bundle); 
    } 
     
    public  String getValue(String key){ 
        return this.propBundle.getString(key); 
    } 
 
} 
```

**sourceforge**地址：

- <a href="https://sourceforge.net/projects/maventools/files/" target="\_blank">https://sourceforge.net/projects/maventools/files/</a>
