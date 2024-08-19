---
layout: post
title: 《Gradle user guide》原创翻译 — 第六章 构建脚本基础
date: 2013-09-21 08:48 +0800
author: onecoder
comments: true
tags: [Gradle, 翻译]
categories: [Java技术研究]
thread_key: 1506
---

译者注：从第六章开始翻译，为了个人学习需要，先省略了前面已经了解和不太相关部分。见谅。<br />
	<br />
	6.1 项目和任务<br />
	<br />
	Gradle里的一切都基于两个基本概念：项目和任务。(projects and tasks)。<br />
	<br />
	每个Gradle构建都是由一个或多个项目组成的。项目代表你的软件中可构建的一些组件。具体的含义取决于你实际构建的东西。例如，项目可能代表一个JAR或者一个web工程。它也可能代表一个由其他项目生成的jar包组成的ZIP压缩包。项目不必代表准备构建的东西，它应该代表准备完成的事情，如，把你的应用发布到生成环境中。如果你仍感觉有些模糊也不用担心。Gradle对约定式构建的支持，给出了对项目更明确的定义。<br />
	<br />
	每个项目由一个或多个任务组成。任务代表一些原子化的构建过程中执行的工作。如，编译一些类，创建一个JAR包，生成javadoc，或是发布一些归档到库中。<br />
	<br />
	现在，我们将会关注在一个项目中定义一些简单的任务。在后面的章节，我们将会学习处理多项目以及更多的关于项目和任务的知识。<br />
	<br />
	6.2 Hello world<br />
	<br />
	你通过使用gradle命令来执行Gradle构建。gradle命令在当前路径下查找build.gradle配置文件。我们称这个build.gradle文件为构建脚本，或像我们随后看到的那样，严格的称其为构建配置脚本。构建脚本定义了项目和它的任务。<br />
	<br />
	尝试创建名为build.gradle的构建脚本。<br />
	例子6.1 第一个构建脚本<br />
	<br />
	build.gradle<br />

```groovy
task hello {
    doLast {
        println 'Hello world!'
    }
}}
```

在命令行中，进入包含脚本的目录然后通过gradle -q hello命令执行构建脚本。<br />
		<br />
		例子6.2 执行构建脚本<br />
		<br />
		gradle -q hello的输出</p>
	<blockquote>
		<p>
			&gt; gradle -q hello<br />
			Hello world!<br />
			&nbsp;</p>
	</blockquote>
	<table cellpadding="0" cellspacing="0">
		<tbody>
			<tr>
				<td>
					-q选项做了什么？<br />
					用户手册中的大多数例子都是用-q选项执行的。这会屏蔽Gradle's 日志信息，因此只会显示任务的输出信息。这会使用户手册中的例子的输出简洁一些。如果你不想可以不使用该选项。参见第18章，记录更详细的日志，影响Gradle输出的命令行选项。</td>
			</tr>
		</tbody>
	</table>
	这里发生了什么？构建脚本定义了一个单独的称作hello的任务，并且给其增加了一个操作。当你执行gradle hello命令的时候，Gradle执行了hello任务，该任务依次执行你提供的操作。操作是等待执行的包含一些Groovy代码的闭包。<br />
	<br />
	如果你认为这看起来和Ant的目标相似，那么你答对了。Gradle的任务就等于Ant中的目标(target)。不过，如你将要看到的那样，它强大的多。我们使用了与Ant不用的术语，是因为我们觉得任务比目标更贴切。不过，这里术语的使用与Ant产生了冲突，在Ant称命令为任务，如javac或copy。所以，当我们说任务的时候，我们都是指Gradle里的任务，等价于Ant里的目标。如果我们讨论Ant里的任务(Ant命令)，我们会说ant 任务。<br />
	<br />
	译者注：接下来会直接翻译第七章的内容，因为和译者直接相关。是关于构建Java工程的。</div>


