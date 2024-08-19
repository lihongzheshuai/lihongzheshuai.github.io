---
layout: post
title: SpringXD 自定义Job模块开发
tags: [Spring]
categories: [Java技术研究]
date: 2016-11-07 13:33:12 +0800
comments: true
author: onecoder
thread_key: 1903
---
SpringXD中的Job实际即为Spring Batch中的Job，因此我们先按照Spring Batch的规范开发一个简单的Job。

<!--break-->

项目依赖：

```xml
<dependencies>
        <dependency>
            <groupId>org.springframework.batch</groupId>
            <artifactId>spring-batch-infrastructure</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.batch</groupId>
            <artifactId>spring-batch-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.logging.log4j</groupId>
            <artifactId>log4j-api</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.logging.log4j</groupId>
            <artifactId>log4j-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
        </dependency>
    </dependencies>
```

实际这里无需配置spring-batch的依赖，因为会在springxd的parent pom中声明。而springxd的parent一般我们都会声明的。即：

```xml
    <groupId>org.springframework.xd</groupId>
        <artifactId>spring-xd-module-parent</artifactId>
        <!-- 1.1.x or later -->
        <version>1.3.1.RELEASE</version>
    </parent>
```

Job开发：

```java
package cn.rongcapital.springxd.job;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.repeat.RepeatStatus;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @author li.hzh
 * @date 2016-11-01 14:03
 */
@Configuration
public class HelloWorldJob {

    private static Logger logger = LoggerFactory.getLogger(HelloWorldJob.class);

    @Autowired
    private JobBuilderFactory jobs;

    @Autowired
    private StepBuilderFactory steps;

    @Bean(name = "helloworldJob")
    public Job job(@Qualifier("step1") Step step1, @Qualifier("step2") Step step2) {
        return jobs.get("myJob").start(step1).next(step2).build();
    }

    @Bean
    protected Step step1() {
        return steps.get("step1").tasklet(new Tasklet() {
            @Override
            public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) throws Exception {
                logger.info("Step One");
                return RepeatStatus.FINISHED;
            }
        }).build();
    }

    @Bean
    protected Step step2() {
        return steps.get("step2")
                .tasklet(new Tasklet() {
                    @Override
                    public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) throws Exception {
                        logger.info("Step Two");
                        return RepeatStatus.FINISHED;
                    }
                })
                .build();
    }
}
```

简单的不能再简单了。就是两个步骤，一个打印Step One Hello，一个打印Step Two World。本地运行确认可以正常执行。

配置SpringXD配置文件
即使是使用JavaConfig的方式开发，也需要配置一个properties文件，声明jobClass的base_package，例如：

```properties
base_packages=org.springframework.springxd.samples.batch
```

究其原因，可参见源码：

```java
/**
      * Create a simple module based on the provided {@link ModuleDescriptor}, {@link ModuleOptions}, and {@link ModuleDeploymentProperties}.
      *
      * @param moduleDescriptor descriptor for the composed module
      * @param moduleOptions module options for the composed module
      * @param deploymentProperties deployment related properties for the composed module
      * @return new simple module instance
      */
     private Module createSimpleModule(ModuleDescriptor moduleDescriptor, ModuleOptions moduleOptions,
               ModuleDeploymentProperties deploymentProperties) {
          if (log.isInfoEnabled()) {
               log.info("creating simple module " + moduleDescriptor);
          }
          SimpleModuleDefinition definition = (SimpleModuleDefinition) moduleDescriptor.getModuleDefinition();
          ClassLoader moduleClassLoader = ModuleUtils.createModuleRuntimeClassLoader(definition, moduleOptions, this.parentClassLoader);

          Class<? extends SimpleModule> moduleClass = determineModuleClass((SimpleModuleDefinition) moduleDescriptor.getModuleDefinition(),
                    moduleOptions);
          Assert.notNull(moduleClass,
                    String.format("Required module artifacts are either missing or invalid. Unable to determine module type for module definition: '%s:%s'.",
                              moduleDescriptor.getType(), moduleDescriptor.getModuleName()));
          return SimpleModuleCreator
                    .createModule(moduleDescriptor, deploymentProperties, moduleClassLoader, moduleOptions, moduleClass);
     }
```

在createSimpleModule方法中需要获取moduleClass，取不到会报错。而获取的方式是，

```java
private Class<? extends SimpleModule> determineModuleClass(SimpleModuleDefinition moduleDefinition,
      ModuleOptions moduleOptions) {
   String name = (String) moduleOptions.asPropertySource().getProperty(MODULE_EXECUTION_FRAMEWORK_KEY);
   if ("spark".equals(name)) {
      return NonBindingResourceConfiguredModule.class;
   }
   else if (ModuleUtils.resourceBasedConfigurationFile(moduleDefinition) != null) {
      return ResourceConfiguredModule.class;
   }
   else if (JavaConfiguredModule.basePackages(moduleDefinition).length > 0) {
      return JavaConfiguredModule.class;
   }
   return null;
}
```

最后一个else if里，可见JavaConfiguredModule会需要查找basePackages属性的。

```java
public static String[] basePackages(SimpleModuleDefinition moduleDefinition) {

   Properties properties = ModuleUtils.loadModuleProperties(moduleDefinition);
   //Assert.notNull(propertiesFile, "required module properties not found.");
   if (properties == null) {
      return new String[0];
   }


   String basePackageNames = properties.getProperty(BASE_PACKAGES);
   return StringUtils.commaDelimitedListToStringArray(basePackageNames);
}
```

而这个属性是从properties配置文件中查找的

```java
/**
 * Return a resource that can be used to load the module '.properties' file (containing <i>e.g.</i> information
 * about module options, or null if no such file exists.
 */
public static Resource modulePropertiesFile(SimpleModuleDefinition definition) {
   return ModuleUtils.locateModuleResource(definition, ".properties");
}
```


进入打包SpringXD Module的环节。

打包SpringXD Module
pom配置

```xml
<parent>
        <groupId>org.springframework.xd</groupId>
        <artifactId>spring-xd-module-parent</artifactId>
        <!-- 1.1.x or later -->
        <version>1.3.1.RELEASE</version>
    </parent>
```

需要制定springxd的parent里，因为其中配置了maven build所需的插件。通过命令打包：

```bash
mvn package
```

然后上传到SpringXD，进入xd-shell

```bash
bin/xd-shell
xd:>module upload --type job --name helloworld --file /data/dps-springxd-job-helloworld-1.0.0.BUILD-SNAPSHOT.jar
Successfully uploaded module 'job:helloworld'
```

执行Job

```bash
xd:>job create --name helloworldJob --definition "helloworld" --deploy
Successfully created and deployed job 'helloworldJob'
xd:>job launch helloworldJob
Successfully submitted launch request for job 'helloworldJob'
```

> 注：在笔者的分布式环境中，通过module upload后，没有自动分发到container节点上，临时通过手动拷贝完成。此问题待排查。
