---
layout: post
title: Mybatis-PageHelper Reentrantlock锁使用问题
tags: [Mybatis]
categories: [Java技术研究]
date: 2016-04-12 22:48:42 +0800
comments: true
thread_key: 1888
---
<a href="https://github.com/pagehelper/Mybatis-PageHelper" target="_blank">Mybatis-PageHelper</a>应该是目前使用比较广泛的一个Mybatis分页插件。我在几个项目里都引入了该插件。今天偶然阅读其源码，却发现了一个不小的问题。

>注：我阅读的是最新的4.1.3的源码。

该分页插件的核心是***PageHelper***类，该类实现了***Mybatis***提供的***Interceptor***接口。接口定义的***intercept***方法实现如下：

```java
/**
 * Mybatis拦截器方法
 *
 * @param invocation 拦截器入参
 * @return 返回执行结果
 * @throws Throwable 抛出异常
 */
public Object intercept(Invocation invocation) throws Throwable {
    if (autoRuntimeDialect) {
        SqlUtil sqlUtil = getSqlUtil(invocation);
        return sqlUtil.processPage(invocation);
    } else {
        if (autoDialect) {
            initSqlUtil(invocation);
        }
        return sqlUtil.processPage(invocation);
    }
}
```

其中，***getSqlUtil***方法，实现如下：

```java
/**
 * 根据daatsource创建对应的sqlUtil
 *
 * @param invocation
 */
public SqlUtil getSqlUtil(Invocation invocation) {
    MappedStatement ms = (MappedStatement) invocation.getArgs()[0];
    //改为对dataSource做缓存
    DataSource dataSource = ms.getConfiguration().getEnvironment().getDataSource();
    String url = getUrl(dataSource);
    if (urlSqlUtilMap.containsKey(url)) {
        return urlSqlUtilMap.get(url);
    }
    ReentrantLock lock = new ReentrantLock(); //这里我认为是有问题的。
    try {
        lock.lock();
        if (urlSqlUtilMap.containsKey(url)) {
            return urlSqlUtilMap.get(url);
        }
        if (StringUtil.isEmpty(url)) {
            throw new RuntimeException("无法自动获取jdbcUrl，请在分页插件中配置dialect参数!");
        }
        String dialect = Dialect.fromJdbcUrl(url);
        if (dialect == null) {
            throw new RuntimeException("无法自动获取数据库类型，请通过dialect参数指定!");
        }
        SqlUtil sqlUtil = new SqlUtil(dialect);
        if (this.properties != null) {
            sqlUtil.setProperties(properties);
        } else if (this.sqlUtilConfig != null) {
            sqlUtil.setSqlUtilConfig(this.sqlUtilConfig);
        }
        urlSqlUtilMap.put(url, sqlUtil);
        return sqlUtil;
    } finally {
        lock.unlock();
    }
}
```

这里有个加锁的操作，使用的是***Reentrantlock***局部变量。这里是有问题的，局部变量的***lock***是无法起到锁的作用的。这段代码实际上仍不是线程安全的。将该***lock***变量提升为类的全局变量即可解决。

```java
private ReentrantLock lock = new ReentrantLock();

/**
 * 根据datasource创建对应的sqlUtil
 *
 * @param invocation
 */
public SqlUtil getSqlUtil(Invocation invocation) {
    MappedStatement ms = (MappedStatement) invocation.getArgs()[0];
    //改为对dataSource做缓存
    DataSource dataSource = ms.getConfiguration().getEnvironment().getDataSource();
    String url = getUrl(dataSource);
    if (urlSqlUtilMap.containsKey(url)) {
        return urlSqlUtilMap.get(url);
    }
    try {
        lock.lock();
       ...
```

顺便也修改了一个datasource拼写错误的问题。

给作者提交了Pull Request。

![](/images/post/mybatis-pagehelper-bug/pull-request.png)