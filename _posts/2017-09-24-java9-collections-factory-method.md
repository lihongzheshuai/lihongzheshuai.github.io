---
layout: post
title: Java9 Collections工厂函数特性说明
tags: [Java9]
date: 2017-09-24 23:25:57 +0800
comments: true
author: onecoder
thread_key: 1911
---
刚发布的Java9中，有一个特性是新增了快速构造不可变集合的工厂函数。官方说明如下：

>
JEP 269: Convenience Factory Methods for Collections
>
Makes it easier to create instances of collections and maps with small numbers of elements. New static factory methods on the List, Set, and Map interfaces make it simpler to create immutable instances of those collections.
>
For example:
Set<String> alphabet = Set.of("a", "b", "c");
>
See Creating Immutable Lists, Sets, and Maps in Java Platform, Standard Edition Java Core Libraries Developer's Guide. For API documentation, see Immutable Set Static Factory Methods, Immutable Map Static Factory Methods, and Immutable List Static Factory Methods.


实际就是在Set、List、Map接口中增加了静态的of函数，快速构造不可变集合。使用样例如下：

```java
Set a = Set.of(1, 2, 3);
List b = List.of(1, 1, 2);
Map c = Map.of(1, 1, 2, 2, 3, 3);
System.out.println(a);
System.out.println(b);
System.out.println(c);
```

需要注意的是，Set.of的入参不能重复，否则会报错。并且由此函数构造出来的集合是不可变集合，后续再调用add或者remove方法，都会报错。相关源码如下：

```java
static <E> Set<E> of(E e1, E e2, E e3) {
    return new ImmutableCollections.SetN<>(e1, e2, e3);
}
```

所有对集合的操作都会抛出异常：

```java
abstract static class AbstractImmutableSet<E> extends AbstractSet<E> implements Serializable {
    @Override public boolean add(E e) { throw uoe(); }
    @Override public boolean addAll(Collection<? extends E> c) { throw uoe(); }
    @Override public void    clear() { throw uoe(); }
    @Override public boolean remove(Object o) { throw uoe(); }
    @Override public boolean removeAll(Collection<?> c) { throw uoe(); }
    @Override public boolean removeIf(Predicate<? super E> filter) { throw uoe(); }
    @Override public boolean retainAll(Collection<?> c) { throw uoe(); }
}
```

除此之外，一个有趣的现象时，每个of函数都重载了12次。分别是入参个数从0-10个。以及一个可变长度参数的函数。

```java
static <E> Set<E> of()
...
static <E> Set<E> of(E e1, E e2, E e3, E e4, E e5, E e6, E e7, E e8, E e9, E e10) 
static <E> Set<E> of(E... elements) 
```

这么设计主要出于性能的考虑。大家都知道Java里，可变长度的参数本质是个数组，对数组参数的调用，需要给数组分配内存空间和初始化，效率低于固定参数。

很多文章中都有关于可变长度参数的讨论，如：

[http://jtechies.blogspot.tw/2012/07/item-42-use-varargs-judiciously.html](http://jtechies.blogspot.tw/2012/07/item-42-use-varargs-judiciously.html)

>
Exercise care when using the varargs facility in performance-critical situations. Every invocation of a varargs method causes an array allocation and initialization. If you have determined empirically that you can’t afford this cost but you need the flexibility of varargs, there is a pattern that lets you have your cake and eat it too. Suppose you’ve determined that 95 percent of the calls to a method have three or fewer parameters. Then declare five overloadings of the method, one each with zero through three ordinary parameters, and a single varargs method for use when the number of arguments exceeds three。

我也做了相关测试如下：

```java
public static void main(String[] args) {
        long start = System.currentTimeMillis();
        for (int i = 0; i < 10000000; i++) {
            appendStr("a", "b");
        }
        long end = System.currentTimeMillis();
        System.out.println("Fixed cost time: " + (end - start));
        long vStart = System.currentTimeMillis();
        for (int i = 0; i < 10000000; i++) {
            appendStrVargs("a", "b");
        }
        long vend = System.currentTimeMillis();
        System.out.println("Vargs cost time: " + (vend - vStart));
    }

    
    private static List<String> appendStr(String a, String b) {
        return ofString(a, b);
    }
    
    private static List<String> appendStrVargs(String... args) {
        return ofString(args);
    }
    
    private static List<String> ofString(String... strs) {
        List<String> result = new ArrayList();
        for (String s : strs) {
            result.add(s);
        }
        return result;
    }
```

测试结果如下：

```
Fixed cost time: 333  
Vargs cost time: 720
```

由此可见，如此设计，自有Java的道理。