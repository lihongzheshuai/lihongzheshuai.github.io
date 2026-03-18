---
layout: post
title: 【GESP】C++四级考试大纲知识点梳理, (4) 变量和作用域
date: 2025-06-13 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 四级]
---

GESP C++四级官方考试大纲中，共有11条考点，本文针对第4条考点进行分析介绍。

> （4）掌握变量作用域的概念，理解全局变量与局部变量的区别。
> {: .prompt-info}

**_四级其他考点回顾：_**

> - [【GESP】C++四级考试大纲知识点梳理, (1) 指针](https://www.coderli.com/gesp-4-exam-syllabus-pointer/)
> - [【GESP】C++四级考试大纲知识点梳理, (2) 结构体和二维数组](https://www.coderli.com/gesp-4-exam-syllabus-struct-two-dimensional-array/)
> - [【GESP】C++四级考试大纲知识点梳理, (3) 模块化和函数](https://www.coderli.com/gesp-4-exam-syllabus-module-function/)
>   {: .prompt-tip}

<!--more-->

---

## 一、变量是什么？

在 C++ 中，变量就像装数据的小盒子。

```cpp
int x = 5;
```

这表示我们创建了一个变量 `x`，并且把数字 `5` 放了进去。

## 二、什么是变量的“作用域”？

变量的**作用域（Scope）**就是——这个变量**在哪些地方可以用**。

打个比方：你在家可以穿拖鞋、吃零食，但是到了学校就不一定能做这些事了。家就是你“变量”的一个作用域，学校是另一个作用域。

在程序里也是一样，一个变量在某些“地方”可以用，在其他地方就不能用了。这些“地方”，就是作用域（Scope）。

## 三、全局变量 和 局部变量

### 3.1 全局变量（Global Variable）

- 定义在**函数外面**
- **所有函数都能使用**

🔍 示例：

```cpp
#include <iostream>
using namespace std;

int number = 10;  // 全局变量

void showNumber() {
    cout << "全局变量number的值是：" << number << endl;
}

int main() {
    showNumber();
    cout << "在main函数中也可以使用number：" << number << endl;
    return 0;
}
```

📌 说明：
`number` 是全局变量，定义在所有函数外面，`main()` 和 `showNumber()` 都可以用它。

---

### 3.2 局部变量（Local Variable）

局部变量是定义在函数、代码块或类成员函数中的变量，它们的作用域**只在当前作用域内有效**。根据不同的位置和行为，可以分为以下几类：

#### ✅ 1. 普通局部变量（Local Variable）

**📌 定义位置：**

在**函数或代码块**内部定义。

**📌 生命周期：**

函数执行时创建，函数执行完后就销毁。

**✅ 示例：**

```cpp
#include <iostream>
using namespace std;

void greet() {
    int age = 10;  // 普通局部变量
    cout << "我今年 " << age << " 岁。" << endl;
}

int main() {
    greet();
    // cout << age;  // ❌ 错误！age 在 main 函数里是无效的
    return 0;
}
```

**🧠 作用域：**

变量`age`只在 `greet()` 函数内部有效。

---

#### ✅ 2. 代码块局部变量（Block Scope Variable）

**📌 定义位置：**

在 `{}` 括起来的**代码块**中定义，比如 `if`、`while` 或 `for` 中。

**📌 生命周期：**

进入代码块时创建，离开代码块就销毁。

**✅ 示例：**

```cpp
#include <iostream>
using namespace std;

int main() {
    if (true) {
        int x = 42;  // 局部变量，仅在 if 代码块内有效
        cout << "x 的值是：" << x << endl;
    }
    // cout << x;  // ❌ 错误！x 只在 if 块里存在
    return 0;
}
```

---

#### ✅ 3. 函数参数（Function Parameter）

**📌 定义位置：**

函数的**参数列表中**，如 `int add(int a, int b)` 中的 `a` 和 `b`。

**📌 生命周期：**

函数被调用时创建，函数执行完后销毁。

**✅ 示例：**

```cpp
#include <iostream>
using namespace std;

int add(int a, int b) {  // a 和 b 是局部变量
    return a + b;
}

int main() {
    cout << add(3, 4) << endl;  // 输出 7
    return 0;
}
```

**💡 说明：**

函数参数也是局部变量，只在函数体内部有效。

---

#### ✅ 4. 静态局部变量（`static` Local Variable）

**📌 定义位置：**

函数或代码块中，但用 `static` 关键字修饰。

**📌 生命周期：**

**只创建一次，整个程序运行期间都存在**。但**作用域仍是局部的**，外部无法访问。

**✅ 示例：**

```cpp
#include <iostream>
using namespace std;

void counter() {
    static int count = 0;  // 静态局部变量
    count++;
    cout << "函数被调用了 " << count << " 次。" << endl;
}

int main() {
    counter();  // 第一次调用，输出1
    counter();  // 第二次调用，输出2
    counter();  // 第三次调用，输出3
    return 0;
}
```

#### 🔍 前序小结

| 特点               | 普通局部变量     | 静态局部变量       |
| ------------------ | ---------------- | ------------------ |
| 作用域             | 当前函数或代码块 | 当前函数或代码块   |
| 生命周期           | 每次调用重新创建 | 程序期间只创建一次 |
| 初始值只初始化一次 | ❌ 否            | ✅ 是              |

---

#### ✅ 5. 类成员函数中的局部变量

**📌 定义位置：**

类的成员函数内部，属于该函数的局部变量。

**📌 示例：**

```cpp
#include <iostream>
using namespace std;

class Person {
public:
    void showAge() {
        int age = 15;  // 局部变量，仅在 showAge() 内有效
        cout << "年龄是：" << age << endl;
    }
};

int main() {
    Person p;
    p.showAge();
    // cout << age;  // ❌ 错误，age 不在 main 作用域中
    return 0;
}
```

---

#### 🧾 小结：各种局部变量对比表

| 类型             | 定义位置           | 生命周期               | 是否能被多次调用记住值 | 使用范围       |
| ---------------- | ------------------ | ---------------------- | ---------------------- | -------------- |
| 普通局部变量     | 函数/代码块内      | 每次进入创建，退出销毁 | 否                     | 当前代码块内   |
| 代码块局部变量   | `{}` 块内部        | 每次进入创建，退出销毁 | 否                     | 当前块内       |
| 函数参数变量     | 函数参数列表       | 调用函数时创建         | 否                     | 当前函数内     |
| 静态局部变量     | 函数/块中加 static | 程序运行期间存在       | ✅ 是                  | 当前函数或块内 |
| 类成员函数内变量 | 类方法内部         | 每次调用创建           | 否                     | 当前函数内     |

---

#### 🧠 加分：如何选择使用哪种局部变量？

| 目的                             | 建议使用类型           |
| -------------------------------- | ---------------------- |
| 临时保存函数内部的小计算值       | 普通局部变量           |
| 在一个循环或判断中只临时使用变量 | 代码块变量             |
| 给函数传值                       | 函数参数               |
| 想记住上次调用的值（比如计数器） | 静态局部变量（static） |

---

### 3.3 变量名冲突怎么办？

C++ 允许**函数里的局部变量**跟**全局变量重名**，但函数会**优先使用局部变量**。

🔍 示例：

```cpp
#include <iostream>
using namespace std;

int x = 100;  // 全局变量

void test() {
    int x = 50;  // 局部变量，隐藏了全局变量
    cout << "函数里的x是：" << x << endl;
}

int main() {
    test();
    cout << "main函数里的x是：" << x << endl;
    return 0;
}
```

📌 输出：

```plaintext
函数里的x是：50
main函数里的x是：100
```

🔎 原因：函数里定义了局部变量 `x`，它会“挡住”外面的全局变量。

---

### 3.4 想在函数里修改全局变量怎么办？

可以**不定义局部变量**，直接用全局变量，或者用作用域运算符 `::` 来指定你要用的变量是全局的。

🔍 示例：

```cpp
#include <iostream>
using namespace std;

int count = 0;  // 全局变量

void addOne() {
    int count = 0;
    ::count = count + 1;  // 修改全局变量
}

int main() {
    addOne();
    cout << "count的值是：" << count << endl;
    return 0;
}
```

**📌 输出：**

```plaintext
count的值是：1
```

---

### 3.5 作用域总结 📋

| 类型     | 定义位置       | 使用范围         | 会不会影响其他函数？ |
| -------- | -------------- | ---------------- | -------------------- |
| 全局变量 | 函数外面       | 所有函数内都可用 | 会（要小心）         |
| 局部变量 | 函数或代码块内 | 只能在该函数内用 | 不会                 |

---

## 四、小练习题 🧠（带答案）

**问题：下面代码输出什么？**

```cpp
#include <iostream>
using namespace std;

int score = 90;

void changeScore() {
    int score = 60;
    cout << "函数内的score是：" << score << endl;
}

int main() {
    changeScore();
    cout << "main函数里的score是：" << score << endl;
    return 0;
}
```

✅ **答案：**

```plaintext
函数内的score是：60
main函数里的score是：90
```

---
