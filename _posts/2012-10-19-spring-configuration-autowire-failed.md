---
layout: post
title: Spring3.1完全基于注解配置@Configuration类中@Autowire无法注入问题解决
date: 2012-10-19 16:15 +0800
author: onecoder
comments: true
tags: [Spring]
categories: [Java技术研究,Spring]
thread_key: 1193
---
在上回介绍Spring3.1+Hibernate4.1.7基于注解配置的时候(<a href="http://www.coderli.com/spring-hibernate-base-annotation">《SpringMVC3.1+Hibernate4.1.7完全基于注解配置(零配置文件)》</a>)说过，在修改配置方式的时候遇到过不少问题。这里介绍一下。
<div>
	<strong>方式一</strong></div>
<div>
	<a href="http://www.coderli.com">OneCoder</a>考虑在DataSourceConfig中，仅保留数据源配置，其他的诸如SessiionFactory的配置都移到AppConfig中。代码如下：</div>

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

	@Bean(autowire=Autowire.BY_TYPE)
	public DataSource dataSource() throws PropertyVetoException {
		ComboPooledDataSource dataSource = new ComboPooledDataSource();
		dataSource.setDriverClass(driverClass);
		dataSource.setJdbcUrl(url);
		dataSource.setUser(user);
		dataSource.setPassword(password);
		return dataSource;
	}
}
```

```java
/**
 * Spring3.1基于注解的配置类， 用于代替原来的<b>applicationContext.xml</b>配置文件
 * 
 * @author lihzh
 * @date 2012-10-12 下午4:23:13
 */
@ComponentScan(basePackages = "com.coderli.shurnim.*.biz")
@Import(DataSourceConfig.class)
@Configuration
@EnableTransactionManagement
public class DefaultAppConfig {
	
	@Autowired
	DataSourceConfig config;

	@Bean
	public PropertySourcesPlaceholderConfigurer placehodlerConfigurer() {
		return new PropertySourcesPlaceholderConfigurer();
	}

	@Bean
	public LocalSessionFactoryBean sessionFactory()
			throws PropertyVetoException {
		LocalSessionFactoryBean sessionFactoryBean = new LocalSessionFactoryBean();
		sessionFactoryBean.setDataSource(config.dataSource());
		Properties hibernateProperties = new Properties();
		hibernateProperties.setProperty("hibernate.dialect",
				"org.hibernate.dialect.MySQLDialect");
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

这里，这样配置的依据是参考Spring中@Configuration注解的注释说明：

> With the @Import annotation
> 
> @Configuration classes may be composed using the @Import annotation, not unlike the way that works in Spring XML. Because @Configuration objects are managed as Spring beans within the container, imported configurations may be injected using @Autowired or @Inject:</p>
> 
> @Configuration
> public class DatabaseConfig {
>      @Bean
>      public DataSource dataSource() {
>          // instantiate, configure and return DataSource
>      }
> }
> 
> @Configuration
> @Import(DatabaseConfig.class)
> public class AppConfig {
>      @Inject DatabaseConfig dataConfig;
> 
>      @Bean
>      public MyBean myBean() {
>          // reference the dataSource() bean method
>          return new MyBean(dataConfig.dataSource());
>      }
> }
> 
> Now both AppConfig and the imported DatabaseConfig can be bootstrapped by registering only AppConfig against the Spring context:
> new AnnotationConfigApplicationContext(AppConfig.class);

启动Tomcat，报错：
<p style="text-align: center; ">
	<img alt="" src="/images/oldposts/q1Viq.jpg" style="height: 130px; width: 640px; " /></p>

空指针异常，显然是DataSourceConfig没有注入进来，更换@Inject注解，问题依旧。
<div>
	<strong>方式二</strong></div>

既然注入DataSourceCOnfig无效，<a href="http://www.coderli.com">OneCoder</a>考虑，可否直接注入DataSource Bean。修改代码如下：

```java
/**
 * Spring3.1基于注解的配置类， 用于代替原来的<b>applicationContext.xml</b>配置文件
 * 
 * @author lihzh
 * @date 2012-10-12 下午4:23:13
 */
@ComponentScan(basePackages = "com.coderli.shurnim.config")
@Import(DataSourceConfig.class)
@Configuration
@EnableTransactionManagement
public class DefaultAppConfig {
	
	@Autowired
	DataSource dataSource;

	@Bean
	public PropertySourcesPlaceholderConfigurer placehodlerConfigurer() {
		return new PropertySourcesPlaceholderConfigurer();
	}

	@Bean
	public LocalSessionFactoryBean sessionFactory()
			throws PropertyVetoException {
		LocalSessionFactoryBean sessionFactoryBean = new LocalSessionFactoryBean();
		sessionFactoryBean.setDataSource(dataSource);
		Properties hibernateProperties = new Properties();
		hibernateProperties.setProperty("hibernate.dialect",
				"org.hibernate.dialect.MySQLDialect");
		sessionFactoryBean.setHibernateProperties(hibernateProperties);
		sessionFactoryBean.setPackagesToScan("com.coderli.shurnim.*.model");
		return sessionFactoryBean;
	}
```


启动Tomcat，报错：
<div style="text-align: center; ">
	<img alt="" src="/images/oldposts/V2Mqu.jpg" style="width: 640px; height: 108px; " /></div>

<a href="http://www.coderli.com">OneCoder</a>在各个Bean的方法上加断点调试，发现dataSource也是null，看来还是没注入进来导致的。也许这两个场景是一个问题，先解决没注入的问题看看吧。
	
说实话，这个问题困扰了<a href="http://www.coderli.com">OneCoder</a>近一天，搜索也没什么好的头绪，搜出来的东西差距都比较大。<a href="http://www.coderli.com">OneCoder</a>只能一遍一遍阅读自己的代码分析可能的原因同时仔细查看Spring官方的注释文档。<a href="http://www.coderli.com">OneCoder</a>在Debug中似乎意识到一个问题，就是<a href="http://www.coderli.com">OneCoder</a>这里使用了

```java	
@Bean
public PropertySourcesPlaceholderConfigurer placehodlerConfigurer() {
	return new PropertySourcesPlaceholderConfigurer();
}
```

这个bean用来使用替换变量符"${}"。这个替换符正式在DataSourceConfig中配置数据源使用的，这样的花，是否会造成Spring初始化Bean的生命周期的混乱呢。因为初始化dataSource Bean的时候需要上述bean，而初始化上述bean的时候，已经错过了DataSource bean的注入时机。那么如何解决呢，<a href="http://www.coderli.com">OneCoder</a>还是得求助官方文档。又是一遍又一遍的阅读，<a href="http://www.coderli.com">OneCoder</a>在@Bean注解的注释中，发现这样的一段话。

> A note on BeanFactoryPostProcessor-returning @Bean methods
> 				<p>
> 					Special consideration must be taken for @Bean methods that return Spring BeanFactoryPostProcessor (BFPP) types. Because BFPP objects must be instantiated very early in the container lifecycle, they can interfere with processing of annotations such as @Autowired, @Value, and @PostConstruct within @Configuration classes. To avoid these lifecycle issues, mark BFPP-returning @Bean methods as static. For example:</p>
> 				<p>
> 					&nbsp;&nbsp;&nbsp;&nbsp; @Bean<br />
> 					&nbsp;&nbsp;&nbsp;&nbsp; public static PropertyPlaceholderConfigurer ppc() {<br />
> 					&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; // instantiate, configure and return ppc ...<br />
> 					&nbsp;&nbsp;&nbsp;&nbsp; }<br />
> 					By marking this method as static, it can be invoked without causing instantiation of its declaring @Configuration class, thus avoiding the above-mentioned lifecycle conflicts. Note however that static @Bean methods will not be enhanced for scoping and AOP semantics as mentioned above. This works out in BFPP cases, as they are not typically referenced by other @Bean methods. As a reminder, a WARN-level log message will be issued for any non-static @Bean methods having a return type assignable to BeanFactoryPostProcessor.</p>

果然被我猜中了，这段意思大概是说，类似PropertyPlaceholderConfigurer这种的Bean是需要在其他Bean初始化之前完成的，这会影响到Spring Bean生命周期的控制，所以如果你用到了这样的Bean，需要把他们声明成Static的，这样就会不需要@Configuration的实例而调用，从而提前完成Bean的构造。并且，这里还提到，如果你没有把实现&nbsp;BeanFactoryPostProcessor接口的Bean声明为static的，他会给出警告。

<a href="http://www.coderli.com">OneCoder</a>赶紧去检查自己的控制台，果然发现了这样一句话：

> WARNING: @Bean method DefaultAppConfig.placehodlerConfigurer is non-static and returns an object assignable to Spring&#39;s BeanFactoryPostProcessor interface. This will result in a failure to process annotations such as @Autowired, @Resource and @PostConstruct within the method&#39;s declaring @Configuration class. Add the &#39;static&#39; modifier to this method to avoid these container lifecycle issues; see @Bean Javadoc for complete details

			
唉，本来<a href="http://www.coderli.com">OneCoder</a>是很重视警告的，这次怎么就没注意到呢。赶紧改成static的。重新启动。终于，一切OK了！


