---
layout: post
title: 【GESP/CSP】编程武器库-1, 字符类型判断
date: 2025-09-21 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 武器库-字符]
categories: [GESP, 必备技能]
---
**开篇语：**

>在之前做题的过程中，我发现有很多题目都会有一些共同的小的功能逻辑，比如判断一个字符是否为数字、字母、空格；字符串的大小写转换以及数字的进制转换等。
>
>这部分的逻辑和代码其实是通用的、可复用的。掌握这部分技能，对每个等级的考生来说，就好像在逐步丰富你的“武器库”，“武器库”足够强大，可大大加快解题速度。
>
>在之前做题的过程中，我就打算抽空逐步整理、总结这部分“技能”，今天终于抽出时间决定开始，本系列今天正式启动。
{: .prompt-info}

> 本人也是边学、边实验、边总结。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

<!--more-->

在之前做过的[***【GESP】C++三级练习luogu-B3640 T3 句子反转***](https://www.coderli.com/gesp-3-luogu-b3640/)和[***【GESP】C++三级练习 luogu-B2117 整理药名***](https://www.coderli.com/gesp-3-luogu-b2117/)等题目中，都涉及到对单个字符进行是否是数字、字母或大小的判断的逻辑。这部分代码理论上是通用的，是你应该掌握的必备技能。今天我们就来详细了解一下这部分技能，开始丰富你的”武器库“。

---

## 一、判断字符是否是数字(0-9)

### 方法一，手动编码

手动编码永远是最直接的方法，但记不住内置函数的时候，可以选择手动编码。

```cpp
// 判断字符是否为数字的函数
bool isNumber(char c) {
    return c >= '0' && c <= '9';
}
```

应用样例：

```cpp
#include <iostream>
using namespace std;

// 判断字符是否为数字的函数
bool isNumber(char c) {
    return c >= '0' && c <= '9';
}

int main() {
    char c = '7';
    if (isNumber(c)) {
        cout << c << " 是数字" << endl;
    } else {
        cout << c << " 不是数字" << endl;
    }
    return 0;
}
```

输出：

```plaintext
7 是数字
```

### 方法二，使用内置 `isdigit` 函数

C++ 标准库提供了 `<cctype>` 头文件，其内定义了一系列常用的字符判断函数。其中就包括判断字符是否是数字的`isdigit`函数。

* **isdigit(c)** → 如果 `c` 是 0\~9 的数字字符，返回非 0（true）。

```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char c = '7';
    if (isdigit(c)) {
        cout << c << " 是数字" << endl;
    } else {
        cout << c << " 不是数字" << endl;
    }
    return 0;
}
```

输出：

```plaintext
7 是数字
```

---

## 二、判断字符是否是字母（英文a~z或A~Z）

### 方法一，手动编码

```cpp
// 判断字符是否为字母的函数
bool isLetter(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}
```

应用样例：

```cpp
#include <iostream>
using namespace std;

// 判断字符是否为字母的函数
bool isLetter(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

int main() {
    char c = 'A';
    if (isLetter(c)) {
        cout << c << " 是字母" << endl;
    } else {
        cout << c << " 不是字母" << endl;
    }
    return 0;
}
```

输出：

```plaintext
A 是字母
```

### 方法二，使用内置 `isalpha` 函数

C++ 标准库 `<cctype>` 头文件中定义了判断字符是否是字母的`isalpha`函数。

* **isalpha(c)** → 如果 `c` 是 A\~Z 或 a\~z，返回 true。

```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char c = 'A';
    if (isalpha(c)) {
        cout << c << " 是字母" << endl;
    } else {
        cout << c << " 不是字母" << endl;
    }
    return 0;
}
```

输出：

```plaintext
A 是字母
```

## 三、判断字符是否是大写字母(A~Z)

### 方法一，手动编码

```cpp
// 判断字符是否为大写字母的函数
bool isUpperCase(char c) {
    return c >= 'A' && c <= 'Z';
}
```

应用样例：

```cpp
#include <iostream>
using namespace std;

// 判断字符是否为大写字母的函数
bool isUpperCase(char c) {
    return c >= 'A' && c <= 'Z';
}

int main() {
    char c = 'A';
    if (isUpperCase(c)) {
        cout << c << " 是大写字母" << endl;
    } else {
        cout << c << " 不是大写字母" << endl;
    }
    return 0;
}
```

输出：

```plaintext
A 是大写字母
```

### 方法二，使用内置 `isupper` 函数

C++ 标准库 `<cctype>` 头文件中定义了判断字符是否是大写字母的`isupper`函数。

* **isupper(c)** → 如果 `c` 是 A\~Z，返回 true。

```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char c = 'A';
    if (isupper(c)) {
        cout << c << " 是大写字母" << endl;
    } else {
        cout << c << " 不是大写字母" << endl;
    }
    return 0;
}
```

输出：

```plaintext
A 是大写字母
```

---

## 四、判断字符是否是小写字母(a~z)

### 方法一，手动编码

```cpp
// 判断字符是否为小写字母的函数
bool isLowerCase(char c) {
    return c >= 'a' && c <= 'z';
}
```

应用样例：

```cpp
#include <iostream>
using namespace std;

// 判断字符是否为小写字母的函数
bool isLowerCase(char c) {
    return c >= 'a' && c <= 'z';
}

int main() {
    char c = 'a';
    if (isLowerCase(c)) {
        cout << c << " 是小写字母" << endl;
    } else {
        cout << c << " 不是小写字母" << endl;
    }
    return 0;
}
```

### 方法二，使用内置 `islower` 函数

C++ 标准库 `<cctype>` 头文件中定义了判断字符是否是小写字母的`islower`函数。

* **islower(c)** → 如果 `c` 是 a\~z，返回 true。

```cpp
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    char c = 'a';
    if (islower(c)) {
        cout << c << " 是小写字母" << endl;
    } else {
        cout << c << " 不是小写字母" << endl;
    }
    return 0;
}
```

输出：

```plaintext
a 是小写字母
```

---

## 四、总结

1. **推荐使用 `<cctype>` 的内置函数**，因为它们更直观、可读性更好。

   * `isdigit` → 数字
   * `isalpha` → 字母
   * `isupper` / `islower` → 大小写

2. **手动 ASCII 范围判断** 更灵活，但代码可读性稍差。当你在考场忘记内置函数写法或者需要一些自定义规则的时候使用。

3. `<cctype>` 中还有很多其他的判断函数，如 `isspace`（判断空格）、`isalnum`（判断字母或数字）等。本质就是针对ASCII表中特定范围的字符，分类判断，这里不做展开。当真正用道时，我们再考虑总结。

总之，本次我们`武器库`更新了字符判断是否是**数字、字母、大写、小写**。4个技能，后续我们将跟随问题，逐步更新。

---

## 附、当前武器库清单

| 分类 | 功能 | 教程 |
|------|------|----------|
| 字符判断 | 判断是否为数字(0-9) | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| 字符判断 | 判断是否为字母(a-z/A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| 字符判断 | 判断是否为大写字母(A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| 字符判断 | 判断是否为小写字母(a-z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |

---

{% include custom/custom-post-content-footer.md %}
