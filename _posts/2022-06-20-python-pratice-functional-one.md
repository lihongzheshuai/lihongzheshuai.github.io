---
title: python练习-函数式编程（一）
tags: [Python]
categories: [Python技术研究]
date: 2022-06-20 23:00:24 +0800
comments: true
author: onecode
---
本部分练习Python函数式编程。练习高阶函数、map、reduce等常用函数。
<!--more-->

``` python
# 1. 高阶函数
from functools import reduce

f = abs
print(f)
print(f(-10))


def absadd(x, y, f):
    return f(x) + f(y)


print(absadd(-3, -4, f))


# 2. map reduce
def fuc_square(x):
    return x * x


r_m = map(fuc_square, [1, 2, 3, 4, 5])
print(list(r_m))


def red_fuc(x, y):
    return x * 10 + y


r_r = reduce(red_fuc, [1, 3, 5, 7, 9])
print(r_r)


# 练习 1
# 利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。
# 输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']：
def normalize(name):
    return str.capitalize(name)


L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)


# 练习 2
# Python提供的sum()函数可以接受一个list并求和，
# 请编写一个prod()函数，可以接受一个list并利用reduce()求积：

def prod(L):
    def multi(x, y):
        return x * y

    return reduce(multi, L)


print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')


# 练习 3
# 利用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456
def str2float(s):
    dic = {"1": 1, "2": 2, "3": 3, ".": ".", "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}
    point = -1

    def map_fuc(x):
        return dic[x]

    def reduce_fuc(x, y):
        # 作用域上溯一层
        nonlocal point
        if y == ".":
            point = 1
            return x
        elif point == -1:
            return x * 10 + y
        else:
            point *= 10
            return x + y / point

    list_nums = list(map(map_fuc, s))
    print(list_nums)
    return reduce(reduce_fuc, list_nums)


print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')


# 3. filter
def is_odd(n):
    return n % 2 == 1


print(list(filter(is_odd, list(range(1, 11)))))


# 练习 生成质数数列
def odd_gen():
    n = 1
    while True:
        n += 2
        yield n


def not_divisible(n):
    return lambda x: x % n > 0


def primes():
    yield 2
    it = odd_gen()
    while True:
        n = next(it)
        yield n
        it = filter(not_divisible(n), it)


# 打印1000以内的素数:
for n in primes():
    if n < 1000:
        print(n)
    else:
        break

c = not_divisible(3)
print(c(3))


# 练习 回数是指从左向右读和从右向左读都是一样的数，例如12321，909。请利用filter()筛选出回数：
def int_gen():
    n = 1
    while True:
        yield n
        n += 1


def is_palindrome(n):
    if n < 10:
        return True
    if n % 10 == 0:
        return False
    temp = 0
    while n > temp:
        temp = temp * 10 + n % 10
        n = int(n / 10)
    return temp == n or int(temp / 10) == n


output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))
if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101,
                                                  111, 121, 131, 141, 151, 161, 171, 181, 191]:
    print('测试成功!')
else:
    print('测试失败!')

# 4. sort
print(sorted([36, 5, -12, 9, -21]))
print(sorted([36, 5, -12, 9, -21], key=abs))
print(sorted([36, 5, -12, 9, -21], key=abs, reverse=True))

# 练习 假设我们用一组tuple表示学生名字和成绩：
# L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
# 请用sorted()对上述列表分别按名字排序：

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]


def by_name(t):
    return t[0]


L2 = sorted(L, key=by_name)
print(L2)


# 再按成绩从高到低排序：
def by_score(t):
    return t[1]


L2 = sorted(L, key=by_score, reverse=True
            )
print(L2)
```
