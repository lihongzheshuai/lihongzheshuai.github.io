---
title: 2022-08-07 Python练习-高级面向对象
tags: [python]
date: 2022-08-07 20:20:24 +0800
comments: true
author: onecode
---
本部分练习Python高级面向对象内容，主要学习__slots__和@property相关用法，详见代码：
<!--more-->
```python
# 1. 使用__slots__，限制允许动态绑定到实例上的属性或方法
from types import MethodType


class Student():
    # 使用__slot__ 限制绑定属性，只允许绑定如下属性或者方法。
    __slots__ = ("age", "set_age")
    pass


# 给实例绑定属性，对其他实例无效
stu1 = Student()
stu1.age = 18
print(stu1.age)
stu2 = Student()
# print(stu2.age)，会报错，
# 类绑定属性，所有实例都有
Student.type = "Pupil"
print(stu2.type)


def set_age(self, age):
    self.age = age


# 给实例绑定方法
stu2.set_age = MethodType(set_age, stu2)
stu2.set_age(25)
print(stu2.age)


# 测试子类__slots__
class GraduateStudent(Student):
    __slots__ = ("name")


g_stu1 = GraduateStudent()
g_stu1.name = "G_Stu_name"
print(g_stu1.name)
# stu1.name = "Name" 会报错
# 可允许绑定范围为子类和父类并集，若父类无限制，实际等于子类可以任意绑定
g_stu1.age = 11
print(g_stu1.age)


# 2. 使用@property，加在方法上，使get set方法变成属性。使类似stu1.score这样直接的属性赋值走方法，实现封装和校验等需求
class StudentPro():

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if value > 100:
            print("Invalid score value.", value, "Score must be between 0 and 100.")
        self.__score = value


stu_pro_one = StudentPro()
stu_pro_one.score = 99
print(stu_pro_one.score)
stu_pro_one.score = 101


# 练习 请利用@property给一个Screen对象加上width和height属性，以及一个只读属性resolution
class Screen(object):

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def resolution(self):
        return self.__width * self.__height

# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')
```
