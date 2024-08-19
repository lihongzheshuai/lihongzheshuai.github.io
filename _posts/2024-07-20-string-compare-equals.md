---
layout: post
title: 字节码分析-Java中String用==判断值相等一定是错的么
date: 2024-07-20 22:57 +0800
author: onecoder
comments: true
tags: [Java,String]
categories: [Java技术研究,JDK]
---
经常听到有同学讨论，在Java中String判断值相等应该用equals()而不能用==，并且分析的信誓旦旦。那么真相真的是这样么？==就完全不能用么？Java内部的原理究竟是如何呢？这需要理解它们背后的原理。下面是详细的原理分析：
<!--more-->
# 一、Java中运算符含义 
## Java中== 运算符的含义
- 在 Java 中，== 操作符用于比较两个对象的引用，换句话说，它判断的是两个对象是否指向同一个内存地址。
- 如果 == 用于比较两个字符串，它实际上是比较这两个字符串对象是否是同一个对象。

## Java中equals含义
在Java中，equals方法用于比较两个对象是否“相等”。默认情况下，equals方法由Object类提供，并且它比较的是对象的引用，即两个对象的内存地址是否相同。因此，除非被覆盖，equals方法的默认行为是检查两个对象是否是同一个实例。

# 二、Java中String对象的处理
## 用 == 比较字符串值是否相等
### 情况一：直接赋值

```java
String str1 = "Hello";
String str2 = "Hello";
System.out.println(str1 == str2); // true
```

在这个例子中，str1 和 str2 是相同的字符串字面量，Java 编译器会把它们优化到字符串池中，因此它们指向同一个内存地址，所以 == 返回 true。
为了印证这个结论，我们查看编译后的字节码如下：
```java
package com.coderli.jdk.basic;

public class StringEqualMain {

    public static void main(String[] args) {
        String str1 = "Hello";
        String str2 = "Hello";
        System.out.println(str1 == str2);
    }
}
```
编译这段代码后，你可以使用javap命令来查看生成的字节码：
```plaintext
javap -c StringEqualMain
```
输出的字节码如下：
```plaintext
public class com.coderli.jdk.basic.StringEqualMain {
  public com.coderli.jdk.basic.StringEqualMain();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: ldc           #7                  // String Hello
       2: astore_1
       3: ldc           #7                  // String Hello
       5: astore_2
       6: getstatic     #9                  // Field java/lang/System.out:Ljava/io/PrintStream;
       9: aload_1
      10: aload_2
      11: if_acmpne     18
      14: iconst_1
      15: goto          19
      18: iconst_0
      19: invokevirtual #15                 // Method java/io/PrintStream.println:(Z)V
      22: return
}
```
让我们逐行解释这些字节码：
1. 方法初始化：
    ```plaintext
    0: aload_0
    1: invokespecial #1                  // Method java/lang/Object."<init>":()V
    4: return
    ```

1. main方法：
    ```plaintext
    0: ldc           #7                  // String Hello
    2: astore_1
    3: ldc           #7                  // String Hello
    5: astore_2
    ```
    - ldc #7：将常量池中的字符串"Hello"加载到栈顶。常量池中的#7对应的是字符串"Hello"。
    - astore_1：将栈顶的引用（字符串"Hello"）存储到局部变量表的索引1（即str1）。
    - ldc #7：再次将常量池中的字符串"Hello"加载到栈顶。
    - astore_2：将栈顶的引用（字符串"Hello"）存储到局部变量表的索引2（即str2）。
  
2. 比较与输出：
    ```plaintext
    6: getstatic     #9                  // Field java/lang/System.out:Ljava/io/PrintStream;
    9: aload_1
    10: aload_2
    11: if_acmpne     18
    14: iconst_1
    15: goto          19
    18: iconst_0
    19: invokevirtual #15                 // Method java/io/PrintStream.println:(Z)V
    22: return
    ```
    - getstatic #9：获取System.out的静态字段引用，压入栈顶。
    - aload_1：将局部变量表索引1的引用（str1）压入栈顶。
    - aload_2：将局部变量表索引2的引用（str2）压入栈顶。
    - if_acmpne 18：比较栈顶的两个引用。如果它们不相同，则跳转到指令18。
    - iconst_1：将常量1压入栈顶（表示str1 == str2为true）。
    - goto 19：跳转到指令19。
    - 18: iconst_0：将常量0压入栈顶（如果str1 != str2）。
    - 19: invokevirtual #15：调用PrintStream.println(boolean)方法，打印栈顶的布尔值。
    - 22: return：从main方法返回。
  
在这种情况下，由于str1和str2指向的是字符串池中的同一个字符串字面量，因此str1 == str2为true，iconst_1被压入栈顶并被打印出来。

### 情况二：new新对象
```java
String str1 = new String("Hello");
String str2 = new String("Hello");
System.out.println(str1 == str2); // false
```
这里，虽然 str1 和 str2 的内容相同，但它们是通过 new 关键字创建的两个不同对象，因此 == 比较时会返回 false。
同样，我们通过字节码来印证我们的想法：
以下是完整的Java代码：

```java
public class Test {
    public static void main(String[] args) {
        String str1 = new String("Hello");
        String str2 = new String("Hello");
        System.out.println(str1 == str2); // false
    }
}
```

将其编译后，使用javap -c Test命令查看字节码：
```plaintext
Compiled from "Test.java"
public class Test {
  public Test();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: new           #2                  // class java/lang/String
       3: dup
       4: ldc           #3                  // String Hello
       6: invokespecial #4                  // Method java/lang/String."<init>":(Ljava/lang/String;)V
       9: astore_1
      10: new           #2                  // class java/lang/String
      13: dup
      14: ldc           #3                  // String Hello
      16: invokespecial #4                  // Method java/lang/String."<init>":(Ljava/lang/String;)V
      19: astore_2
      20: getstatic     #5                  // Field java/lang/System.out:Ljava/io/PrintStream;
      23: aload_1
      24: aload_2
      25: if_acmpeq     32
      28: iconst_0
      29: goto          33
      32: iconst_1
      33: invokevirtual #6                  // Method java/io/PrintStream.println:(Z)V
      36: return
}

```
我们逐行解释这些字节码：
1. 类的构造方法：
    ```plaintext
    0: aload_0
    1: invokespecial #1                  // Method java/lang/Object."<init>":()V
    4: return
    ```

2. main方法：
    ```plaintext
    0: new           #2                  // class java/lang/String
    3: dup
    4: ldc           #3                  // String Hello
    6: invokespecial #4                  // Method java/lang/String."<init>":(Ljava/lang/String;)V
    9: astore_1
    ```
    - new #2：创建一个新的String对象。
    - dup：复制栈顶的引用，这样构造方法调用时对象仍在栈顶。
    - ldc #3：将常量池中的字符串"Hello"加载到栈顶。常量池中的#3对应的是字符串"Hello"。
    - invokespecial #4：调用String的构造方法，使用常量池中的字符串"Hello"初始化新创建的String对象。
    - astore_1：将栈顶的引用（新创建的String对象）存储到局部变量表的索引1（即str1）。
  
3. 第二个字符串对象的创建：
    ```plaintext
    10: new           #2                  // class java/lang/String
    13: dup
    14: ldc           #3                  // String Hello
    16: invokespecial #4                  // Method java/lang/String."<init>":(Ljava/lang/String;)V
    19: astore_2
    ```
    - 这段代码与创建第一个字符串对象的代码相同，只是最终将新创建的String对象存储到局部变量表的索引2（即str2）。
  
4. 比较与输出：
    ```plaintext
    20: getstatic     #5                  // Field java/lang/System.out:Ljava/io/PrintStream;
    23: aload_1
    24: aload_2
    25: if_acmpeq     32
    28: iconst_0
    29: goto          33
    32: iconst_1
    33: invokevirtual #6                  // Method java/io/PrintStream.println:(Z)V
    36: return
    ```
    - getstatic #5：获取System.out的静态字段引用，压入栈顶。
    - aload_1：将局部变量表索引1的引用（str1）压入栈顶。
    - aload_2：将局部变量表索引2的引用（str2）压入栈顶。
    - if_acmpeq 32：比较栈顶的两个引用。如果它们相同，则跳转到指令32。
    - 28: iconst_0：将常量0压入栈顶（表示str1 != str2）。
    - goto 33：跳转到指令33。
    - 32: iconst_1：将常量1压入栈顶（如果str1 == str2）。
    - 33: invokevirtual #6：调用PrintStream.println(boolean)方法，打印栈顶的布尔值。
    - 36: return：从main方法返回。

在这种情况下，由于str1和str2是通过new String("Hello")创建的不同对象，因此str1 == str2为false，iconst_0被压入栈顶并被打印出来。

### 核心差异解析
1. 字符串对象的创建方式：
    - 直接赋值方式：
        - 使用ldc指令将字符串字面量"Hello"加载到栈顶。这种方式使用了字符串池（String Pool），相同的字符串字面量只会在字符串池中存储一份。
        - ldc #2 加载的都是同一个字符串池中的引用，因此str1 == str2比较时结果为true。
    - new 关键字创建新对象：
        - 使用new指令创建新的String对象，然后使用invokespecial指令调用构造方法初始化该对象。
        - 每次创建新的String对象都会分配不同的内存地址，因此即使内容相同，str1 == str2比较时结果也为false。

2. 字节码指令的差异：
    - 直接赋值方式：
        - ldc #2：加载常量池中的字符串"Hello"到栈顶。
        - astore_1 和 astore_2：将栈顶的引用分别存储到局部变量表的索引1和索引2。
    - new 关键字创建新对象：
        - new #2：创建新的String对象。
        - dup：复制栈顶的引用，保持构造方法调用时对象仍在栈顶。
        - ldc #3：加载常量池中的字符串"Hello"到栈顶。
        - invokespecial #4：调用String构造方法，使用加载的字符串字面量初始化新创建的String对象。
        - astore_1 和 astore_2：将新创建的String对象的引用分别存储到局部变量表的索引1和索引2。

3. 引用比较：
    - 两种方式都使用了if_acmpne指令进行引用比较，但由于对象的创建方式不同，比较结果不同：
        - 直接赋值方式：引用相同，比较结果为true。
        - new 关键字创建新对象：引用不同，比较结果为false。

通过这些差异，我们可以看到，直接赋值使用字符串池来优化内存，而使用new关键字则总是创建新的对象，即使内容相同。

## 使用 equals() 方法判断字符串是否相等
在Java中equals() 方法在 String 类中被重写，用于比较两个字符串对象的内容是否相同。无论两个字符串对象是否是同一个对象，只要它们的内容相同，equals() 方法都会返回 true。
其源码实现如下：
```java
public boolean equals(Object anObject) {
    // 如果指定对象和当前对象的内存地址相等，则说明在内存中是同一个对象，直接返回 true
    if (this == anObject) {
        return true;
    }
    // 如果指定对象和当前对象的内存地址不相等 
    // 则判断指定对象是否是 String 类型
    if (anObject instanceof String) {
        String anotherString = (String) anObject;
        // 比较指定对象与当前对象的字符串长度，如果长度不一致，则直接返回 false
        int n = value.length;
        if (n == anotherString.value.length) {
            // 获取当前字符串对象的字符数组
            char v1[] = value; 
            // 获取指定字符串对象的字符数组
            char v2[] = anotherString.value; 
            int i = 0;
            // 遍历这两个字符串对象中的每一个字符
            while (n--!= 0) { 
                // 如果遍历过程中有一个字符不一致，则直接返回 false
                if (v1[i]!= v2[i]) 
                    return false;
                i++;
            }
            // 如果遍历结束，每个字符都一致，则返回 true
            return true;
        }
    }
    return false;
}
```

总体步骤为：
1. 首先判断指定对象和当前对象的内存地址是否相等，如果相等则直接返回`true`，因为这意味着它们在内存中是同一个对象。
2. 若内存地址不相等，则判断指定对象是否为`String`类型。如果不是，则直接返回`false`。
3. 若是`String`类型，则先将该对象强转为`String`类型。然后比较两个字符串的长度，如果长度不一致，直接返回`false`。
4. 若长度一致，则通过循环遍历这两个字符串对象中的每一个字符。如果遍历过程中有一个字符不一致，直接返回`false`。
5. 若遍历结束，每个字符都一致，则返回`true`。

在字符比较时，直接使用`==`操作符即可，因为 Java 中的字符采用 Unicode 编码，而 Unicode 字符集中的前 128 个字符与 ASCII 字符集兼容，所以在 Java 中，`char`类型的数据运算和比较对应着一张 ASCII 码表，两个`char`类型的数据直接用`==`比较其内容是否相等。
例如：
```java
String str1 = new String("Hello");
String str2 = new String("Hello");
System.out.println(str1.equals(str2)); // true
```
在这个例子中，虽然 str1 和 str2 是不同的对象，但它们的内容相同，所以 equals() 返回 true。

# 三、补充说明：字符串池（String Pool）机制
前面在分析==比较的时候，提到了字符串池的概念，Java中的字符串常量池（String Pool）是一个专门用来存储字符串字面量的内存区域。这些字符串字面量在编译时就确定，并且在运行时驻留在字符串常量池中。
- 当你创建一个字符串字面量时，如果该字符串已经存在于字符串池中，Java 会直接返回池中的引用，而不是重新创建一个新的对象。
- 使用 new 关键字创建的字符串不会被放入字符串池中，而是在堆上创建一个新的对象。

常量池的范围和行为有一些重要的特点和规则：
### 字符串常量池的特点
1. 字符串字面量：
    - 任何用双引号括起来的字符串字面量（如"Hello"）都会自动放入字符串常量池中。
    - 如果在代码中多次使用相同的字符串字面量，这些字面量会引用字符串常量池中的同一个实例。
2. 字符串的intern()方法：
    - 调用字符串的intern()方法会将该字符串加入常量池（如果尚未在常量池中），并返回常量池中的字符串引用。
    - 例如：
        ```java
        String str1 = new String("Hello");
        String str2 = str1.intern();
        String str3 = "Hello";
        System.out.println(str2 == str3); // true
        ```
    - 在上述代码中，str2 和 str3 都引用常量池中的同一个字符串。

3. 编译时常量：
    - 编译时常量表达式的结果也会驻留在常量池中，例如：
        ```java
        String str1 = "Hel" + "lo"; // 编译时优化为 "Hello"
        String str2 = "Hello";
        System.out.println(str1 == str2); // true
        ```

1. 动态创建的字符串：
    - 通过new关键字创建的字符串不会自动进入常量池，例如：
        ```java
        String str1 = new String("Hello");
        String str2 = "Hello";
        System.out.println(str1 == str2); // false
        ```
    - 这段代码中，str1引用的是堆中创建的新字符串对象，而str2引用的是常量池中的字符串。

### 字符串常量池的示例代码
以下是一些示例代码来说明字符串常量池的行为：
```java
public class StringPoolExample {
    public static void main(String[] args) {
        // 直接使用字符串字面量
        String str1 = "Hello";
        String str2 = "Hello";
        System.out.println(str1 == str2); // true

        // 使用new关键字创建字符串
        String str3 = new String("Hello");
        String str4 = new String("Hello");
        System.out.println(str3 == str4); // false
        System.out.println(str1 == str3); // false

        // 使用intern()方法
        String str5 = str3.intern();
        System.out.println(str1 == str5); // true

        // 编译时常量
        String str6 = "Hel" + "lo";
        System.out.println(str1 == str6); // true

        // 动态创建的字符串
        String part1 = "Hel";
        String part2 = "lo";
        String str7 = part1 + part2;
        System.out.println(str1 == str7); // false
        System.out.println(str1 == str7.intern()); // true
    }
}
```
### 关键点总结
- 字符串字面量：直接使用双引号括起来的字符串字面量会自动驻留在字符串常量池中。
- intern()方法：可以手动将字符串放入常量池，并返回常量池中的字符串引用。
- 编译时常量表达式：在编译时能够确定结果的字符串表达式也会驻留在常量池中。
- new关键字创建的字符串：通过new关键字创建的字符串不会自动进入常量池，而是创建新的字符串对象。

字符串常量池的使用可以减少内存的重复分配，提高内存使用效率，但需要注意其行为和使用场景，以避免不必要的内存浪费和错误判断。
# 四、总结
- 使用 ==：
    - 适用于需要判断两个引用是否指向同一个对象的情况。
    - 例如，在某些性能优化的场景下，利用字符串池可以通过 == 判断一些常量字符串的相等性。
- 使用 equals()：
    - 适用于需要判断两个字符串内容是否相等的情况。
    - 一般情况下，对于字符串内容比较，应优先使用 equals() 方法。
