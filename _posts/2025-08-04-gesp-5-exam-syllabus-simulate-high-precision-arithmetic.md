---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (2) 模拟高精度计算
date: 2025-08-04 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 五级]
---
GESP C++五级官方考试大纲中，共有`9`条考点，本文针对第`2`条考点进行分析介绍。
> （2）掌握 C++数组模拟高精度加法、减法、乘法和除法的相关知识。
{: .prompt-info}

由于本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。

<!--more-->

---

高精度计算在C++中常用数组或字符串按位模拟，当数值过大，超出基本数据类型（如int, long long）范围时，无法直接利用内置数据类型计算，这时需要将数字拆分成数组中的每一位，按位进行加法、减法、乘法和除法运算。下面分别介绍这四种运算。

## 一、高精度加法

### 1.1 高精度加法模拟原理

高精度加法的模拟过程本质是“模拟小学竖式加法”的计算方法。它将大整数拆分成一位一位的数字（通常逆序存储在数组中），然后从最低位依次对应相加，同时处理可能出现的进位，直到最高位。具体来说：

- **分位存储**：将大整数以字符串形式输入后，反转存储到数组，使数组下标0对应个位，方便从低位开始相加。  
- **逐位相加**：从个位开始，将两个数对应位的数字相加，并加上上一位的进位值。  
- **进位处理**：如果某一位的和大于或等于10，就向高一位进1，当前位存余数（即该位对10取模）。  
- **循环至最高位**：依次处理所有位，直到最大位数结束，并处理最后的进位（可能新增一位）。  
- **结果输出**：结果数组中同样是低位在前，输出时逆序打印得到最终和。

### 1.2 高精度加法代码示例

***详细实现步骤如下：***

1. **输入与存储**  
   - 将两个大整数以字符串形式输入，因为基本数据类型无法存储超大数。  
   - 将字符串反向存入数组中，个位数字存入数组0号位置，往高位递增存放。这样做是为了方便从低位开始加法运算和处理进位。

2. **准备变量**  
   - 准备三个数组，分别存储两个加数和结果。  
   - 确定两个字符串的长度，取两者最大长度maxLen，控制加法循环次数。  
   - 准备一个变量carry存储进位，初始为0。

3. **逐位相加**  
   - 从数组的0号位置（最低位）开始逐位相加：  
     `sum = a[i] + b[i] + carry`  
   - 将当前位的结果存入结果数组：`c[i] = sum % 10`  
   - 更新进位：`carry = sum / 10`  
   - 注意某一加数位可能没有数据时，视为0。

4. **处理最后进位**  
   - 如果循环结束后carry不为0，说明最高位有进位，存入结果数组的最高位。

5. **输出结果**  
   - 结果数组存储同样是低位到高位，输出时逆序打印结果数组从最高位到最低位即可。

```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

// 定义数组最大长度
const int N = 1e5 + 10;
// 定义三个数组分别存储两个加数和结果
int a[N] = {0}, b[N] = {0}, c[N] = {0};

int main() {
    // 输入两个大整数字符串
    string s1, s2;
    cin >> s1 >> s2;

    // 获取两个字符串的长度
    int len1 = (int)s1.size();
    int len2 = (int)s2.size();

    // 将第一个数字反向存入数组a，个位存在a[0]
    for (int i = 0; i < len1; i++) {
        a[i] = s1[len1 - 1 - i] - '0';
    }
    
    // 将第二个数字反向存入数组b，个位存在b[0]
    for (int i = 0; i < len2; i++) {
        b[i] = s2[len2 - 1 - i] - '0';
    }

    // 取两个数字的最大长度
    int maxLen = max(len1, len2);
    // 进位标志
    int carry = 0;
    
    // 从低位到高位逐位相加
    for (int i = 0; i < maxLen; i++) {
        // 当前位相加结果，包含进位
        int temp = a[i] + b[i] + carry;
        // 当前位保存个位数
        c[i] = temp % 10;
        // 更新进位
        carry = temp / 10;
    }
    
    // 处理最高位的进位
    if (carry) {
        c[maxLen++] = carry;
    }

    // 从高位到低位输出结果
    for (int i = maxLen - 1; i >= 0; i--) {
        cout << c[i];
    }
    cout << endl;

    return 0;
}
```

---

## 二、高精度减法

### 2.1 高精度减法模拟原理

高精度减法的模拟过程本质是“模拟小学竖式减法”的计算过程，用数组逐位储存大数各位数字，从低位开始逐位相减，遇到被减数当前位小于减数当前位时，向高一位借位，当前位加10继续减法运算。具体来说：

- **数据存储**：将大整数以字符串形式输入后，逆序存储在数组中，使得数组下标0对应个位数字，方便从低位向高位处理。  
- **逐位减法**：从最低位开始对应位相减，若当前位被减数小于减数，则向高位借位（即高一位被减数减1，本位加10），保证本位减法可执行。  
- **借位机制**：借位是高精度减法的关键，类似手工竖式减法中因不足以减去当前位数字而从高位借1。  
- **前导零处理**：最后需要去除结果最高位的多余零（前导零），保持结果的正确性和简洁性。  
- **符号处理**：如果被减数小于减数，需先判断大小，交换两数，计算差值后结果带负号。

### 2.2 高精度减法代码示例

***详细实现步骤如下：***

1. **输入与存储**
    - 将被减数和减数以字符串形式输入。
    - 判断两数大小，若被减数小于减数，则交换并记录结果需要取负号。
    - 将两个数逆序存入数组，个位对应数组0号位置，方便从低位开始处理。
2. **逐位减法模拟**
    - 从最低位开始逐位相减：`c[i] = a[i] - b[i]`。
    - 当`a[i] < b[i]`时，需要向`a[i+1]`借位，即`a[i+1] -= 1`，然后`a[i] += 10`再继续减。
    - 借位操作保证每一位减法正确。
3. **去除高位多余的零**
    - 结果可能会带有前导零，如`000123`，需去掉这些多余的零，保留至少一位。
    - 遍历结果数组最高位向低位，删除所有多余的零。
4. **输出结果**
    - 如果前面判断过被减数小于减数，输出负号。
    - 逆序输出结果数组。

```cpp
#include <iostream>
#include <string>
#include <algorithm>
#include <cstring>
using namespace std;

// 定义数组最大长度，可以处理10^5位的大数
const int N = 1e5 + 10;
// 定义三个数组，分别存储被减数、减数和差
int a[N], b[N], c[N];

int main() {
    // 输入两个大整数字符串
    string s1, s2;
    cin >> s1 >> s2;

    // 判断大小，决定是否需要负号并交换
    bool negative = false;
    // 如果s1的位数小于s2，或位数相等但s1小于s2
    if (s1.size() < s2.size() || (s1.size() == s2.size() && s1 < s2)) {
        swap(s1, s2);     // 交换两个字符串
        negative = true;  // 标记结果需要加负号
    }

    // 获取两个字符串的长度
    int len1 = (int)s1.size();
    int len2 = (int)s2.size();

    // 逆序存入数组，将个位存在数组0号位置
    for (int i = 0; i < len1; i++) {
        a[i] = s1[len1 - 1 - i] - '0';  // 字符转数字需要减去字符'0'
    }
    for (int i = 0; i < len2; i++) {
        b[i] = s2[len2 - 1 - i] - '0';
    }

    // 逐位相减并处理借位
    for (int i = 0; i < len1; i++) {
        // 当前位相减，注意减数可能已经用完，用0补充
        c[i] = a[i] - (i < len2 ? b[i] : 0);
        
        // 如果当前位结果小于0，需要向高位借位
        if (c[i] < 0) {
            c[i] += 10;        // 当前位加10
            a[i + 1]--;        // 向高一位借1
        }
    }

    // 去除高位多余的零
    int len = len1;
    // 如果最高位是0且长度大于1，则继续去除
    while (len > 1 && c[len - 1] == 0) {
        len--;
    }

    // 输出结果
    if (negative) {
        cout << '-';  // 如果之前判断需要负号，先输出负号
    }
    // 从高位到低位输出结果
    for (int i = len - 1; i >= 0; i--) {
        cout << c[i];
    }
    cout << endl;

    return 0;
}
```

{% include custom/custom-post-content-inner.html %}

---

## 三、高精度乘法

### 3.1 高精度乘法模拟原理

高精度乘法的模拟过程本质是“模拟小学竖式乘法”，用数组逐位存储大整数的每一位数字，从低位到高位，进行逐位相乘并错位累加，最后统一处理进位，得到乘积。具体原理如下：

- **位数拆分与存储**：将两个大整数字符串逆序存入数组，便于按位计算，数组下标0代表数字的个位。  
- **逐位乘法与累加**：每位数字相乘后的结果根据两因数对应位的下标和确定乘积在结果数组中的位置（即数组下标为两个位下标之和），模拟手工乘法中错位相加的过程。  
- **进位处理**：乘积数组中可能出现大于10的数，需要类似加法逐位处理进位，保证每位数字在0-9之间。  
- **结果整理**：去除最高位多余的零，将数组结果逆序输出即为最终乘法结果。、

### 3.2 高精度乘法代码示例

***详细实现步骤如下：***

1. **高精度数字的存储**
将两个大整数以字符串形式输入，逆序存入数组中，使得数组下标0对应个位数字（最小位），方便从低位向高位计算。
2. **逐位乘法及累加**
双层循环遍历两个数组的每个位数字，相乘后将结果累加到对应的结果数组位置。
    - 对于第i位和第j位数字相乘，乘积累加到结果数组的第`i+j`位（模拟竖式乘法的位移）。
    - 累加时注意，因为可能对应位已有数值累计，多次累加需要正确相加。
3. **统一进位处理**
乘积累加后，结果数组中的某些位可能大于10，需要从低位开始逐位进位处理：
    - 当前位置数字除以10的商作为进位加到下一位，余数保留在当前位，保证每个位数字在0~9范围。
4. **去除前导零与输出**
计算结束后，可能在结果高位有多余的0，需删除（至少保留一位0表示结果为零）。
结果数组逆序输出即为最终正确的乘积。

```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

// 定义最大位数，N 足够大以支持高精度乘法
const int N = 1e5 + 5;
int a[N], b[N], c[N];

int main() {
    string s1, s2;
    // 输入两个大整数（以字符串形式）
    cin >> s1 >> s2;

    // 获取两个字符串的长度
    int len1 = (int) s1.size();
    int len2 = (int) s2.size();

    // 将输入的字符串逆序存入数组 a 和 b
    // 这样最低位在数组下标 0，方便后续计算
    for (int i = 0; i < len1; i++) {
        a[i] = s1[len1 - 1 - i] - '0'; // 字符转数字并逆序
    }
    for (int i = 0; i < len2; i++) {
        b[i] = s2[len2 - 1 - i] - '0'; // 字符转数字并逆序
    }

    // 高精度乘法核心：逐位相乘并累加到结果数组 c
    // c[i + j] 存储 a[i] * b[j] 的结果
    for (int i = 0; i < len1; i++) {
        for (int j = 0; j < len2; j++) {
            c[i + j] += a[i] * b[j];
        }
    }

    // 处理进位
    // 如果某一位大于等于 10，则向高位进位
    int len = len1 + len2; // 结果最大长度
    for (int i = 0; i < len; i++) {
        if (c[i] >= 10) {
            c[i + 1] += c[i] / 10; // 进位到高一位
            c[i] %= 10;            // 当前位只保留个位数
        }
    }

    // 去除结果前导零（高位多余的 0）
    while (len > 1 && c[len - 1] == 0) {
        len--;
    }

    // 逆序输出最终结果（高位到低位）
    for (int i = len - 1; i >= 0; i--) {
        cout << c[i];
    }
    cout << endl;

    return 0;
}
```

---

## 四、高精度除法

### 4.1 高精度除法模拟原理

高精度除法是四种运算中最难的，过程最复杂的。

高精度除法的模拟过程本质是“模拟小学竖式除法”的手工计算方法，但作用于超大整数。本质上，高精度除法是“用连续的高精度减法反复试商，结合被除数从高位向低位逐步推进”，模拟了手工竖式除法的思想。具体如下：

1. **数据表示**  
   被除数通常以字符串形式输入。对应地，用数组存储每一位数字。

2. **试商和减法**  
   - 从被除数高位开始取足够的位数构成当前的“部分被除数”  
   - 用高精度减法不断减去除数，计算当前“部分被除数”能够减去除数多少次，这个次数即为当前商位的数字（试商）  
   - 更新部分被除数为减去的余数  
   - 依次移动被除数的下一位，重复上述过程，直到处理完整个被除数

3. **逐位得到商**  
   通过试商和高精度减法迭代，逐位得到商的每一位，同时维护剩余的余数。

4. **余数和商的整洁输出**  
   - 可能有前导零，需要跳过或处理，保证输出正常的商与余数  
   - 余数即最后剩余的部分被除数

### 4.2 高精度除法代码示例

***详细实现步骤如下：***

1. **数据结构定义**
   - 定义数组最大长度常量 `N`
   - 定义被除数数组 `a[]`、除数数组 `b[]`、商数组 `res[]`
   - 定义临时余数数组 `tmp[]`

2. **核心辅助函数定义**
   - `compare()` 函数：比较两个高精度数的大小
   - `subtract()` 函数：高精度减法运算
   - `add()` 函数：高精度加法运算
   - `push_digit()` 函数：向临时余数数组添加新的数位
   - `trial_divide()` 函数：试商过程，确定当前位的商
   - `read_and_reverse()` 函数：读取输入并逆序存储
   - `print_bigint()` 函数：正序输出高精度整数
   - `print_bigint_reverse()` 函数：逆序输出高精度整数

3. **读取和预处理阶段**
     - 使用`read_and_reverse()`函数读取被除数和除数字符串，并逆序存储到数组中
     - 初始化临时余数数组`tmp[]`和商数组`res[]`

4. **主要除法流程**
     - 从被除数最高位开始，依次处理每一位数字
     - 使用`push_digit()`函数将当前处理位加入临时余数
     - 调用`trial_divide()`函数进行试商，确定当前位的商值
     - 将试商得到的商存入结果数组`res[]`
     - 用`subtract()`函数从临时余数中减去(商×除数)的结果
     - 重复以上步骤直到处理完被除数的所有位

5. **结果处理与输出**
     - 去除商的前导零
     - 正序输出商的每一位
     - 使用`print_bigint_reverse()`函数输出最终余数

```cpp
#include <iostream>
#include <cstring>
using namespace std;

// N 表示高精度整数的最大位数（数组长度）
const int N = 1e5 + 5;

// a: 被除数A（高精度整数，低位在下标0）
// b: 除数B（高精度整数，低位在下标0）
// res: 商（高精度整数，低位在下标0）
// tmp: 当前余数（高精度整数，低位在下标0）
int a[N], b[N], res[N];
int tmp[N];

/**
 * 比较两个高精度整数A和B
 * @param A 高精度整数A的数组（低位在下标0）
 * @param la A的长度（有效位数）
 * @param B 高精度整数B的数组
 * @param lb B的长度
 * @return 1: A > B, 0: A == B, -1: A < B
 * 
 * 算法说明：
 * 1. 先比较长度，长度大的数更大。
 * 2. 长度相等时，从高位到低位逐位比较。
 */
int compare(int A[], int la, int B[], int lb) {
    if (la != lb) {
        return la > lb ? 1 : -1;
    }
    for (int i = la - 1; i >= 0; i--) {
        if (A[i] != B[i]) {
            return A[i] > B[i] ? 1 : -1;
        }
    }
    return 0;
}

/**
 * 高精度减法：A -= B，结果保存在A中（假设A >= B）
 * @param A 被减数数组，结果也保存在A中
 * @param la A的长度，按引用传递，可能会减少
 * @param B 减数数组
 * @param lb B的长度
 * 
 * 算法说明：
 * 逐位相减，若当前位不够减则向高位借1（即+10，下一位-1）。
 * 最后去除高位多余的0。
 */
void subtract(int A[], int &la, int B[], int lb) {
    for (int i = 0; i < la; i++) {
        A[i] -= (i < lb ? B[i] : 0); // 若B位数不够则补0
        if (A[i] < 0) {
            A[i] += 10;
            A[i + 1]--;
        }
    }
    // 去除高位多余的0，保证最高位不是0（除非结果为0）
    while (la > 1 && A[la - 1] == 0) {
        la--;
    }
}

/**
 * 向tmp[]右移一位并添加一个新数字
 * @param tmp 当前余数数组（低位在下标0）
 * @param lt 当前余数长度，按引用传递
 * @param digit 要添加的新数字（来自被除数a的高位）
 * 
 * 算法说明：
 * 1. 所有位右移一位，为新数字腾出空间。
 * 2. 新数字放在最低位（下标0）。
 * 3. 更新余数长度lt。
 * 4. 去除高位多余的0。
 */
void push_digit(int tmp[], int &lt, int digit) {
    for (int i = lt; i > 0; i--) {
        tmp[i] = tmp[i - 1];
    }
    tmp[0] = digit;
    lt++;
    // 去除高位多余的0
    while (lt > 1 && tmp[lt - 1] == 0) {
        lt--;
    }
}

/**
 * 高精度加法：C = A + B
 * @param A 数组A（低位在下标0）
 * @param la A的长度
 * @param B 数组B
 * @param lb B的长度
 * @param C 结果数组C
 * @param lc 结果长度，按引用传递
 * 
 * 算法说明：
 * 逐位相加，处理进位，结果存入C。
 */
void add(const int A[], int la, const int B[], int lb, int C[], int &lc) {
    int carry = 0; // 进位
    int len = max(la, lb); // 取较大长度
    for (int i = 0; i < len; ++i) {
        int ai = (i < la) ? A[i] : 0;
        int bi = (i < lb) ? B[i] : 0;
        int val = ai + bi + carry;
        C[i] = val % 10;
        carry = val / 10;
    }
    lc = len;
    if (carry) {
        C[lc++] = carry;
    }
    // 去除高位多余的0
    while (lc > 1 && C[lc - 1] == 0) {
        lc--;
    }
}

/**
 * 试除法，返回当前位的商x和sum = x * B
 * @param tmp 当前余数（低位在下标0）
 * @param lt 当前余数长度
 * @param b 除数（低位在下标0）
 * @param lb 除数长度
 * @param sum 存放x*B
 * @param len_sum sum的长度
 * @return x 当前位的商
 * 
 * 算法说明：
 * 1. 从x=0开始，累加b到local_sum，直到local_sum > tmp。
 * 2. x为能减去的最大次数，sum为x*b。
 * 3. 该过程等价于用加法模拟减法，效率较低但易于理解（二分查找法效率更高，只是暂未学到：）。
 */
int trial_divide(int tmp[], int lt, const int b[], int lb, int sum[], int &len_sum) {
    int x = 0; // 当前位的商
    int local_sum[N] = {0}; // 累加b的结果，表示x*b
    int len_local_sum = 0;  // local_sum的长度

    while (true) {
        int sum2[N] = {0}; // sum2用于存储local_sum + b的结果
        int len_sum2 = 0;  // sum2的实际长度

        // 将local_sum与b相加，结果存入sum2
        add(local_sum, len_local_sum, b, lb, sum2, len_sum2);

        // 如果tmp >= sum2，说明还可能继续加一次b
        if (compare(tmp, lt, sum2, len_sum2) >= 0) {
            // 更新local_sum为sum2，即local_sum += b
            for (int j = 0; j < len_sum2; ++j) {
                local_sum[j] = sum2[j];
            }
            len_local_sum = len_sum2; // 更新local_sum的长度
            x++; // 商加1
        } else {
            // 如果tmp < sum2，不能再加，退出循环
            break;
        }
    }
    // 将local_sum（即x*b的结果）复制到sum数组中
    for (int j = 0; j < len_local_sum; ++j) {
        sum[j] = local_sum[j];
    }
    // 设置sum的实际长度
    len_sum = len_local_sum;
    // 返回当前位的商x
    return x;
}

/**
 * 读取输入并逆序存入数组
 * @param s 输入字符串（高位在前，低位在后）
 * @param arr 存放数字的数组（低位在下标0）
 * @return 数组长度
 * 
 * 算法说明：
 * 1. 从字符串末尾到开头依次存入arr，保证arr[0]为最低位。
 */
int read_and_reverse(const string &s, int arr[]) {
    int len = (int)s.length();
    for (int i = 0; i < len; ++i) {
        arr[len - 1 - i] = s[i] - '0';
    }
    return len;
}

/**
 * 输出高精度整数（高位在前，低位在后）
 * @param arr 数组
 * @param len 长度
 */
void print_bigint(const int arr[], int len) {
    for (int i = 0; i < len; ++i) {
        cout << arr[i];
    }
}

/**
 * 输出高精度整数（逆序，低位在前，高位在后）
 * @param arr 数组
 * @param len 长度
 */
void print_bigint_reverse(const int arr[], int len) {
    for (int i = len - 1; i >= 0; --i) {
        cout << arr[i];
    }
}

int main() {
    // sa, sb为输入的被除数和除数（字符串形式）
    string sa, sb;
    cin >> sa >> sb;

    // la, lb分别为a, b的长度
    int la = read_and_reverse(sa, a);
    int lb = read_and_reverse(sb, b);

    int lt = 0, lr = 0; // lt: 余数长度, lr: 商长度

    // 执行高精度除法
    // 从a的最高位（la-1）到最低位（0）依次处理
    for (int i = la - 1; i >= 0; i--) {
        // 将a[i]加入余数tmp，右移一位
        push_digit(tmp, lt, a[i]);
        int sum[N] = {0}; // 存放x*b
        int len_sum = 0;
        // 试除，得到当前位的商x和x*b
        int x = trial_divide(tmp, lt, b, lb, sum, len_sum);
        res[lr++] = x; // 存入商
        // 用高精度减法更新余数
        subtract(tmp, lt, sum, len_sum);
    }

    // 去除商的前导0（高位的0）
    int p = 0;
    while (p < lr - 1 && res[p] == 0) {
        p++;
    }

    // 输出商（高位在前，低位在后）
    for (int i = p; i < lr; i++) {
        cout << res[i];
    }
    cout << '\n';

    // 输出余数
    cout << "Remainder: ";
    if (lt == 0) {
        cout << 0;
    } else {
        // 余数逆序输出（高位在前）
        print_bigint_reverse(tmp, lt);
    }
    cout << '\n';

    return 0;
}
```

## 五、总结

| 操作 | 难点        | 时间复杂度 |
| -- | --------- | ----- |
| 加法 | 进位处理      | $O(n)$  |
| 减法 | 借位处理      | $O(n)$  |
| 乘法 | 进位处理，多重循环 | $O(n^2)$ |
| 除法 | 高位逐位除     | $O(n)$  |

---
{% include custom/custom-post-content-footer.md %}
