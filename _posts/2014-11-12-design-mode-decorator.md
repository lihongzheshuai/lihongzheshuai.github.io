---
layout: post
title: 乱学设计模式——装饰模式
date: 2014-11-12 18:25
author: onecoder
comments: true
tags: [decorator, Java, 装饰模式, 设计模式]
thread_key: 1854
---
码农写码3，4年，设计模式用了不少，但又有一种在乱用的感觉。要么叫不出名字，要么感觉摸不到其精髓。其实所谓Java中的23种设计模式，OneCoder之前也乱乱的看过几遍，但是至今感觉也没有什么深刻的领悟。

之前，看到每种设计模式总会有一种“理所应当”的感觉，心里就好像在说本来就应该这么做啊，我也是这么写的啊。但是后头回头品味，总感觉缺少更认真的思考，应用的很不自如。得进步。

这次整理，其实也是“乱”学。乱在没有考虑具体的计划，没有想要一口气把设计模式从头再学一遍。但是，这次我是想带着问题，带着思考的去学习一个设计模式。我给自己定的效果就是，我这次思考过的设计模式，我就要真正的理解他，从而能够活用。

因此，也许你已经不会奇怪为什么今天会突兀的出来一个装饰器模式。因为，这就是今天我遇到的问题，也是促使我好好思考一下的原因。

先理解一下设计模式的六大原则，之前看到一个人介绍的阿里面试题中也有这个问题：
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
理解起来都不难。不过需要在设计的时候勤反思，加深理解。

先说说这次遇到的问题吧，在网上看到一篇文章：Proxy遇上Decorator 。即介绍代理和装饰器这两种模式的。习惯性的自己先思考一下其中的区别和联系。发现脑子里好像满满一坨shit一般，这也促使OneCoder决定每再遇到一个设计模式，就认真的思考一番。设想下应用场景，写写代码应用一般，比较一下没有应用设计模式的情况下会是如何。

引用一段理论文字：
<blockquote>装饰(Decorator)装饰模式是一种结构型模式，它主要是解决：“过度地使用了继承来扩展对象的功能”，由于继承为类型引入的静态特质，使得这种扩展方式缺乏灵活性；并且随着子类的增多（扩展功能的增多），各种子类的组合（扩展功能的组合）会导致更多子类的膨胀（多继承）。继承为类型引入的静态特质的意思是说以继承的方式使某一类型要获得功能是在编译时。所谓静态，是指在编译时；动态，是指在运行时。
GoF《设计模式》中说道：动态的给一个对象添加一些额外的职责。就增加功能而言，Decorator模式比生成子类更为灵活。</blockquote>
由此也可以看出，装饰模式正是遵守的设计模式6大原则中合成复用原则，当然任何设计模式都是为了开闭原则服务的。

为了加深自己的理解，先手动画一幅图：

<img class="aligncenter" src="/images/oldposts/decorator-uml.png" alt="" width="644" height="258" />
其中ReviewChineseDecorator和ReviewEnglishDecorator就是两个装饰器。装饰的是ReviewImpl。这里设想的是这样的场景，一个人想要进行复习(ReviewImpl.doReview())，本来只有一些特定内容要复习。结果，后来又增加的中文和英文的复习任务。这个时候，如果不应用设计模式，那么就要修改doReview的代码，增加英语和语文复习的内容。这自然范围了开闭原则。当然你也可以采用继承，增加子类，但是这又违反了合成复用原则。而且，那种在调用者一端构造一堆子类实例然后调用的方式，又显得不够优雅。于是，装饰模式来了。

装饰器与被装饰者实现同一个接口，并持有被装饰着实例，从而可以动态的为被装饰着添加功能。代码如下：

```java
/**
* Created by OneCoder on 2014/11/12.
*/
public class ReviewEnglishDecorator  implements Review {

    private Review reviewer;

    public ReviewEnglishDecorator(Review reviewer) {
        this.reviewer = reviewer ;
    }

    /**
     * 开始复习
     */
    @Override
    public void doReview() {
        System.out.println("Review English.") ;
        reviewer.doReview();
    }
}

/**
* Created by OneCoder on 2014/11/12.
*/
public class ReviewImpl implements Review {

    /**
     * 开始复习
     */
    @Override
    public void doReview() {
        System.out.println("Review Something.") ;
    }
}

/**
* Created by OneCoder on 2014/11/12.
*/
public class DecoratorMain {

    public static void main(String[] args) {
        Review review = new ReviewEnglishDecorator(new ReviewChineseDecorator(new ReviewImpl())) ;
        review.doReview() ;
    }

}
```
调用者的代码是不是看起来特别的熟悉，我们在使用Java中的各种流的时候，经常遇到这种代码：
```java
InputStream input = new DataInputStream(new BufferedInputStream(new FileInputStream("C:/test.exe")));
```
这就是典型的装饰模式。

其实网上关于各种设计模式的介绍导出都是，有很多其实讲的都很清楚。这里OneCoder只是为了自己能加深印象，深入理解，自己讲给自己听的而已。

《大话设计模式》这本中中对于设计模式的讲解，可谓更加的清晰，也是采用我最喜欢的对比的方式，即没有设计模式会怎样，有了又会带来什么好处。这对于理解设计模式来说，是再好不过的了。
