---
layout: post
title: 【GESP】C++一级练习BCQM3021，输入-计算-输出-2
date: 2024-09-25 20:00 +0800
author: OneCoder
image: /images/post/gesp/gesp-1.png
comments: true
tags: [GESP, C++]
categories: [GESP, 一级]
---


<!--more-->
在C++中，使用 `printf` 输出 `double` 类型的值时，正确的格式化符是 `%f`，而不是 `%lf`。

虽然在变量声明时，`double` 和 `float` 有区别，但 `printf` 在格式化时，`%f` 处理的是所有浮点数，包括 `float` 和 `double`。使用 `%lf` 只在 `scanf` 中用于读取 `double` 类型的值。

### 示例：
```cpp
#include <cstdio>

int main() {
    double num = 3.14159;
    printf("%f\n", num);  // 正确，输出 3.141590
    return 0;
}
```

### 总结：
- **`printf` 输出 `double` 类型的值时：用 `%f`**。
- **`scanf` 读取 `double` 类型的值时：用 `%lf`**。

在 `C++` 和 `C` 中，使用 `printf` 函数时，虽然 `double` 和 `float` 在类型上有所不同，但对于 `printf` 来说，它只认 `%f` 作为格式化符。对于 `double` 类型的输出，**无论是 `%f` 还是 `%lf`**，通常都能正常工作，这是因为：

### 1. **历史原因与标准**
在标准 C 库中，`printf` 规范中规定了 `%f` 作为格式化浮点数的通用符号，适用于 `float` 和 `double` 类型。事实上，`float` 类型在调用 `printf` 时，会被自动提升为 `double`（称为默认的“浮点数提升”）。因此，对于 `printf` 来说，处理的是 `double` 类型的数据，而不是 `float`，所以 `%f` 足够处理两者。

`%lf` 虽然表示长浮点数（`long float`），但在 `printf` 中它并不是标准格式。实际上 `%lf` 的使用行为与 `%f` 相同，因为 `printf` 不区分 `float` 和 `double`。这也是为什么你看到使用 `%lf` 也能正常输出 `double` 的原因，但标准要求应该使用 `%f`。

### 2. **推荐使用 `%f`**
即使在某些编译器下，`%lf` 和 `%f` 都能正常输出 `double`，但根据标准 C/C++ 规范，**推荐使用 `%f`** 来格式化输出浮点数（包括 `double`）。

### 示例：
```cpp
#include <cstdio>

int main() {
    double num = 3.14159;
    
    // 使用 %f 输出 double
    printf("%f\n", num);   // 输出：3.141590
    
    // 使用 %lf 输出 double （非标准，但通常也能输出）
    printf("%lf\n", num);  // 输出：3.141590（行为和 %f 一样）
    
    return 0;
}
```

### 3. **`scanf` 与 `printf` 的不同处理**
在 `scanf` 中，`%lf` 是必须的，用来明确区分 `double` 和 `float`。但是 `printf` 中不区分，因此 `%f` 是正确的选择。

### 总结：
- **`printf` 输出 `double` 时，规范推荐使用 `%f`，虽然 `%lf` 也能工作，但不属于标准规定。**
- **`scanf` 中必须使用 `%lf` 来读取 `double` 类型。**

因此，为了编写符合标准的代码，建议在 `printf` 中使用 `%f`，在 `scanf` 中使用 `%lf` 来处理 `double` 类型。

---

在 `C++` 和 `C` 中，使用 `printf` 函数时，虽然 `double` 和 `float` 在类型上有所不同，但对于 `printf` 来说，它只认 `%f` 作为格式化符。对于 `double` 类型的输出，**无论是 `%f` 还是 `%lf`**，通常都能正常工作，这是因为：

### 1. **历史原因与标准**
在标准 C 库中，`printf` 规范中规定了 `%f` 作为格式化浮点数的通用符号，适用于 `float` 和 `double` 类型。事实上，`float` 类型在调用 `printf` 时，会被自动提升为 `double`（称为默认的“浮点数提升”）。因此，对于 `printf` 来说，处理的是 `double` 类型的数据，而不是 `float`，所以 `%f` 足够处理两者。

`%lf` 虽然表示长浮点数（`long float`），但在 `printf` 中它并不是标准格式。实际上 `%lf` 的使用行为与 `%f` 相同，因为 `printf` 不区分 `float` 和 `double`。这也是为什么你看到使用 `%lf` 也能正常输出 `double` 的原因，但标准要求应该使用 `%f`。

### 2. **推荐使用 `%f`**
即使在某些编译器下，`%lf` 和 `%f` 都能正常输出 `double`，但根据标准 C/C++ 规范，**推荐使用 `%f`** 来格式化输出浮点数（包括 `double`）。

### 示例：

```cpp
#include <cstdio>

int main() {
    double num = 3.14159;
    
    // 使用 %f 输出 double
    printf("%f\n", num);   // 输出：3.141590
    
    // 使用 %lf 输出 double （非标准，但通常也能输出）
    printf("%lf\n", num);  // 输出：3.141590（行为和 %f 一样）
    
    return 0;
}
```

### 3. **`scanf` 与 `printf` 的不同处理**
在 `scanf` 中，`%lf` 是必须的，用来明确区分 `double` 和 `float`。但是 `printf` 中不区分，因此 `%f` 是正确的选择。

### 总结：
- **`printf` 输出 `double` 时，规范推荐使用 `%f`，虽然 `%lf` 也能工作，但不属于标准规定。**
- **`scanf` 中必须使用 `%lf` 来读取 `double` 类型。**

因此，为了编写符合标准的代码，建议在 `printf` 中使用 `%f`，在 `scanf` 中使用 `%lf` 来处理 `double` 类型。


---

所有代码已上传至Github：[***https://github.com/lihongzheshuai/yummy-code***](https://github.com/lihongzheshuai/yummy-code)
