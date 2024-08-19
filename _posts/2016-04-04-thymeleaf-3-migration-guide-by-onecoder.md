---
layout: post
title: Thymeleaf 3 迁移指南
tags: [Thymeleaf]
categories: [知识扩展]
date: 2016-04-04 14:54:46 +0800
comments: true
thread_key: 1886
---
2016年2月23日，Thymeleaf 发布了 3.0 Beta2版，此迁移指南重点翻译自官方手册:[Thymeleaf 3 ten-minute migration guide](http://www.thymeleaf.org/doc/articles/thymeleaf3migration.html)。

[***十分钟迁移到Thymeleaf 3***](http://www.thymeleaf.org/doc/articles/thymeleaf3migration.html)

如果你是打算从Thymeleaf2迁移到Thymeleaf3的用户。首先，一个好消息是你当前的Thymeleaf模板与Thymeleaf3完全兼容。所以，如果要进行迁移，你只要做一些配置上的修改。

Thymeleaf 3.0 BETA版本是稳定且完全覆盖2.1版本的特性，所以，推荐你进行升级。因为新版本的性能更好而且有许多新的特性。

唯一的问题是，不是所有的Thymeleaf方言（dialect）都迁移到了Thymeleaf 3中。因此，在迁移前要做好这方面的兼容性检查。

下面来介绍一下Thymeleaf 3中的一些变化和特性。

### 1. 模板变化

唯一的变化是，推荐你去掉模板中的 ***th:inline=“text”*** 属性。因为在HTML或XML模板中，不再需要该属性去支持文本中内联表达式的特性。当然，只是推荐你去去掉该属性，不去掉，你原来模板一样可以工作。去掉的好处是会给你带来执行性能方面的提升。

详细信息可参见下文的***内联机制***部分。

### 2. 配置变化

看一个thymeleaf-spring4集成的配置文件的例子。

首先你需要更新Maven依赖

```xml
<dependency>
  <groupId>org.thymeleaf</groupId>
  <artifactId>thymeleaf</artifactId>
  <version>3.0.0.BETA02</version>
</dependency>
<dependency>
  <groupId>org.thymeleaf</groupId>
  <artifactId>thymeleaf-spring4</artifactId>
  <version>3.0.0.BETA02</version>
</dependency>
```
然后是spring 配置

```java
@Configuration
@EnableWebMvc
@ComponentScan("com.thymeleafexamples")
public class ThymeleafConfig extends WebMvcConfigurerAdapter implements ApplicationContextAware {

  private ApplicationContext applicationContext;

  public void setApplicationContext(ApplicationContext applicationContext) {
    this.applicationContext = applicationContext;
  }

  @Bean
  public ViewResolver viewResolver() {
    ThymeleafViewResolver resolver = new ThymeleafViewResolver();
    resolver.setTemplateEngine(templateEngine());
    resolver.setCharacterEncoding("UTF-8");
    return resolver;
  }

  private TemplateEngine templateEngine() {
    SpringTemplateEngine engine = new SpringTemplateEngine();
    engine.setTemplateResolver(templateResolver());
    return engine;
  }

  private ITemplateResolver templateResolver() {
    SpringResourceTemplateResolver resolver = new SpringResourceTemplateResolver();
    resolver.setApplicationContext(applicationContext);
    resolver.setPrefix("/WEB-INF/templates/");
    resolver.setTemplateMode(TemplateMode.HTML);
    return resolver;
  }
}
```

与Thymeleaf 2相比，第一个区别是，现在推荐的模板解析类是 SpringResourceTemplateResolver。该类依赖于 Spring的ApplicationContext 上下文。因此，你的配置类需要实现 ApplicationContextAware 接口。

第二个区别是。提供了TemplateMode.HTML 枚举常量。模板类型的方法参数不再是string类型的。

如果你需要添加其他方言，可以通过engine.addDialect(…)方法，当然你需要先确认Thymeleaf 3是否支持。

你可以到官方下载一些集成配置的例子。

- [Thymeleaf 3 + Spring 4 + Java config example](https://github.com/jmiguelsamper/thymeleaf3-spring-helloworld)
- [Thymeleaf 3 + Spring 4 + XML config example](https://github.com/jmiguelsamper/thymeleaf3-spring-xml-helloworld)
- [Thymeleaf 3 + Servlet 3 example](https://github.com/jmiguelsamper/thymeleaf3-servlet-helloworld)

### 3. 完整的HTML5 标记支持

Thymeleaf 3.0 不再是基于XML结构的。由于引入新的解析引擎，模板的内容格式不再需要严格遵守XML规范。即不在要求标签闭合，属性加引号等等。当然，出于易读性考虑，还是推荐你按找XML的标准去编写模板。

下面的代码在Thymeleaf 3.0里是合法的：

```html
<div><p th:text=${mytext} ng-app>Whatever
```

新解析引擎的介绍，可参考：[https://github.com/thymeleaf/thymeleaf/issues/390](https://github.com/thymeleaf/thymeleaf/issues/390)

### 4. 模板类型

Thymeleaf 3 移除了之前版本的模板类型，新的模板类型为：

- HTML
- XML
- TEXT
- JAVASCRIPT
- CSS
- RAW

2个标记型模板(HTML和XML)，3个文本型模板(TEXT, JAVASCRIPT和CSS) 一个无操作(no-op)模板 (RAW)。

HTML模板支持包括HTML5，HTML4和XHTML在内的所有类型的HTML标记。且不会检查标记是否完整闭合。此时，标记的作用范围按可能的最大化处理。

详细介绍可参见：Thymeleaf 3.0 Template Mode set
一些关于模板类型的例子：[https://github.com/jmiguelsamper/thymeleaf3-template-modes-example](https://github.com/jmiguelsamper/thymeleaf3-template-modes-example)

#### 4.1 文本型模板

文本型模板使得Thymeleaf可以支持输出CSS、Javascript和文本文件。在你想要在CSS或Javascript文件中使用服务端的变量时；或者想要输出纯文本的内容时，比如，在邮件中，该特性是否有用。

在文本模式中使用Thymeleaf的特性，你需要使用一种新的语法，例如：

```html
[# th:each="item : ${items}"]
  - [# th:utext="${item}" /]
[/]
```

该语法的介绍，参见：[https://github.com/thymeleaf/thymeleaf/issues/395](https://github.com/thymeleaf/thymeleaf/issues/395)

#### 4.2 增强的内联机制

现在可无需额外的标签，直接在文本中输出数据：

<p>This product is called [[${product.name}]] and it's great!</p>

详见：Inlined output expressions
关于内联机制的讨论： Refactoring of the inlining mechanism

### 5. 片段（Fragment）表达式

Thymeleaf 3.0 引入了一个新的片段表达式。形如：~{commons::footer}。

该特性十分有用（真的是是否有用，直接解决了一直困扰我的定义通用的header和footer的问题）。直接看例子来理解一下该语法吧：

```html
<head th:replace="base :: common_header(~{::title},~{::link})">
  <title>Awesome - Main</title>
  <link rel="stylesheet" th:href="@{/css/bootstrap.min.css}">
  <link rel="stylesheet" th:href="@{/themes/smoothness/jquery-ui.css}">
</head>
```

这里，将两外另个包含&lt;title&gt;和&lt;link&gt;标签的片段作为参数传递给了common_header片段，在common_header中使用如下：

```html
<head th:fragment="common_header(title,links)">
  <title th:replace="${title}">The awesome application</title>

  <!-- Common styles and scripts -->
  <link rel="stylesheet" type="text/css" media="all" th:href="@{/css/awesomeapp.css}">
  <link rel="shortcut icon" th:href="@{/images/favicon.ico}">
  <script type="text/javascript" th:src="@{/sh/scripts/codebase.js}"></script>

  <!--/* Per-page placeholder for additional links */-->
  <th:block th:replace="${links}" />

</head>
```

渲染出结果如下：

```html
<head>

  <title>Awesome - Main</title>

  <!-- Common styles and scripts -->
  <link rel="stylesheet" type="text/css" media="all" href="/awe/css/awesomeapp.css">
  <link rel="shortcut icon" href="/awe/images/favicon.ico">
  <script type="text/javascript" src="/awe/sh/scripts/codebase.js"></script>

  <link rel="stylesheet" href="/awe/css/bootstrap.min.css">
  <link rel="stylesheet" href="/awe/themes/smoothness/jquery-ui.css">

</head>
```

更多关于片段表达式的内容可参考：[https://github.com/thymeleaf/thymeleaf/issues/451](https://github.com/thymeleaf/thymeleaf/issues/451)

### 6. 无操作标记（token）

Thymeleaf 3.0 另一个新的特性就是无操作（NO-OP  no-operation）标记，下划线&quot;\_&quot;，代表什么也不做。

例如：

```html
<span th:text="${user.name} ?: _">no user authenticated</span>
```

当user.name 为空的时候，直接输出标签体中的内容：no user authenticated。该特性让我们可以直接使用原型模板中的值作为默认值。

该特性详细资料参考：[The NO-OP token](https://github.com/thymeleaf/thymeleaf/issues/452)

### 7 模板逻辑解耦

Thymeleaf 3.0 允许 HTML和XML模式下的模板内容和控制逻辑完全解耦。

例如，在3.0版本里，一个“干净”的home.html模板内容如下：

```html
<!DOCTYPE html>
<html>
  <body>
    <table id="usersTable">
      <tr>
        <td class="username">Jeremy Grapefruit</td>
        <td class="usertype">Normal User</td>
      </tr>
      <tr>
        <td class="username">Alice Watermelon</td>
        <td class="usertype">Administrator</td>
      </tr>
    </table>
  </body>
</html>
```

我们只需额外定义一个home.th.xml文件，就可以把之前的home.html文件当作Thymeleaf模板来使用，内容如下：

```xml
<?xml version="1.0"?>
<thlogic>
  <attr sel="#usersTable" th:remove="all-but-first">
    <attr sel="/tr[0]" th:each="user : ${users}">
      <attr sel="td.username" th:text="${user.name}" />
      <attr sel="td.usertype" th:text="#{|user.type.${user.type}|}" />
    </attr>
  </attr>
</thlogic>
```

逻辑解耦时，指定的属性会在模本解析的过程中插入指定的位置。通过sel属性指定选择器。

逻辑解耦，意味着可以使用纯HTML文件作为设计模板，允许设计人员不再需要具备Thymeleaf的相关知识。
详细介绍：[Decoupled Template Logic](https://github.com/thymeleaf/thymeleaf/issues/465)

### 8. 性能提升

除了之前提到的特性之外，Thymeleaf 3.0 的另外一个重要突破就是有明显的性能提升。

2.1版本之前采用的基于XML的模板引擎，虽然有助于实现很多的特性，但是在有些情况下也造成了性能的损失。在绝大多数的项目里Thymeleaf的渲染时间是几乎可以忽略不计的，这也就凸显出来了Thymeleaf在某些特定情景下的性能问题。(例如：在高负载的网站中处理成千上万行的表格)。

Thymeleaf 3 重点关注性能问题并完全重写了引擎。因此与之前版本相比性能有很大的提升。而且，这种提升不仅仅局限于渲染时间，也包括更低的内存占用以及在高并发场景下的低延迟。

关于Thymeleaf 3 技术架构的讨论可参见：[New event-based template processing engine](https://github.com/thymeleaf/thymeleaf/issues/389)

值得一提的是，性能提升不仅是架构层面的事，也包括3.0 版本里的一些有助于性能提升的新特性。例如，在3.0版本里使用SpringEL表达式的编译器(从Spring Framework4.2.4版本开始)，在使用Spring的场景下，可进一步的提升性能。具体参见：[Configuring the SpringEL compiler](https://github.com/thymeleaf/thymeleaf-spring/issues/95)

即使没有使用Spring而是使用OGNL表达式，在3.0版本里也有性能优化。Thymeleaf甚至给OGNL代码库贡献了很多源码，这些代码有助于提升Thymeleaf在新的MVC1.0（JSR371）标准环境下的性能。

### 9. 不依赖于Servlet API

其实Thymeleaf3.0 之前版本在离线执行的情况下已经做到了不依赖于Java Servlet API，就是说在执行模板的过程中不依赖于Web容器。一个实用的场景就是用作邮件模板。

然而，在Thymeleaf3.0里做到了在Web环境下也完全不依赖Servlet API。这样就使得与那些不依赖Java Servlet框架（如 [vert.x](http://vertx.io/), [RatPack](https://ratpack.io/), [Play Framework](https://www.playframework.com/)）的集成更加简单方便。

更多参见： [New extension point: Link Builders](https://github.com/thymeleaf/thymeleaf/issues/458) 和 [Generalisation of the IEngineContext mechanism.](https://github.com/thymeleaf/thymeleaf/issues/459)

### 10. 新的方言系统

Thymeleaf 3 提供了新的方言系统。如果你在早期版本上开发了Thymeleaf的方言，你需要使其与Thymeleaf 3 兼容。

新的方言接口十分简单

```java
public interface IDialect {

  public String getName();

}
```

可以通过实现IDialect的子类接口，实现更多不同的特性。

列举一下新方言系统增强的点：

- 除了processors之外，还提供了pre-processors 和 post-processors，模板的内容可以在处理之前和之后被修改。例如，我们可以使用pre-processors来缓存内容或者用post-processors来压缩输出结果。
- 提出了方言优先级的概念，可以对方言的处理器(processor)进行排序。处理器优先级的排序是跨方言的。
- 对象表达式方言提供可以模本内任意地方使用的新的表达式对象和工具对象。如：#strings, #numbers, #dates 等。

更多特性，可参见：

- [New Dialect API](https://github.com/thymeleaf/thymeleaf/issues/401)
- [New Pre-Processor and Post-Processor APIs](https://github.com/thymeleaf/thymeleaf/issues/400)
- [New Processor API](https://github.com/thymeleaf/thymeleaf/issues/399)

### 11 重构了核心API

核心接口进行了深度重构，详见：

- [Refactoring of the Template Resolution API](https://github.com/thymeleaf/thymeleaf/issues/419)
- [Refactoring of the Context API](https://github.com/thymeleaf/thymeleaf/issues/420)
- [Refactoring of the Message Resolution API](https://github.com/thymeleaf/thymeleaf/issues/421)

### 12 总结

Thymeleaf 3 是Thymeleaf 模板引擎经过4年多不懈的努力和工作后的一个重要的里程碑式的成果。提供了许多令人兴奋的新特性以及许多隐藏的改进。
所以，别再犹豫，赶紧来试试吧。

参考：

- [http://www.thymeleaf.org/doc/articles/thymeleaf3migration.html](http://www.thymeleaf.org/doc/articles/thymeleaf3migration.html)
- [https://github.com/thymeleaf/thymeleaf/issues/451](https://github.com/thymeleaf/thymeleaf/issues/451)
