---
layout: post
title: IP范围过滤实现
date: 2014-10-24 10:44
author: onecoder
comments: true
tags: [Java]
categories: [Java技术研究]
thread_key: 1841
---
项目里要求实现在项目上线前社内测试团地可以正常访问系统，而外部访问用户看到的是系统尚未开放的页面。

OneCoder的第一反映就是实现一个filter，配置可访问的IP规则，通过正则进行匹配。通过的正常进入系统，不通过的redirect到指定欢迎页面。

整个代码没什么难度，核心就是一个IP规则的检验功能。考虑到配置的简便性，即一般熟悉192.168.1.*和192.168.2.1-23，这种全部匹配和范围匹配的配置方式。OneCoder决定采用拆分解析匹配的方式。规则之间用分号;分隔，是或的关系。代码实现如下：

```java
package com.coderli.web.filter.ip;

/**
 * IP规则正则处理工具类
 *
 * @author OneCoder
 * @date 2014年10月23日 下午1:23:09
 */
public class IPRegexUtil {

     /**
      * 校验所给IP是否满足给定规则
      *
      * @author li_hongzhe @nhn.com
      * @date 2014年10月23日 下午1:38:37
      * @param ipStr
      *            待校验IP
      * @param ipPattern
      *            IP匹配规则。支持 * 匹配所有和 - 匹配范围。用分号分隔 <br>
      *            例如：10.34.163.*;10.34.162.1 -128
      * @return
      */
     public static boolean validateIP(String ipStr, String ipPattern) {
           if ( ipStr == null || ipPattern == null) {
               return false;
          }
          String[] patternList = ipPattern.split( ";");
           for (String pattern : patternList) {
               if ( passValidate(ipStr, pattern)) {
                    return true;
              }
          }
           return false;
     }

     private static boolean passValidate(String ipStr, String pattern) {
          String[] ipStrArr = ipStr.split( "\\.");
          String[] patternArr = pattern.split( "\\.");
           if ( ipStrArr. length != 4 || patternArr. length != 4) {
               return false;
          }
           int end = ipStrArr. length;
           if ( patternArr[3].contains( "-")) {
               end = 3;
              String[] rangeArr = patternArr[3].split( "-");
               int from = Integer.valueOf(rangeArr[0]).intValue();
               int to = Integer.valueOf(rangeArr[1]).intValue();
               int value = Integer.valueOf(ipStrArr[3]).intValue();
               if ( value < from || value > to) {
                    return false;
              }
          }
           for ( int i = 0; i < end; i++) {
               if ( patternArr[ i].equals( "*")) {
                    continue;
              }
               if (!patternArr[ i].equalsIgnoreCase( ipStrArr[ i])) {
                    return false;
              }
          }
           return true;
     }

}
```

实现过滤器如下：

```java
package com.coderli.web.filter.ip;

import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
* IP地址过滤器，如果IP地址在过滤的范围内，则允许访问。<br>
* 如果没在范围内，则跳转到禁止页面。
*
* @author OneCoder
* @date 2014年10月24日 上午9:54:33
*/
public class IPFilter implements Filter {

     private String ipPattern;

     @Override
     public void destroy() {
          // TODO Auto-generated method stub

     }

     @Override
     public void doFilter(ServletRequest request, ServletResponse response,
               FilterChain filterChain) throws IOException, ServletException {
          String ip = request.getRemoteHost();
          String reqUrl = ((HttpServletRequest) request).getRequestURI();
          if (reqUrl.contains("forbidden")) {
               filterChain.doFilter(request, response);
               return;
          }
          if (IPRegexUtil.validateIP(ip, ipPattern)) {
               filterChain.doFilter(request, response);
          } else {
               ((HttpServletResponse) response).sendRedirect("/shurnim/forbidden");
          }
     }

     @Override
     public void init(FilterConfig filterConfig) throws ServletException {
          this.ipPattern = filterConfig.getInitParameter("ip-pattern");
     }

     public String getIpPattern() {
          return ipPattern;
     }

     public void setIpPattern(String ipPattern) {
          this.ipPattern = ipPattern;
     }

}
```

web.xml配置如下：

```xml
     <filter>
           <filter-name >IPFilter </filter-name >
           <filter-class >com.coderli.web.filter.ip.IPFilter </filter-class >
           <init-param >
               <param-name >ip-pattern</ param-name>
                <param-value >10.34.163.169;10.34.163.1-254 </param-value >
           </init-param >
     </filter >
     <filter-mapping >
           <filter-name >IPFilter </filter-name >
           <url-pattern >/* </url-pattern >
     </filter-mapping >
```

代码似乎没什么好解释的，目前看似乎是满足了需求了。
