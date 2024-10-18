---
layout: post
title: 一起学Java(15)-[JDK篇]教你了解Java8特性，Lambda表达式学习
date: 2024-10-16 22:00 +0800
author: onecoder
comments: true
tags: [Java, JDK, 一起学Java]
categories: [一起学Java系列,（3）JDK篇]
---
在文章[***《2024年主流使用的JDK版本及其核心特性介绍》***](https://www.coderli.com/feature-of-popular-jdk-version/)中，我们详细介绍了Java8、Java11、Java17等主流Java版本主要新增特性。针对其中的一些核心特性，展开研究一二。

<!--more-->

## Lambda 表达式 (JEP 126) 详细介绍

Lambda 表达式是 Java 8 引入的一个重要新特性，它允许将函数作为参数传递，并简化了代码的表达方式。Lambda 表达式通常用于表达行为，而不需要定义完整的类或匿名内部类。Lambda 表达式最常见的用法是在集合和流（Stream）API中进行数据操作（[*Stream API (JEP 107) 流 API*](https://www.coderli.com/feature-of-popular-jdk-version/#4-jdk-8)）。

### 1. **Lambda 表达式的设计定位**

Lambda 表达式的设计目的是简化函数式编程风格的实现，特别是针对**单方法接口**（即只有一个抽象方法的接口，通常被称为**函数式接口**）。在引入Lambda表达式之前，匿名内部类是处理回调或简短行为的常用手段，但它的语法冗长且复杂。

**设计目标：**

- **简化代码表达**：减少样板代码（boilerplate code）的编写，例如匿名内部类的定义。
- **提高代码可读性**：使代码更清晰、更简洁。
- **支持函数式编程**：允许将函数作为参数传递或返回，使得编程更加灵活。
  
**核心概念：**

- **函数式接口**：任何只包含一个抽象方法的接口都可以用 Lambda 表达式来实现。例如 `java.lang.Runnable`、`java.util.Comparator` 等。
- **行为参数化**：可以通过 Lambda 表达式传递行为（函数），避免传统通过类继承或接口实现来传递行为的方式。

### 2. **Lambda 表达式的语法和原理**

Lambda 表达式的语法形式如下：

```java
(parameters) -> expression
或者
(parameters) -> { statements }
```

#### 语法说明

- **参数列表**：Lambda 表达式的输入参数，可以有多个参数，如果只有一个参数，圆括号可以省略。
- **箭头符号（`->`）**：分隔参数和Lambda体。
- **Lambda体**：可以是一个表达式或者多个语句。如果是一个表达式，可以省略花括号和返回值。

### 3. **Lambda 表达式的用法**

#### (1) **函数式接口**

Lambda 表达式只能用于实现**函数式接口**。函数式接口是只有一个抽象方法的接口，可以通过 `@FunctionalInterface` 注解显式声明一个接口为函数式接口。

**示例：**

```java
package com.coderli.one.jdk8;

@FunctionalInterface
public interface LambdaInterfaceDemo {
    void doSomething();
}
```

在这个例子中，`MyFunctionalInterface` 是一个函数式接口，它只有一个抽象方法 `doSomething`，因此可以使用 Lambda 表达式来实现它。

#### (2) **Lambda 表达式示例**

1. **无参数，无返回值的 Lambda 表达式**

```java
Runnable r = () -> System.out.println("Running in a separate thread");
new Thread(r).start();
```

等同于：

```java
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Running in a separate thread");
    }
};
```

1. **带参数的 Lambda 表达式**

```java
MyFunctionalInterface f = (name) -> System.out.println("Hello, " + name);
f.doSomething("Alice");
```

等同于：

```java
MyFunctionalInterface f = new MyFunctionalInterface() {
    @Override
    public void doSomething(String name) {
        System.out.println("Hello, " + name);
    }
};
```

1. **带返回值的 Lambda 表达式**

```java
Comparator<Integer> comparator = (a, b) -> a.compareTo(b);
```

等同于：

```java
Comparator<Integer> comparator = new Comparator<Integer>() {
    @Override
    public int compare(Integer a, Integer b) {
        return a.compareTo(b);
    }
};
```

#### (3) **在集合中的应用**

Lambda 表达式和集合的组合通常通过 `Stream API` 来操作集合数据。这大大简化了对集合的过滤、映射和归约操作。

**示例：**

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

// 使用 Lambda 表达式过滤
List<String> filteredNames = names.stream()
    .filter(name -> name.startsWith("A"))
    .collect(Collectors.toList());

System.out.println(filteredNames);
```

输出：

```console
[Alice]
```

#### (4) **使用 `forEach` 简化遍历**

在没有 Lambda 表达式的情况下，我们通常使用 `for` 循环来遍历集合：

```java
for (String name : names) {
    System.out.println(name);
}
```

使用 Lambda 表达式，集合的遍历可以简化为：

```java
names.forEach(name -> System.out.println(name));
```

#### (5) **方法引用**

Lambda 表达式还支持**方法引用**，可以直接引用现有方法作为 Lambda 表达式的实现。

**示例：**

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");
names.forEach(System.out::println);
```

这段代码与 `names.forEach(name -> System.out.println(name));` 等效。

### 4. **Lambda 表达式的内部原理**

Lambda 表达式的原理基于**匿名类**的优化，但它并不直接生成匿名类对象，而是通过 Java 的**动态方法调用**技术实现，具有更高效的运行时性能。具体来说，Lambda 表达式通过 `invokedynamic` 字节码指令，在运行时动态生成目标方法的实现。

- **目标类型**：Lambda 表达式会推断其对应的函数式接口类型，称为目标类型。
- **捕获变量**：Lambda 表达式可以使用外部作用域中的变量，但这些变量必须是**最终的**（final）或者**有效最终的**（effectively final），即这些变量一旦赋值后不会再被修改。

### 总结

- **设计定位**：Lambda 表达式用于简化函数式接口的实现，减少样板代码，支持行为参数化。
- **原理**：通过动态方法调用，Lambda 表达式避免了传统匿名类的性能开销，并通过目标类型推断实现了灵活性。
- **用法**：常用于集合操作、事件处理等场景，通过简化的语法使代码更具可读性和可维护性。

---

所有代码已上传至：[***https://github.com/lihongzheshuai/java-all-in-one***](https://github.com/lihongzheshuai/java-all-in-one)
