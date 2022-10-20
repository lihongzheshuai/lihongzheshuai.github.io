---
title: Python练习-常用内建模块itertools
tags: [python]
date: 2022-10-20 22:20:24 +0800
comments: true
author: onecoder
---
本部分学习Python常用内建模块itertools。itertools中提供了很多有用迭代器方法，用于生成和处理序列。直接通过代码学习

<!--more-->
```python
# 本部分学习Python内置的迭代器
import itertools
from functools import reduce

# 从6开始，依次加1计数，无限输出
counts = itertools.count(6)
# 利用takewhile截取
clist = itertools.takewhile(lambda x: x <= 10, counts)
print(list(clist))

# 循环输出
cycles = itertools.cycle("OneCoder")
i = 0
for c in cycles:
    if i > 15:
        break
    print(c)
    i += 1

# 元素重复
repeats = itertools.repeat("OneCoder", 3)
for r in repeats:
    print(r)

# chain 把一组迭代对象串联起来，形成一个更大的迭代器
for c in itertools.chain("Asdf", "Qwer"):
    print(c)

# groupby 集合相邻相同元素
for k, group in itertools.groupby("AAABBcCDDD", lambda str: str.upper()):
    print(k, list(group))


# 练习 根据圆周率计算公式求pi：pi/4 = 1 - 1/3 + 1/5 - 1/7 ...
def pi(N):
    num_list = list(itertools.takewhile(lambda n: n <= 2 * N, itertools.count(1, 2)))
    flag = -1
    def map_f(x):
        nonlocal flag
        flag *= -1
        return 4 * flag / x
    return reduce(lambda x, y: x + y, map(map_f, num_list))


# 测试:
print(pi(10))
print(pi(100))
print(pi(1000))
print(pi(10000))
assert 3.04 < pi(10) < 3.05
assert 3.13 < pi(100) < 3.14
assert 3.140 < pi(1000) < 3.141
assert 3.1414 < pi(10000) < 3.1415
print('ok')
```
输出如下：
```
[6, 7, 8, 9, 10]
O
n
e
C
o
d
e
r
O
n
e
C
o
d
e
r
OneCoder
OneCoder
OneCoder
A
s
d
f
Q
w
e
r
A ['A', 'A', 'A']
B ['B', 'B']
C ['c', 'C']
D ['D', 'D', 'D']
3.0418396189294032
3.1315929035585537
3.140592653839794
3.1414926535900345
ok
```
