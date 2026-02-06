---
layout: post
title: 【GESP】C++八级考试大纲知识点梳理 (6) 图论算法：最小生成树与最短路
date: 2026-02-06 08:00 +0800
author: OneCoder
comments: true
math: true
mermaid: true
tags: [GESP, C++, 考试大纲, 图论, 算法]
categories: [GESP, 八级]
---

> **GESP C++ 八级考试大纲知识点梳理系列文章：**
> 1. [计数原理：加法与乘法](https://www.coderli.com/gesp-8-exam-syllabus-counting-principles/)
> 2. [排列与组合](https://www.coderli.com/gesp-8-exam-syllabus-permutations-combinations/)
> 3. [杨辉三角与组合数](https://www.coderli.com/gesp-8-exam-syllabus-yanghui-triangle/)
> 4. [倍增法](https://www.coderli.com/gesp-8-exam-syllabus-binary-lifting/)
> 5. [代数与平面几何](https://www.coderli.com/gesp-8-exam-syllabus-algebra-geometry/)
> 6. [图论算法：最小生成树与最短路](https://www.coderli.com/gesp-8-exam-syllabus-graph-theory/)
{: .prompt-tip}

本篇我们来攻克 GESP 八级考纲中分量极重的一块内容——**图论算法**。图论是算法竞赛中的核心版块，八级主要通过最经典的**最小生成树**和**最短路径**问题来考察大家对图结构的理解和算法实现能力。

> **考纲要求：**
> (6) 掌握图论算法及综合应用技巧。包括最小生成树的概念、Kruskal 算法、Prim 算法，掌握最短路径的概念、单源最短路径的 Dijkstra 算法、Floyd 算法等。理解实现同一功能的不同算法的比较，并可以灵活解决相关问题。
{: .prompt-info}

> 本人也是边学、边实验、边总结，且对考纲深度和广度的把握属于个人理解。因此本文更多的不是一个教程，而是个人知识梳理，如有遗漏、疏忽，欢迎指正、交流。
{: .prompt-warning}

---

## 一、最小生成树 (Minimum Spanning Tree, MST)

### 1.1 基本概念

在一个**连通、无向、带权**的图中，我们需要从中选择 $n-1$ 条边，将图中的 $n$ 个点全部连接起来，并且使得这 $n-1$ 条边的**权值之和最小**。这样构成的树，就称为**最小生成树**。

**关键特征：**

1. **包含所有顶点**：必须连接图中的所有点。
2. **边数最少**：$n$ 个点对应 $n-1$ 条边，不能有回路（环）。
3. **权值最小**：所有边的权重之和最小。

### 1.2 Kruskal 算法（加边法）

Kruskal 算法（克鲁斯卡尔算法）由 Joseph Kruskal 在 1956 年提出。它的核心思想是 **“贪心”**，关注的重点是 **边**。

**算法直观理解：**
想象森林中有很多棵树（初始时，每个点就是一棵树）。我们的目标是将这些树合并成一棵大树。
为了保证总代价最小，我们总是优先选择 **“最便宜”** 的边来连接两棵树。如果一条边的两个端点已经在同一棵树上了，那这条边就是多余的（连上会形成环），我们直接丢弃。
因为这个过程主要是通过不断“添加边”来构建生成树，所以也被形象地称为 **“加边法”**。

**核心逻辑：**

1. **贪心策略**：越短的边越优先考虑。
2. **避圈原则**：选边时，不能让图中出现环。

**算法流程：**

1. **排序**：将图中所有的边按照权值**从小到大**进行排序。
2. **选边**：依次枚举每一条边。
3. **判断**：如果这条边的两个端点当前**还未连通**（即不在同一个集合中），就选择这条边；如果已经连通，则跳过（否则会形成环）。
4. **重复**：直到选出了 $n-1$ 条边为止。

**核心实现技巧：**
* **并查集 (Union-Find)**：用于高效地判断两个点是否连通，以及将两个集合合并。

> **什么是并查集？**
> 并查集是一种非常精巧且高效的树型数据结构，主要用于处理 **不相交集合** 的合并及查询问题。
> 你可以把它生动地理解为 **“帮派找老大”** 的游戏：
> 1. **查 (Find)**：**找老大**。给你一个点，顺藤摸瓜找到它的最高层老大（根节点）。如果两个人的老大是同一个人，那他们就是“一伙的”（连通的）。(配合**路径压缩**优化，查询极快)。
> 2. **并 (Union)**：**合并帮派**。当合并两个点时，通过“擒贼先擒王”，直接让其中一个老大归顺另一个老大，这样两个帮派的所有人就都变成一家人了。

> ```cpp
> // 查找老大（带路径压缩）
> int find(int x) {
>     // 如果我的上级不是我自己，说明我上面还有人，继续往上找
>     if (parent[x] != x) parent[x] = find(parent[x]); // 递归找老大，顺便把自己挂到老大名下
>     return parent[x];
> }
>
> // 合并帮派
> bool unite(int x, int y) {
>     int rootX = find(x);
>     int rootY = find(y);
>     if (rootX != rootY) { // 如果老大不同，说明原本不连通
>         parent[rootX] = rootY; // 让 rootX 归顺 rootY
>         return true; // 合并成功
>     }
>     return false; // 本来就是一伙的，没法合并（否则会形成环）
> }
> ```

> **路径压缩 (Path Compression)**：
> 在 `find(x)` 函数中，`parent[x] = find(parent[x]);` 这一行代码就是路径压缩。
> 想象一下链条：1 -> 2 -> 3 -> 4 (4是老大)。
> 当你查询 1 时，它会一路找到 4。
> 路径压缩做了一件“聪明”的事：它直接把 1 的爸爸改成 4，把 2 的爸爸也改成 4。
> 下次再查 1 或 2，直接就是老大，不需要再一级一级往上爬了。
> 这使得并查集的查询操作变得极其迅速，几乎可以认为是常数时间。

**算法代码示例 (C++)：**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 定义边结构体
struct Edge {
    int u, v, w;
    // 重载小于号，用于排序
    bool operator<(const Edge& other) const {
        return w < other.w;
    }
};

const int MAXN = 5005;
int parent[MAXN]; // 并查集数组
vector<Edge> edges;
int n, m;

// 并查集初始化
void init() {
    for (int i = 1; i <= n; i++) parent[i] = i;
}

// 并查集查找（带路径压缩）
int find(int x) {
    if (parent[x] != x) parent[x] = find(parent[x]);
    return parent[x];
}

// 并查集合并
bool unite(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY) {
        parent[rootX] = rootY;
        return true;
    }
    return false;
}

void kruskal() {
    sort(edges.begin(), edges.end()); // 1. 边的排序
    init();
    
    long long mst_weight = 0;
    int edge_count = 0;
    
    for (const auto& edge : edges) {
        // 2. 选边并判断
        if (unite(edge.u, edge.v)) {
            mst_weight += edge.w;
            edge_count++;
            if (edge_count == n - 1) break; // 选满 n-1 条边即可停止
        }
    }
    
    if (edge_count < n - 1) {
        cout << "无法构成生成树" << endl;
    } else {
        cout << "最小生成树权值: " << mst_weight << endl;
    }
}

int main() {
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.push_back({u, v, w});
    }
    kruskal();
    return 0;
}
```

### 1.3 Prim 算法（加点法）

Prim 算法（普里姆算法）最早由 Robert Prim 在 1957 年发现（实际上 Jarník 在 1930 年已经发现）。它的核心思想也是 **“贪心”**，但与 Kruskal 不同，它关注的是 **点**。

**算法直观理解：**
Prim 算法的过程非常像一棵植物在“发芽生长”。
初始时，我们选择任意一个点作为种子（生成树的根）。然后，这棵小树开始向外延伸。
每次生长，它都会探查周围所有能连接到的“外部点”，并选择一条 **“最短”** 的枝条（边），把那个对应的点拉入自己的怀抱（生成树集合）。
重复这个过程，直到所有的点都被纳入这棵大树中。
因为这个过程主要是通过不断“捕获点”来构建生成树，所以也被形象地称为 **“加点法”**。

**核心逻辑：**
1. **集合划分**：将世界划分为 **“已收录集合 S”** 和 **“未收录集合 V-S”**。
2. **最近邻接**：总是寻找从 S 到 V-S 的最短边。

**算法流程：**
1. **集合划分**：将点分为两类，**已在这个树上的点 (集合 S)** 和 **尚未加入的点 (集合 V-S)**。初始时，随机选一个点进 S。
2. **寻找最短边**：找出所有连接 S 中顶点和 V-S 中顶点的边中，**权值最小**的那条边。
3. **加点**：将该边连接的那个未加入的点加入 S。
4. **重复**：直到所有点都加入 S。

**算法代码示例 (C++ 邻接矩阵版，适合稠密图)：**

```cpp
#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAXN = 5005;
const int INF = 0x3f3f3f3f;
int graph[MAXN][MAXN];
int dist[MAXN]; // dist[i] 表示点 i 到当前生成树集合的最短距离
bool visited[MAXN]; // 标记点是否已加入生成树
int n, m;

int prim() {
    // 初始化
    memset(dist, 0x3f, sizeof(dist));
    memset(visited, false, sizeof(visited));
    
    dist[1] = 0; // 从点 1 开始
    int total_weight = 0;
    
    for (int i = 1; i <= n; i++) {
        // 1. 寻找距离生成树最近的点
        int u = -1;
        int min_dist = INF;
        for (int j = 1; j <= n; j++) {
            if (!visited[j] && dist[j] < min_dist) {
                min_dist = dist[j];
                u = j;
            }
        }
        
        if (u == -1) return -1; // 图不连通
        
        visited[u] = true; // 加入生成树
        total_weight += min_dist;
        
        // 2. 更新其他点到生成树的距离
        for (int v = 1; v <= n; v++) {
            if (!visited[v] && graph[u][v] < dist[v]) {
                dist[v] = graph[u][v];
            }
        }
    }
    return total_weight;
}
```

### 1.4 算法比较

| 算法 | 关注对象 | 适用场景 | 时间复杂度 |
| :--- | :--- | :--- | :--- |
| **Kruskal** | **边** | **稀疏图** (边少点多) | $O(E \log E)$ 或 $O(E \log V)$ |
| **Prim** (朴素) | **点** | **稠密图** (边多点少) | $O(V^2)$ |
| Prim (堆优化) | 点 | 稀疏图 | $O(E \log V)$ |

> **总结：** 一般竞赛中，**Kruskal** 因为代码好写且并查集通用性强，是首选。如果是完全图或者边非常密集的图，用朴素版 **Prim**。

---

## 二、最短路径 (Shortest Path)

最短路径问题通常分为两类：**单源最短路径**（从一个起点到所有其他点）和**多源最短路径**（任意两点之间）。

### 2.1 Dijkstra 算法 (单源，无负权边)

Dijkstra 算法（迪杰斯特拉算法）由 Edsger W. Dijkstra 在 1956 年提出。它是解决 **单源最短路径** 问题最经典、最常用的算法。

**算法直观理解：**
Dijkstra 算法的思想非常像“**水的蔓延**”或者“**多米诺骨牌**”。
想象起点是一个水源，水流以不同的速度（边权）沿着沟渠（边）向外流动。水流最先到达的点，一定就是离起点“最近”的点。
一旦水流到达了某个点，我们就以此点为中转站，继续向它的邻居蔓延。
由于水总是优先流向最近的地方（贪心），所以当我们第一次访问到某个点时，那一定就是到达它的最短路径。

**核心逻辑：**
1. **贪心策略**：每次从“未确定节点”中取一个距离起点最近的，那这个距离就是它的最终最短距离（因为没有负权边，后面不可能绕得更远再回来变短）。
    > **举例说明：**
    > 假设起点是 A。当前 A 能直接到的点有 B (距离 2) 和 C (距离 10)。
    > 目前 B 是离 A 最近的点（距离 2），C 较远（距离 10）。
    > 我们的贪心策略说：**“A 到 B 的最短距离一定就是 2 了，不可能更短了。”**
    > **为什么？**
    > 假设有一条更短的路能到 B，那它必须先经过其他的点（比如 C）。
    > 但 A 到 C 既然已经比 A 到 B 远了（10 > 2），那么从 A -> C -> ... -> B 这条路，只会在 10 的基础上**越加越大**（因为没有负权边），绝不可能变得比 2 还小。
    > 所以，**当前最近的那个点，一定已经达成了它的“最终命运”。**
2. **松弛操作 (Relaxation)**：利用这个刚确定的最短距离点，去尝试更新它的邻居。就像是“我也找到组织了，我的邻居们通过我走能不能更近一点？”

> **注意事项：**
> 图中 **不能包含负权边**。因为如果存在负权边，之前确定的“最短路径”可能会被后来经过负权边的“更短路径”推翻，Dijkstra 的贪心策略就会失效。

**算法流程：**
1. **初始化**：起点距离设为 0，其他点设为无穷大。
2. **选点**：在所有**未确定最短路**的点中，找一个距离起点最近的点 $u$。
3. **松弛 (Relax)**：用点 $u$ 作为中转站，尝试更新它相连的邻居点 $v$ 的距离。如果 `dist[u] + w(u,v) < dist[v]`，则更新 `dist[v]`。
4. **标记**：点 $u$ 的最短路已确定，标记为已访问。
5. **重复**：直到所有点都被访问。

**优化**：朴素版查找最小距离点需要 $O(V)$，总复杂度 $O(V^2)$。使用**优先队列 (priority_queue)** 优化后，复杂度降为 $O(E \log V)$，适合稀疏图。

**代码示例 (堆优化版)：**

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <cstring>
using namespace std;

struct Edge {
    int to, w;
};

// 优先队列节点，存储 {距离, 点编号}
// 注意：priority_queue 默认是大顶堆，需要重载 > 或者存负数
struct Node {
    int id, dist;
    bool operator>(const Node& other) const {
        return dist > other.dist; // 距离小的优先
    }
};

const int MAXN = 1005;
const int INF = 0x3f3f3f3f;
vector<Edge> adj[MAXN];
int dist[MAXN];
int n, m, start_node;

void dijkstra(int s) {
    memset(dist, 0x3f, sizeof(dist));
    dist[s] = 0;
    
    // 小顶堆
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    pq.push({s, 0});
    
    while (!pq.empty()) {
        Node cur = pq.top();
        pq.pop();
        int u = cur.id;
        int d = cur.dist;
        
        // 懒惰删除：如果当前取出的距离不是最新的最短距离，跳过
        if (d > dist[u]) continue;
        
        for (const auto& edge : adj[u]) {
            int v = edge.to;
            int weight = edge.w;
            // 松弛操作
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({v, dist[v]});
            }
        }
    }
}

int main() {
    cin >> n >> m >> start_node;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w}); // 有向图使用
        // adj[v].push_back({u, w}); // 如果是无向图需加上这一句
    }
    
    dijkstra(start_node);
    
    for (int i = 1; i <= n; i++) {
        cout << dist[i] << " ";
    }
    return 0;
}
```

### 2.2 Floyd-Warshall 算法 (多源)

Floyd-Warshall 算法（通常简称为 Floyd 算法）由 Robert Floyd 和 Stephen Warshall 在 1962 年分别提出。它是解决 **多源最短路径**（即求任意两点间的最短路径）最简洁、最优雅的算法。

> **什么是多源最短路径？**
> 单源最短路径（如 Dijkstra）是求 **一个起点** 到 **其他所有点** 的最短距离。
> 而多源最短路径，则是要求出图中 **任意两个点** (u, v) 之间的最短距离。你可以把它理解为跑了 $N$ 遍 Dijkstra（分别以每个点为起点），但 Floyd 算法用更优雅的方式一次性解决了这个问题。

**算法直观理解：**
Floyd 算法的核心思想是 **“中转”**（插点）。
对于任意两点 $i$ 和 $j$，它们之间的距离有两种可能：
1. 直接相连（或者按原路走）。
2. 经过某个中间点 $k$ 进行中转（$i \to k \to j$），如果这条路更近，那就应该走这条路。
Floyd 算法就是尝试把图中的 **每一个点** 都当作一次“中转站”，看看经过这个中转站能不能缩短其他两点间的距离。

**核心逻辑 (动态规划)：**
它本质是一个动态规划算法。
我们定义状态 `dp[k][i][j]` 为：**只允许经过前 $k$ 个点作为中转节点** 时，从 $i$ 到 $j$ 的最短路径。
显然，如果允许经过的点更多（比如允许经过第 $k$ 个点），路径只可能变得更短或不变。

**状态定义**：`dp[k][i][j]` 表示只允许经过前 $k$ 个点作为中转节点时，从 $i$ 到 $j$ 的最短路径。
**状态转移**：`dp[k][i][j] = min(dp[k-1][i][j], dp[k-1][i][k] + dp[k-1][k][j])`。
空间优化后，第一维 $k$ 可以省略。

**算法流程：**
最简单的代码，**三重循环**：枚举中转点 $k$，枚举起点 $i$，枚举终点 $j$。

**代码示例：**

```cpp
#include <iostream>
#include <algorithm>
using namespace std;

const int MAXN = 205;
const int INF = 0x3f3f3f3f;
int dp[MAXN][MAXN];
int n, m;

int main() {
    cin >> n >> m;
    
    // 初始化
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (i == j) dp[i][j] = 0;
            else dp[i][j] = INF;
        }
    }
    
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        // 注意处理重边，取最小值
        dp[u][v] = min(dp[u][v], w); 
        // dp[v][u] = min(dp[v][u], w); // 无向图
    }
    
    // 核心代码：三重循环，k 必须在最外层
    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                // 如果经过 k 能更短，就更新
                if (dp[i][k] != INF && dp[k][j] != INF) {
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j]);
                }
            }
        }
    }
    
    return 0;
}
```

### 2.3 算法比较与选择

| 算法 | 类型 | 适用图 | 是否支持负权 | 时间复杂度 | 空间复杂度 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dijkstra** (堆优化) | 单源 | 稀疏图 | **否** | $O(E \log V)$ | $O(V+E)$ |
| **Floyd** | 多源 | 稠密图 ($N \le 300$) | **是** (无负环) | $O(N^3)$ | $O(V^2)$ |

---

## 三、实战综合应用建议

### 1. **判连通性**
    
* **场景举例**：
    * 给定 $N$ 个城市和 $M$ 条路，问这 $N$ 个城市是否能互相到达？或者问还需要修几条路才能连通？
    * 游戏中有多少个独立的公会联盟？
* **核心思想**：
    * 只是数个数或判连通，**并查集** 最快（$O(\alpha(N))$）。
    * 如果还需要知道怎么连代价最小（比如修路成本），那就必须用 **最小生成树 (MST)**。

### 2. **“瓶颈”问题 (Minimax)**

* **场景举例**：
    * 货车运货，路径上能通过的最大承重取决于最窄的那座桥。问从 A 到 B，最大能运多重的货？
    * 网络传输，带宽取决于最慢的那段光缆。
* **核心思想**：
    * 这类问题被称为 **“瓶颈路”** 问题。想象一下，木桶能装多少水取决于最短的那块板（最小边权最大），或者通过隧道的车辆高度取决于最低的那个隧道口（最大边权最小）。
    * 两点间“最大边权最小”的路径，一定都在最小生成树上。我们只需要建好 MST，然后用来做 DFS/BFS 甚至倍增 LCA 查询即可。

### 3. **多源变单源 (Super Source)**

* **场景举例**：
    * 有 5 个披萨店（起点），你要在地图上任意位置点外卖，问离你最近的那个披萨店要多久送到？
* **核心思想**：
    * 不要傻傻地跑 5 遍 Dijkstra。
    * **建立一个虚拟的“超级源点” $S$**。
    * 让 $S$ 连向这 5 个披萨店，边权都设为 0。
    * 然后只跑一遍以 $S$ 为起点的 Dijkstra。求出的 `dist[u]` 就是 $u$ 离**任意一个**披萨店的最近距离。

图论算法是 GESP 八级的重中之重，代码量相对较大，建议同学们多动手默写模板 (Dijkstra 堆优化、Kruskal)，做到 5 分钟内能准确敲出。

---

{% include custom/custom-post-content-footer.md %}
