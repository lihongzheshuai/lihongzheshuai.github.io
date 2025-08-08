---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (3-1) 链表-单链表
date: 2025-08-08 08:00 +0800
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

>本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

***五级其他考点回顾：***

> * [【GESP】C++五级考试大纲知识点梳理, (1) 初等数论](https://www.coderli.com/gesp-5-exam-syllabus-elementary-number-theory/)
> * [【GESP】C++五级考试大纲知识点梳理, (2) 模拟高精度计算](https://www.coderli.com/gesp-5-exam-syllabus-simulate-high-precision-arithmetic/)
{: .prompt-tip}

<!--more-->

---

## 一、链表的基本概念

链表是一种动态数据结构，由一系列节点组成，每个节点包含数据和指向下一个节点（或上一个节点）的指针。与数组相比，链表的优点是插入和删除操作效率较高，但随机访问效率较低。

### 1.1 链表的类型

1. **单链表**：每个节点包含数据和指向下一个节点的指针，最后一个节点的指针指向空（null）。
2. **双链表**：每个节点包含数据、指向下一个节点的指针和指向前一个节点的指针，首节点的上一指针和尾节点的下一指针为空。
3. **循环链表**：单链表或双链表的变种，尾节点的下一指针指向头节点（单循环链表）或头节点的上一指针指向尾节点（双循环链表），形成闭环。

***类型对比小结：***

| 链表类型     | 指针方向         | 特点与应用                     |
| -------- | ------------ | ------------------------- |
| **单链表**  | 每个节点指向下一个节点  | 简单、空间小，但无法从后往前遍历          |
| **双向链表** | 每个节点指向前后两个节点 | 支持双向遍历，插入删除更灵活，但占空间更大     |
| **循环链表** | 尾节点连接头节点形成环  | 适合需要“循环访问”的场景，如约瑟夫问题 |

---

## 二、单链表基本操作

### 2.1 节点定义

```cpp
// 定义链表节点结构体
struct Node {
    int data;      // 节点存储的数据
    Node* next;    // 指向下一个节点的指针
    // 构造函数，初始化节点
    // @param val: 节点的初始值
    Node(int val) : data(val), next(nullptr) {}  // 初始化列表，next指针初始化为空
};
```

---

### 2.2 创建单向链表

创建链表函数主要分为以下几个步骤：

1. **初始化**：创建头指针和尾指针，初始值为空
2. **遍历数据**：遍历输入数组中的每个值
3. **创建节点**：为每个值创建新的链表节点
4. **连接节点**：
   * 如果是第一个节点，同时更新头尾指针
   * 否则将新节点连接到尾部，并更新尾指针
5. **返回结果**：返回链表的头指针

```cpp
// 创建链表函数，使用尾插法
// @param vals: 用于创建链表的数据数组
// @return: 返回创建的链表头指针
Node* createList(const vector<int>& vals) {
    // 初始化头尾指针为空
    Node* head = nullptr;  // 头指针，指向链表的第一个节点
    Node* tail = nullptr;  // 尾指针，指向链表的最后一个节点
    
    // 遍历输入数组，依次创建节点
    for (int val : vals) {
        // 创建新节点
        Node* newNode = new Node(val);
        
        // 如果是第一个节点，同时更新头尾指针
        if (!head) {
            head = newNode;
            tail = newNode;
        }
        // 否则在尾部追加新节点
        else {
            tail->next = newNode;  // 当前尾节点指向新节点
            tail = newNode;        // 更新尾节点指针
        }
    }
    
    // 返回链表头指针
    return head;
}
```

---

### 2.3 插入节点

#### 2.3.1 在给定位置插入

在给定位置插入节点函数主要分为以下几个步骤：

1. **遍历到指定位置**：使用循环遍历链表，找到目标位置的前一个节点。
2. **创建新节点**：为新值创建新的链表节点。
3. **插入节点**：将新节点插入到目标位置后，更新指针。

```cpp
// 在链表指定位置插入节点的函数，位置从0开始
// @param head: 链表头指针的引用，用于修改链表头指针
// @param pos: 插入位置（插入到pos位置，原pos位置的节点后移）
// @param val: 要插入的节点值
void insertAtPosition(Node*& head, int pos, int val) {
    // 从头节点开始遍历
    Node* cur = head;

    // 如果pos为0，插入头节点
    if (pos == 0) {
        Node* newNode = new Node(val);
        newNode->next = head;
        head = newNode;
        return;
    }

    // 遍历到指定位置，同时确保不会访问空指针
    for (int i = 0; i < pos - 1 && cur; ++i) {
        cur = cur->next;
    }

    // 如果找到了指定位置（cur不为空）
    if (cur) {
        // 创建新节点
        Node* newNode = new Node(val);
        // 新节点的next指向当前节点的下一个节点
        newNode->next = cur->next;
        // 当前节点的next指向新节点
        cur->next = newNode;
    }
}
```

#### 2.3.2 在给定节点后插入

在给定节点后插入节点函数主要分为以下几个步骤：

1. **判断给定节点是否为空**：如果给定节点为空，直接返回空指针。
2. **创建新节点**：为新值创建新的链表节点。
3. **插入节点**：将新节点插入到目标位置后，更新指针。

```cpp
// 在给定节点后插入节点的函数
// @param target: 给定节点指针
// @param val: 要插入的节点值
void insertAfter(Node* target, int val) {
    // 如果给定节点为空，直接返回空指针
    if (!target) {
        return;
    }

    // 创建新节点
    Node* newNode = new Node(val);
    // 新节点的next指向给定节点的下一个节点
    newNode->next = target->next;
    // 给定节点的next指向新节点
    target->next = newNode;
}
```

---

### 2.4 删除节点

#### 2.4.1 删除指定位置的节点

删除指定位置节点函数主要分为以下几个步骤：

1. **判断头节点**：如果头节点为空，直接返回空指针。
2. **判断删除头节点**：如果要删除的位置为0，删除头节点，更新头指针。
3. **遍历查找**：从头节点开始遍历，找到要删除位置的前一个节点。
4. **删除节点**：如果找到该节点，将其从链表中移除，释放内存。
   * 保存要删除节点的指针。
   * 更新前一个节点的 next 指针，跳过要删除的节点。
   * 释放要删除节点的内存。

```cpp
// 删除链表中位置pos的节点的函数
// @param head: 链表头指针的引用，用于修改链表头指针
// @param pos: 删除节点的位置（从0开始）
// @return: 返回删除节点后的链表头指针
void deleteAtPosition(Node*& head, int pos) {
    // 如果链表为空，直接返回空指针
    if (!head) {
        return;
    }

    // 如果pos为0，删除头节点
    if (pos == 0) {
        Node* tmp = head;   // 保存头节点指针
        head = head->next;  // 头指针指向下一个节点
        delete tmp;         // 释放原头节点内存
        return;             // 返回新的头指针
    }

    // 遍历链表寻找要删除的节点
    Node* cur = head;
    // 遍历到要删除的节点的前一个节点
    for (int i = 0; i < pos - 1 && cur->next; ++i) {
        cur = cur->next;
    }

    // 如果找到了要删除的节点（cur->next不为空）
    if (cur->next) {
        Node* tmp = cur->next;  // 保存要删除的节点指针
        cur->next = tmp->next;  // 跳过要删除的节点
        delete tmp;             // 释放要删除节点的内存
    }

    return;
}
```

#### 2.4.2 删除指定值的节点

删除指定值节点函数主要分为以下几个步骤：

1. **判断头节点**：如果头节点的值就是要删除的值，直接删除头节点。修改头指针指向头节点的下一个节点。
2. **遍历查找**：从头节点开始遍历，找到值为 val 的节点的前一个节点。
3. **删除节点**：如果找到该节点，将其从链表中移除，释放内存。
   * 保存要删除节点的指针。
   * 更新前一个节点的 next 指针，跳过要删除的节点。
   * 释放要删除节点的内存。。

```cpp
// 删除链表中值为val的节点的函数
// @param head: 链表头指针的引用，用于修改链表头指针
// @param val: 要删除的节点的值
void deleteNode(Node*& head, int val) {
    // 如果链表为空，直接返回空指针
    if (!head) {
        return;
    }

    // 如果头节点就是要删除的节点
    if (head->data == val) {
        Node* tmp = head;   // 保存头节点指针
        head = head->next;  // 头指针指向下一个节点
        delete tmp;         // 释放原头节点内存
        return;             
    }

    // 遍历链表寻找值为val的节点
    Node* cur = head;
    // 当后继节点存在且值不等于val时继续遍历
    while (cur->next && cur->next->data != val) {
        cur = cur->next;
    }

    // 如果找到了值为val的节点（cur->next不为空）
    if (cur->next) {
        Node* tmp = cur->next;  // 保存要删除的节点指针
        cur->next = tmp->next;  // 跳过要删除的节点
        delete tmp;             // 释放要删除节点的内存
    }

    return;
}
```

---

### 2.5 遍历链表

遍历链表函数主要分为以下几个步骤：

1. **初始化**：使用一个指针从链表头开始遍历。
2. **遍历节点**：循环遍历链表，直到指针指向空指针。
3. **访问数据**：在每个节点上访问数据，并打印或处理。
4. **移动指针**：将指针移动到下一个节点。

```cpp
// 遍历链表并打印所有节点的值
// @param head: 链表头指针
void traverse(Node* head) {
    // 从头节点开始遍历，直到遇到空指针
    for (Node* cur = head; cur; cur = cur->next)
        // 打印当前节点的值，并用空格分隔
        cout << cur->data << " ";
    // 遍历结束后换行
    cout << endl;
}
```

---

### 2.6 反转链表

反转链表的主要思想是重新调整节点之间的指向关系，将原本指向后继节点的指针改为指向前驱节点。具体来说：

1. **原始链表结构**：`A->B->C->D->null`，每个节点都指向下一个节点
2. **反转后结构**：`null<-A<-B<-C<-D`，每个节点都指向前一个节点
3. **关键步骤**：
   * 需要记录当前节点的下一个节点（否则改变指针后会丢失）
   * 将当前节点的指针指向前一个节点
   * 依次向后移动，直到处理完所有节点

反转链表函数主要分为以下几个步骤：

1. **初始化**：使用两个指针 `prev` 和 `cur`，分别指向 `nullptr` 和头节点。
2. **遍历链表**：循环遍历链表，直到 `cur` 指向空指针。
3. **反转指针**：在每个节点上，将 `next` 指针指向前一个节点 `prev`。
4. **更新指针**：将 `prev` 移动到当前节点 `cur`，将 `cur` 移动到下一个节点 `next`。
5. **返回新头结点**：循环结束后，`prev` 指向新的头结点。

```cpp
// 反转链表函数，将链表反向连接
// @param head: 链表头指针
// @return: 返回反转后的链表头指针
Node* reverseList(Node* head) {
    // prev指向前一个节点，初始为空
    Node* prev = nullptr;
    // cur指向当前节点，初始为头节点
    Node* cur = head;

    // 遍历链表直到当前节点为空
    while (cur) {
        // 保存下一个节点，因为马上要改变cur->next
        Node* next = cur->next;
        // 反转指针，让当前节点指向前一个节点
        cur->next = prev;
        // prev移动到当前节点
        prev = cur;
        // cur移动到下一个节点
        cur = next;
    }

    return prev;  // 新头结点
}
```

> 注：这里特意采用了返回值的方式来返回新的头结点，代替了之前插入和删除函数里使用的指针引用的方式，在函数内部直接修改外部头指针的指向。个人认为，更易于理解和实现，供参考。
{: .prompt-tip}

---

## 三、总结

* 单链表的插入和删除操作需要找到目标位置的前一个节点，时间复杂度为 $O(n)$。
  * 如果在给定的节点后插入新节点，时间复杂度为 $O(1)$。因为只需要改变指针的指向，不需要移动其他节点。
* 单链表的遍历和反转操作只需要从头节点开始，时间复杂度为 $O(n)$。
* 单链表的空间复杂度为 $O(n)$，每个节点需要额外的指针空间。

## 四、附整体测试代码

```cpp
int main() {
    // 测试用例1: 创建链表
    vector<int> vals1 = {1, 2, 3, 4, 5};
    Node* head1 = createList(vals1);
    traverse(head1);

    // 测试用例2: 在位置0插入值为6的节点
    insertAtPosition(head1, 0, 6);
    traverse(head1);

    // 测试用例3: 在位置2插入值为7的节点
    insertAtPosition(head1, 2, 7);
    traverse(head1);

    // 测试用例4: 在位置2的节点后插入值为7的节点
    Node* target = head1->next->next;
    insertAfter(target, 8);
    traverse(head1);

    // 测试用例5: 删除位置0的节点
    deleteAtPosition(head1, 0);
    traverse(head1);

    // 测试用例6: 删除位置2的节点
    deleteAtPosition(head1, 2);
    traverse(head1);

    // 测试用例7: 删除值为7的节点
    deleteNode(head1, 7);
    traverse(head1);

    // 测试用例8: 反转链表
    Node* head3 = reverseList(head1);
    traverse(head3);

    return 0;
}
```

执行结果如下：

```plaintext
1 2 3 4 5 
6 1 2 3 4 5
6 1 7 2 3 4 5
6 1 7 8 2 3 4 5
1 7 8 2 3 4 5
1 7 2 3 4 5
1 2 3 4 5
5 4 3 2 1
```

---
{% include custom/custom-post-content-footer.md %}
