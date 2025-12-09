---
layout: post
title: 【GESP】C++六级考试大纲知识点梳理, (7) 栈与队列
date: 2025-12-09 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 栈, 队列]
categories: [GESP, 六级]
---
GESP C++六级官方考试大纲中，第`7`条考点回归到了最基础也是最常用的两个线性数据结构：**栈 (Stack)** 和 **队列 (Queue)**。

> （7）掌握栈、队列、循环队列的基本定义，应用场景和常见操作。
{: .prompt-info}

> 本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

> 栈和队列是算法世界的“左膀右臂”。如果说数组和链表是存储数据的“地基”，那么栈和队列就是基于这些地基构建的“规则容器”。它们不改变数据的存储方式，而是**规定了数据进出的顺序**。掌握它们，是理解深度优先搜索 (DFS)、广度优先搜索 (BFS) 等复杂算法的前提。
{: .prompt-warning}

***六级考点系列：***

> * [【GESP】C++六级考试大纲知识点梳理, (1) 树的概念与遍历](https://www.coderli.com/gesp-6-exam-syllabus-1-tree/)
> * [【GESP】C++六级考试大纲知识点梳理, (2) 哈夫曼树、完全二叉树与二叉排序树](https://www.coderli.com/gesp-6-exam-syllabus-2-huffman-bst/)
> * [【GESP】C++六级考试大纲知识点梳理, (3) 哈夫曼编码与格雷码](https://www.coderli.com/gesp-6-exam-syllabus-3-huffman-gray/)
> * [【GESP】C++六级考试大纲知识点梳理, (4) 搜索算法](https://www.coderli.com/gesp-6-exam-syllabus-4-search/)
> * [【GESP】C++六级考试大纲知识点梳理, (5) 动态规划与背包问题](https://www.coderli.com/gesp-6-exam-syllabus-5-dp-knapsack/)
> * [【GESP】C++六级考试大纲知识点梳理, (6) 面向对象编程(OOP)基础](https://www.coderli.com/gesp-6-exam-syllabus-6-oop/)
{: .prompt-tip}

<!--more-->

---

## 一、栈 (Stack)

### 1.1 基本定义

**栈**是一种**后进先出** (LIFO, Last In First Out) 的线性表。它的限制在于：**仅允许在表的一端进行插入和删除运算**。这一端被称为**栈顶 (Top)**，相对的另一端称为**栈底 (Bottom)**。

### 1.2 生活中的类比

* **弹夹**：最后压进去的子弹，是第一个被射出去的。
* **一摞盘子**：洗好的盘子一个接一个往上叠（入栈），取用时只能拿最上面的那个（出栈）。
* **浏览器的“后退”按钮**：你访问的网页依次入栈，点后退时，最近访问的页面先出来。

### 1.3 核心操作

* **Push (入栈/压栈)**：把数据放到栈顶。
* **Pop (出栈/弹栈)**：移除栈顶的数据。
* **Top (取栈顶)**：查看栈顶的数据（不移除）。
* **Empty (判空)**：检查栈里是不是空的。

### 1.4 C++ STL 实现

在 C++ 中，我们通常直接使用标准库 `<stack>`，不需要手写数组模拟（除非题目特定要求）。

```cpp
#include <iostream>
#include <stack> // 引入头文件
using namespace std;

int main() {
    stack<int> s; // 定义一个存储 int 的栈

    // 1. 入栈 push
    s.push(10);
    s.push(20);
    s.push(30); 
    // 此时栈内结构（从底到顶）：10 -> 20 -> 30

    // 2. 取栈顶 top
    cout << "栈顶元素: " << s.top() << endl; // 输出 30

    // 3. 出栈 pop
    s.pop(); // 移除 30
    cout << "弹出一个后，栈顶元素: " << s.top() << endl; // 输出 20

    // 4. 判空 empty 和 大小 size
    if (!s.empty()) {
        cout << "栈不为空，大小为: " << s.size() << endl; // 输出 2
    }

    return 0;
}
```

输出

```plaintext
栈顶元素: 30
弹出一个后，栈顶元素: 20
栈不为空，大小为: 2
```

### 1.5 应用场景

* **函数调用栈**：程序运行时的递归调用。
* **括号匹配检验**：比如判断 `(([]))` 是否合法。
* **表达式求值**：中缀表达式转后缀表达式。
* **深度优先搜索 (DFS)**：DFS 的本质就是递归，递归的本质就是栈。

### 1.6 经典案例：后缀表达式求值

#### 题目描述

给定一个后缀表达式（字符串数组），包含整数和运算符 `+`, `-`, `*`, `/`。请计算其结果。

* **输入**：`["2", "1", "+", "3", "*"]`
* **输出**：`9`
* **解释**：该表达式等价于 `(2 + 1) * 3 = 9`。

#### 解题思路

利用 **栈 (Stack)** 的 LIFO 特性：

1. **遇数字**：转换后 **入栈**。
2. **遇运算符**：**弹出** 栈顶两个数进行计算（**次顶** <op> **栈顶**），将结果 **入栈**。
3. **结束**：栈中剩余的唯一数值即为结果。

#### 代码样例

```cpp
#include <iostream>
#include <stack>
#include <string>
#include <vector>
using namespace std;

int evalRPN(vector<string>& tokens) {
    stack<int> st;
    for (const string& s : tokens) {
        if (s == "+" || s == "-" || s == "*" || s == "/") {
            int b = st.top(); st.pop(); // 栈顶是右操作数
            int a = st.top(); st.pop(); // 次顶是左操作数
            if (s == "+") st.push(a + b);
            else if (s == "-") st.push(a - b);
            else if (s == "*") st.push(a * b);
            else if (s == "/") st.push(a / b);
        } else {
            st.push(stoi(s)); // 字符串转整数入栈
        }
    }
    return st.top();
}

int main() {
    vector<string> tokens = {"4", "13", "5", "/", "+"}; // 4 + (13 / 5)
    cout << "Result: " << evalRPN(tokens) << endl; // Output: 6
    return 0;
}
```

---

## 二、队列 (Queue)

### 2.1 基本定义

**队列**是一种**先进先出** (FIFO, First In First Out) 的线性表。它的限制在于：**只允许在表的一端进行插入，在另一端进行删除**。插入的一端叫**队尾 (Rear/Back)**，删除的一端叫**队头 (Front)**。

### 2.2 生活中的类比

* **食堂排队打饭**：先来的同学先打饭（先出队），后来的同学排在队尾（入队）。不能插队！
* **打印机任务**：先点击打印的文件先被打印。

### 2.3 核心操作

* **Push / Enqueue (入队)**：把数据加到队尾。
* **Pop / Dequeue (出队)**：移除队头的数据。
* **Front (取队头)**：查看队头的数据。
* **Back (取队尾)**：查看队尾的数据。

### 2.4 C++ STL 实现

使用标准库 `<queue>`。

```cpp
#include <iostream>
#include <queue> // 引入头文件
using namespace std;

int main() {
    queue<string> q; // 定义一个存储 string 的队列

    // 1. 入队 push
    q.push("张三");
    q.push("李四");
    q.push("王五");
    // 此时队列结构（从头到尾）：张三 -> 李四 -> 王五

    // 2. 访问队头 front 和 队尾 back
    cout << "现在轮到谁打饭: " << q.front() << endl; // 张三
    cout << "队尾排的是谁: " << q.back() << endl;   // 王五

    // 3. 出队 pop
    q.pop(); // 张三打完饭走了
    cout << "下一个轮到: " << q.front() << endl; // 李四

    return 0;
}
```

输出

```plaintext
现在轮到谁打饭: 张三
队尾排的是谁: 王五
下一个轮到: 李四
```

### 2.5 应用场景

* **广度优先搜索 (BFS)**：层序遍历图或树。
* **任务调度**：操作系统管理 CPU 任务，先到先服务。
* **缓冲区**：消息队列，处理网络数据包。

### 2.6 经典案例：迷宫最短路径 (BFS)

#### 题目描述

给定一个 $5 \times 5$ 的迷宫（0为通路，1为障碍），求从起点 $(0,0)$ 到终点 $(4,4)$ 的最短步数。

* **输入**：一个 $5 \times 5$ 的二维数组。
* **输出**：一个整数，表示最短步数（若无法到达输出 -1）。

#### 解题思路

BFS (广度优先搜索) 是解决无权图最短路径的经典算法，核心利用 **队列 (Queue)** 的 **FIFO** 特性实现“层层向外扩散”：

1. **初始化**：起点入队，步数记为0，标记已访问。
2. **扩散**：
    * 取出队头当前点。
    * 如果是终点，返回步数。
    * 向 **上、下、左、右** 四个方向探索。
    * 若新位置合法（在界内、无墙、未访问），则记录步数（当前+1）、标记访问并 **入队**。
3. **结束**：队列为空仍未达终点，说明无路可通。

#### 代码样例

```cpp
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

struct Node {
    int x, y, step;
};

int bfs(vector<vector<int>>& maze) {
    int n = maze.size(); // 行数
    int m = maze[0].size(); // 列数
    vector<vector<bool>> visited(n, vector<bool>(m, false));
    
    queue<Node> q;
    q.push({0, 0, 0}); // 起点 (0,0) 步数 0
    visited[0][0] = true;

    // 方向数组：右、左、下、上
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};

    while (!q.empty()) {
        Node curr = q.front();
        q.pop();

        // 到达终点 (右下角)
        if (curr.x == n - 1 && curr.y == m - 1) return curr.step;

        for (int i = 0; i < 4; i++) {
            int nx = curr.x + dx[i];
            int ny = curr.y + dy[i];

            // 越界与障碍检查
            if (nx >= 0 && nx < n && ny >= 0 && ny < m && 
                maze[nx][ny] == 0 && !visited[nx][ny]) {
                visited[nx][ny] = true; // 标记已访问
                q.push({nx, ny, curr.step + 1}); // 入队，步数+1
            }
        }
    }
    return -1;
}

int main() {
    // 0: 通路, 1: 墙
    vector<vector<int>> maze = {
        {0, 1, 0, 0, 0},
        {0, 1, 0, 1, 0},
        {0, 0, 0, 0, 0},
        {0, 1, 1, 1, 0},
        {0, 0, 0, 1, 0}
    };
    
    cout << "Min Steps: " << bfs(maze) << endl; // Output: 8
    return 0;
}
```

---

## 三、循环队列 (Circular Queue)

### 3.1 基本定义

**循环队列** 是队列的一种优化实现，它将普通队列的线性存储空间（如数组）逻辑上变为一个**首尾相接的环状空间**。这样做的目的是为了高效利用存储空间，避免在队头元素出队后，数组前端出现无法利用的“空闲区域”，从而解决普通队列在数组实现时可能出现的**假溢出**问题。

它本质上依然遵循队列的 **先进先出 (FIFO)** 原则，只是在元素的入队和出队操作中，通过取模运算来维护队头和队尾的下标，使其能在数组中“循环”使用空间。

### 3.2 为什么要循环队列？

如果我们用一个普通的数组 `arr[10]` 来模拟队列：

* `head` 指向队头，`tail` 指向队尾。
* 随着数据入队（`tail++`）和出队（`head++`），这两个指针都会一直向后移动。
* 最终，`tail` 移到了数组的最末端，即使数组前面因为出队已经空出了很多位置，我们也无法再插入数据了。这被称为**假溢出**。

为了利用前面空出来的空间，我们将数组看作一个首尾相接的圆环，这就是**循环队列**。

### 3.3 核心公式 (基于数组下标 0 开始)

假设数组最大容量为 `MAX_SIZE`。

1. **入队下标移动**：`tail = (tail + 1) % MAX_SIZE;`    *利用取模运算 `%`，当 `tail` 到达末尾时，自动回到数组开头 `0`。*

2. **出队下标移动**：`head = (head + 1) % MAX_SIZE;`    *利用取模运算 `%`，当 `head` 到达末尾时，自动回到数组开头 `0`。*

3. **判满条件 (Full)**：由于 `head == tail` 通常用来表示空队列，为了区分“满”和“空”，我们通常**牺牲一个存储单元**。 即：**当队尾的下一个位置是队头时，认为队列满了。** `((tail + 1) % MAX_SIZE) == head`

4. **判空条件 (Empty)**：`head == tail`

5. **队列元素个数 (Size)**：`(tail - head + MAX_SIZE) % MAX_SIZE`

### 3.4 手写循环队列示例

这是 GESP 选择题或阅读程序题中容易出现的代码逻辑。

```cpp
#include <iostream>
using namespace std;

const int MAX_SIZE = 5; // 实际只能存 4 个，留 1 个位区分空/满
int q[MAX_SIZE];
int head = 0, tail = 0;

// 入队
bool enqueue(int val) {
    if ((tail + 1) % MAX_SIZE == head) {
        cout << "队列满，无法插入: " << val << endl;
        return false;
    }
    q[tail] = val;
    tail = (tail + 1) % MAX_SIZE;
    return true;
}

// 出队
bool dequeue() {
    if (head == tail) {
        cout << "队列空，无法删除" << endl;
        return false;
    }
    cout << "出队: " << q[head] << endl;
    head = (head + 1) % MAX_SIZE;
    return true;
}

int main() {
    enqueue(1);
    enqueue(2);
    enqueue(3);
    enqueue(4);
    enqueue(5); // 队列容量为5，存满4个即判满，这里会失败

    dequeue(); // 出队 1
    enqueue(5); // 现在有位置了，可以入队 5
    
    return 0;
}
```

---

## 四、栈与队列对比总结

| 特性 | 栈 (Stack) | 队列 (Queue) |
| :--- | :--- | :--- |
| **进出规则** | **LIFO** (后进先出) | **FIFO** (先进先出) |
| **开口方向** | 仅一端 (栈顶) | 两端 (队头出，队尾入) |
| **STL 容器** | `std::stack` | `std::queue` |
| **典型算法** | DFS, 递归, 表达式求值 | BFS, 缓冲区 |
| **核心行为** | 压入弹夹，子弹发射 | 食堂打饭，排队窗口 |

对于六级考试，重点在于：

1. **熟练调用 STL**：在编程题中快速使用 `stack` 和 `queue` 解决问题。
2. **理解循环队列下标**：在选择题中，给定 `head`, `tail` 和 `MAX_SIZE`，能正确计算入队出队后的新下标，或计算当前元素个数。

掌握了这两个“容器”，你就掌握了控制数据流动的“交通规则”，为后续学习图论算法打下坚实基础。

---

{% include custom/custom-post-content-footer.md %}
