---
title: Python练习-面像对象基础
tags: [python]
date: 2022-08-04 20:20:24 +0800
comments: true
author: onecode
---
本部分练习Python面像对象编程基础知识。练习代码如下：
<!--more-->
```python
python面像对象学习相关代码

import types

from demo.module.module import Student
import demo.module.module as im_module

# 对象类型
print(type(123))
print(type("123"))
print(type(Student("Object", 99)))
print(type(im_module.stu1))

print(type(abs) == types.BuiltinFunctionType)
print(type((x for x in range(10))) == types.GeneratorType)

print(isinstance("abc", str))
print(isinstance([1, 2, 3], (list, tuple)))

print(dir(Student))
print(dir("123"))
print(hasattr(im_module.stu1, "__init__"))
print(hasattr(im_module.stu1, "__name"))
getattr(im_module.stu1, "print_score")()


class Fruit():
    category = "one"

    def __init__(self, name):
        self.name = name


apple = Fruit("Apple")
pear = Fruit("pear")
print(getattr(apple, "name"))
pear.category = "two"
print(getattr(apple, "category"))
print(getattr(pear, "name"))
print(getattr(pear, "category"))


# 练习
# 为了统计学生人数，可以给Student类增加一个类属性，每创建一个实例，该属性自动增加：

class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

# 测试:
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Bart')
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)
            print('测试通过!')
```
