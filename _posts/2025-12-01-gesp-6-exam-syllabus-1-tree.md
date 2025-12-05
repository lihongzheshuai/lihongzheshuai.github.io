---
layout: post
title: 【GESP】C++六级考试大纲知识点梳理, (1) 树的概念与遍历
date: 2025-12-01 22:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 树]
categories: [GESP, 六级]
---
GESP C++六级官方考试大纲中，包含了对更高级数据结构（如树）和基础算法的深入要求。本文针对第`1`条考点进行分析介绍。

> （1）掌握树的基本概念，掌握其构造与遍历的相关算法。
{: .prompt-info}

> 本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

***六级考点系列：***

> * [【GESP】C++五级考试大纲知识点梳理](https://www.coderli.com/categories/%E4%BA%94%E7%BA%A7/) （回顾五级内容）
{: .prompt-tip}

树（Tree）是计算机科学中非常重要的一种非线性数据结构，它模拟了具有层次关系的数据集合。在六级考试中，重点是二叉树（Binary Tree）的理解与操作，但对一般树的概念也需掌握。

<!--more-->

---

## 一、树的基本概念

### 1.1 树的定义

树是由 $n$ ($n \ge 0$) 个节点组成的有限集合。

* 如果 $n=0$，称为**空树**。
* 如果 $n>0$，这 $n$ 个节点中存在一个唯一的节点称为**根节点**（Root）。
* 其余节点可分为 $m$ ($m \ge 0$) 个互不相交的有限集 $T_1, T_2, \dots, T_m$，其中每个集合本身又是一棵树，称为根节点的**子树**（Subtree）。

### 1.2 常用术语

理解树的术语是解题的基础：

1. **节点（Node）**：包含数据元素及若干指向子树的分支信息。
2. **度（Degree）**：
    * **节点的度**：一个节点拥有的子树个数（即子节点个数）。
    * **树的度**：树中所有节点的度的最大值。
3. **叶子节点（Leaf）**：度为 0 的节点（也称为终端节点）。
4. **分支节点**：度不为 0 的节点（也称为非终端节点）。
5. **孩子（Child）与双亲（Parent）**：
    * **结点的子树的根称为该结点的孩子**。
    * **该结点称为孩子的双亲（父节点）**。
6. **兄弟（Sibling）**：同一个双亲的孩子之间互称兄弟。
7. **深度（Depth）与高度（Height）**：
    * **深度**：从根节点开始自顶向下逐层累加的。根节点的深度为 1（也有定义为 0，视题目约定）。
    * **高度**：从叶子节点开始自底向上逐层累加的。
    * **树的深度/高度**：树中节点的最大层数。
8. **路径**：从一个节点到另一个节点所经过的节点序列。

### 1.3 特殊的树：二叉树 (Binary Tree)

二叉树是树的一种特殊形式，它的每个节点**最多只有两个子节点**，分别称为**左孩子**和**右孩子**。二叉树是有序树，左右子树不能互换。

#### **满二叉树 (Full Binary Tree)**

* **定义**：一棵深度为 $k$ 且有 $2^k - 1$ 个节点的二叉树称为满二叉树。
* **特点**：每一层都“铺满”了节点，没有空缺。除了叶子节点外，每个节点都有两个子节点。
* **图示**：

    ```mermaid
        graph TD
            A((1)) --- B((2))
            A --- C((3))
            B --- D((4))
            B --- E((5))
            C --- F((6))
            C --- G((7))
    ```

#### **完全二叉树 (Complete Binary Tree)**

* **定义**：深度为 $k$ 的二叉树，如果前 $k-1$ 层是满的，且第 $k$ 层的节点都**连续集中在最左边**，这棵树就是完全二叉树。
* **特点**：完全二叉树是由满二叉树而引出来的。满二叉树一定是完全二叉树，但完全二叉树不一定是满二叉树。
* **图示**：（节点 6 存在，但节点 7 缺失，且中间没有空洞）

    ```mermaid
    graph TD
        A((1)) --- B((2))
        A --- C((3))
        B --- D((4))
        B --- E((5))
        C --- F((6))
    ```

* **对比总结**：

  | 特性 | 满二叉树 | 完全二叉树 |
  | :--- | :--- | :--- |
  | **节点总数** | $2^k - 1$ | $2^{k-1} \le n \le 2^k - 1$ |
  | **叶子节点位置** | 仅在最后一层 | 最后一层和倒数第二层 |
  | **节点分布** | 均匀对称 | 最后一层左对齐 |

---

## 二、树的构造与存储

在 C++ 中，树的存储主要有两种方式：**数组存储（顺序存储）**和**链式存储**。

### 2.1 数组存储

主要用于**完全二叉树**。
将完全二叉树的节点按层序编号（从 1 开始），存储在一维数组中。

* **节点 $i$ 的左孩子是 $2 \times i$。**
* **节点 $i$ 的右孩子是 $2 \times i + 1$。**
* **节点 $i$ 的父节点是 $i / 2$。**

```cpp
const int N = 1005;
int tree[N]; // tree[i] 存储编号为 i 的节点的值

// 访问 i 的左孩子
int left_child = tree[2 * i];
// 访问 i 的右孩子
int right_child = tree[2 * i + 1];
```

### 2.2 链式存储（推荐）

对于一般二叉树，最常用的是链式存储。每个节点包含数据域和指向左右孩子的指针。

**结构体定义：**

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    // 构造函数
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};
```

**静态数组模拟链表（竞赛常用）：**
如果不想动态 `new` 节点，可以使用数组模拟。

```cpp
const int N = 100005;
struct Node {
    int val;
    int left, right; // 存储的是子节点在数组中的下标，0表示空
} tree[N];

int idx = 0; // 节点计数器
int newNode(int v) {
    idx++;
    tree[idx].val = v;
    tree[idx].left = tree[idx].right = 0;
    return idx;
}
```

{% include custom/custom-post-content-inner.html %}

---

## 三、树的遍历算法

树的遍历是指按照一定规则访问树中所有节点，且每个节点仅访问一次。主要分为**深度优先遍历**（DFS）和**广度优先遍历**（BFS）。

### 3.1 深度优先遍历 (DFS)

根据访问根节点的时机不同，分为前序、中序和后序遍历。

1. **前序遍历 (Pre-order)**：根 $\to$ 左 $\to$ 右
2. **中序遍历 (In-order)**：左 $\to$ 根 $\to$ 右
3. **后序遍历 (Post-order)**：左 $\to$ 右 $\to$ 根

**递归实现示例（C++）：**

```cpp
#include <iostream>
using namespace std;

struct TreeNode {
    char val;
    TreeNode *left, *right;
    TreeNode(char x) : val(x), left(NULL), right(NULL) {}
};

// 1. 前序遍历：根 -> 左 -> 右
void preOrder(TreeNode* root) {
    if (root == NULL) return;
    cout << root->val << " ";  // 访问根
    preOrder(root->left);      // 递归左
    preOrder(root->right);     // 递归右
}

// 2. 中序遍历：左 -> 根 -> 右
void inOrder(TreeNode* root) {
    if (root == NULL) return;
    inOrder(root->left);       // 递归左
    cout << root->val << " ";  // 访问根
    inOrder(root->right);      // 递归右
}

// 3. 后序遍历：左 -> 右 -> 根
void postOrder(TreeNode* root) {
    if (root == NULL) return;
    postOrder(root->left);     // 递归左
    postOrder(root->right);    // 递归右
    cout << root->val << " ";  // 访问根
}

int main() {
    /* 构建如下二叉树
         A
       /   \
      B     C
       \   /
        D E
    */
    TreeNode* root = new TreeNode('A');
    root->left = new TreeNode('B');
    root->right = new TreeNode('C');
    root->left->right = new TreeNode('D');
    root->right->left = new TreeNode('E');

    cout << "前序遍历: "; preOrder(root); cout << endl;
    cout << "中序遍历: "; inOrder(root); cout << endl;
    cout << "后序遍历: "; postOrder(root); cout << endl;

    return 0;
}
```

**输出结果：**

```text
前序遍历: A B D C E 
中序遍历: B D A E C 
后序遍历: D B E C A 
```

### 3.2 广度优先遍历 (BFS) / 层序遍历

按照树的层次，从上到下、从左到右依次访问节点。通常使用**队列 (queue)** 来实现。

**算法步骤：**

1. 将根节点入队。
2. 当队列不为空时，循环执行：
   * 取出队首节点，访问它。
   * 如果该节点有左孩子，将左孩子入队。
   * 如果该节点有右孩子，将右孩子入队。

**代码示例：**

```cpp
#include <iostream>
#include <queue>
using namespace std;

// 假设 TreeNode 定义同上

void levelOrder(TreeNode* root) {
    if (root == NULL) return;

    queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        TreeNode* current = q.front();
        q.pop();

        cout << current->val << " ";

        if (current->left != NULL) q.push(current->left);
        if (current->right != NULL) q.push(current->right);
    }
}
```

### 3.3 已知遍历序列还原二叉树

这是考试中常见的考点。

**（1）已知前序 + 中序**：**可以**唯一确定一棵二叉树。
  
* **前序第一个是根**，去中序里找这个根，把中序分为左子树部分和右子树部分，递归构建。
* **示例解析**：
  * 前序遍历：`A B D C E`
  * 中序遍历：`B D A E C`

**推导过程**：

1. **确定根节点**：前序遍历的第一个节点 `A` 是整棵树的根。
2. **划分左右子树**：在中序遍历中找到 `A`，其左边 `B D` 属于左子树，右边 `E C` 属于右子树。
3. **分析左子树**（节点 `B`和`D`）：
   * 前序中 `B` 先出现，所以 `B` 是左子树的根。
   * 在中序遍历 `B D` 中，`D` 在 `B` 的**右边**。根据中序“左-根-右”的规则，这意味着 `D` 是 `B` 的**右孩子**。
   * *(注：如果 `D` 是左孩子，中序遍历应该是 `D B`)*。
4. **分析右子树**（节点 `E`和`C`）：
   * 前序中 `C` 先出现（注意 `E` 是在 `C` 之后才出的，因为前序是 `A` -> `Left(B,D)` -> `Right(C,E)`，在 `A B D C E` 中，`C` 是右子树的第一个节点），所以 `C` 是右子树的根。
   * 在中序遍历 `E C` 中，`E` 在 `C` 的**左边**。所以 `E` 是 `C` 的**左孩子**。

        ```mermaid
        graph TD
            A((A))
            B((B))
            C((C))
            D((D))
            E((E))

            A --- B
            A --- C
            B -- right --> D
            C -- left --> E
        ```

**（2）已知后序 + 中序**：**可以**唯一确定一棵二叉树。

* 后序最后一个是根，去中序里找这个根，分割左右，递归构建。
* **示例解析**：
  * 后序遍历：`D B E C A`
  * 中序遍历：`B D A E C`

**推导过程**：

1. **确定根节点**：后序遍历的最后一个节点 `A` 是整棵树的根。
2. **划分左右子树**：在中序遍历中找到 `A`，左边 `B D` 是左子树，右边 `E C` 是右子树。
3. **分析左子树**（节点 `B`和`D`）：
   * 后序遍历中（`D B`），`B` 是最后一个出现的，所以 `B` 是左子树的根。
   * 在中序遍历 `B D` 中，`D` 在 `B` 之后，说明 `D` 是 **右孩子**。
4. **分析右子树**（节点 `E`和`C`）：
   * 后序遍历中（`E C`），`C` 是最后一个出现的，所以 `C` 是右子树的根。
   * 在中序遍历 `E C` 中，`E` 在 `C` 之前，说明 `E` 是 **左孩子**。

        ```mermaid
        graph TD
            A((A))
            B((B))
            C((C))
            D((D))
            E((E))

            A --- B
            A --- C
            B -- right --> D
            C -- left --> E
        ```

**（3）已知前序 + 后序**：**不能**唯一确定二叉树（无法区分左右子树）。

* **示例**：
  * 前序遍历：`A B`
  * 后序遍历：`B A`
* **分析**：根肯定是 `A`，子节点是 `B`。但无法确定 `B` 是 `A` 的左孩子还是右孩子。
* 两种情况的中序遍历分别是 `B A`（B为左）和 `A B`（B为右），但题目未提供中序，故无法唯一确定。

## 四、一般树的存储与遍历

对于度大于 2 的树（多叉树），通常使用**邻接表**（Adjacency List）也就是 `vector` 数组来存储。

**存储方式：**

```cpp
#include <vector>
using namespace std;

const int MAXN = 10005;
vector<int> tree[MAXN]; // tree[u] 存储节点 u 的所有子节点

// 添加边 u -> v (u是父，v是子)
void addEdge(int u, int v) {
    tree[u].push_back(v);
}
```

**遍历（以 DFS 为例）：**

```cpp
void dfs(int u) {
    // 访问节点 u
    cout << u << " ";
    
    // 遍历所有子节点
    for (int i = 0; i < tree[u].size(); i++) {
        int v = tree[u][i];
        dfs(v);
    }
}
```

---

## 五、总结

| 知识点 | 重点内容 | 备注 |
| :--- | :--- | :--- |
| **基本概念** | 根、叶子、深度、度、完全二叉树 | 区分深度和高度 |
| **存储结构** | 链式存储（Struct指针）、数组模拟 | 完全二叉树适合数组 |
| **遍历算法** | 前序、中序、后序（DFS），层序（BFS） | 递归是核心 |
| **二叉树还原** | 前+中、后+中 可还原 | 前+后 不可还原 |

树的题目在 GESP 六级中通常考察递归思维，务必熟练掌握递归函数的编写和树形结构的指针操作。

---
{% include custom/custom-post-content-footer.md %}
