---
title: python练习-高级特性
tags: [Python]
categories: [Python技术研究]
date: 2022-06-07 20:18:24 +0800
comments: true
author: onecode
---

``` python
# 高级特性
# 1. 切片和列表生成器
from collections.abc import Iterable, Iterator

list_one = list(range(10))
print(list_one[:3])
print(list_one[2:7])
print(list_one[-5:-1])
# 取后5个数
print(list_one[-5:])
# 取偶数
print(list_one[:10:2])
# 取奇数
print(list_one[1:10:2])
# 字符串也可以切片
str_one = "My name is Yummy"
print(str_one[:5])
print(str_one[:10:3])


def trim_str(str):
    result = str
    if str[-1] == " ":
        result = str[:-1]
    return result


print(trim_str("Yummy ") + "!")
print(trim_str("Yummy") + "!")

# 2. 迭代
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)
for v in d.values():
    print(v)
for k, v in d.items():
    print(k, v)
for s in "Yummy":
    print(s)

print(isinstance(123, Iterable))

for i, value in enumerate(["A", "B", "C"]):
    print(i, value)

for x, y in [(1, 2), (4, 6), (7, "A")]:
    print(x, y)


# 测试
def findMinAndMax(param):
    max, min = None, None
    if param and param != []:
        for v in param:
            if max == None:
                max = min = v
            elif v > max:
                max = v
            elif v < min:
                min = v
    return (min, max)


if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')

# 3. 列表生成
list_two = [x * x for x in range(1, 11)]
print(list_two)
list_three = [x * x for x in range(1, 11) if x % 2 != 0]
print(list_three)
list_four = [m + n for m in "ABC" for n in "123"]
print(list_four)
d_str = {"A": "1", "B": "2", "C": "3"}
list_five = [k + "=" + v for k, v in d_str.items()]
print(list_five)
# 变成小写
print([v.lower() for v in list_five])
list_six = [x * x if x % 2 == 0 else -x for x in range(1, 11)]
print(list_six)
# 练习变小写，需要判断类型
L1 = ['Hello', 'World', 18, 'Apple', None]
L_output = [x.lower() if isinstance(x, str) else x for x in L1]
print(L_output)

# 4. 生成器
g = (x * x if x % 2 == 0 else -x for x in range(1, 11))
next(g)
print(next(g))
for v in g:
    print(v)


def feb(max):
    a, b, n = 0, 1, 0
    while n < max:
        a, b = b, a + b
        yield a
        n += 1
    return "over"


fg = feb(10)
for v in fg:
    print(v)


# 练习：生成器，杨辉三角形
#           1
#          / \
#         1   1
#        / \ / \
#       1   2   1
#      / \ / \ / \
#     1   3   3   1
#    / \ / \ / \ / \
#   1   4   6   4   1
#  / \ / \ / \ / \ / \
# 1   5   10  10  5   1
def g_triangle():
    last_row = [1]
    cur_row = [1]
    n = 0
    while n < 10:
        if n == 0:
            cur_row = [1]
        elif n == 1:
            cur_row = [1, 1]
        else:
            idx = 1
            while idx < n:
                cur_row.append(last_row[idx - 1] + last_row[idx])
                idx += 1
            cur_row.append(1)
        yield cur_row
        last_row = cur_row
        cur_row = [1]
        n += 1
    return


n = 0
results = []
for t in g_triangle():
    results.append(t)
    n = n + 1
    if n == 10:
        break

for t in results:
    print(t)

if results == [
    [1],
    [1, 1],
    [1, 2, 1],
    [1, 3, 3, 1],
    [1, 4, 6, 4, 1],
    [1, 5, 10, 10, 5, 1],
    [1, 6, 15, 20, 15, 6, 1],
    [1, 7, 21, 35, 35, 21, 7, 1],
    [1, 8, 28, 56, 70, 56, 28, 8, 1],
    [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
]:
    print('测试通过!')
else:
    print('测试失败!')

#5. 迭代器 可以被next()函数调用并不断返回下一个值的对象称为迭代器
print(isinstance((x for x in range(10)), Iterator))
print(isinstance((x for x in range(10)), Iterable))
print(isinstance([], Iterator))
print(isinstance([], Iterable))
```
