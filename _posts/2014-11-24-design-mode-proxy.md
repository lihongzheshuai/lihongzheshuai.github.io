---
layout: post
title: 乱学设计模式——代理模式
date: 2014-11-24 18:33
author: onecoder
comments: true
tags: [Java, 设计模式]
categories: [设计模式]
thread_key: 1862
---
在乱学装饰模式的时候给出了一篇参考文章，是对比装饰模式和代理模式的。自然，这就是OneCoder现在需要理解的问题。
先复习一下设计模式6大原则：

设计模式的六大原则（引自：http://zz563143188.iteye.com/blog/1847029）
<blockquote>
1.	开闭原则（Open Close Principle）
开闭原则就是说对扩展开放，对修改关闭。在程序需要进行拓展的时候，不能去修改原有的代码，实现一个热插拔的效果。所以一句话概括就是：为了使程序的扩展性好，易于维护和升级。想要达到这样的效果，我们需要使用接口和抽象类，后面的具体设计中我们会提到这点。
<br>
2.	里氏代换原则（Liskov Substitution Principle）
里氏代换原则(Liskov Substitution Principle LSP)面向对象设计的基本原则之一。 里氏代换原则中说，任何基类可以出现的地方，子类一定可以出现。 LSP是继承复用的基石，只有当衍生类可以替换掉基类，软件单位的功能不受到影响时，基类才能真正被复用，而衍生类也能够在基类的基础上增加新的行为。里氏代换原则是对“开-闭”原则的补充。实现“开-闭”原则的关键步骤就是抽象化。而基类与子类的继承关系就是抽象化的具体实现，所以里氏代换原则是对实现抽象化的具体步骤的规范。—— From Baidu 百科
<br>
3.	依赖倒转原则（Dependence Inversion Principle）
这个是开闭原则的基础，具体内容：真对接口编程，依赖于抽象而不依赖于具体。
<br>
4.	接口隔离原则（Interface Segregation Principle）
这个原则的意思是：使用多个隔离的接口，比使用单个接口要好。还是一个降低类之间的耦合度的意思，从这儿我们看出，其实设计模式就是一个软件的设计思想，从大型软件架构出发，为了升级和维护方便。所以上文中多次出现：降低依赖，降低耦合。
<br>
5.	迪米特法则（最少知道原则）（Demeter Principle）
为什么叫最少知道原则，就是说：一个实体应当尽量少的与其他实体之间发生相互作用，使得系统功能模块相对独立。
<br>
6.	合成复用原则（Composite Reuse Principle）
原则是尽量使用合成/聚合的方式，而不是使用继承。
</blockquote>

代理模式：为其他对象提供一种代理以控制对这个对象的访问。


还是来个图表示一下：

<img class="aligncenter" src="/images/oldposts/proxy-uml.png" alt="" width="384" height="206" />

这里设想了一个简单的卖房子的场景。在没有代理的情况下，房子的拥有者想要卖房子，需要自己发布信息，带买家看房，办理交接手续等事情。这时候房主发现这样太麻烦了。于是他请来了代理HouseProxy，代理负责除必须房主参加的办理手续之外的所有事情。
这正是代理模式应用场景中的：智能指引，指当调用真实的对象时，代理处理另外的一些事情。

对比装饰模式，感觉非常相近，所以才会有之前一直提到的文章。代理模式感觉是一个代理处理了所有其他的事情，装饰模式是需要一系列各种各种的“能人”，各取所长。

实现代码很简单了：
{% highlight java %}
/**
* Created by OneCoder on 2014/11/24.
*/
public class HouseOwner implements ISellHouse {

    @Override
    public void sellHouse() {
        System.out.println("Sell my house.") ;
    }
}

/**
* Created by OneCoder on 2014/11/24.
*/
public class HouseProxy implements ISellHouse {

    private ISellHouse seller;

    public HouseProxy(ISellHouse seller) {
        this.seller = seller ;
    }

    @Override
    public void sellHouse() {
        System.out.println("Proxy: Publish the information.");
        System. out.println("Proxy: Contact the buyer.");
        seller.sellHouse();
        System. out.println("Proxy: Get commision.");
    }
}
{% endhighlight %}
似乎没什么可说的，OneCoder自我感觉是可以区分和使用这两种设计模式了，目的达到了。

PS:
<strong>1、最近博客更新的比较慢，家里的事情比较多，不过学习是一定要坚持的，哪怕是龟兔赛跑，我也在前进。</strong>
<strong>2、博客最近流量超标(15G/月)，原因是遭到来自IP：114.215.138.184（爱论文网？）的不间断爬取。精力有限，经济有限(已经又充了流量。)，所以，OneCoder准备慢慢把博客完全搬家到github.io上，这个过程也许很漫长。。。</strong>

爬虫可以。。。没完没了的爬。。就不必了吧。。。。
