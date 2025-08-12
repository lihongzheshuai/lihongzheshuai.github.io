---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (3-2) 链表-双向链表
date: 2025-08-12 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲]
categories: [GESP, 五级]
---
GESP C++五级官方考试大纲中，共有`9`条考点，本文针对第`3`条考点进行分析介绍。
> （3）掌握链表的创建、插入、删除、遍历和反转操作，理解单链表、双链表、循环链表的区别。
{: .prompt-info}

由于内容比较多，且涉及到代码的编写和验证，本知识点将分单链表、双链表、循环链表3次进行介绍。

> 本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

***五级其他考点回顾：***

> * [【GESP】C++五级考试大纲知识点梳理, (1) 初等数论](https://www.coderli.com/gesp-5-exam-syllabus-elementary-number-theory/)
> * [【GESP】C++五级考试大纲知识点梳理, (2) 模拟高精度计算](https://www.coderli.com/gesp-5-exam-syllabus-simulate-high-precision-arithmetic/)
> * [【GESP】C++五级考试大纲知识点梳理, (3-1) 链表-单链表](https://www.coderli.com/gesp-5-exam-syllabus-linked-list-1-singly/)
{: .prompt-tip}

<!--more-->

---

## 一、双向链表的基本概念

双向链表（Doubly Linked List）是一种链式数据结构，每个节点包含三个部分：

1. **数据域**（data）
2. **前驱指针**（prev）：指向前一个节点
3. **后继指针**（next）：指向下一个节点

相对于单链表，双向链表的优点是可以**双向遍历**，在已知节点指针的情况下，插入和删除效率更高；缺点是需要额外的空间存储 `prev` 指针。

### 1.1 双向链表的特点

| 特性         | 双向链表 |
| ------------ | -------- |
| **指针方向** | 每个节点有 `prev` 和 `next` 两个指针 |
| **优点**     | 支持前后遍历，已知节点指针时插入/删除可 $O(1)$ 完成 |
| **缺点**     | 占用更多内存，实现稍复杂 |

---

## 二、双向链表基本操作

### 2.1 节点定义

```cpp
// 定义双向链表节点结构体
struct DNode {
    int data;         // 数据域
    DNode* prev;      // 指向前一个节点
    DNode* next;      // 指向下一个节点
    // 构造函数
    DNode(int val) : data(val), prev(nullptr), next(nullptr) {}
};
```

---

### 2.2 创建双向链表

创建双向链表主要包含以下几个步骤：

1. **初始化指针**
   * 创建头指针 `head` 和尾指针 `tail`，初始均为空
   * 用于跟踪链表的首尾节点位置

2. **创建新节点**
   * 为每个数据值创建新的节点
   * 设置节点的数据域和指针域

3. **建立节点间连接**
   * 如果是第一个节点：
     * 将头尾指针都指向该节点
   * 如果不是第一个节点：
     * 将新节点的 `prev` 指向当前尾节点
     * 将当前尾节点的 `next` 指向新节点
     * 更新尾指针为新节点

4. **返回链表头**
   * 返回创建完成的链表的头指针

```cpp
// 创建双向链表
// @param vals: 用于创建链表的数据数组
// @return: 返回创建的双向链表头指针
DNode* createDList(const vector<int>& vals) {
    DNode* head = nullptr;  // 头指针，指向链表的第一个节点
    DNode* tail = nullptr;  // 尾指针，指向链表的最后一个节点

    // 遍历输入数组，依次创建节点
    for (int val : vals) {
        DNode* newNode = new DNode(val); // 创建新节点
        if (!head) {
            // 如果是第一个节点，同时更新头尾指针
            head = tail = newNode;
        } else {
            // 否则在尾部追加新节点
            tail->next = newNode;      // 当前尾节点的next指向新节点
            newNode->prev = tail;      // 新节点的prev指向旧尾节点
            tail = newNode;            // 更新尾指针为新节点
        }
    }
    // 返回链表头指针
    return head;
}
```

---

### 2.3 插入节点

#### 2.3.1 在给定位置插入

在给定位置插入节点主要包含以下几个步骤：

1. **判断位置合法性**
   * 如果位置为0，插入头部
   * 如果位置大于链表长度，插入尾部
   * 否则，遍历到指定位置前一个节点

2. **创建新节点**
   * 为新值创建新的链表节点

3. **插入节点**
   * 将新节点插入到目标位置后，更新指针
   * 如果是在头部插入，更新头指针
   * 如果是在中间插入，更新前一个节点的 `next` 指针和新节点的 `prev` 指针
   * 如果是在尾部插入，更新尾指针和前一个节点的 `next` 指针

```cpp
// 在位置pos插入节点（pos从0开始）
// @param head: 双向链表头指针的引用，便于修改头指针
// @param pos: 要插入的位置（0表示头部）
// @param val: 要插入的新节点的值
void insertAtPosition(DNode*& head, int pos, int val) {
    DNode* newNode = new DNode(val);  // 创建新节点

    // 如果插入到头部
    if (pos == 0) {
        newNode->next = head;  // 新节点的next指向原头节点
        if (head) {
            head->prev = newNode;  // 如果原头节点存在，prev指向新节点
        }
        head = newNode;  // 更新头指针为新节点
        return;
    }

    DNode* cur = head;  // 从头节点开始遍历
    // 遍历到插入位置的前一个节点
    for (int i = 0; i < pos - 1 && cur; ++i) {
        cur = cur->next;
    }

    // 如果找到了插入位置的前一个节点
    if (cur) {
        newNode->next = cur->next;      // 新节点的next指向当前位置的下一个节点
        newNode->prev = cur;            // 新节点的prev指向当前位置节点
        if (cur->next)                  // 如果当前位置的下一个节点存在
            cur->next->prev = newNode;  // 下一个节点的prev指向新节点
        cur->next = newNode;            // 当前节点的next指向新节点
    }
}
```

#### 2.3.2 在给定节点后插入

在给定节点后插入新节点主要包含以下几个步骤：

1. **判断目标节点是否为空**
   * 如果目标节点为空，直接返回，不进行插入操作

2. **创建新节点**
   * 为新值创建新的链表节点

3. **插入节点**
   * 将新节点插入到目标位置后，更新指针
   * 新节点的 `next` 指向目标节点的下一个节点
   * 新节点的 `prev` 指向目标节点
   * 如果目标节点的下一个节点存在，更新其 `prev` 指针指向新节点
   * 目标节点的 `next` 指向新节点

```cpp
// 在指定节点后插入新节点
// @param target: 目标节点指针，在其后插入新节点
// @param val: 要插入的新节点的值
void insertAfter(DNode* target, int val) {
    if (!target) {
        return;  // 如果目标节点为空，直接返回
    }

    DNode* newNode = new DNode(val);  // 创建新节点

    // 新节点的next指向目标节点的下一个节点
    newNode->next = target->next;
    // 新节点的prev指向目标节点
    newNode->prev = target;

    // 如果目标节点的下一个节点存在，让其prev指向新节点
    if (target->next)
        target->next->prev = newNode;

    // 目标节点的next指向新节点
    target->next = newNode;
}
```

---

### 2.4 删除节点

#### 2.4.1 删除指定位置

删除指定位置的节点主要包含以下几个步骤：

1. **判断链表是否为空**
   * 如果链表为空，直接返回，不进行删除操作

2. **判断要删除的位置**
   * 如果要删除的位置为0，删除头节点
   * 否则，遍历到指定位置前一个节点

3. **删除节点**
   * 如果要删除的位置前一个节点存在，更新其 `next` 指针指向要删除节点的下一个节点
   * 如果要删除的节点的下一个节点存在，更新其 `prev` 指针指向要删除节点的前一个节点
   * 释放要删除的节点的内存

```cpp
// 删除指定位置的节点
// @param head: 双向链表的头指针的引用
// @param pos: 要删除的节点的位置（从0开始）
void deleteAtPosition(DNode*& head, int pos) {
    if (!head) {
        // 如果链表为空，直接返回
        return;
    }

    DNode* cur = head;  // 用于遍历的指针

    // 如果要删除的是头节点
    if (pos == 0) {
        head = head->next;         // 头指针指向下一个节点
        if (head) {
            head->prev = nullptr;  // 新头节点的prev设为nullptr
        }
        delete cur;                // 释放原头节点
        return;
    }

    // 遍历到要删除的节点
    for (int i = 0; i < pos && cur; ++i) {
        cur = cur->next;
    }

    // 如果找到了要删除的节点
    if (cur) {
        if (cur->prev) {
            cur->prev->next = cur->next;  // 前一个节点的next指向当前节点的下一个节点
        }
        if (cur->next) {
            cur->next->prev = cur->prev;  // 下一个节点的prev指向当前节点的前一个节点
        }
        delete cur;  // 释放当前节点
    }
}
```

#### 2.4.2 删除指定值

删除链表中第一个值为val的节点主要包含以下几个步骤：

1. **判断链表是否为空**
   * 如果链表为空，直接返回，不进行删除操作

2. **遍历链表查找节点**
   * 从头节点开始遍历链表，查找第一个值为val的节点

3. **删除节点**
   * 如果找到该节点，更新前一个节点的next指针指向当前节点的下一个节点
   * 如果要删除的是头节点，更新头指针为下一个节点
   * 如果当前节点不是尾节点，更新下一个节点的prev指针指向当前节点的前一个节点
   * 释放当前节点的内存

```cpp
// 删除链表中第一个值为val的节点
// @param head: 双向链表头指针的引用，便于修改头指针
// @param val: 要删除的节点的值（只删除第一个匹配的节点）
void deleteNode(DNode*& head, int val) {
    DNode* cur = head;  // 用于遍历链表的指针

    // 遍历链表，查找第一个值为val的节点
    while (cur && cur->data != val) {
        cur = cur->next;
    }

    // 如果找到了该节点
    if (cur) {
        // 如果要删除的不是头节点
        if (cur->prev) {
            // 前一个节点的next指向当前节点的下一个节点
            cur->prev->next = cur->next;
        } else {
            // 如果要删除的是头节点，更新头指针
            head = cur->next;
        }

        // 如果当前节点不是尾节点
        if (cur->next) {
            // 下一个节点的prev指向当前节点的前一个节点
            cur->next->prev = cur->prev;
        }

        // 释放当前节点的内存
        delete cur;
    }
}
```

---

### 2.5 遍历链表

#### 2.5.1 正向遍历

正向遍历链表主要包含以下几个步骤：

1. **判断链表是否为空**
   * 如果链表为空，直接返回，不进行遍历操作

2. **遍历链表**
   * 从头节点开始遍历链表，每次移动到下一个节点
   * 输出当前节点的数据
   * 直到遍历到尾节点，结束遍历

```cpp
// 正向遍历双向链表
void traverseForward(DNode* head) {
    // 从头节点开始遍历
    // cur不为空时继续遍历,每次移动到下一个节点
    for (DNode* cur = head; cur; cur = cur->next)
        // 输出当前节点的数据
        cout << cur->data << " ";
    // 换行
    cout << endl;
}
```

#### 2.5.2 反向遍历

反向遍历链表主要包含以下几个步骤：

1. **判断链表是否为空**
   * 如果链表为空，直接返回，不进行遍历操作

2. **遍历链表**
   * 从尾节点开始遍历链表，每次移动到前一个节点
   * 输出当前节点的数据
   * 直到遍历到头节点，结束遍历

```cpp
// 反向遍历双向链表
void traverseBackward(DNode* tail) {
    // 从尾节点开始遍历
    // cur不为空时继续遍历,每次移动到前一个节点
    for (DNode* cur = tail; cur; cur = cur->prev)
        // 输出当前节点的数据
        cout << cur->data << " ";
    // 换行
    cout << endl;
}
```

---

### 2.6 反转链表

反转链表主要包含以下几个步骤：

1. **判断链表是否为空**
   * 如果链表为空，直接返回，不进行反转操作

2. **反转链表**
   * 从头节点开始遍历链表，每次移动到下一个节点
   * 交换当前节点的 `prev` 和 `next` 指针
   * 直到遍历到尾节点，结束遍历
   * 最后返回新的头节点

```cpp
// 反转双向链表
// @param head: 双向链表的头指针
// @return: 反转后的链表头指针
DNode* reverseDList(DNode* head) {
    DNode* cur = head;     // 当前遍历到的节点
    DNode* tmp = nullptr;  // 用于临时保存前驱指针

    // 遍历链表，交换每个节点的prev和next指针
    while (cur) {
        // 先保存当前节点的prev指针（原链表的前驱）
        tmp = cur->prev;
        // 交换当前节点的prev和next指针
        cur->prev = cur->next;
        cur->next = tmp;
        // 移动到下一个节点（由于prev和next已交换，所以用cur->prev）
        cur = cur->prev;
    }

    // 反转过程中，每个节点的prev和next都被交换。
    // 循环结束时，cur为nullptr，tmp为尾节点的前一个节点（原倒数第二个节点）
    // 由于交换了prev和next，tmp->prev实际上指向原链表的最后一个节点（即新链表的头节点5）。
    // 所以需要将head赋值为tmp->prev，才能得到反转后的新头节点。
    if (tmp) {
        head = tmp->prev;
    }
    return head;
}
```

---

{% include custom/custom-post-content-inner.html %}

## 三、总结

* 双向链表的**插入/删除**在已知节点指针的情况下可 $O(1)$ 完成，查找仍为 $O(n)$。
* 额外维护 `prev` 指针，空间占用增加，但功能更强。
* 反向遍历、删除尾节点等操作比单链表方便。

---

## 四、附整体测试代码

```cpp
// 示例用法
int main() {
    // 创建一个包含1~5的整数的vector
    vector<int> vals = {1, 2, 3, 4, 5};
    // 用vector创建双向链表
    DNode* head = createDList(vals);
    // 正向遍历链表并输出
    traverseForward(head);
    // 反向遍历链表并输出（从最后一个节点开始）
    traverseBackward(head->next->next->next->next);

    // 在第2个位置插入值为6的节点
    insertAtPosition(head, 2, 6);
    // 正向遍历链表并输出
    traverseForward(head);

    // 在头部插入值为0的节点
    insertAtPosition(head, 0, 0);
    // 正向遍历链表并输出
    traverseForward(head);

    // 在第3个节点（值为3）后插入值为7的节点
    insertAfter(head->next->next, 7);
    // 正向遍历链表并输出
    traverseForward(head);

    // 删除头节点
    deleteAtPosition(head, 0);
    // 正向遍历链表并输出
    traverseForward(head);

    // 删除中间节点（原第3个节点，现为第2个节点，值为3）
    deleteAtPosition(head, 2);
    // 正向遍历链表并输出
    traverseForward(head);

    // 删除值为7的节点
    deleteNode(head, 7);
    // 正向遍历链表并输出
    traverseForward(head);

    // 删除值为6的节点
    deleteNode(head, 6);
    // 正向遍历链表并输出
    traverseForward(head);

    // 删除值为1的节点
    deleteNode(head, 1);
    // 正向遍历链表并输出
    traverseForward(head);

    // 删除值为0的节点
    deleteNode(head, 0);
    // 正向遍历链表并输出
    traverseForward(head);

    // 删除值为5的节点
    deleteNode(head, 5);
    // 正向遍历链表并输出
    traverseForward(head);

    // 在头部插入值为1的节点
    insertAtPosition(head, 0, 1);
    // 正向遍历链表并输出
    traverseForward(head);

    // 在第4个位置插入值为5的节点
    insertAtPosition(head, 4, 5);
    // 正向遍历链表并输出
    traverseForward(head);

    // 反转链表
    head = reverseDList(head);
    // 正向遍历链表并输出
    traverseForward(head);

    // 程序结束
    return 0;
}
```

**运行结果示例：**

```plaintext
1 2 3 4 5 
5 4 3 2 1
1 2 6 3 4 5
0 1 2 6 3 4 5
0 1 2 7 6 3 4 5
1 2 7 6 3 4 5
1 2 6 3 4 5
1 2 6 3 4 5
1 2 3 4 5
2 3 4 5
2 3 4 5
2 3 4
1 2 3 4
1 2 3 4 5
5 4 3 2 1
```

---

{% include custom/custom-post-content-footer.md %}
