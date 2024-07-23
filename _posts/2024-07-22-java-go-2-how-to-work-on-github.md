---
layout: post
title: 一起学Java(2)-如何利用Github进行项目代码fork和协作同步
date: 2024-07-22 22:07 +0800
author: onecoder
comments: true
tags: [java,git,一起学Java]
---
在第一步中（[一起学Java(1)-新建一个Gradle管理的Java项目](https://www.coderli.com/java-go-1-new-gradle-project/)）我们已经完成了项目的创建并托管到了Github上。现在自然要首先解决同学们如何下载代码和进行代码同步更新和联系的问题。这就涉及到Git的fork理念和协作模式的问题。具体介绍如下。
<!--more-->

### Fork的理念

Fork是GitHub上的一个重要功能，主要用于：

- **创建代码仓库的副本**：当你fork一个仓库时，你在自己的GitHub账户下创建了该仓库的完整副本，包括所有的历史记录和分支。
- **独立开发环境**：Fork出来的仓库完全独立于原始仓库（upstream），你可以自由地在自己的仓库中进行开发和实验，而不会影响原始仓库。
- **贡献代码**：Fork是GitHub协作模式的基础，通过fork和pull request的机制，开发者可以在不直接修改原始仓库的情况下，贡献代码和改进。

### 本项目操作步骤

以本项目为例，同学们可通过如下操作下载、更新代码并可在自己的仓库上进行练习和代码更新，这也是Git上开源项目的标准操作模式：

#### 1. Fork仓库

首先，同学需要注册Github账号，登陆后打开本项目地址页，通过Fork按钮，进行仓库fork，这会在开发者自己的GitHub账户下创建一个副本。
![fork](/images/post/java-go-2-work-on-github/fork.png)

#### 2. 克隆fork后的仓库

在本地克隆fork后的仓库进行开发。(即你个人账号下fork后的仓库代码地址)

```bash
git clone https://github.com/your-username/xxxxx(你fork后的仓库地址).git
```

显然，在学习中，我原始仓库会不断更新。如果你希望将原始仓库的最新更改合并到你的fork仓库中，可以按照以下步骤进行代码更新：

#### 3. 添加原始仓库为远程仓库

在你的本地仓库中添加原始仓库的远程地址（通常称为`upstream`）。

```bash
git remote add upstream https://github.com/lihongzheshuai/java-all-in-one.git
```

#### 4. 从原始仓库获取最新更新

获取原始仓库的更新，这不会直接合并这些更新，只是下载到你的本地仓库。

```bash
git fetch upstream
```

#### 5. 合并更新到本地主分支

切换到你的本地主分支（通常是`main`或`master`，这里以main为例），并将从原始仓库获取的更新合并到你的分支中。

```bash
git checkout main
git merge upstream/main
```

#### 6. 推送更新到你的远程仓库

可将本地合并后的更改推送到你自己的GitHub fork仓库中。如果你在本地进行验证修改，也可以commit后一起push到你的远端分支。当然为了保证主干代码的顺利演进，自然建议你在新建的分支上进行个人的代码修改和验证操作。（具体Git命令和操作这里先不展开）

```bash
git push origin main
```


### 注意事项

- 确保在进行更新前，已经提交或暂存了当前的工作，以免丢失未保存的更改。
- 合并过程中，如果有冲突，需耐心解决并测试代码确保功能正常。
- 推送到远程仓库后，可以在GitHub上查看合并后的代码是否正确显示。

通过以上步骤，你就可以确保你的fork仓库始终与原始仓库保持最新状态。


#### 7. 创建Pull Request

如果你希望将你的代码合并（贡献）到我的仓库里，你可以在GitHub上创建一个Pull Request，请求将你fork仓库中的分支合并到原始仓库的主分支中。

```plaintext
fork仓库 (feature-branch) -> 原始仓库 (main)
```

#### 8. 代码审查和合并

原始仓库的维护者（我）会对Pull Request进行审查，提出修改建议或直接合并。

### 总结

总之，Git的fork和协作模式通过分布式版本控制和pull request机制，使得开发者可以独立开发、并行工作，且不影响主仓库的稳定性。这种模式极大地促进了开源项目的协作和贡献。一起学Java的项目也建议大家熟悉和体验这种协作模式，增加一项技能。