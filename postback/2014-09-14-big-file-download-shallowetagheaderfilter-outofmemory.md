---
layout: post
title: 关于ShallowEtagHeaderFilter 大文件下载Out of memory问题解决
date: 2014-09-14 13:50
author: onecoder
comments: true
tags: [Java]
thread_key: 1805
---
<p>
	最近解决大文件下载的问题，遇到一个&quot;Out of memory&quot;的exception。建厂controller层的代码，发现是用BufferdOutputStream写入Response中的，缓冲区也只有8m，按理说不应该出现内存溢出的。</p>
<p>
	仔细观察异常堆栈，发现堆栈中出现了&ldquo;ShallowEtagHeaderFilter &rdquo;这个拦截器。该拦截器是用来处理ETag信息的。关于Etag和该拦截器的介绍可参考：<br />
	摘自百度百科：<br />
	<a href="http://baike.baidu.com/view/3039264.htm">http://baike.baidu.com/view/3039264.htm</a><br />
	ShallowEtagHeaderFilter介绍：<br />
	<a href="http://blog.csdn.net/geloin/article/details/7445251">http://blog.csdn.net/geloin/article/details/7445251</a></p>
<p>
	阅读代码发现问题就出在这个过滤器中，这个过滤器中会将Buffered流转换成ByteArray流写入Response。而ByteArrayOutputStream都存储内存中，还需要频繁的扩容。这在大文件下载的时候自然会内存溢出。</p>
<p>
	解决方案</p>
<p>
	考虑到大部分url还是需要该拦截器进行过滤的，只是需要排除掉跟文件下载相关的url。所以这里OneCoder决定复写该Filter，设置一个黑名单，复写其中的doFilterInternal方法，对于黑名单中的url都直接传递给下一个filter，否则super一下，继续走原来的逻辑。</p>

```java
/**
 * The filter is used for resolving the big file download problem when using
 * {@link ShallowEtagHeaderFilter}. The urls on the black list will be passed
 * directly to the next filter in the chain, the others will be filtered as
 * before.
 * <p>
 * Sample:<br>
 * {@code <filter>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp {@code<filter-name>BigFileEtagFilter</filter-name>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp
 * {@code<filter-class>com.coderli.filter.BigFileDownloadEtagHeaderFilter</filter-class>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp {@code<!-- url sperators includes: blank space ; , and /r/n.
 * Black list is optional.>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp {@code<init-param>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp&amp;nbsp&amp;nbsp&amp;nbsp {@code<param-name>blackListURL</param-name>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp&amp;nbsp&amp;nbsp&amp;nbsp
 * {@code <param-value> /aa /bb/** /cc/* </param-value>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp {@code</init-param>}<br>
 * {@code</filter>}<br>
 * {@code<filter-mapping>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp {@code<filter-name>BigFileEtagFilter</filter-name>}<br>
 * &amp;nbsp&amp;nbsp&amp;nbsp {@code<url-pattern>/*</url-pattern>}<br>
 * {@code</filter-mapping>}
 * 
 * @author li_hongzhe@nhn.com
 * @date 2014-9-12 9:46:38
 */
public class BigFileDownloadEtagHeaderFilter extends ShallowEtagHeaderFilter {

	private final String[] NULL_STRING_ARRAY = new String[0];
	private final String URL_SPLIT_PATTERN = &quot;[, ;\r\n]&quot;;

	private final PathMatcher pathMatcher = new AntPathMatcher();

	private final Logger logger = LoggerFactory
			.getLogger(BigFileDownloadEtagHeaderFilter.class);
	// url while list
	// private String[] whiteListURLs = null;
	// url black list
	private String[] blackListURLs = null;

	@Override
	public final void initFilterBean() {
		initConfig();
	}

	@Override
	protected void doFilterInternal(HttpServletRequest request,
			HttpServletResponse response, FilterChain filterChain)
			throws ServletException, IOException {
		String reqUrl = request.getPathInfo();
		if (isBlackURL(reqUrl)) {
			logger.debug(&quot;Current url  {} is on the black list.&quot;, reqUrl);
			filterChain.doFilter(request, response);
		} else {
			super.doFilterInternal(request, response, filterChain);
		}
	}

	private void initConfig() {
		// No need white list now.
		// String whiteListURLStr = getFilterConfig().getInitParameter(
		// &quot;whiteListURL&quot;);
		// whiteListURLs = strToArray(whiteListURLStr);
		String blackListURLStr = getFilterConfig().getInitParameter(
				&quot;blackListURL&quot;);
		blackListURLs = strToArray(blackListURLStr);
	}

	// No need white list now.
	// private boolean isWhiteURL(String currentURL) {
	// for (String whiteURL : whiteListURLs) {
	// if (pathMatcher.match(whiteURL, currentURL)) {
	// logger.debug(
	// &quot;url filter : white url list matches : [{}] match [{}] continue&quot;,
	// whiteURL, currentURL);
	// return true;
	// }
	// logger.debug(
	// &quot;url filter : white url list not matches : [{}] match [{}]&quot;,
	// whiteURL, currentURL);
	// }
	// return false;
	// }

	private boolean isBlackURL(String currentURL) {
		for (String blackURL : blackListURLs) {
			if (pathMatcher.match(blackURL, currentURL)) {
				logger.debug(
						&quot;url filter : black url list matches : [{}] match [{}] break&quot;,
						blackURL, currentURL);
				return true;
			}
			logger.debug(
					&quot;url filter : black url list not matches : [{}] match [{}]&quot;,
					blackURL, currentURL);
		}
		return false;
	}

	private String[] strToArray(String urlStr) {
		if (urlStr == null) {
			return NULL_STRING_ARRAY;
		}
		String[] urlArray = urlStr.split(URL_SPLIT_PATTERN);
		List<String> urlList = new ArrayList<String>();

		for (String url : urlArray) {
			url = url.trim();
			if (url.length() == 0) {
				continue;
			}
			urlList.add(url);
		}
		return urlList.toArray(NULL_STRING_ARRAY);
	}
}
```

<p>
	OneCoder也是参考网上有人提供的现成的样例，做了简单修改而已：<a href="http://jinnianshilongnian.iteye.com/blog/1663481">http://jinnianshilongnian.iteye.com/blog/1663481</a></p>
<p>
	关于ShallowEtagHeaderFilter这个&ldquo;Bug&rdquo;，<a href="http://www.coderli.com">OneCoder</a>发现网上也有人向spring反应了，不过好像Spring方面认为这是使用问题，不作为bug来进行处理，那我们就自己解决一下。</p>

