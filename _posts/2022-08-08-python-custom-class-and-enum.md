---
title: Python练习-定制类和枚举
tags: [python]
date: 2022-08-08 20:20:24 +0800
comments: true
author: onecode
---
本部分学习Python中定制类和枚举部分。定制类其实就是类似Java中复写String，HashCode等方法，不过更灵活，可覆盖的方法更多。
<!--more-->
```python
# 1. 定制类
class Student():
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    def __str__(self):
        return "Student object. Name: %s, Age: %d" % (self.__name, self.__age)


print(Student("LiLei", 28))

# 2. 枚举类
from enum import Enum, unique

Month = Enum("MonthName", ("Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec"))
print(Month.Jan)
print(Month.Jan.value)
for name, member in Month.__members__.items():
    print(name, "=>", member, ",", member.value)

@unique
class WeekDay(Enum):
    Mon = 1
    Tue = 2
    Wed = 3
    Sun = 7

print(WeekDay.Mon)
print(WeekDay.Mon.value)
print(WeekDay(7))

#练习 把Student的gender属性改造为枚举类型，可以避免使用字符串：
class Gender(Enum):
    Male = 0
    Female = 1

class Student(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

# 测试:
bart = Student('Bart', Gender.Male)
if bart.gender == Gender.Male:
    print('测试通过!')
else:
    print('测试失败!')
```
