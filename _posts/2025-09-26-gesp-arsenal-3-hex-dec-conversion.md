---
layout: post
title: 【GESP/CSP】编程武器库-3, 十六进制转换十进制
date: 2025-09-26 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 武器库-进制转换]
categories: [GESP, 必备技能]
---

> 前文（[**_【GESP/CSP】编程武器库-2, 十进制转换十六进制_**](https://www.coderli.com/gesp-arsenal-2-dec-hex-conversion/)），我们介绍了从十进制到十六进制的处理手段，很显然这只做到了一半。在之前做过的[**_【GESP】C++四级真题 luogu-B3869 [GESP202309 四级] 进制转换_**](https://www.coderli.com/gesp-4-luogu-b3869/)题目中，需要将不同进制的数字转换成十进制表示出来，其中十六进制由于涉及字母，相对特殊，其他进制类比即可，今天就专门总结下这个知识点，希望下次遇到可以"信手拈来"。
> {: .prompt-info}

当前武器库清单

| 分类                                                                                                       | 功能                    | 教程                                                                                                      |
| ---------------------------------------------------------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------- |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为数字(0-9)     | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)  |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为字母(a-z/A-Z) | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)  |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为大写字母(A-Z) | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)  |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/)                   | 判断是否为小写字母(a-z) | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha)  |
| [进制转换](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E8%BF%9B%E5%88%B6%E8%BD%AC%E6%8D%A2/) | 十进制和十六进制转换    | [【GESP/CSP】编程武器库-2, 十进制转换十六进制](https://www.coderli.com/gesp-arsenal-2-dec-hex-conversion) |

> 本人也是边学、边实验、边总结。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
> {: .prompt-warning}

<!--more-->

---

## 一、十六进制值(整型变量)直接输出

在 C++ 代码中，可以直接写十六进制常量。它们一般以 `0x` 开头，例如 `0xFF`。编译器会自动识别为十进制数存储。所以，如果只想把十六进制整数常量显示为十进制，直接输出即可：

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 0xFF;   // 十六进制 0xFF 转换后存储为十进制 255
    int b = 0x1A;   // 十六进制 0x1A 转换后存储为十进制 26

    cout << "a = " << a << endl;  // 255
    cout << "b = " << b << endl;  // 26
    cout << "a + b = " << a + b << endl;  // 281
    return 0;
}
```

输出：

```plaintext
a = 255
b = 26
a + b = 281
```

说明：

- 虽然书写时用了十六进制，但变量内部保存的就是对应的十进制数。
- 之后就能像普通整数一样进行运算。

这种情况下其实是不涉及什么转换操作的。因此，如果题目是可以用整型进行存储计算的，那么当从控制台读取输入的时候，也直接将十六进制输入格式，读取成整数就好了。

用户直接输入十六进制格式整数，可以使用 **输入控制符 `hex`**：

```cpp
#include <iostream>
using namespace std;

int main() {
    int num;
    cout << "请输入一个十六进制数 (如 FF 或 0x1A): ";
    cin >> hex >> num;   // 按十六进制解析输入

    cout << "对应的十进制是: " << dec << num << endl;
    return 0;
}
```

运行示例：

```plaintext
输入：FF/0xFF
输出：对应的十进制是: 255
```

---

## 二、十六进制字符串转换

有时十六进制数以 **字符串形式** 存在，例如 `"FF"`、`"0x1A"`；或者是用户 **从控制台输入**的字符串。
这时需要额外的转换。

### 1. 内置函数`stoi` 方法

C++11 提供了 `stoi` 函数，可以直接把字符串转为整数，并指定进制：

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s1 = "FF";      // 十六进制字符串
    string s2 = "0x1A";    // 带 0x 前缀

    int num1 = stoi(s1, nullptr, 16);  // 转换为十进制
    int num2 = stoi(s2, nullptr, 16);

    cout << "num1 = " << num1 << endl;  // 255
    cout << "num2 = " << num2 << endl;  // 26
    return 0;
}
```

输出：

```plaintext
num1 = 255
num2 = 26
```

说明：

`stoi` 的函数原型大致是这样的：

```cpp
int stoi(const string& str, size_t* pos = 0, int base = 10);
```

- **第一个参数 `str`**：要转换的字符串。
- **第二个参数 `pos`**：指向 `size_t` 类型的指针，用来存储“第一个未被转换字符”的下标位置。
- **第三个参数 `base`**：进制，常用 `10`（十进制）、`16`（十六进制）等。

第一、第三个参数都好理解，举例介绍下第二个参数的作用，感兴趣的了解即可，实际使用中，基本可以无脑传`nullptr`。

#### 1.1 补充介绍stoi第二个参数用法

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "0xFFend";
    size_t idx;
    int num = stoi(s, &idx, 16);

    cout << "num = " << num << endl;   // 输出 255
    cout << "idx = " << idx << endl;   // 输出 5, 表示第一个未被转换字符的下标位置
    cout << "剩余部分: " << s.substr(idx) << endl;  // 输出 end
    return 0;
}
```

输出：

```plaintext
num = 4094
idx = 5
剩余部分: nd
```

👉 `stoi` 只解析 `"0xFF"`，把 `end` 留了下来。

---

### 2. 手动算法

如果你不习惯记忆函数用法，或者某些题目有特殊要求，你也可以按照进制转换逻辑，手动实现一个进制转换的函数

进制转换的基本逻辑为：十六进制 `"1A"` = `1 × 16^1 + 10 × 16^0 = 26`。

因此代码实现的核心思想为：把十六进制字符串从左到右逐位扫描，每遇到一位就将其转换成 0–15 的数值，然后“高位先走”——把前面已经算好的结果整体乘以 16，再加上当前这一位的值。  
一句话：**“逢位乘 16 再加新值”**，循环一遍就把整个十六进制字符串累加成了十进制整数。

代码示例：

```cpp
#include <iostream>
#include <string>
using namespace std;

int hexToDec(const string& s) {
    int result = 0;
    for (char c : s) {
        int value;
        if (c >= '0' && c <= '9') {
            value = c - '0';
        } else if (c >= 'A' && c <= 'F') {
            value = c - 'A' + 10;
        } else if (c >= 'a' && c <= 'f') {
            value = c - 'a' + 10;
        } else {
            continue; // 跳过不合法字符
        }
        result = result * 16 + value;
    }
    return result;
}

int main() {
    string s = "FE";
    cout << hexToDec(s) << endl;  // 输出 254
    return 0;
}
```

输出：

```plaintext
254
```

上述代码为十六进制字符串转换成十进制整数核心逻辑。不支持有进制前缀`0x`的情况，如果有前缀，你只需要先截取掉，在按上述代码处理即可。这里就不再赘述，留作读者自己实现。

---
