---
title: Python练习-模块和初级面像对象
tags: [Python]
categories: [Python技术研究]
date: 2022-08-01 20:20:24 +0800
comments: true
author: onecode
---
本部分练习Python模块和初级面像对象相关知识。练习代码如下：
<!--more-->
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' a test module '

__author__ = 'OneCoder Lihz'

import sys


def test():
    args = sys.argv
    print("args:", args)
    if len(args) == 1:
        print('Hello, world!')
    elif len(args) == 2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')


# 测试用法，当import导入时，__name__不等于main，代码不会执行。
if __name__ == '__main__':
    test()

# __doc__访问模块注释
print(__doc__)

print(sys.path)


# 类
class Student:
    # 必须的属性
    def __init__(self, name, score):
        # 类访问限制，私有属性
        self.__name = name
        self.__score = score

    def print_score(self):
        print(self.__name, "'s score is:", self.__score)


stu1 = Student("Sun One", 98)
# 随意添加属性
stu1.age = 18
stu1.print_score()


class Fruit:
    def __init__(self, name):
        self.__name = name

    def print_name(self):
        print("Fruit name is", self.__name)


class Apple(Fruit):
    def print_name(self):
        print("This is an apple")


class Pear(Fruit):
    pass
    # def __init__(self, name):
    #     self.__name = name
    #     print("Print name in class pear", self.__name)


fruit = Fruit("Grape")
fruit.print_name()
apple = Apple("Apple")
apple.print_name()
pear = Pear("Pear")
pear.print_name()
```
