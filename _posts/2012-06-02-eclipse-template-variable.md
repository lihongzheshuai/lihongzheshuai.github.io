---
layout: post
title: Eclipse使用技巧 - 自定义注释模板变量
date: 2012-06-02 18:08 +0800
author: onecoder
comments: true
tags: [eclipse, 模版, 自定义]
thread_key: 258
---
Eclipse的代码注释模板很丰富，如：user、year、date、time等等，请参考附件。 尽管模板变量如此之多，但是对于复杂多边的实际项目而言，还是不够用，怎么办？自己增加新的呗！ Eclipse配置界面都不支持定制自己的注释模板变量，没办法，改Eclipse源码。 具体怎么改，好像无头苍蝇，百度和谷歌了2天，还是无果，在边搜边摸索的过程中才知道需要修改如下两个架包对应的源码

* org.eclipse.jdt.ui.jar 
* org.eclipse.text.jar 

发现了三个重要的文件： 

* org.eclipse.jface.text.template.TextTemplateMessageg.properties
*  org.eclipse.jface.text.templates.GlobalTemplateVariables.java 
* org.eclipse.jdt.internal.corext.template.java.CodeTemplateContextType.java

#### TextTemplateMessageg.properties

定义了一些全局模板：

```properties
# global variables
GlobalVariables.variable.description.cursor=The cursor position after editing template variables
GlobalVariables.variable.description.dollar=The dollar symbol
GlobalVariables.variable.description.date=Current date
GlobalVariables.variable.description.year=Current year
GlobalVariables.variable.description.time=Current time
GlobalVariables.variable.description.user=User name
GlobalVariables.variable.description.selectedWord= The selected word
GlobalVariables.variable.description.selectedLines= The selected lines
```

我们可以看到user、year、date、time都在里面。 如果要增加自己的模板变量，就加吧？例如： 

```properties
GlobalVariables.variable.description.copyright=Copyright all resolved
```

#### SimpleTemplateVariableResolver

全局模板变量在***GlobalTemplateVariables***里面，均继承自***SimpleTemplateVariableResolver*** 增加一个对应*GlobalVariables.variable.description.copyright*的模板变量

```java
  /**
     * The copyright variable evaluates to the current copyright.
     * Added by 博主 2011-10-30
      */
    public static class Copyright extends SimpleTemplateVariableResolver
    {
        /**
         * 默认从环境变量中取copyright信息，环境变量可以定义在eclipse.ini的vmargs下面
         */
        private static String value = System.getProperty("copyright");
        /**
         * Creates a new copyright variable
         */
        public Copyright()
        {
            super("copyright", TextTemplateMessages.getString("GlobalVariables.variable.description.copyright")); //$NON-NLS-1$ //$NON-NLS-2$
        }

        /**
         * {@inheritDoc}
         */
        protected String resolve(TemplateContext context)
        {
            if (value != null)
            {
                return TextTemplateMessages.getString("GlobalVariables.variable.description.copyright");
            }
            return value; //$NON-NLS-1$
        }
    }
```

#### CodeTemplateContextType

让Eclipse的Reference界面配置code template里支持$**{copyright}**，修改：CodeTemplateContextType，在其构造方法里面增加Copyright实例

```java
public CodeTemplateContextType(String contextName) {
        super(contextName);

        fIsComment= false;

        // global
        addResolver(new GlobalTemplateVariables.Dollar());
        addResolver(new GlobalTemplateVariables.Date());
        addResolver(new GlobalTemplateVariables.Year());
        addResolver(new GlobalTemplateVariables.Time());
        addResolver(new GlobalTemplateVariables.User());
        //  Added by 博主 2011-10-30
       addResolver(new GlobalTemplateVariables.Copyright());
```

将修改的内容加到***org.eclipse.jdt.ui.jar***和***org.eclipse.text.jar***这两个包中 先退出Eclipse，再使用BeyondCompare之类的比较工具，将修改编译好的calss文件和properties文件覆盖到原有包中，不过如果你动jar的命令行操作，也可以使用jar命令打包。 好了，现在重新启动Eclipse，赶紧到windows-preferences->java-code style->code template界面去体验一下吧。

新建一个java类，在类名上方按Ctrl+Alt+j就可以出现自己的copyright注释了。 想想很简单。

**附录：Eclipse针对java代码模板的内置变量**

> cursor 将编辑器的光标放在这个位置。 N/A  <br />
> date 插入当前日期。 <br />
> dollar 插入货币的文字符号。 $  <br />
> elemType 尝试猜测具有给定 ID 的这个元素的类型。 MyType  <br />
> enclosing_method 插入模板被插入其中的那个方法的名称。 method()  <br />
> enclosing_method_arguments 为包围方法插入参数。 arg1, arg2  <br />
> enclosing_package 插入当前类的包名。 com.example.ui  <br />
> enclosing_project 插入包含所编辑的这个类的项目的名称。 myProject  <br />
> enclosing_type 插入正在编辑的类型（类）的名称。 MyType  <br />
> exception_variable_name 插入一个异常变量名称，进行最佳猜测。 e, ioe  <br />
> file 文件的简称。 MyType.java  <br />
> import 如果尚未导入，那么针对给定类型插入一个导入声明。 import com.example.ui.MyOtherType  <br />
> importStatic 与 import 相同，只不过是静态导入。 import static com.example.ui.MyOtherType.*  <br />
> line_selection 将选中的行插入到这里。这对用模板包装行是很有用的。 以选中行作为主体的 do、while 循环  <br />
> primary_type_name 没有扩展名的文件简称。 MyType  <br />
> time 插入当前的时间。  <br />
> todo 注释中的 TODO 标记。 TODO  <br />
> user 当前用户的名字。 ngood  <br />
> var 解析为本地变量，如果不只一个，就提供一个列表。 myvar  <br />
> word_selection 插入当前选中的单词。 N/A  <br />
> year 将现在的年份插入到代码中。 2010  <br />

原文地址<br/>
[http://shareal.blog.163.com/blog/static/27659056201193063914196](http://shareal.blog.163.com/blog/static/27659056201193063914196)