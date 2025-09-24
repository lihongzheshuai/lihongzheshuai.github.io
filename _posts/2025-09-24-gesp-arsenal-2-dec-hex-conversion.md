---
layout: post
title: 【GESP/CSP】编程武器库-2, 十进制和十六进制转换
date: 2025-09-24 08:00 +0800
author: OneCoder
comments: true
math: true
tags: [GESP, C++, 武器库-进制转换]
categories: [GESP, 必备技能]
---

>在之前做过的[***【GESP】C++四级真题 luogu-B3851 [GESP202306 四级] 图像压缩***](https://www.coderli.com/gesp-4-luogu-b3851/)题目中，需要将一个数字转换为十六进制表示并输出出来，如果你的"武器库"缺少这部分技能，你可能会一下不知所措，今天就专门总结下这个知识点，希望下次遇到可以"信手拈来"。
{: .prompt-info}

当前武器库清单

| 分类 | 功能 | 教程 |
|------|------|----------|
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为数字(0-9) | [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为字母(a-z/A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为大写字母(A-Z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| [字符判断](https://www.coderli.com/tags/%E6%AD%A6%E5%99%A8%E5%BA%93-%E5%AD%97%E7%AC%A6/) | 判断是否为小写字母(a-z) |  [【GESP/CSP】编程武器库-1, 字符类型判断](https://www.coderli.com/gesp-arsenal-1-char-check-number-alpha) |
| 进制转换 | 十进制和十六进制转换 |  [【GESP/CSP】编程武器库-2, 十进制和十六进制转换](https://www.coderli.com/gesp-arsenal-2-dec-hex-conversion) |

> 本人也是边学、边实验、边总结。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

<!--more-->

---

一般来说，在涉及进制转换的题目中，你可能遇到两种情况：一是直接输出转换后的表示，这种情况相对简单，可以利用输出流的格式化输出功能；二是需要将转换后的结果存储到变量中，这种情况相对复杂一些。接下来分别介绍。

---

## 一、直接输出转换后的表示

这种情况最常见于题目要求“请输出数字的十六进制表示”。
直接输出相对简单，C++ 提供了非常方便的**格式化输出**功能。

### 1.1 使用 `cout` 格式化

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int n = 255;

    cout << hex << n << endl;              // ff （小写）
    cout << uppercase << hex << n << endl; // FF （大写）
    cout << setw(4) << setfill('0') << hex << n << endl; // 00ff
    return 0;
}
```

* `hex`：切换到十六进制输出
* `uppercase`：字母部分大写
* `setw(4)`：宽度至少 4
* `setfill('0')`：不足部分用 0 补齐

输出：

```plaintext
ff
FF
00FF
```

如果需要带 `0x` 前缀，可以加 `showbase`：

```cpp
cout << showbase << hex << n << endl; // 0xff
```

输出(255对应)：

```plaintext
0xff
```

>需要注意的是：
在 `iostream` 里，`setw()` 的宽度是对 **整个输出字段** 起作用，而不是只对数值部分。
{: .prompt-warning}

所以如果直接写：

```cpp
cout << showbase << uppercase << hex << setw(4) << setfill('0') << 255;
```

实际输出会是 `0xFF`，而不是你预期的 `0x00FF` ——因为 `0x` 也被算进了宽度。

所以，一种方法是，我们分开输出前缀和数值，只对数值部分使用 `setw()`：

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    // 定义一个十进制数 255 用于演示
    int n = 255;
    
    cout << "0x"  // 输出十六进制前缀
         << uppercase  // 设置大写字母输出模式
         << hex       // 设置十六进制输出模式
         << setw(4)   // 设置输出宽度为4
         << setfill('0')  // 设置填充字符为'0'
         << n        // 输出数字
         << endl;   // 输出 0x00FF
}
```

输出：

```plaintext
0x00FF
```

另一种相对更快速的办法是使用`printf`函数。

---

### 1.2 使用 `printf`

如果你更习惯 C 风格的 `printf`，也有对应写法：

```cpp
#include <cstdio>

int main() {
    int n = 255;

    printf("%x\n", n);    // ff （小写）
    printf("%X\n", n);    // FF （大写）
    printf("%04x\n", n);  // 00ff （补位）
    printf("%#X\n", n);   // 0XFF （带前缀）
    printf("%#06x\n", n); // 0x00FF （带前缀并补位）
    return 0;
}
```

说明：

* `%x`：小写十六进制
* `%X`：大写十六进制
* `%04x`：宽度 4，前面补 0
* `%#x` / `%#X`：带前缀 `0x` / `0X`
* `%#06x`：带前缀并补位，宽度 6

输出：

```plaintext
ff
FF
00ff
0XFF
0x00ff
```

👉 综上：如果题目只要求输出结果，用 `cout` 的格式化或 `printf` 的格式控制就足够了。

---

## 二、存储转换后的结果

有些题目解题需要的可能不只是“打印出来”，而是需要把转换后的十六进制**存储到变量**中（通常是 `string`），供后续使用。这时就需要额外处理。

### 2.1 用 `ostringstream`

C++ 提供了字符串流 `ostringstream`，用法和 `cout` 类似：

```cpp
#include <iostream>
#include <sstream>
#include <string>
#include <iomanip>
using namespace std;

string decimalToHex(int num) {
    ostringstream oss;
    // 设置宽度和填充
    oss << setw(4) << setfill('0');
    // 设置大写和十六进制
    oss << uppercase << hex;
    // 设置显示前缀
    oss << showbase;
    oss << num;
    return oss.str();
}

int main() {
    int n = 255;  // 定义一个十进制数
    string hexStr = decimalToHex(n);  // 调用转换函数，将十进制转为十六进制字符串
    cout << hexStr << endl; // 输出结果：0X00FF（带前缀的大写十六进制）
}
```

输出：

```plaintext
0XFF
```

可以看到，这里的处理方式与前文`cout`格式输出的方式相同，都是输出控制参数设置格式后，再转换成字符串。因此，类似的，如果你需要输出类似`0x00FF`格式的十六进制格式，只需要在`decimalToHex`函数内，手动添加前缀`0x`即可。

### 2.2 自己实现

如果你觉得记忆这么多参数很麻烦，你也可以手动实现格式转换。
思路是：不断取余 `% 16`，映射到 `0-9` / `A-F`，再反转。

```cpp
#include <iostream>
#include <string>
using namespace std;

// 将0-15的数字转换为对应的十六进制字符
// 参数 val: 0-15之间的整数
// 返回值: 对应的十六进制字符（0-9或A-F）
char toHexChar(int val) {
    return (val < 10) ? '0' + val : 'A' + (val - 10);
}

// 将十进制数转换为十六进制字符串
// 参数 num: 待转换的十进制数
// 返回值: 转换后的十六进制字符串（大写）
string decimalToHex(int num) {
    // 处理0的特殊情况
    if (num == 0) {
        return "0";
    }
    
    string res;
    // 不断除以16取余，从低位到高位构建十六进制字符串
    while (num > 0) {
        // 取余得到当前位的值（0-15），转换为十六进制字符
        res = toHexChar(num % 16) + res;
        // 除以16，处理下一位
        num /= 16;
    }
    return res;
}

int main() {
    cout << decimalToHex(254) << endl; // FE
}
```

输出：

```plaintext
FE
```

从代码可以看出，该方法可讲10进制数转换成16进制字符串，数字大小不限(整数范围内)。但是没有处理按格式输出的情况，如要求输出`0X00FF`格式的十六进制字符串，需要在函数内手动添加前缀`0X`且需要处理前置补`0`的情况。

```cpp
#include <iostream>
#include <string>
using namespace std;

// 将0-15的数字转换为对应的十六进制字符
// 参数 val: 0-15之间的整数
// 返回值: 对应的十六进制字符（0-9或A-F）
char toHexChar(int val) {
    return (val < 10) ? '0' + val : 'A' + (val - 10);
}

// 将十进制数转换为十六进制字符串
// 参数 num: 待转换的十进制数
// 返回值: 转换后的十六进制字符串（大写，格式如"0x00FF"）
string decimalToHex(int num) {
    // 处理0的特殊情况
    if (num == 0) {
        return "0x0000";
    }
    
    string res;
    // 不断除以16取余，从低位到高位构建十六进制字符串
    while (num > 0) {
        // 取余得到当前位的值（0-15），转换为十六进制字符
        res = toHexChar(num % 16) + res;
        // 除以16，处理下一位
        num /= 16;
    }
    
    // 补齐4位
    while (res.length() < 4) {
        res = "0" + res;
    }
    
    // 添加0x前缀
    return "0x" + res;
}

int main() {
    cout << decimalToHex(254) << endl; // 0x00FE
}
```

输出：

```plaintext
0x00FE
```

---

还有一种常见的利用16进制字符串(一维数组)取对应位置的字符的方式

```cpp
#include <iostream>
#include <string>
using namespace std;

// 将十进制数转换为十六进制字符串（固定4位，带0X前缀）
// 参数：num - 待转换的十进制数
// 返回：转换后的十六进制字符串，格式如"0X00FF"
string decimalToHex(int num) {
    // 定义包含所有十六进制字符的字符数组（0-9和A-F）
    static const char hex_digits[] = "0123456789ABCDEF";
    // 初始化结果字符串，长度为4，用'0'填充
    std::string res(4, '0');
    
    // 从右向左，每次处理一个十六进制位
    for (int i = 3; i >= 0; --i) {
        // 通过num % 16获取当前位的值(0-15)
        // 然后用这个值作为下标从hex_digits数组中取出对应的字符
        // 例如:如果num % 16 = 15,就会取出hex_digits[15]即'F'
        res[i] = hex_digits[num % 16];
        // num除以16，准备处理下一位
        num /= 16;
    }
    
    // 添加"0X"前缀并返回结果
    res = "0X" + res;
    return res;
}

int main() {
    cout << decimalToHex(254) << endl; // FE
}
```

输出：

```plaintext
0X00FE
```

从代码可看出，该方法更适合需要将10进制数转换为***固定宽度(补齐0)***的16进制字符串的场景，因为其中写死了16进制输出的长度。例如：4位长度，补齐0。`std::string res(4, '0');`。当然，你可以将该方法修改扩展成跟第一个方法一样可支持任意长度数字的情况。这个小问题就留给大家了。

总之，如果你不愿意记忆内置函数，你可以选一种手动实现的方式记忆下来，考试时直接使用，节约考试思考时间。

---

## 三、总结与对比

| 场景          | 推荐做法                            | 示例               |
| ----------- | ------------------------------- | ---------------- |
| **只需控制台输出** | `cout` + `hex` / `printf("%x")` | `ff / FF / 0xff` |
| **需要存储结果**  | `ostringstream` 或手写函数           | `"FF"`（字符串形式）    |

---

{% include custom/custom-post-content-footer.md %}
