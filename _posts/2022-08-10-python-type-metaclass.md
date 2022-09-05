---
title: 2022-08-10 Python练习-type 和 metaClass
tags: [python]
date: 2022-08-10 20:20:24 +0800
comments: true
author: onecode
---
本部分学习用Type和metaClass动态创建类，添加属性和方法。
```python
# 使用元类 type 可以检查对象类型，也可以动态创建一个新类

class Student(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def do_study(self, value):
        print(self.name, "is studying", value)


stu2 = Student("S-Name", 18)
print(type(stu2))


def fn(self, name):
    print("Hello:", name)


MetaStu = type("MetaStu", (object,), dict(hello=fn))
meta_stu_instance = MetaStu()
meta_stu_instance.hello("Coder")


# 使用metaclass类
# 先定义metaclass，就可以创建类，最后创建实例。
# 所以，metaclass允许你创建类或者修改类。换句话说，你可以把类看成是metaclass创建出来的“实例”。

# 可以通过__new__方法动态添加属性和方法
class StudentMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['study'] = lambda self, value: self.do_study(value)
        return type.__new__(cls, name, bases, attrs)


class MyStudent(Student, metaclass=StudentMetaClass):
    pass


my_stu = MyStudent("OneCoder", 38)
my_stu.study("Python")
```
输出如下：
<!--more-->
<pre>
<class '__main__.Student'>
Hello: Coder
OneCoder is studying Python
</pre>
