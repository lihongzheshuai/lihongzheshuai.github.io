---
layout: post
title: 【GESP】C++三级考试大纲知识点梳理, (6) 字符串
date: 2025-04-08 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++]
categories: [GESP, 三级]
---
GESP C++三级官方考试大纲中，共有8条考点，之前已对前4个考点进行了总结梳理，6号考点是关于C++语言字符串应用的，属于基本语言语法和应用范围，网上的资料很多，本不想再赘述。但在孩子做题的过程中发现，对字符串应掌握哪些常用函数以及如何应用还不是很熟悉，因此将这部分内容单独整理出来，供孩子参考。
> （6）掌握字符串及其函数的使用包括但不限于大小写转换、字符串搜索、分割、替换。
{: .prompt-info}

<!--more-->

## 字符串常用函数详解

### 1. 基本操作函数

#### 1.1 长度和容量

- `size()` / `length()`: 返回字符串长度
- `empty()`: 判断字符串是否为空
- `capacity()`: 返回当前分配的存储空间大小

```cpp
string str = "Hello";
cout << str.size() << endl;     // 输出：5
cout << str.empty() << endl;    // 输出：0（false）
cout << str.capacity() << endl; // 输出：15（可能因编译器不同而异）
```

#### 1.2 访问和修改

- `at(pos)`: 访问指定位置字符（带边界检查）
- `operator[]`: 访问指定位置字符（无边界检查）
- `front()`: 访问第一个字符
- `back()`: 访问最后一个字符

```cpp
string str = "Hello";
cout << str.at(0) << endl;      // 输出：H
cout << str[1] << endl;         // 输出：e
cout << str.front() << endl;    // 输出：H
cout << str.back() << endl;     // 输出：o
```

### 2. 字符串修改函数

#### 2.1 添加和删除

- `append()`: 在末尾添加字符串
- `push_back()`: 在末尾添加单个字符
- `insert()`: 在指定位置插入
- `erase()`: 删除指定位置的字符或子串
- `clear()`: 清空字符串

```cpp
string str = "Hello";
str.append(" World");           // Hello World
str.push_back('!');            // Hello World!
str.insert(5, " C++");         // Hello C++ World!
str.erase(5, 4);               // Hello World!
```

#### 2.2 替换和子串

- `replace()`: 替换子串
- `substr()`: 获取子串

```cpp
string str = "Hello World";
str.replace(6, 5, "C++");      // Hello C++
string sub = str.substr(6, 3);  // 获取子串："C++"
```

### 3. 字符串查找函数

#### 3.1 查找函数

- `find()`: 从前向后查找子串，返回找到的第一个匹配子串的起始位置。返回值类型为 `size_t`。若未找到则返回 `string::npos`（通常是 -1）
- `rfind()`: 从后向前查找子串，返回找到的最后一个匹配子串的起始位置。返回值类型为 `size_t`。若未找到则返回 `string::npos`
- `find_first_of()`: 查找字符串中第一个与指定字符集合中任意字符匹配的位置。返回值类型为 `size_t`。若未找到则返回 `string::npos`
- `find_last_of()`: 查找字符串中最后一个与指定字符集合中任意字符匹配的位置。返回值类型为 `size_t`。若未找到则返回 `string::npos`
- `find_first_not_of()`: 查找字符串中第一个不在指定字符集合中的字符位置。返回值类型为 `size_t`。若未找到则返回 `string::npos`
- `find_last_not_of()`: 查找字符串中最后一个不在指定字符集合中的字符位置。返回值类型为 `size_t`。若未找到则返回 `string::npos`

```cpp
string str = "Hello World Hello";
cout << str.find("Hello") << endl;          // 输出：0
cout << str.rfind("Hello") << endl;         // 输出：12
cout << str.find_first_of("aeiou") << endl; // 输出：1（e的位置）
```

### 4. 字符串转换函数

#### 4.1 大小写转换

- `toupper()`: 转换为大写
- `tolower()`: 转换为小写

```cpp
string str = "Hello";
transform(str.begin(), str.end(), str.begin(), ::toupper);  // HELLO
transform(str.begin(), str.end(), str.begin(), ::tolower);  // hello
```

#### 4.2 类型转换

- `to_string()`: 数值转字符串
- `stoi()`, `stol()`, `stof()`, `stod()`: 字符串转数值

```cpp
int num = 42;
string str = to_string(num);    // 数字转字符串
int back = stoi("42");          // 字符串转数字
```

### 5. 字符串比较函数

- `compare()`: 比较字符串
- 关系运算符：`==`, `!=`, `<`, `>`, `<=`, `>=`

```cpp
string str1 = "Hello";
string str2 = "World";
cout << str1.compare(str2) << endl;  // 输出负数（str1 < str2）
cout << (str1 < str2) << endl;       // 输出：1（true）
```

这些是 C++ 字符串操作中最常用的函数，掌握这些函数可以帮助更好地处理字符串相关的问题。

---

## 字符大小写判断和转换函数

### 1. 字符判断函数

C++ 提供了一系列用于判断字符类型的函数，这些函数定义在 `<cctype>` 头文件中：

- `isupper(c)`: 判断字符是否为大写字母
- `islower(c)`: 判断字符是否为小写字母
- `isalpha(c)`: 判断字符是否为字母
- `isdigit(c)`: 判断字符是否为数字
- `isalnum(c)`: 判断字符是否为字母或数字
- `isspace(c)`: 判断字符是否为空白字符

```cpp
char c = 'A';
if (isupper(c)) {
    cout << c << " 是大写字母" << endl;
}
if (isalpha(c)) {
    cout << c << " 是字母" << endl;
}
```

### 2. 字符转换函数

#### 2.1 单个字符转换

- `toupper(c)`: 将字符转换为大写
- `tolower(c)`: 将字符转换为小写

```cpp
char c = 'a';
char upper_c = toupper(c);  // 'A'
char lower_c = tolower('B'); // 'b'
```

---
{% include custom/custom-post-content-footer.md %}
