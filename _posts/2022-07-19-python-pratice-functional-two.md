---
title: 2022-07-19 python练习-函数式编程（二）
tags: [python]
date: 2022-07-19 22:09:24 +0800
comments: true
author: onecode
---
本部门练习Python函数式编程，第二部分。
<!--more-->

``` python
# 1. 返回函数、闭包
import functools
import time


def cal_sums(*args):
    def do_sum():
        result = 0
        for x in args:
            result += x
        return result

    return do_sum


call_sum = cal_sums(1, 3, 5, 7, 9)
call_sum_two = cal_sums(1, 3, 5, 7, 9)
print(call_sum)
print(call_sum_two)
print(call_sum())


def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i * i

        fs.append(f)
    return fs


f1, f2, f3 = count()

print(f1)
print(f1(), f2())


def count_two():
    fs = []

    def g(j):
        def f():
            return j * j

        return f

    for i in range(1, 4):
        fs.append(g(i))
    return fs


f4, f5, f6 = count_two()
print(f4(), f5(), f6())


# 练习 利用闭包返回一个计数器函数，每次调用它返回递增整数：
def createCounter():
    x = 0

    def counter():
        nonlocal x
        x += 1
        return x

    return counter


# 测试:
counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')

# 2. 匿名函数
l = list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(l)


# 练习
# 请用匿名函数改造下面的代码：

def is_odd(n):
    return n % 2 == 1


L = list(filter(is_odd, range(1, 20)))
M = list(filter(lambda x: x % 2 == 1, range(1, 20)))
print(M)


# 3. 装饰器

def print_date():
    print('2022-07-10')


f = print_date

print(print_date.__name__)
print(f.__name__)


def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper


@log
def print_date():
    print('2022-07-10')


print_date()


@log
def print_sth(str):
    print(str)
    return "print_sth_return"


p_r = print_sth("print-something")
print(p_r)
print(print_sth.__name__)


def log_fun_name(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper


@log_fun_name
def print_sth(str):
    print(str)
    return "print_sth_return"


p_r = print_sth("print-something")
print(p_r)
print(print_sth.__name__)


# 练习 1.请设计一个decorator，它可作用于任何函数上，并打印该函数的执行时间：

def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kvs):
        start_time = time.time()
        result = fn(*args, **kvs)
        end_time = time.time()
        print('%s executed in %s ms' % (fn.__name__, end_time - start_time))
        return result

    return wrapper


# 测试
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;


@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;


f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')


# 练习2. 请编写一个decorator，能在函数调用的前后打印出'begin call'和'end call'的日志。
#
# 再思考一下能否写出一个@log的decorator，使它既支持：
# @log
# def f():
#     pass
# 又支持
# @log('execute')
# def f():
#     pass

def log(*text):
    print(text)

    def wrapper(func):
        def excute(*args, **kvs):
            print("Text:", text, "Length", len(text))
            print("begin call")
            result = func(*args, **kvs)
            print("end call")
            return result

        return excute

    return wrapper


@log("execute", "exg", "abcd")
def f():
    return "Have Args"


print(f())


@log()
def f():
    return "No args"


print(f())

#4. 偏函数
int2 = functools.partial(int, base=2)
print(int2("10000"))
```
