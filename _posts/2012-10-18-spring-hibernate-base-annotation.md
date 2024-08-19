---
layout: post
title: SpringMVC3.1+Hibernate4.1.7完全基于注解配置(零配置文件)
date: 2012-10-18 13:58 +0800
author: onecoder
comments: true
tags: [Spring,Hibernate]
categories: [Java技术研究]
thread_key: 1187
---
其实这篇文章应该是上篇<a href="http://www.coderli.com/springmvc-servlet3-code-bases-configuration">《Servlet3.0下基于注解的SpringMVC3.1配置-完全零配置文件》</a>的续篇，因为上篇只介绍到web工程和Spring(包括MVC)的零配置，相对于传统的SSH来说，相当于SS零配置了。那么S和H的结合如果零配置文件呢。

Hibernate的注解配置大家应该不会陌生。主要就是对实体类的配置，注明对应的表和字段即可。

```java
/**
 * 用户模型
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
@Entity
@Table(name="snm_user")
public class User implements Serializable {

private static final long serialVersionUID = -6925982814013703984L;

@Id
private int id;
@Column(length = 20, nullable = false)
private String name;
@Column(length = 32, nullable = false)
private String password;
@Column(length = 64, nullable = false)
private String email;
@Column(name = "ctime", length = 20, nullable = false)
private long createTime;
....
```

主要还是原有数据源和SessionFactory的注解配置方式的改变。这里利用Spring提供的注解方式，单独抽出一个数据源配置类

```java
/**
 * 数据源配置类
 * 
 * @author lihzh
 * @alia OneCoder
 * @blog http://www.coderli.com
 */
@Configuration
@PropertySource("/conf/jdbc.properties")
public class DataSourceConfig {

@Value("${jdbc.driverClass}") String driverClass;
@Value("${jdbc.url}") String url;
@Value("${jdbc.user}") String user;
@Value("${jdbc.password}") String password;

@Bean
public DataSource dataSource() throws PropertyVetoException {
ComboPooledDataSource dataSource = new ComboPooledDataSource();
dataSource.setDriverClass(driverClass);
dataSource.setJdbcUrl(url);
dataSource.setUser(user);
dataSource.setPassword(password);
return dataSource;
}

@Bean
public LocalSessionFactoryBean sessionFactory() throws PropertyVetoException {
LocalSessionFactoryBean sessionFactoryBean = new LocalSessionFactoryBean();
sessionFactoryBean.setDataSource(dataSource());
Properties hibernateProperties = new Properties();
hibernateProperties.setProperty("hibernate.dialect", "org.hibernate.dialect.MySQLDialect");
sessionFactoryBean.setHibernateProperties(hibernateProperties);
sessionFactoryBean.setPackagesToScan("com.coderli.shurnim.*.model");
return sessionFactoryBean;
}

@Bean
public HibernateTransactionManager txManager() throws PropertyVetoException {
HibernateTransactionManager txManager = new HibernateTransactionManager();
txManager.setSessionFactory(sessionFactory().getObject());
return txManager;
}

}
```

配置了数据源，SessionFactory和事物管理类。在SessionFactory中声明了扫描实体注解的包路径。这里把数据源的配置单独提到了jdbc.properties这个配置文件中，主要是考虑在实际实施过程中，数据库链接是一个需要经常修改的项，所以提出在项目配置之外，以方便实施人员独立配置。

然后在原有的DefaultAppConfig中引用该配置。用@Import注解：

```java
@Configuration
@ComponentScan(basePackages = "com.coderli.shurnim.*.biz")
@Import(DataSourceConfig.class)
@EnableTransactionManagement
public class DefaultAppConfig {
```

同时启用了事物注解。至此，Spring3.1+Hibernate4.1.7的配置基本完成了。启动项目。稍微修改一下原UserAction，使其读取数据库

```java
@RequestMapping("/user.do")
@Transactional
public void test(HttpServletResponse response) throws IOException {
_log.info("Hi, u guy");
List&lt;User&gt; users = userDAO.getAll();
response.getWriter().write("name: " + users.get(0).getName() + "; email: " + users.get(0).getEmail());
}
```

<p style="text-align: center; ">
		<img alt="" src="/images/oldposts/115Gdw.jpg" /></p>

启动服务，一切OK。

需要说明的是，<a href="http://www.coderli.com">OneCoder</a>的学习习惯是不停的折腾，所以这里虽然是配置好了，正常使用。但是在配置过程中，还是遇到一些没有解决的问题。比如，根据@Configuration的注解说明，<a href="http://www.coderli.com">OneCoder</a>曾响在DataSourceConfig中仅仅保留数据源配置，将SessionFactory和事物的配置都放到AppConfig中，然后通过@Autowire或者@Inject的注解引用进来，用了两种方式都还没有成功。待<a href="http://www.coderli.com">OneCoder</a>研究清楚后，再一一说明。这里给出配置，仅仅给大家提供一个样例参考。更多的细节，还需要大家自己研究：）。<a href="http://www.coderli.com">OneCoder</a>感觉，这种配置方式，还有挺有意思的。