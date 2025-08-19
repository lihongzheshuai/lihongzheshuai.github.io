---
layout: post
title: 【GESP】C++五级考试大纲知识点梳理, (3-4) 链表-双向循环链表
date: 2025-08-19 08:00 +0800
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
> * [【GESP】C++五级考试大纲知识点梳理, (3-3) 链表-单向循环链表](https://www.coderli.com/gesp-5-exam-syllabus-3-linked-list-3-singly-circle/)
{: .prompt-tip}

<!--more-->

---

## 一、概念与特点

**双向循环链表（Doubly Circular Linked List, DCLL）** 是 **双向链表** 和 **循环链表** 的结合体：

* 每个节点包含 **数据域** 和两个 **指针域**：

  * `prev` → 指向前驱节点
  * `next` → 指向后继节点
* 链表首尾相接：

  * `head->prev` 指向最后一个节点
  * `tail->next` 指向头节点

🔑 特点：

1. **可双向遍历**（前后自由移动）。
2. **首尾相连**（形成闭环，无需判空尾结点）。
3. **插入、删除更灵活**，特别是在首尾操作时无需特殊处理。

---

## 二、逻辑结构图

假设链表包含 3 个节点：A、B、C

```plaintext
      ┌─────┐      ┌─────┐      ┌─────┐
      │  A  │ <--> │  B  │ <--> │  C  │
      └─────┘      └─────┘      └─────┘
        ↑ ↓                         ↑ ↓
          └────────────►────────────┘ 
        └───────────────◄─────────────┘
```

* `A.prev = C`
* `C.next = A`

---

## 三、基本操作

### 3.1 节点结构定义

```cpp
struct Node {
    // 节点数据域
    int data;
    // 指向前驱节点的指针
    Node* prev;
    // 指向后继节点的指针
    Node* next;
    // 构造函数，初始化节点
    // @param val: 节点数据值
    Node(int val) : data(val), prev(nullptr), next(nullptr) {}
};
```

### 3.2 创建双向循环链表

***创建双向循环链表的主要步骤：***

1. **检查输入数组是否为空**：
   * 如果数组为空，直接返回空指针。
2. **创建头节点**：
   * 初始化头节点，数据域为数组第一个元素。
3. **初始化尾指针**：
   * 尾指针指向头节点，后续节点将连接到这里。
4. **遍历数组创建节点**：
   * 从数组第二个元素开始，创建新节点。
   * 尾节点的 `next` 指向新节点。
   * 新节点的 `prev` 指向当前尾节点。
   * 更新尾节点为新节点。
5. **首尾相连**：
   * 头节点的 `prev` 指向尾节点，尾节点的 `next` 指向头节点，形成循环。
6. **返回头指针**：
   * 完成链表创建，返回头节点指针。

```cpp
/**
 * 创建一个双向循环链表（Doubly Circular Linked List）
 * @param arr 输入的整型数组，用于初始化链表节点的数据域
 * @return 返回链表头指针，若数组为空则返回nullptr
 */
Node* createDCLL(std::vector<int> arr) {
    // 如果输入数组为空，直接返回空指针
    if (arr.empty()) {
        return nullptr;
    }

    // 创建头节点，并初始化尾指针
    Node* head = new Node(arr[0]);
    Node* tail = head;

    // 依次创建后续节点，并连接前后指针
    for (int i = 1; i < arr.size(); i++) {
        Node* newNode = new Node(arr[i]); // 新节点
        tail->next = newNode;             // 当前尾节点的next指向新节点
        newNode->prev = tail;             // 新节点的prev指向当前尾节点
        tail = newNode;                   // 更新尾节点为新节点
    }

    // 将链表首尾相连，形成循环
    // 头节点的prev指向尾节点
    head->prev = tail;  
    // 尾节点的next指向头节点
    tail->next = head;

    // 返回头指针
    return head;
}
```

---

### 3.3  插入节点

#### 3.3.1 在给定位置插入

***在双向循环链表指定位置插入新节点的主要步骤：***

1. **创建新节点**：
   * 初始化新节点，数据域为指定值。
2. **处理头节点插入**：
   * 如果要插入的位置是头节点（`pos == 0`），则：
     * 新节点的 `next` 指向当前头节点。
     * 新节点的 `prev` 指向当前头节点的 `prev`（即原尾节点）。
     * 原头节点的 `prev` 的 `next` 指向新节点。
     * 更新头节点的 `prev` 为新节点。
     * 更新头指针为新节点。
3. **遍历到指定位置**：
   * 从头节点开始遍历，移动 `pos - 1` 次，到达要插入位置的前一个节点。
   * 如果遍历到 `nullptr`，说明位置无效，直接返回。
4. **插入新节点**：
   * 新节点的 `next` 指向当前位置的下一个节点。
   * 新节点的 `prev` 指向当前位置节点。
   * 如果当前位置的下一个节点存在，更新其 `prev` 为新节点。
   * 更新当前位置的下一个节点为新节点。

```cpp
/**
 * 在双向循环链表指定位置插入新节点
 * @param head 双向循环链表的头指针的引用，用于修改头指针
 * @param pos 要插入的位置（从0开始）
 * @param val 要插入的节点的数据域值
 */
void insertAtPosition(Node*& head, int pos, int val) {
    // 创建新节点
    Node* newNode = new Node(val);

    if (pos == 0) {
        // 如果要插入的是头节点
        newNode->next = head;  // 新节点的next指向原头节点
        newNode->prev = head->prev;  // 新节点的prev指向原头节点的prev
        head->prev->next = newNode;  // 原头节点的prev的next指向新节点
        head->prev = newNode;  // 更新头节点的prev为新节点
        head = newNode;  // 更新头指针为新节点
        return;
    }

    Node* cur = head;  // 从头节点开始遍历
    for (int i = 0; i < pos - 1 && cur; ++i) {
        cur = cur->next;
    }

    // 如果找到了要插入的位置（cur不为空）
    if (cur) {
        newNode->next = cur->next;  // 新节点的next指向当前位置的下一个节点
        newNode->prev = cur;  // 新节点的prev指向当前位置节点
        if (cur->next) {  // 如果当前位置的下一个节点存在
            cur->next->prev = newNode;  // 下一个节点的prev指向新节点
        }
        cur->next = newNode;  // 当前节点的next指向新节点
    }
}
```

#### 3.3.2 在指定节点后插入

***在双向循环链表指定节点后插入新节点的主要步骤：***

1. **创建新节点**：
   * 初始化新节点，数据域为指定值。
2. **处理指定节点为空**：
   * 如果指定节点为空，直接返回。
3. **插入新节点**：
   * 新节点的 `next` 指向指定节点的下一个节点。
   * 新节点的 `prev` 指向指定节点。
   * 指定节点的下一个节点的 `prev` 指向新节点。
   * 指定节点的 `next` 指向新节点。

```cpp
/**
 * 在指定节点后插入新节点
 * @param head 双向循环链表的头指针的引用，用于修改头指针
 * @param pos 要插入的节点指针，在其后插入新节点
 * @param val 要插入的节点的数据域值
 */
void insertAfter(Node*& head, Node* pos, int val) {
    // 如果指定节点为空，直接返回
    if (!pos) {
        return;
    }

    // 创建新节点
    Node* newNode = new Node(val);

    // 新节点的next指向指定节点的next
    newNode->next = pos->next;

    // 新节点的prev指向指定节点
    newNode->prev = pos;

    // 指定节点的next的prev指向新节点
    pos->next->prev = newNode;

    // 指定节点的next指向新节点
    pos->next = newNode;
}
```

### 3.4 删除节点

#### 3.4.1 删除指定位置

***删除双向循环链表指定位置节点的核心步骤：***

1. **空链表判断**：
   * 检查链表是否为空，为空则直接返回。

2. **头节点删除处理**：
   * 找到尾节点（`head->prev`）。
   * 更新尾节点的 `next` 和新头节点的 `prev` 指针。
   * 释放原头节点内存。
   * 更新头指针。
   * 更新新头节点的 `prev` 为原头节点的 `prev`（即原尾节点）。

3. **非头节点删除**：
   * 遍历定位到目标位置的前一个节点。
   * 检查位置是否有效。

4. **执行删除操作**：
   * 暂存待删除节点。
   * 将当前节点的 `next` 指向待删除节点的下一个节点。
   * 将待删除节点的下一个节点的 `prev` 指向当前节点。
   * 释放目标节点内存。

```cpp
/**
 * 删除双向循环链表指定位置的节点
 * @param head 双向循环链表的头指针的引用，用于修改头指针
 * @param pos 要删除的位置（从0开始）
 */
void deleteAtPosition(Node*& head, int pos) {
    // 如果链表为空，直接返回
    if (!head) {
        return;
    }

    // 如果要删除的是头节点
    if (pos == 0) {
        // 找到尾节点
        Node* tail = head->prev;
        // 尾节点的next指向头节点的下一个节点
        tail->next = head->next;
        // 释放头节点
        delete head;
        // 更新头指针为下一个节点
        head = tail->next;
        // 更新头节点的prev为新头节点的prev（即原尾节点）
        head->prev = tail;
        return;
    }

    // 遍历到指定位置
    Node* cur = head;
    for (int i = 0; i < pos - 1 && cur; ++i) {
        cur = cur->next;
    }

    // 如果找到了要删除的位置（cur不为空）
    if (cur) {
        // 保存要删除节点的指针
        Node* toDelete = cur->next;
        // 当前节点指向下下一个节点
        cur->next = toDelete->next;
        // 释放要删除节点的内存
        delete toDelete;
        // 更新当前节点的prev指向要删除节点的prev
        cur->next->prev = cur;
        return;
    }
}
```

#### 3.4.2 删除指定值的节点

***删除双向循环链表指定值的节点的主要步骤：***

1. **空链表判断**：
   * 检查链表是否为空，为空则直接返回。

2. **遍历链表**：
   * 使用 `cur` 指针遍历链表。
   * 使用 `prev` 指针记录前一个节点。
   * 使用 `do-while` 循环确保遍历一圈。

3. **头节点删除处理**：
   * 找到尾节点（`head->prev`）。
   * 更新头指针为下一个节点。
   * 更新尾节点的 `next` 指向新头节点。
   * 释放原头节点内存。
   * 更新新头节点的 `prev` 为原尾节点。

4. **非头节点删除**：
   * 更新前一个节点的 `next` 指向当前节点的下一个节点。
   * 释放当前节点内存。
   * 更新下一个节点的 `prev` 指向前一个节点。
   * 移动指针到下一个节点。

5. **继续遍历**：
   * 如果当前节点值不等于目标值：
     * 更新 `prev` 为当前节点。
     * 移动 `cur` 到下一个节点。

```cpp
/**
 * 删除双向循环链表中指定值的所有节点
 * @param head 双向循环链表的头指针的引用，用于修改头指针
 * @param val 要删除的节点的值
 */
void deleteNode(Node*& head, int val) {
    // 如果链表为空，直接返回
    if (!head) {
        return;
    }

    // 用于遍历链表的指针
    Node* cur = head;
    // 用于保存前一个节点的指针
    Node* prev = nullptr;

    do {
        // 如果当前节点的值等于给定值
        if (cur->data == val) {
            // 如果当前节点是头节点
            if (cur == head) {
                // 找到尾节点
                Node* tail = head->prev;
                // 更新头节点为下一个节点
                head = cur->next;
                // 更新尾节点的next指向新头节点
                tail->next = head;
                // 释放原头节点
                delete cur;
                // 更新头节点的prev为原尾节点
                head->prev = tail;
                cur = head;
            } else {
                // 将前一个节点的next指向当前节点的下一个节点
                prev->next = cur->next;
                // 释放当前节点
                delete cur;
                // 更新前一个节点的next的prev为前一个节点
                prev->next->prev = prev;
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

### 3.5 遍历链表

***正向遍历:***

```cpp
/**
 * 正向遍历双向循环链表
 * @param head 双向循环链表的头指针
 */
void printForward(Node* head) {
    // 如果链表为空，直接返回
    if (!head) {
        return;
    }
    
    // 从头节点开始遍历
    Node* p = head;
    
    // 使用do-while循环确保至少执行一次
    // 直到再次回到头节点为止
    do {
        // 打印当前节点的数据
        std::cout << p->data << " ";
        // 移动到下一个节点
        p = p->next;
    } while (p != head);
    
    // 打印换行
    std::cout << std::endl;
}
```

***反向遍历:***

```cpp
/**
 * 反向遍历双向循环链表
 * @param head 双向循环链表的头指针
 */
void printBackward(Node* head) {
    // 如果链表为空，直接返回
    if (!head) {
        return;
    }
    
    // 从尾节点开始遍历（头节点的prev指向尾节点）
    Node* p = head->prev;
    // 保存尾节点位置，用于判断遍历结束
    Node* tail = p;
    
    // 使用do-while循环确保至少执行一次
    // 直到再次回到尾节点为止
    do {
        // 打印当前节点的数据
        std::cout << p->data << " ";
        // 移动到前一个节点
        p = p->prev;
    } while (p != tail);
    
    // 打印换行
    std::cout << std::endl;
}
```

### 3.6 反转双向循环链表

***反转双向循环链表的主要步骤：***

1. **空链表判断**：
   * 检查链表是否为空，为空则直接返回。
2. **只有一个节点判断**：
   * 检查链表是否只有一个节点，若只有一个节点，则直接返回。
3. **遍历链表**：
   * 使用 `cur` 指针遍历链表。
   * 使用 `prev` 指针记录前一个节点。
   * 使用 `do-while` 循环确保遍历一圈。
4. **指针反转**：
   * 反转当前节点的 `next` 和 `prev` 指针。
   * 移动 `prev` 指针到当前节点。
   * 移动 `cur` 指针到下一个节点。
5. **更新头指针**：
   * 遍历结束后，更新头指针为 `prev`。

```cpp
/**
 * 反转双向循环链表
 * @param head 双向循环链表的头指针的引用，用于修改头指针
 */
void reverse(Node*& head) {
    // 如果链表为空或只有一个节点，直接返回
    if (!head || head->next == head) {
        return;
    }

    // 用于遍历链表的指针
    Node* cur = head;
    // 用于保存前一个节点的指针
    Node* prev = head->prev;

    do {
        // 保存当前节点的下一个节点
        Node* next = cur->next;
        // 反转当前节点的指针
        cur->next = prev;
        cur->prev = next;
        // 移动前一个节点指针
        prev = cur;
        // 移动到下一个节点
        cur = next;
    } while (cur != head);

    // 更新头指针
    head = prev;
}
```

---

## 四、附整体测试代码

```cpp
int main() {
    // 创建一个包含1~5的整数的双向循环链表
    std::vector<int> arr = {1, 2, 3, 4, 5};
    Node* head = createDCLL(arr);

    // 正向遍历链表并输出
    traverseForward(head);

    // 在头部插入一个值为0的节点
    insertAtPosition(head, 0, 0);
    // 再次正向遍历链表并输出
    traverseForward(head);

    // 在第二个位置插入一个值为6的节点
    insertAtPosition(head, 2, 6);
    // 再次正向遍历链表并输出
    traverseForward(head);

    // 在最后一个位置插入一个值为7的节点
    insertAtPosition(head, 7, 7);
    // 再次正向遍历链表并输出
    traverseForward(head);

    // 在第二个节点（值为2）后插入一个值为8的节点
    insertAfter(head, head->next, 8);
    // 再次正向遍历链表并输出
    traverseForward(head);

    // 删除头节点
    deleteAtPosition(head, 0);
    // 再次正向遍历链表并输出
    traverseForward(head);

    // 删除第三个节点（原值为3）
    deleteAtPosition(head, 2);
    // 再次正向遍历链表并输出
    traverseForward(head);

    // 删除头节点
    deleteAtPosition(head, 0);
    // 再次正向遍历链表并输出
    traverseForward(head);

    // 反向遍历链表并输出（从最后一个节点开始）
    printBackward(head);

    // 删除值为8的节点
    deleteNode(head, 8);
    // 再次反向遍历链表并输出
    printBackward(head);

    // 删除值为7的节点
    deleteNode(head, 7);
    // 再次反向遍历链表并输出
    printBackward(head);

    // 删除值为4的节点
    deleteNode(head, 4);
    // 再次反向遍历链表并输出
    printBackward(head);

    // 插入一个值为4的节点在第二个位置
    // 插入一个值为1的节点在头部
    insertAtPosition(head, 2, 4);
    insertAtPosition(head, 0, 1);

    // 反转链表
    reverse(head);

    // 再次正向遍历链表并输出
    traverseForward(head);

    // 再次反向遍历链表并输出（从最后一个节点开始）
    printBackward(head);

    return 0;
}
```

***输出如下：***

```plaintext
1 2 3 4 5 
0 1 2 3 4 5
0 1 6 2 3 4 5
0 1 6 2 3 4 5 7
0 1 8 6 2 3 4 5 7
1 8 6 2 3 4 5 7
1 8 2 3 4 5 7
8 2 3 4 5 7
7 5 4 3 2 8
7 5 4 3 2
5 4 3 2
5 3 2
5 4 3 2 1
1 2 3 4 5
```

---

## 五、链表小结

截至目前为止，GESP五级考试大纲中的第三条链表相关内容已整理完成，小结如下：

| 链表类型       | 是否能向前遍历 | 是否能向后遍历 | 是否首尾相连 | 插入/删除复杂度     | 适用场景          |
| ---------- | ------- | ------- | ------ | ------------ | ------------- |
| **单链表**    | ✅    | ❌       | ❌      | $O(1)$（已知节点指针）<br>  $O(n)$（未知节点指针,遍历查找位置） | 基础数据结构，简单场景   |
| **双链表**| ✅| ✅| ❌| $O(1)$（已知节点指针）<br>  $O(n)$（未知节点指针,遍历查找位置） | 频繁前后操作，如浏览器历史 |
| **单向循环链表** | ✅    | ❌ | ✅  | $O(1)$（已知节点指针）<br> $O(n)$（未知节点指针,遍历查找位置） | 循环调度、轮询机制、循环播放等场景 |
| **双向循环链表** | ✅       | ✅       | ✅      | $O(1)$（已知节点指针）<br> $O(n)$（未知节点指针,遍历查找位置） | 复杂调度系统、音乐播放循环 |

---

{% include custom/custom-post-content-footer.md %}
