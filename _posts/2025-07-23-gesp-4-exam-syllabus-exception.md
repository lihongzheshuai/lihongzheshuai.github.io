---
layout: post
title: 【GESP】C++四级考试大纲知识点梳理, (11) 异常处理机制
date: 2025-07-23 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 四级]
---
终于到最后一条了，GESP C++四级官方考试大纲中，共有11条考点，本文针对第11条考点进行分析介绍。
> （11）了解异常处理机制，掌握异常处理的常用方法。
{: .prompt-info}

其实，由于本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。

***四级其他考点回顾：***

> * [【GESP】C++四级考试大纲知识点梳理, (1) 指针](https://www.coderli.com/gesp-4-exam-syllabus-pointer/)
> * [【GESP】C++四级考试大纲知识点梳理, (2) 结构体和二维数组](https://www.coderli.com/gesp-4-exam-syllabus-struct-two-dimensional-array/)
> * [【GESP】C++四级考试大纲知识点梳理, (3) 模块化和函数](https://www.coderli.com/gesp-4-exam-syllabus-module-function/)
> * [【GESP】C++四级考试大纲知识点梳理, (4) 变量和作用域](https://www.coderli.com/gesp-4-exam-syllabus-variable-scope/)
> * [【GESP】C++四级考试大纲知识点梳理, (5) 值传递](https://www.coderli.com/gesp-4-exam-syllabus-pass-by-value-reference-pointer/)
> * [【GESP】C++四级考试大纲知识点梳理, (6) 递推算法](https://www.coderli.com/gesp-4-exam-syllabus-iteration-algo/)
> * [【GESP】C++四级考试大纲知识点梳理, (7) 排序算法基本概念](https://www.coderli.com/gesp-4-exam-syllabus-sorting-algo-conception/)
> * [【GESP】C++四级考试大纲知识点梳理, (8) 冒泡、插入、选择排序](https://www.coderli.com/gesp-4-exam-syllabus-three-sorting-methods/)
> * [【GESP】C++四级考试大纲知识点梳理, (9) 简单算法复杂度的估算](https://www.coderli.com/gesp-4-exam-syllabus-estimation-of-algorithm-time-complexity/)
> * [【GESP】C++四级考试大纲知识点梳理, (10) 文件读写和重定向](https://www.coderli.com/gesp-4-exam-syllabus-file-read-write/)
{: .prompt-tip}

<!--more-->

---

在 C++ 中，**异常处理机制**主要用于处理程序运行时发生的异常情况，使程序具有更强的鲁棒性（容错性）和可维护性。

## 一、异常处理机制的定位和作用

C++ 中的**异常处理机制**是一种**结构化错误处理机制**，其**定位**和**作用**主要有：

✅ 1. **程序健壮性的重要保障**

异常处理用于应对**程序运行时的非正常情况**，如除以 0、数组越界、内存不足、非法输入等。这些问题如果不处理，程序可能**崩溃或输出错误结果**。

✅ 2. **错误处理与业务逻辑解耦**

异常处理将“**如何应对错误**”与“**主流程的正常逻辑**”分离，使代码结构更清晰、可维护性更强。

✅ 3. **支持跨层传播的错误传递机制**

异常可以从函数内部“**抛出**”并在调用者（甚至更高层）中“**捕获**”，避免了每层函数都要显式返回错误码。

---

## 二、异常处理的常用方法

C++ 提供了标准的异常处理机制，主要通过 `try`、`catch` 和 `throw` 关键字实现。

* **throw**：用于抛出异常，表示程序检测到错误或异常情况。
* **try**：定义可能抛出异常的代码块。
* **catch**：捕获并处理特定类型的异常。

### 2.1 基本异常处理

使用 `try` 和 `catch` 捕获特定类型的异常。通常，异常可以是内置类型（如 `int`、`std::string`）或自定义异常类。

代码示例:

```cpp
#include <iostream>
#include <string>

int divide(int a, int b) {
    if (b == 0) {
        throw std::string("Division by zero is not allowed");
    }
    return a / b;
}

int main() {
    try {
        int result = divide(10, 0);
        std::cout << "Result: " << result << std::endl;
    } catch (const std::string& e) {
        std::cerr << "Error: " << e << std::endl;
    }
    return 0;
}
```

**说明**：

* `throw` 抛出 `std::string` 类型的异常。
* `catch` 捕获 `std::string` 类型的异常并打印错误信息。
* 如果没有异常，`try` 块中的代码正常执行。

---

### 2.2 捕获多种异常类型

可以通过多个 `catch` 块捕获不同类型的异常。C++ 允许按异常类型的层次结构进行匹配。

代码示例:

```cpp
#include <iostream>
#include <stdexcept>

void processValue(int value) {
    if (value < 0) {
        throw std::invalid_argument("Negative value not allowed");
    } else if (value > 100) {
        throw std::out_of_range("Value exceeds maximum limit");
    }
    std::cout << "Value processed: " << value << std::endl;
}

int main() {
    try {
        processValue(-5);
        processValue(150);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Invalid argument: " << e.what() << std::endl;
    } catch (const std::out_of_range& e) {
        std::cerr << "Out of range: " << e.what() << std::endl;
    } catch (...) {
        std::cerr << "Unknown error occurred" << std::endl;
    }
    return 0;
}
```

**说明**：

* 使用标准库中的异常类（如 `std::invalid_argument` 和 `std::out_of_range`）。
* `catch (...)` 是通配符捕获，用于处理未明确指定的异常类型。
* 异常按声明顺序匹配，因此更具体的异常类型应放在前面。

---

### 2.3 自定义异常类

对于复杂程序，建议定义自定义异常类，继承自 `std::exception` 或其子类，以便提供更详细的错误信息。

代码示例:

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <cmath>

class MyException : public std::exception {
private:
    std::string message;
public:
    MyException(const std::string& msg) : message(msg) {}
    const char* what() const noexcept override {
        return message.c_str();
    }
};

double calculateSquareRoot(double x) {
    if (x < 0) {
        throw MyException("Cannot calculate square root of a negative number");
    }
    return sqrt(x);
}

int main() {
    try {
        double result = calculateSquareRoot(-4.0);
        std::cout << "Square root: " << result << std::endl;
    } catch (const MyException& e) {
        std::cerr << "Custom error: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Standard error: " << e.what() << std::endl;
    } catch (...) {
        std::cerr << "Unknown error" << std::endl;
    }
    return 0;
}
```

**说明**：

* `MyException` 继承自 `std::exception`，重写了 `what()` 方法以提供自定义错误信息。
* 异常类可以通过成员变量存储额外信息，增强错误描述的灵活性。
* 多个 `catch` 块按继承层次匹配异常。

---

### 2.4 异常规范（C++11 前）与 noexcept（C++11 后）

* **异常规范（C++11 前）**：C++98/03 使用 `throw()` 动态异常规范来指定函数可能抛出的异常类型，但此特性在 C++11 中被废弃。
* **noexcept（C++11 后）**：用于声明函数不会抛出异常，优化性能并提高代码安全性。

代码示例:

```cpp
#include <iostream>

// 声明函数不会抛出异常
void safeFunction() noexcept {
    std::cout << "This function does not throw exceptions" << std::endl;
}

void mayThrow() {
    throw std::runtime_error("An error occurred");
}

int main() {
    try {
        safeFunction();
        mayThrow();
    } catch (const std::exception& e) {
        std::cerr << "Caught: " << e.what() << std::endl;
    }
    return 0;
}
```

执行结果：

```plaintext
This function does not throw exceptions
Caught: An error occurred
```

**说明**：

* `noexcept` 修饰的函数若抛出异常，将导致程序调用 `std::terminate()`。
* 使用 `noexcept` 可以提高编译器优化效率，特别是在模板代码中。

---

### 2.5 栈展开与 RAII

C++ 的异常处理会触发栈展开（stack unwinding），即从抛出异常的点到捕获异常的 `catch` 块之间，局部对象的析构函数会被调用。这使得 RAII（资源获取即初始化）技术在异常处理中尤为重要。

代码示例：RAII 与异常处理

```cpp
#include <iostream>
#include <stdexcept>

class Resource {
public:
    Resource() { std::cout << "Resource acquired" << std::endl; }
    ~Resource() { std::cout << "Resource released" << std::endl; }
};

void riskyOperation() {
    Resource res; // RAII 对象
    std::cout << "Inside riskyOperation" << std::endl;
    throw std::runtime_error("Something went wrong");
}

int main() {
    try {
        riskyOperation();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    return 0;
}
```

代码输出：

```plaintext
Resource acquired
Inside riskyOperation
Resource released
Error: Something went wrong
```

**说明**：

* `Resource` 对象的析构函数在异常抛出时自动调用，确保资源正确释放。
* RAII 避免了资源泄漏问题，特别是在复杂控制流中。

---

{% include custom/custom-post-content-inner.html %}

## 三、标准异常类

C++ 标准库提供了 `std::exception` 层次结构的异常类，常用类包括：

* `std::logic_error`：逻辑错误，如 `std::invalid_argument`、`std::out_of_range`。
* `std::runtime_error`：运行时错误，如 `std::overflow_error`、`std::underflow_error`。
* `std::bad_alloc`：内存分配失败。
* `std::bad_cast`：动态类型转换失败。

使用标准异常类的好处在于:

1. **可移植性**：标准异常类在所有支持 C++ 的平台上都可用，代码可以轻松地在不同编译器和操作系统间移植
2. **可读性**：标准异常类的命名清晰直观（如 `std::invalid_argument`、`std::out_of_range` 等），其他程序员一看就能理解异常的类型和含义
3. **一致性**：使用标准异常类可以与 C++ 标准库保持一致的错误处理风格

---

## 四、异常处理的最佳实践

1. **优先使用标准异常类**：除非有特殊需求，否则使用 `std::exception` 及其子类。
2. **捕获异常时使用引用**：避免对象拷贝，使用 `const std::exception&`。
3. **按需捕获异常**：避免滥用 `catch (...)`，因为它可能掩盖未预期的错误。
4. **确保资源安全**：使用 RAII 管理资源，避免异常导致的资源泄漏。
5. **明确异常语义**：抛出异常时提供清晰的错误信息。
6. **谨慎使用 noexcept**：仅在确定函数不会抛出异常时使用。

---

## 五、总结

C++ 的异常处理机制通过 `try`、`catch` 和 `throw` 提供了一种强大的错误处理方式。常用方法包括基本异常处理、捕获多种异常类型、自定义异常类、使用 `noexcept` 优化性能以及结合 RAII 确保资源安全。遵循最佳实践（如使用标准异常类、避免滥用通配符捕获）可以编写健壮且可维护的代码。

---
{% include custom/custom-post-content-footer.md %}
