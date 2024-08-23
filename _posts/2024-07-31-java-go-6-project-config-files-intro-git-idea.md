---
layout: post
title: 一起学Java(6)-[起步篇]教你掌握本协作项目中Gie和IDEA相关配置文件
date: 2024-07-31 13:01 +0800
author: onecoder
comments: true
tags: [Java,Gradle,Git,一起学Java]
categories: [一起学Java系列,（1）起步搭建篇]
---
前两篇文章（《[一起学Java(4)-java-all-in-one协作项目相关文件研究（Gradle篇-上）](https://www.coderli.com/java-go-4-project-config-files-intro-gradle-one/)》和《[一起学Java(5)-java-all-in-one协作项目相关文件研究（Gradle篇-下））](https://www.coderli.com/java-go-4-project-config-files-intro-gradle-two/)》）我们已经完成了对项目中Gradle相关文件的研究，按照计划我们继续研究项目的其他配置文件，主要是Git和IDEA自身两类。

<!--more-->

## 一、Git相关文件

### .gitignore文件

`.gitignore` 文件是用于Git版本控制系统的配置文件，顾名思义主要作用是告诉Git哪些文件或目录应该被忽略，不需要纳入版本控制。一般有如下几类情况：

1. **忽略不需要的文件**：避免将一些不需要的文件（如编译生成的二进制文件、中间文件、日志文件等）纳入版本控制。
2. **保护敏感信息**：防止将包含敏感信息的文件（如配置文件中的密码、API密钥等）纳入版本控制。
3. **提高效率**：减少不必要的文件纳入版本控制，可以提高Git操作的效率。

在本项目中，配置忽略的也是一些编程或工具自动生成的文件路径或具体文件，因为这些文件在团队每个人的本地都是根据我们的编译工具自动生成的，纳入版本管理会造成冲突反而造成问题，这是我们在做项目协作中常常被忽略的问题：

```plaintext
.gradle
build/
!gradle/wrapper/gradle-wrapper.jar
!**/src/main/**/build/
!**/src/test/**/build/

### IntelliJ IDEA ###
.idea/modules.xml
.idea/jarRepositories.xml
.idea/compiler.xml
.idea/libraries/
*.iws
*.iml
*.ipr
out/
!**/src/main/**/out/
!**/src/test/**/out/

### Eclipse ###
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
.sts4-cache
bin/
!**/src/main/**/bin/
!**/src/test/**/bin/

### NetBeans ###
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/

### VS Code ###
.vscode/

### Mac OS ###
.DS_Store
```

### **.gitignore** 文件的位置

`.gitignore` 文件通常位于Git仓库的根目录，也可以放在子目录中，子目录中的`.gitignore`文件只对其所在目录及子目录生效。`.gitignore` 文件的忽略规则是递归的，即父目录中的规则会影响子目录中的文件，除非子目录中有自己的 `.gitignore` 文件。

### **.gitignore** 文件的基本语法

- 空行或以 `#` 开头的行会被视为注释。
- 可以使用通配符 `*`、`?` 和 `[]` 来匹配文件名。
- 以斜杠 `/` 结尾表示目录。
- 以 `!` 开头表示反向匹配，即忽略某些文件的例外情况。

### 注意事项

- `.gitignore` 文件只能忽略那些未被Git追踪的文件。如果某个文件已经被纳入版本控制，即使将其添加到 `.gitignore` 中，Git仍然会继续追踪该文件的变化。要忽略这些已经被追踪的文件，需要先从版本控制中移除它们：

  ```bash
  git rm --cached <file>
  ```

通过合理配置 `.gitignore` 文件，可以有效管理和优化Git仓库，确保版本控制的高效和安全。显然为了保证团队一致性，该文件应该纳入版本管理。

## 二、IDEA工具相关文件

`.idea` 目录是JetBrains系列IDE（如IntelliJ IDEA、PyCharm、WebStorm等）创建的项目配置目录，包含了一些项目相关的配置信息。`.idea` 目录下可能存在的文件及目录很多，并且不同的文件根据其作用和定位是否应该纳入版本管理的情况也不一样，一些常见的文件和目录如下：

1. **.idea/compiler.xml**:
   - 这个文件保存与编译器相关的配置，例如编译输出路径、编译选项等。通过配置这个文件，可以控制项目的编译行为，确保项目能够正确编译和生成目标文件。建议纳入版本管理。

2. **.idea/encodings.xml**:
   - 这个文件定义了项目中使用的文件编码设置。不同的文件可以有不同的编码方式，通过这个文件可以确保所有文件的编码一致，避免因编码问题导致的乱码或其他问题。

3. **.idea/misc.xml**:
   - 包含一些通用的项目设置，例如 JDK 版本、项目名称等。这个文件通常还包括一些 IDE 的全局设置，如插件启用状态等。建议纳入版本管理。

4. **.idea/modules.xml**:
   - 列出了项目中包含的所有模块及其配置。模块是 IntelliJ 项目的基本组成单元，每个模块可以有独立的源码、资源和配置。这个文件帮助 IDE 识别和管理项目中的多个模块。

5. **.idea/vcs.xml**:
   - 保存版本控制系统的配置，例如使用的版本控制类型（Git、SVN 等）及其具体设置。通过这个文件，IDE 可以正确地与版本控制系统交互，管理代码的版本历史。建议纳入版本管理。

6. **.idea/workspace.xml**:
   - 存储用户特定的工作区配置，这些配置包括打开的文件、编辑器布局、窗口位置等。这是一个用户个性化的配置文件，不应该在团队中共享，因为不同开发者的工作习惯不同。

7. **.idea/inspectionProfiles/**:
   - 这个目录包含代码检查（inspection）配置文件。代码检查是 IntelliJ 提供的一个功能，可以自动检查代码中的潜在问题，并提供修复建议。通过自定义这些配置文件，可以控制检查规则，适应项目的编码规范。

8. **.idea/runConfigurations/**:
   - 保存运行和调试配置，例如应用程序的启动参数、环境变量、JVM 参数等。每个配置对应一个运行或调试的场景，开发者可以根据需要创建不同的配置来测试和运行项目。

9. **.idea/libraries/**:
   - 包含项目使用的库文件及其配置。这些库可能是第三方依赖，通过这个目录中的配置文件，IDE 可以正确识别和引用这些库，确保项目能正常编译和运行。

10. **.idea/codeStyles/**:
    - 定义代码风格和格式化设置，例如缩进、空格使用、换行规则等。通过这些配置文件，可以确保团队成员在不同的开发环境中使用一致的代码风格，提高代码的可读性和一致性。

对于本项目(java-all-in-one)来说，`.idea`目录下除.gitignore文件外只有6个文件：

![.idea目录](/images/post/java-go-6-idea-files/idea-files.png)

其中.gitignore、compiler.xml、vcs.xml、misc.xml和workspace.xml前文均已做过说明。只有gradle.xml和jarRepositories.xml还没介绍，下面重点介绍一下。

### **gradle.xml**

在使用 IntelliJ IDEA 的 Gradle 项目中，`gradle.xml` 文件是存储项目特定的 Gradle 设置的配置文件。它帮助 IntelliJ IDEA 了解如何处理与 Gradle 构建系统相关的操作和配置。如果删除该文件，IDEA将不知道该项目是一个通过Gradle配置的项目。`gradle.xml`文件的主要配置作用如下：

1. **Gradle 项目结构**：定义项目的 Gradle 相关信息，包括项目的 Gradle 版本、Gradle 构建文件的位置等。
2. **同步设置**：控制 IntelliJ IDEA 如何与 Gradle 项目进行同步，例如是否自动同步，是否在项目启动时进行同步等。
3. **任务配置**：存储在 IDEA 中运行 Gradle 任务的配置，可以直接从 IDE 运行特定的 Gradle 任务。
4. **其他特定设置**：包括 Gradle 相关的 VM 选项、堆内存设置等。

以下是本项目 `gradle.xml` 文件内容：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="GradleMigrationSettings" migrationVersion="1" />
  <component name="GradleSettings">
    <option name="linkedExternalProjectsSettings">
      <GradleProjectSettings>
        <option name="externalProjectPath" value="$PROJECT_DIR$" />
        <option name="gradleHome" value="$USER_HOME$/Downloads/Compressed/gradle-8.9" />
        <option name="modules">
          <set>
            <option value="$PROJECT_DIR$" />
          </set>
        </option>
      </GradleProjectSettings>
    </option>
  </component>
</project>
```

核心配置说明：

1. **`<component name="GradleSettings">`**：
   - **含义**：这个组件包含与 Gradle 相关的设置。
   - **作用**：管理 IntelliJ IDEA 与 Gradle 项目之间的交互和配置。

2. **`<option name="linkedExternalProjectsSettings">`**：
   - **含义**：这个选项包含所有链接的外部 Gradle 项目的设置。
   - **作用**：存储与外部 Gradle 项目相关的所有配置。

3. **`<GradleProjectSettings>`**：
   - **含义**：包含具体的 Gradle 项目设置。
   - **作用**：定义项目的 Gradle 配置参数。

4. **`<option name="externalProjectPath" value="$PROJECT_DIR$" />`**：
   - **含义**：定义外部 Gradle 项目的路径。
   - **作用**：告诉 IntelliJ IDEA 外部 Gradle 项目所在的目录。在此示例中，使用 `$PROJECT_DIR$` 表示项目的根目录。

5. **`<option name="gradleHome" value="$USER_HOME$/Downloads/Compressed/gradle-8.9" />`**：
   - **含义**：指定 Gradle 的主目录位置。
   - **作用**：告诉 IntelliJ IDEA 使用用户目录下特定位置的 Gradle 安装。在使用 Gradle Wrapper 时，通常不需要设置此项，直接依赖于 `gradle-wrapper.properties` 中的配置即可。
   - **注意**：此配置与使用 Gradle Wrapper 的理念相矛盾，建议使用 Gradle Wrapper 来管理 Gradle 版本。

6. **`<option name="modules">`**：
   - **含义**：这个选项包含一个模块的集合。
   - **作用**：定义项目中包含的模块。

研究到这里，发现一个我们项目的问题，我们项目是使用Gradle Wrapper的，不知道为什么这里配置了gradleHome，并且从路径来看显然是我本地路径的地址。因此，为了避免与 Gradle Wrapper 的使用理念相冲突，可以移除 `gradleHome` 的配置，并依赖 `gradle-wrapper.properties` 来管理 Gradle 版本。

调整后的配置示例（建议`git pull`更新项目代码）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="GradleMigrationSettings" migrationVersion="1" />
  <component name="GradleSettings">
    <option name="linkedExternalProjectsSettings">
      <GradleProjectSettings>
        <option name="externalProjectPath" value="$PROJECT_DIR$" />
        <!-- 移除本地 gradleHome 设置，依赖 Gradle Wrapper -->
        <option name="modules">
          <set>
            <option value="$PROJECT_DIR$" />
          </set>
        </option>
      </GradleProjectSettings>
    </option>
  </component>
</project>
```

通过这种方式，可以确保项目使用 Gradle Wrapper 来管理 Gradle 版本，保持构建环境的一致性和可靠性。但由于`gradle.xml`中可能存在某些个人偏好的配置，因此该文件可根据团队管理需要决定是否纳入版本控制。如果决定忽略 `gradle.xml` 文件，可以在 `.gitignore` 文件中添加以下配置：

```gitignore
# Ignore IntelliJ IDEA Gradle configuration
.idea/gradle.xml
```

### jarRepositories.xml 文件（本地文件，仓库里没有）

`jarRepositories.xml` 是 IntelliJ IDEA 项目中用于定义项目使用的 JAR 文件库（repository）配置的文件。它帮助 IntelliJ IDEA 识别项目中使用的 JAR 文件库的位置和相关设置。这在使用 IntelliJ IDEA 进行依赖管理时特别有用，

我本地文件内容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="RemoteRepositoriesConfiguration">
    <remote-repository>
      <option name="id" value="central" />
      <option name="name" value="Maven Central repository" />
      <option name="url" value="https://repo1.maven.org/maven2" />
    </remote-repository>
    <remote-repository>
      <option name="id" value="jboss.community" />
      <option name="name" value="JBoss Community repository" />
      <option name="url" value="https://repository.jboss.org/nexus/content/repositories/public/" />
    </remote-repository>
    <remote-repository>
      <option name="id" value="MavenRepo" />
      <option name="name" value="MavenRepo" />
      <option name="url" value="https://repo.maven.apache.org/maven2/" />
    </remote-repository>
  </component>
</project>
```

主要是配置的跟中Maven中心库的地址，在大多数使用 Gradle 或 Maven 进行依赖管理的项目中，`jarRepositories.xml` 文件并不是必需的，因为这些构建工具已经有效地管理了依赖和仓库配置。因此我决定在本地也删除该文件，以保持项目纯净和验证理解。

至此，项目中所有配置文件我已经都梳理过一遍了，至少做到在当前阶段对我的项目中的每个文件的作用都清晰明了，希望你也可以跟上。后续我们将进入一些代码实战和研究，希望大家可以共同进步。