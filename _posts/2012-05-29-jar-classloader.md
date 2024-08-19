---
layout: post
title: Java文件读取 jar包内文件读取
date: 2012-05-29 22:12 +0800
author: onecoder
comments: true
tags: [Classloader, Java]
categories: [Java技术研究,JDK]
thread_key: 134
---

最近遇到一些Jar包内外配置文件读取的问题。索性自己测试总结一下，与大家分享。

主要是关于ClassLoader.getResource和Class.getResource方法路径区别的问题。
<!--more-->

# 1. 绝对路径文件读取，最简单，最直接的方式
```java
	/**
	 * 从绝对路径读取文件，最基本的文件读取方式
	 * 
	 * @author lihzh
	 * @data 2012-4-11 下午9:33:44
	 */
	@Test
	public void testGetFileFromAbsolutePath() {
		String dirPathNotUnderClasspath = "D:\\workspace-home\\JavaDemo\\conf";
		File dirFile = new File(dirPathNotUnderClasspath);
		AssertDirFile(dirFile);
	}

   /**
	 * 对文件夹类型文件的断言
	 * 
	 * @param dirFile
	 * @author lihzh
	 * @data 2012-4-11 下午9:49:14
	 */
	private void AssertDirFile(File dirFile) {
		// 文件存在
		Assert.assertTrue(dirFile.exists());
		// 是绝对路径
		Assert.assertTrue(dirFile.isAbsolute());
		// 是个文件夹
		Assert.assertTrue(dirFile.isDirectory());
		// 获取文件夹下所有文件
		File[] files = dirFile.listFiles();
		// 下面有文件
		Assert.assertNotNull(files);
		// 且只有一个
		Assert.assertEquals(1, files.length);
		// 文件名匹配
		Assert.assertEquals("test.properties", files[0].getName());
	}
```

# 2. 相对于执行编译命令路径的方式读取

```java
	/**
	 * 从相对路径读取文件，相对于编译路径，在Eclipse中即为工程所在根目录。 本质还是绝对路径读取。
	 * 
	 * @author lihzh
	 * @data 2012-4-11 下午9:51:10
	 */
	@Test
	public void testGetFileFromRelativePath() {
		String dirPath = System.getProperty("user.dir") + "\\conf";
		File dirFile = new File(dirPath);
		AssertDirFile(dirFile);
	}
```

# 3. 用URI构造本地文件读取

```java
   /**
	 * 构造URI/URL格式的文件路径，读取本地文件
	 * 
	 * @author lihzh
	 * @throws URISyntaxException
	 * @throws MalformedURLException
	 * @data 2012-4-11 下午10:25:00
	 */
	@Test
	public void testGetFileFromURIPath() throws URISyntaxException,
			MalformedURLException {
		// 直接用URI构造, 由于URI和URL可以互转，所以如果为URL直接用URL.toURI转换成URI即可
		URI uri = new URI("file:/D:/workspace-home/JavaDemo/conf/");
		File dirFile = new File(uri);
		AssertDirFile(dirFile);
	}
```

**特别说明：**用URI/URL的方式构造路径是个人比较推荐的，可以解决一些路径读取的问题。例如：Spring会对URI/URL格式的路径进行专有处理可以准确定位的位置，而直接使用绝对路径，在用Classpath和FileSystem两种不同的初始化方式下，可能会出现错误。

# 4. 利用ClassLoader读取Jar包内部文件

```java
   /**
	 * 从依赖的Jar包中读取文件, Jar包内的文件是无法用File读取的，只能用Stream的方式读取。
	 * 
	 * @author lihzh
	 * @throws URISyntaxException
	 * @throws IOException
	 * @data 2012-4-11 下午11:07:58
	 */
	@Test
	public void testGetFileFromJarInClassPath() throws URISyntaxException,
			IOException {
		Enumeration<URL> urls = this.getClass().getClassLoader().getResources("conf/test.properties");
		URL url = this.getClass().getClassLoader().getResource("conf/test.properties");
		Assert.assertTrue(urls.hasMoreElements());
		Assert.assertNotNull(url);
		// 注意两种不同调用方式的路径的区别，此处如果不以'/' 开头，会被当作相对于当前类所在的包类处理,自然无法找到。
		// 因为在Class的getResource方法的开头，有一个resolveName方法，处理了传入的路径格式问题。而ClassLoader类里的
		// getResource和getResources均无此处理。使用时候需要用心。
		URL clzURL = this.getClass().getResource("/conf/test.properties");
		URL nullURL = this.getClass().getResource("conf/test.properties");
		Assert.assertNotNull(clzURL);
		Assert.assertNull(nullURL);
		URL thisClzURL = this.getClass().getResource("");
		Assert.assertNotNull(thisClzURL);
		// 开始读取文件内容
		InputStream is = this.getClass().getResourceAsStream("/conf/test.properties");
		Properties props = new Properties();
		props.load(is);
		Assert.assertTrue(props.containsKey("test.key"));
		Assert.assertEquals("thisIsValue", props.getProperty("test.key"));
	}
```

# 5. 读取Jar内某路径下的所有文件
```java
	/**
	 * 从ClassPath中的Jar包读取某文件夹下的所有文件
	 * 
	 * @author lihzh
	 * @throws IOException 
	 * @data 2012-4-13 下午10:22:24
	 */
	@Test
	public void testGetFilesFromJarInClassPathWithDirPath() throws IOException {
		String dirPath = "conf/";
		URL url = this.getClass().getClassLoader().getResource(dirPath);
		Assert.assertNotNull(url);
		String urlStr = url.toString();
		// 找到!/ 截断之前的字符串
		String jarPath = urlStr.substring(0, urlStr.indexOf("!/") + 2);
		URL jarURL = new URL(jarPath);
		JarURLConnection jarCon = (JarURLConnection) jarURL.openConnection();
		JarFile jarFile = jarCon.getJarFile();
		Enumeration<JarEntry> jarEntrys = jarFile.entries();
		Assert.assertTrue(jarEntrys.hasMoreElements());
		Properties props = new Properties();
		while (jarEntrys.hasMoreElements()) {
			JarEntry entry = jarEntrys.nextElement();
			// 简单的判断路径，如果想做到像Spring，Ant-Style格式的路径匹配需要用到正则。
			String name = entry.getName();
			if (name.startsWith(dirPath) && !entry.isDirectory()) {
				// 开始读取文件内容
				InputStream is = this.getClass().getClassLoader().getResourceAsStream(name);
				Assert.assertNotNull(is);
				props.load(is);
			}
		}
		Assert.assertTrue(props.containsKey("test.key"));
		Assert.assertEquals("thisIsValue", props.getProperty("test.key"));
		Assert.assertTrue(props.containsKey("test.key.two"));
		Assert.assertEquals("thisIsAnotherValue", props.getProperty("test.key.two"));
	}
```

对于不在ClassPath下的Jar包的读取，当作一个本地文件用JarFile读取即可。路径可使用绝对路径。或者用上面的url.getConnection也可以处理。这里不再实现。 希望对你有所帮助。
