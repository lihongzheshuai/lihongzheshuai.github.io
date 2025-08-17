---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (3-3) 链表-单向循环链表
date: 2025-08-17 08:00 +0800
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
> * [【GESP】C++五级考试大纲知识点梳理, (3-2) 链表-双向链表](https://www.coderli.com/gesp-5-exam-syllabus-linked-list-2-double/)
{: .prompt-tip}

<!--more-->

---

## 一、循环链表的基本概念

循环链表（Circular Linked List）是一种特殊的链表结构，其最后一个节点的指针不为 `nullptr`，而是指向链表的头节点，从而形成一个**环状结构**。

循环链表分为：

1. **单向循环链表**：每个节点只有一个 `next` 指针，指向下一个节点，最后一个节点的 `next` 指向头节点。
2. **双向循环链表**：在双向链表基础上，首尾相连，`head->prev` 指向尾节点，`tail->next` 指向头节点。

---

### 1.1 循环链表的特点

| 特性          | 循环链表 |
| ------------- | -------- |
| **首尾相连**  | 最后节点的 `next`（或 `prev`）指向头节点 |
| **遍历特点**  | 任意节点出发可访问所有节点 |
| **适用场景**  | 约瑟夫问题、循环队列、循环任务调度 |

---

## 二、单向循环链表基本操作

### 2.1 节点定义

```cpp
// 单向循环链表节点
// 循环链表节点结构体定义
struct CNode {
    int data;      // 节点数据
    CNode* next;   // 指向下一个节点的指针
    // 构造函数，初始化节点数据和指针
    CNode(int val) : data(val), next(nullptr) {}
};
```

---

### 2.2 创建单向循环链表

***创建单向循环链表的主要步骤：***

1. 初始化头尾指针为空
2. 遍历输入数组，为每个元素创建新节点
3. 对于第一个节点：
   * 头尾指针都指向它
   * 将节点的next指向自身，形成循环
4. 对于后续节点：
   * 将新节点连接到尾部
   * 更新尾指针
   * 将尾节点的next指向头节点
5. 返回头节点

```cpp
/**
 * 创建单向循环链表
 * @param vals 用于创建链表的数据数组
 * @return 返回创建的循环链表的头节点
 */
CNode* createCList(const vector<int>& vals) {
    // 初始化头尾指针为空
    CNode* head = nullptr;
    CNode* tail = nullptr;

    // 遍历输入数组，逐个创建节点
    for (int val : vals) {
        // 创建新节点
        CNode* newNode = new CNode(val);
        
        if (!head) {
            // 如果是第一个节点，头尾指针都指向它
            head = tail = newNode;
            tail->next = head; // 首尾相连，形成循环
        } else {
            // 非第一个节点，将新节点接到尾部
            tail->next = newNode;
            tail = newNode;
            tail->next = head; // 更新尾节点指向头节点，保持循环特性
        }
    }
    return head;
}
```

---

### 2.3 插入节点

#### 2.3.1 在给定位置插入

***在循环链表指定位置插入新节点的主要步骤：***

1. 创建新节点

   * 分配新节点内存。
   * 为其赋值（`data` 字段）。

2. 判断插入位置

* **pos = 0（头部插入）**
  * 新节点指向原头结点。
  * 找到尾结点（尾节点的 `next` 指向旧头）。
  * 修改尾节点的 `next` 指向新节点。
  * 更新头指针指向新节点。

* **0 < pos（其他位置插入，不考虑pos是否超过链表长度）**

  * 从头结点开始遍历，找到 `pos-1` 位置的节点 `cur`。
  * 让新节点的 `next` 指向 `cur->next`。
  * 再让 `cur->next` 指向新节点。

3. 特殊情况处理

* 特殊情况：如果原链表为空（`head == NULL`），则：
  * 新节点 `next` 指向自己。
  * `head = newNode`。

```cpp
/**
 * 在循环链表指定位置插入新节点
 * @param head 循环链表的头节点引用
 * @param pos 要插入的位置，从0开始
 * @param val 要插入的值
 */
void insertAtPosition(CNode*& head, int pos, int val) {
    // 创建新节点
    CNode* newNode = new CNode(val);

    if (!head) { // 空链表情况处理
        head = newNode;        // 新节点作为头节点
        head->next = head;     // 指向自身形成循环
        return;
    }

    if (pos == 0) { // 在头部插入的情况
        CNode* tail = head;
        // 找到尾节点
        while (tail->next != head) {
            tail = tail->next;
        }
        // 新节点指向原头节点
        newNode->next = head;
        // 尾节点指向新节点
        tail->next = newNode;
        // 更新头节点
        head = newNode;
        return;
    }

    // 找到插入位置的前一个节点
    CNode* cur = head;
    for (int i = 0; i < pos - 1 && cur->next != head; ++i) {
        cur = cur->next;
    }

    // 执行插入操作
    newNode->next = cur->next;     // 新节点指向下一个节点
    cur->next = newNode;           // 当前节点指向新节点
}
```

#### 2.3.2 在指定节点后插入

***在循环链表指定节点后插入新节点的主要步骤：***

1. 检查目标节点是否为空
   * 如果目标节点为空，直接返回

2. 创建新节点
   * 分配新节点内存
   * 初始化新节点的数据字段

3. 调整指针完成插入
   * 新节点的 `next` 指向目标节点的下一个节点
   * 目标节点的 `next` 指向新节点

```cpp
/**
 * 在给定节点后插入新节点
 * @param target 给定节点指针
 * @param val 要插入的值
 */
void insertAfter(CNode* target, int val) {
    // 如果给定节点为空，直接返回空指针
    if (!target) {
        return;
    }

    // 创建新节点
    CNode* newNode = new CNode(val);
    // 新节点的next指向给定节点的下一个节点
    newNode->next = target->next;
    // 给定节点的next指向新节点
    target->next = newNode;
}
```

---

### 2.4 删除节点

#### 2.4.1 删除指定位置

***删除循环链表指定位置节点的主要步骤：***

1. 检查链表是否为空
   * 如果链表为空，直接返回
2. 检查要删除的位置是否为头节点，如果是头节点，特殊处理，即：
   * 找到尾节点
   * 尾节点的 `next` 指向头节点的下一个节点
   * 释放头节点
   * 更新头节点为下一个节点
3. 找到要删除节点的前一个节点
   * 从头节点开始遍历，找到位置 `pos-1` 的节点
4. 检查要删除的节点是否存在
   * 如果 `cur->next` 为空，说明位置无效，直接返回
5. 删除节点
   * 保存要删除节点的指针
   * 当前节点指向下下一个节点
   * 释放要删除节点的内存

```cpp
/**
 * 删除循环链表中给定位置的节点
 * @param head 循环链表的头节点的引用，用于修改头节点
 * @param pos 要删除的节点的位置（从0开始）
 */
void deleteAtPosition(CNode*& head, int pos) {
    // 如果链表为空，直接返回
    if (!head) {
        return;
    }

    // 如果要删除的是头节点
    if (pos == 0) {
        // 如果链表只有一个节点，直接释放头节点
        if (head->next == head) {
            delete head;
            head = nullptr;
            return;
        }
        
        // 找到尾节点
        CNode* tail = head;
        while (tail->next != head)
            tail = tail->next;
        
        // 保存头节点指针
        CNode* tmp = head;
        // 头节点指向下一个节点
        head = head->next;
        // 尾节点的next指向新头节点
        tail->next = head;
        // 释放原头节点
        delete tmp;
        return;
    }

    // 找到要删除的节点的前一个节点
    CNode* cur = head;
    for (int i = 0; i < pos - 1 && cur->next != head; ++i)
        cur = cur->next;

    // 如果找到了要删除的节点（cur->next不为空）
    if (cur->next) {
        // 保存要删除的节点指针
        CNode* tmp = cur->next;
        // 当前节点指向下一个节点
        cur->next = tmp->next;
        // 释放要删除节点
        delete tmp;
    }
}
```

#### 2.4.2 删除指定值的节点

***删除循环链表指定值节点的主要步骤：***

1. 检查链表是否为空
   * 如果链表为空，直接返回

2. 初始化遍历指针
   * 当前指针 `cur` 指向头节点
   * 前驱指针 `prev` 初始化为空

3. 循环遍历链表，直到回到头节点
   * 如果当前节点值等于目标值：
     * 如果是头节点，需要特殊处理：
       * 找到尾节点
       * 更新头节点为下一个节点
       * 更新尾节点的 `next` 指向新头节点
       * 释放原头节点
     * 如果是其他节点：
       * 前驱节点的 `next` 指向当前节点的下一个节点
       * 释放当前节点
       * 更新当前指针为前驱的下一个节点
   * 如果当前节点值不等于目标值：
     * 更新前驱指针为当前节点
     * 移动当前指针到下一个节点

```cpp
/**
 * 删除循环链表中给定值的所有节点
 * @param head 循环链表的头节点的引用，用于修改头节点
 * @param val 要删除的节点的值
 */
void deleteNode(CNode*& head, int val) {
    // 如果链表为空，直接返回
    if (!head) {
        return;
    }

    // 用于遍历链表的指针
    CNode* cur = head;
    // 用于保存前一个节点的指针
    CNode* prev = nullptr;

    do {
        // 如果当前节点的值等于给定值
        if (cur->data == val) {
            // 如果当前节点是头节点
            if (cur == head) {
                // 找到尾节点
                CNode* tail = head;
                while (tail->next != head) {
                    tail = tail->next;
                }
                // 更新头节点为下一个节点
                head = cur->next;
                // 更新尾节点的next指向新头节点
                tail->next = head;
                // 释放原头节点
                delete cur;
                // 移动到下一个节点
                cur = head;
            } else {
                // 将前一个节点的next指向当前节点的下一个节点
                prev->next = cur->next;
                // 释放当前节点
                delete cur;
                // 移动到下一个节点
                cur = prev->next;
            }
        } else {
            // 移动前一个节点指针
            prev = cur;
            // 移动到下一个节点
            cur = cur->next;
        }
    } while (cur != head);
}
```

---

### 2.5 遍历链表

***遍历循环链表的主要步骤：***

1. 检查链表是否为空，若为空则直接返回。
2. 初始化当前指针 `cur` 指向头节点。
3. 从头节点开始循环遍历链表，条件是当前指针 `cur` 不为头节点。
   * 输出当前节点数据。
   * 将当前指针 `cur` 移动到下一个节点。

```cpp
/**
 * 遍历循环链表
 * @param head 循环链表的头节点
 */
void traverseCList(CNode* head) {
    // 空链表直接返回
    if (!head) {
        return;
    }
    
    // 从头节点开始遍历
    CNode* cur = head;
    
    // 使用do-while循环遍历,因为至少要访问一次头节点
    do {
        // 输出当前节点数据
        cout << cur->data << " ";
        // 移动到下一个节点
        cur = cur->next;
    } while (cur != head);  // 当再次回到头节点时停止
    
    // 换行
    cout << endl;
}
```

---

### 2.6 反转单向循环链表

***反转循环链表的主要步骤：***

1. 检查链表是否为空，若为空则直接返回。
2. 初始化三个指针：
   * `prev` 指向 `nullptr`，表示前一个节点为空。
   * `cur` 指向头节点，当前节点指针。
   * `tail` 指向头节点，尾节点指针。
3. 找到尾节点：
   * 循环遍历链表，直到 `tail->next` 指向头节点。
4. 反转链表：
   * 循环遍历链表，直到 `cur` 回到头节点：
     * 保存当前节点的下一个节点指针。
     * 当前节点指向前一个节点或新尾节点。
     * 更新前一个节点指针为当前节点。
     * 更新当前节点指针为下一个节点。
5. 更新头节点：
   * 头节点指向 `prev`，即反转后的新头节点。
6. 返回反转后的头节点。

```cpp
/**
 * 反转循环链表
 * @param head 循环链表的头节点
 * @return 返回反转后的循环链表头节点
 */
CNode* reverseCList(CNode* head) {
    // 特殊情况：空链表或只有一个节点
    if (!head || head->next == head) {
        return head;
    }

    CNode* prev = nullptr;  // 保存前一个节点指针
    CNode* cur = head;      // 当前节点指针
    CNode* tail = head;     // 尾节点指针

    // 找到尾节点
    while (tail->next != head) {
        tail = tail->next;
    }

    do {
        // 保存下一个节点指针
        CNode* nextNode = cur->next;
        // 当前节点指向前一个节点或新尾节点
        cur->next = prev ? prev : tail;
        // 更新前一个节点指针
        prev = cur;
        // 更新当前节点指针
        cur = nextNode;
    } while (cur != head);  // 直到回到头节点

    // 更新头节点
    head = prev;
    // 返回反转后的头节点
    return head;
}
```

---

## 三、总结

* 循环链表**首尾相连**，适合需要循环遍历的场景。
* 单向循环链表与普通单链表的主要区别是尾节点 `next` 指向头节点。
* 反转、插入、删除时要特别注意环结构，防止死循环。

---

## 四、附整体测试代码

```cpp
int main() {
    // 创建一个循环链表，初始值为1，2，3，4，5
    vector<int> vals = {1, 2, 3, 4, 5};
    CNode* head = createCList(vals);
    
    // 遍历循环链表
    traverseCList(head);

    // 在位置0处插入节点0
    insertAtPosition(head, 0, 0);
    // 遍历循环链表
    traverseCList(head);

    // 在位置2处插入节点6
    insertAtPosition(head, 2, 6);
    // 遍历循环链表
    traverseCList(head);

    // 在位置7处插入节点7
    insertAtPosition(head, 7, 7);
    // 遍历循环链表
    traverseCList(head);

    // 在节点2的后面插入节点8
    insertAfter(head->next->next, 8);
    // 遍历循环链表
    traverseCList(head);

    // 删除位置0处的节点
    deleteAtPosition(head, 0);
    // 遍历循环链表
    traverseCList(head);

    // 删除位置7处的节点
    deleteAtPosition(head, 7);
    // 遍历循环链表
    traverseCList(head);

    // 删除值为1的节点
    deleteNode(head, 1);
    // 遍历循环链表
    traverseCList(head);

    // 删除值为6的节点
    deleteNode(head, 6);
    // 遍历循环链表
    traverseCList(head);

    // 删除值为8的节点
    deleteNode(head, 8);
    // 遍历循环链表
    traverseCList(head);

    // 在位置0处插入节点1
    insertAtPosition(head, 0, 1);
    // 遍历循环链表
    traverseCList(head);

    // 反转循环链表
    head = reverseCList(head);
    // 遍历循环链表
    traverseCList(head);
}
```

**运行结果示例：**

```plaintext
1 2 3 4 5 
0 1 2 3 4 5
0 1 6 2 3 4 5
0 1 6 2 3 4 5 7
0 1 6 8 2 3 4 5 7
1 6 8 2 3 4 5 7
1 6 8 2 3 4 5
6 8 2 3 4 5
8 2 3 4 5
2 3 4 5
1 2 3 4 5
5 4 3 2 1
```

---

{% include custom/custom-post-content-footer.md %}
