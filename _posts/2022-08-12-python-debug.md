---
title: Python练习-调试和测试
tags: [Python]
categories: [Python技术研究]
date: 2022-08-12 20:20:24 +0800
comments: true
author: onecode
---
本部分学习Python代码调试和测试方法。可用的代码调试方法有：

print打印
logging记录
pdb调试/pdb.settrace()
unittest单元测试等。
样例代码如下：
<!--more-->
```python
# 程序调试
# 1.用断言
import pdb


def div(s):
    n = int(s)
    assert n != 0, "n is zero"
    return 10 / n


div(1)
# 可以在启动时增加 -O参数关闭断言

# 2.用logging
import logging

s = '5'
n = int(s)
logging.basicConfig(level=logging.INFO)
logging.info('n = %d' % n)
print(10 / n)

# 3. 用pdb.set_trace()，执行到此，进入pdb模式
# pdb.set_trace()
s = '0'
n = int(s)
logging.basicConfig(level=logging.INFO)
logging.info('n = %d' % n)
# print(10 / n)

# 4. 单元测试unittest
import unittest


class Dict(dict):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


# 从unittest.TestCase继承。
# 以test开头的方法就是测试方法
class unitTestDemo(unittest.TestCase):

    def test_init(self):
        d = Dict(a=1, b='test')
        print("testing...")
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')


# 练习 对Student类编写单元测试，结果发现测试不通过，请修改Student类，让测试通过：

class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        if 60 <= self.score < 80:
            return 'B'
        if 80 <= self.score <= 100:
            return 'A'
        if self.score < 0 or self.score > 100:
            raise ValueError()
        return 'C'


class TestStudent(unittest.TestCase):

    def test_80_to_100(self):
        s1 = Student('Bart', 80)
        s2 = Student('Lisa', 100)
        self.assertEqual(s1.get_grade(), 'A')
        self.assertEqual(s2.get_grade(), 'A')

    def test_60_to_80(self):
        s1 = Student('Bart', 60)
        s2 = Student('Lisa', 79)
        self.assertEqual(s1.get_grade(), 'B')
        self.assertEqual(s2.get_grade(), 'B')

    def test_0_to_60(self):
        s1 = Student('Bart', 0)
        s2 = Student('Lisa', 59)
        self.assertEqual(s1.get_grade(), 'C')
        self.assertEqual(s2.get_grade(), 'C')

    def test_invalid(self):
        s1 = Student('Bart', -1)
        s2 = Student('Lisa', 101)
        with self.assertRaises(ValueError):
            s1.get_grade()
        with self.assertRaises(ValueError):
            s2.get_grade()


if __name__ == '__main__':
    unittest.main()
```
其中，练习题部分，通过单元测试可以发现与预期不一致的地方，从而定位原函数中的错误。

Python中还有一种特殊且有用的测试，文档测试，可以对注释中特定格式的代码进行测试，例如：
```python
# 测试文档
class Dict(dict):
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

if __name__=='__main__':
    import doctest
    doctest.testmod()
```
其中>>>部分的代码极为测试代码，下面的100，200即为期望输出值。练习如下，对fact进行doctest，完善注释代码：
```python
def fact(n):
    '''
    Calculate 1*2*...*n
    
    >>> fact(1)
    1
    >>> fact(10)
    ?
    >>> fact(-1)
    ?
    '''
    if n < 1:
        raise ValueError()
    if n == 1:
        return 1
    return n * fact(n - 1)
 ```
 直接运行获得错误信息如下：
```
 Error
**********************************************************************
File "C:\Users/lihongzhe/PycharmProjects/pyforwork/demo\testDocs.py", line 50, in fact
Failed example:
    fact(-1)
Exception raised:
    Traceback (most recent call last):
      File "C:\Program Files\JetBrains\PyCharm Community Edition 2022.1.3\plugins\python-ce\helpers\pycharm\docrunner.py", line 138, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest fact[2]>", line 1, in <module>
        fact(-1)
      File "C:\Users/lihongzhe/PycharmProjects/pyforwork/demo\testDocs.py", line 54, in fact
        raise ValueError()
    ValueError
```
 
```
 Failure
<Click to see difference>

**********************************************************************
File "C:\Users/lihongzhe/PycharmProjects/pyforwork/demo\testDocs.py", line 48, in fact
Failed example:
    fact(10)
Expected:
    ?
Got:
    3628800
```
 根据错误信息，修改注释代码如下：
 ```python
 def fact(n):
    '''
    Calculate 1*2*...*n

    >>> fact(1)
    1
    >>> fact(10)
    3628800
    >>> fact(-1)
    Traceback (most recent call last):
    ...
    ValueError
    '''
    if n < 1:
        raise ValueError()
    if n == 1:
        return 1
    return n * fact(n - 1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
 ```
 测试通过。
