---
layout: post
title: Spring源码学习-含有通配符路径解析（上）
date: 2012-06-10 21:07 +0800
author: onecoder
comments: true
tags: [Spring]
categories: [Java技术研究,Spring]
thread_key: 359
---
继续前文<a href="http://www.coderli.com/spring-filesystem-filepath-parse/" target="_blank">《[原创] Spring源码学习-FileSystemXmlApplicationContext路径格式及解析方式》</a>的问题。

先测试分析包含通配符(?)的。

```java
	/**
	 * 测试包含通配符:*,?的路径
	 * <p>;D:\\workspace-home\\spring-custom\\src\\main\\resources\\spring\\ap?-context.xml</p>;
	 * 通过读取配置文件失败的情况，因为此时Spring不支持\\路径的通配符解析
	 * 
	 * @author lihzh
	 * @date 2012-5-5 上午10:53:53
	 */
	@Test
	public void testAntStylePathFail() {
		String pathOne = "D:\\workspace-home\\spring-custom\\src\\main\\resources\\spring\\ap?-context.xml";
		ApplicationContext appContext = new FileSystemXmlApplicationContext(pathOne);
		assertNotNull(appContext);
		VeryCommonBean bean = null;
		try {
			bean = appContext.getBean(VeryCommonBean.class);
			fail("Should not find the [VeryCommonBean].");
		} catch (NoSuchBeanDefinitionException e) {
		}
		assertNull(bean);
	}
```

该测试用例是可以正常通过测试，也就是是找不到该Bean的。这又是为什么? Spring不是支持通配符吗？FileSystemXmlApplicationContext的注释里也提到了通配符的情况：

```java
* <p>;The config location defaults can be overridden via {@link #getConfigLocations},
 * Config locations can either denote concrete files like "/myfiles/context.xml"
 * or Ant-style patterns like "/myfiles/*-context.xml" (see the
 * {@link org.springframework.util.AntPathMatcher} javadoc for pattern details).
```

从代码中寻找答案。回到上回的else分支中，因为包含通配符，所以进入第一个子分支。

```java
	/**
	 * Find all resources that match the given location pattern via the
	 * Ant-style PathMatcher. Supports resources in jar files and zip files
	 * and in the file system.
	 * @param locationPattern the location pattern to match
	 * @return the result as Resource array
	 * @throws IOException in case of I/O errors
	 * @see #doFindPathMatchingJarResources
	 * @see #doFindPathMatchingFileResources
	 * @see org.springframework.util.PathMatcher
	 */
	protected Resource[] findPathMatchingResources(String locationPattern) throws IOException {
		String rootDirPath = determineRootDir(locationPattern);
		String subPattern = locationPattern.substring(rootDirPath.length());
		Resource[] rootDirResources = getResources(rootDirPath);
		Set<Resource>; result = new LinkedHashSet<Resource>;(16);
		for (Resource rootDirResource : rootDirResources) {
			rootDirResource = resolveRootDirResource(rootDirResource);
			if (isJarResource(rootDirResource)) {
				result.addAll(doFindPathMatchingJarResources(rootDirResource, subPattern));
			}
			else if (rootDirResource.getURL().getProtocol().startsWith(ResourceUtils.URL_PROTOCOL_VFS)) {
				result.addAll(VfsResourceMatchingDelegate.findMatchingResources(rootDirResource, subPattern, getPathMatcher()));
			}
			else {
				result.addAll(doFindPathMatchingFileResources(rootDirResource, subPattern));
			}
		}
		if (logger.isDebugEnabled()) {
			logger.debug("Resolved location pattern [" + locationPattern + "] to resources " + result);
		}
		return result.toArray(new Resource[result.size()]);
	}
```

此方法传入的完整的没有处理的路径，从第一行开始，就开始分步处理解析传入的路径，首先是决定**根**路径: ***determineRootDir(locationPattern)***

```java
    /**
	 * Determine the root directory for the given location.
	 * <p>;Used for determining the starting point for file matching,
	 * resolving the root directory location to a <code>;java.io.File</code>;
	 * and passing it into <code>;retrieveMatchingFiles</code>;, with the
	 * remainder of the location as pattern.
	 * <p>;Will return "/WEB-INF/" for the pattern "/WEB-INF/*.xml",
	 * for example.
	 * @param location the location to check
	 * @return the part of the location that denotes the root directory
	 * @see #retrieveMatchingFiles
	 */
	protected String determineRootDir(String location) {
		int prefixEnd = location.indexOf(":") + 1;
		int rootDirEnd = location.length();
		while (rootDirEnd >; prefixEnd && getPathMatcher().isPattern(location.substring(prefixEnd, rootDirEnd))) {
			rootDirEnd = location.lastIndexOf('/', rootDirEnd - 2) + 1;
		}
		if (rootDirEnd == 0) {
			rootDirEnd = prefixEnd;
		}
		return location.substring(0, rootDirEnd);
	}
```

这个"根"，就是不包含通配符的最长的部分，以我们的路径为例，这个"根"本来应该是: ***D:\\workspace-home\\spring-custom\\src\\main\\resources\\spring\\***，但是实际上，从***determineRootDir***的实现可以看出，

首先，先找到冒号':'索引位，赋值给 ***prefixEnd***。

然后，在从冒号开始到最后的字符串中，循环判断是否包含通配符，如果包含，则截断最后一个由"/"分割的部分，例如：在我们路径中，就是最后的ap?-context.xml这一段。再循环判断剩下的部分，直到剩下的路径中都不包含通配符。

如果查找完成后，rootDirEnd=0了，则将之前赋值的prefixEnd的值赋给rootDirEnd，也就是":"所在的索引位。
	
最后，将字符串从开始截断rootDirEnd。
		
我们的问题，就出在关键的第二步，Spring这里只在字符串中查找"/"，并没有支持"\\\\"这样的路径分割方式，所以，自然找不到"\\\\"，rootDirEnd = -1 + 1 = 0。所以循环后，阶段出来的路径就是***D:***自然Spring会找不到配置文件，容器无法初始化

基于以上分析，我们将路径修改为：***D:/workspace-home/spring-custom/src/main/resources/spring/ap?-context.xml***，再测试如下：

```java
   /**
	 * 测试包含通配符:*,?的路径
	 * <p>;D:/workspace-home/spring-custom/src/main/resources/spring/ap?-context.xml</p>;
	 * 通过读取配置文件
	 * 
	 * @author lihzh
	 * @date 2012-5-5 上午10:53:53
	 */
	@Test
	public void testAntStylePath() {
		String pathOne = "D:/workspace-home/spring-custom/src/main/resources/spring/ap?-context.xml";
		ApplicationContext appContext = new FileSystemXmlApplicationContext(pathOne);
		assertNotNull(appContext);
		VeryCommonBean bean = appContext.getBean(VeryCommonBean.class);
		assertNotNull(bean);
		assertEquals("verycommonbean-name", bean.getName());
	}
```

测试通过。

刚才仅仅分析了，我们之前路径的问题所在，还有一点我想也是大家关心的，就是通配符是怎么匹配的呢？那我们就继续分析源码，回到 ***findPathMatchingResources***方法。

将路径分成包含通配符和不包含的两部分后，Spring会将根路径生成一个Resource，用的还是getResources方法。然后检查根路径的类型，是否是Jar路径？是否是VFS路径？对于我们这种普通路径，自然走到最后的分支。
	
```java	
	/**
	 * Find all resources in the file system that match the given location pattern
	 * via the Ant-style PathMatcher.
	 * @param rootDirResource the root directory as Resource
	 * @param subPattern the sub pattern to match (below the root directory)
	 * @return the Set of matching Resource instances
	 * @throws IOException in case of I/O errors
	 * @see #retrieveMatchingFiles
	 * @see org.springframework.util.PathMatcher
	 */
	protected Set<Resource>; doFindPathMatchingFileResources(Resource rootDirResource, String subPattern)
			throws IOException {

		File rootDir;
		try {
			rootDir = rootDirResource.getFile().getAbsoluteFile();
		}
		catch (IOException ex) {
			if (logger.isWarnEnabled()) {
				logger.warn("Cannot search for matching files underneath " + rootDirResource +
						" because it does not correspond to a directory in the file system", ex);
			}
			return Collections.emptySet();
		}
		return doFindMatchingFileSystemResources(rootDir, subPattern);
	}
```

```java
   /**
	 * Find all resources in the file system that match the given location pattern
	 * via the Ant-style PathMatcher.
	 * @param rootDir the root directory in the file system
	 * @param subPattern the sub pattern to match (below the root directory)
	 * @return the Set of matching Resource instances
	 * @throws IOException in case of I/O errors
	 * @see #retrieveMatchingFiles
	 * @see org.springframework.util.PathMatcher
	 */
	protected Set<Resource>; doFindMatchingFileSystemResources(File rootDir, String subPattern) throws IOException {
		if (logger.isDebugEnabled()) {
			logger.debug("Looking for matching resources in directory tree [" + rootDir.getPath() + "]");
		}
		Set<File>; matchingFiles = retrieveMatchingFiles(rootDir, subPattern);
		Set<Resource>; result = new LinkedHashSet<Resource>;(matchingFiles.size());
		for (File file : matchingFiles) {
			result.add(new FileSystemResource(file));
		}
		return result;
	}
```

```java
   /**
	 * Retrieve files that match the given path pattern,
	 * checking the given directory and its subdirectories.
	 * @param rootDir the directory to start from
	 * @param pattern the pattern to match against,
	 * relative to the root directory
	 * @return the Set of matching File instances
	 * @throws IOException if directory contents could not be retrieved
	 */
	protected Set<File>; retrieveMatchingFiles(File rootDir, String pattern) throws IOException {
		if (!rootDir.exists()) {
			// Silently skip non-existing directories.
			if (logger.isDebugEnabled()) {
				logger.debug("Skipping [" + rootDir.getAbsolutePath() + "] because it does not exist");
			}
			return Collections.emptySet();
		}
		if (!rootDir.isDirectory()) {
			// Complain louder if it exists but is no directory.
			if (logger.isWarnEnabled()) {
				logger.warn("Skipping [" + rootDir.getAbsolutePath() + "] because it does not denote a directory");
			}
			return Collections.emptySet();
		}
		if (!rootDir.canRead()) {
			if (logger.isWarnEnabled()) {
				logger.warn("Cannot search for matching files underneath directory [" + rootDir.getAbsolutePath() +
						"] because the application is not allowed to read the directory");
			}
			return Collections.emptySet();
		}
		String fullPattern = StringUtils.replace(rootDir.getAbsolutePath(), File.separator, "/");
		if (!pattern.startsWith("/")) {
			fullPattern += "/";
		}
		fullPattern = fullPattern + StringUtils.replace(pattern, File.separator, "/");
		Set<File>; result = new LinkedHashSet<File>;(8);
		doRetrieveMatchingFiles(fullPattern, rootDir, result);
		return result;
	}
```

```java
   /**
	 * Recursively retrieve files that match the given pattern,
	 * adding them to the given result list.
	 * @param fullPattern the pattern to match against,
	 * with prepended root directory path
	 * @param dir the current directory
	 * @param result the Set of matching File instances to add to
	 * @throws IOException if directory contents could not be retrieved
	 */
	protected void doRetrieveMatchingFiles(String fullPattern, File dir, Set<File>; result) throws IOException {
		if (logger.isDebugEnabled()) {
			logger.debug("Searching directory [" + dir.getAbsolutePath() +
					"] for files matching pattern [" + fullPattern + "]");
		}
		File[] dirContents = dir.listFiles();
		if (dirContents == null) {
			if (logger.isWarnEnabled()) {
				logger.warn("Could not retrieve contents of directory [" + dir.getAbsolutePath() + "]");
			}
			return;
		}
		for (File content : dirContents) {
			String currPath = StringUtils.replace(content.getAbsolutePath(), File.separator, "/");
			if (content.isDirectory() && getPathMatcher().matchStart(fullPattern, currPath + "/")) {
				if (!content.canRead()) {
					if (logger.isDebugEnabled()) {
						logger.debug("Skipping subdirectory [" + dir.getAbsolutePath() +
								"] because the application is not allowed to read the directory");
					}
				}
				else {
					doRetrieveMatchingFiles(fullPattern, content, result);
				}
			}
			if (getPathMatcher().match(fullPattern, currPath)) {
				result.add(content);
			}
		}
	}
```

主要的匹配工作，是从***doRetrieveMatchingFiles***方法开始的。前面的都是简单的封装过渡，在***retrieveMatchingFiles***中判断了下根路径是否存在、是否是文件夹、是否可读。否则都直接返回空集合。都满足了以后才进入，***doRetrieveMatchingFiles***方法。在该方法中

- 首先，列出该文件夹下的所有文件。
- 然后，遍历所有文件，如果仍是文件夹，递归调用***doRetrieveMatchingFiles***方法。如果不是，则调用***getPathMatcher().match(fullPattern, currPath)***进行文件名的最后匹配，将满足条件放入结果集。该match方法，实际是调用了***AntPathMatcher***的***doMatch***方法，
	
```java
   /**
	 * Actually match the given <code>;path</code>; against the given <code>;pattern</code>;.
	 * @param pattern the pattern to match against
	 * @param path the path String to test
	 * @param fullMatch whether a full pattern match is required (else a pattern match
	 * as far as the given base path goes is sufficient)
	 * @return <code>;true</code>; if the supplied <code>;path</code>; matched, <code>;false</code>; if it didn't
	 */
	protected boolean doMatch(String pattern, String path, boolean fullMatch,
			Map<String, String>; uriTemplateVariables) {

		if (path.startsWith(this.pathSeparator) != pattern.startsWith(this.pathSeparator)) {
			return false;
		}

		String[] pattDirs = StringUtils.tokenizeToStringArray(pattern, this.pathSeparator);
		String[] pathDirs = StringUtils.tokenizeToStringArray(path, this.pathSeparator);

		int pattIdxStart = 0;
		int pattIdxEnd = pattDirs.length - 1;
		int pathIdxStart = 0;
		int pathIdxEnd = pathDirs.length - 1;

		// Match all elements up to the first **
		while (pattIdxStart <= pattIdxEnd && pathIdxStart <= pathIdxEnd) {
			String patDir = pattDirs[pattIdxStart];
			if ("**".equals(patDir)) {
				break;
			}
			if (!matchStrings(patDir, pathDirs[pathIdxStart], uriTemplateVariables)) {
				return false;
			}
			pattIdxStart++;
			pathIdxStart++;
		}

		if (pathIdxStart >; pathIdxEnd) {
			// Path is exhausted, only match if rest of pattern is * or **'s
			if (pattIdxStart >; pattIdxEnd) {
				return (pattern.endsWith(this.pathSeparator) ? path.endsWith(this.pathSeparator) :
						!path.endsWith(this.pathSeparator));
			}
			if (!fullMatch) {
				return true;
			}
			if (pattIdxStart == pattIdxEnd && pattDirs[pattIdxStart].equals("*") && path.endsWith(this.pathSeparator)) {
				return true;
			}
			for (int i = pattIdxStart; i <= pattIdxEnd; i++) {
				if (!pattDirs[i].equals("**")) {
					return false;
				}
			}
			return true;
		}
		else if (pattIdxStart >; pattIdxEnd) {
			// String not exhausted, but pattern is. Failure.
			return false;
		}
		else if (!fullMatch && "**".equals(pattDirs[pattIdxStart])) {
			// Path start definitely matches due to "**" part in pattern.
			return true;
		}

		// up to last '**'
		while (pattIdxStart <= pattIdxEnd && pathIdxStart <= pathIdxEnd) {
			String patDir = pattDirs[pattIdxEnd];
			if (patDir.equals("**")) {
				break;
			}
			if (!matchStrings(patDir, pathDirs[pathIdxEnd], uriTemplateVariables)) {
				return false;
			}
			pattIdxEnd--;
			pathIdxEnd--;
		}
		if (pathIdxStart >; pathIdxEnd) {
			// String is exhausted
			for (int i = pattIdxStart; i <= pattIdxEnd; i++) {
				if (!pattDirs[i].equals("**")) {
					return false;
				}
			}
			return true;
		}

		while (pattIdxStart != pattIdxEnd && pathIdxStart <= pathIdxEnd) {
			int patIdxTmp = -1;
			for (int i = pattIdxStart + 1; i <= pattIdxEnd; i++) {
				if (pattDirs[i].equals("**")) {
					patIdxTmp = i;
					break;
				}
			}
			if (patIdxTmp == pattIdxStart + 1) {
				// '**/**' situation, so skip one
				pattIdxStart++;
				continue;
			}
			// Find the pattern between padIdxStart & padIdxTmp in str between
			// strIdxStart & strIdxEnd
			int patLength = (patIdxTmp - pattIdxStart - 1);
			int strLength = (pathIdxEnd - pathIdxStart + 1);
			int foundIdx = -1;

			strLoop:
			for (int i = 0; i <= strLength - patLength; i++) {
				for (int j = 0; j < patLength; j++) {
					String subPat = pattDirs[pattIdxStart + j + 1];
					String subStr = pathDirs[pathIdxStart + i + j];
					if (!matchStrings(subPat, subStr, uriTemplateVariables)) {
						continue strLoop;
					}
				}
				foundIdx = pathIdxStart + i;
				break;
			}

			if (foundIdx == -1) {
				return false;
			}

			pattIdxStart = patIdxTmp;
			pathIdxStart = foundIdx + patLength;
		}

		for (int i = pattIdxStart; i <= pattIdxEnd; i++) {
			if (!pattDirs[i].equals("**")) {
				return false;
			}
		}

		return true;
	}
```
	
比较方法如下

- 首先，分别将输入路径和待比较路径，按照文件分隔符分割成字符串数组。（例如：｛"D:", "workspace-home", "spring-custom"...｝)
- 然后，设置好起始和结束位后，对这两个数组进行while循环（代码中第一个while循环），逐断比较匹配(***matchStrings***)情况。如果有一段不满足则返回fasle。
	
由于我们当前的测试路径中不包含**的部分，所以主要的判断基本都在第一个while就可以搞定。这部分工作自然是由***matchStrings***完成的。

如果让你完成一个通配符路径匹配的功能，你会如何去做？是否自然的联想到了正则？似乎是个好选择，看看spring是怎么做的。

```java		
private boolean matchStrings(String pattern, String str, Map<String, String>; uriTemplateVariables) {
		AntPathStringMatcher matcher = new AntPathStringMatcher(pattern, str, uriTemplateVariables);
		return matcher.matchStrings();
	}
```
		
在构造***AntPathStringMatcher***实例的时候，spring果然也创建了正则：
		
```java
		AntPathStringMatcher(String pattern, String str, Map<String, String>; uriTemplateVariables) {
		this.str = str;
		this.uriTemplateVariables = uriTemplateVariables;
		this.pattern = createPattern(pattern);
	}

private Pattern createPattern(String pattern) {
		StringBuilder patternBuilder = new StringBuilder();
		Matcher m = GLOB_PATTERN.matcher(pattern);
		int end = 0;
		while (m.find()) {
			patternBuilder.append(quote(pattern, end, m.start()));
			String match = m.group();
			if ("?".equals(match)) {
				patternBuilder.append('.');
			}
			else if ("*".equals(match)) {
				patternBuilder.append(".*");
			}
			else if (match.startsWith("{") && match.endsWith("}")) {
				int colonIdx = match.indexOf(':');
				if (colonIdx == -1) {
					patternBuilder.append(DEFAULT_VARIABLE_PATTERN);
					variableNames.add(m.group(1));
				}
				else {
					String variablePattern = match.substring(colonIdx + 1, match.length() - 1);
					patternBuilder.append('(');
					patternBuilder.append(variablePattern);
					patternBuilder.append(')');
					String variableName = match.substring(1, colonIdx);
					variableNames.add(variableName);
				}
			}
			end = m.end();
		}
		patternBuilder.append(quote(pattern, end, pattern.length()));
		return Pattern.compile(patternBuilder.toString());
	}
```

简单说，就是spring先用正则：

```java
private static final Pattern GLOB_PATTERN = Pattern.compile("\\?|\\*|\\{((?:\\{[^/]+?\\}|[^/{}]|\\\\[{}])+?)\\}");
```

找到路径中的"?"和"\*"通配符，然后转换为Java正则的任意字符"."和".\*"。生成另一个正则表达式去匹配查找到的文件的路径。如果匹配则返回true。
	
至此，对于路径中包含?和\*的情况解析spring的解析方式，我们已经基本了解了。本来想把\*\*的情况一起介绍了，不过考虑的篇幅过长，我们下次再一起研究吧。
	
写在最后：所有研究均为笔者工作之余消遣之做，错误指出还望指出，欢迎各种形势的探讨。