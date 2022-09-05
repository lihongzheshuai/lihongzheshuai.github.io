---
title: python练习-Hello World
tags: [python]
date: 2022-05-19 22:56:24 +0800
comments: true
author: onecode
---

``` python
# Python demo for lihz
# 1. Hello World
print("Hello World Python")

# 2. 输入输出
print("The quick brown fox", "jumps over the lazy dog")
print("100", "+", "200", "=", 100 + 200)
# name = input("What is your name ? \r\n")
# print("My name is",name)
print('''Line1
Line2
Line3''')

# 3. 字符串
print(chr(66))
print(chr(22334))
# bytes 数据类型
x = b'abc'
print(x)
print("中文".encode("utf-8"))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode("utf-8"))
print("My name is %s" % "OneCoder")
age = 38
print(f"My age is {age}")

# 4. list  tuple
# list 有序集合
numbers = ["8676", "8616", "8385"]
print("The length of list numbers is %s" % len(numbers))
numbers.append("8528")
numbers.pop(1)
numbers.insert(1, "8448")
print(numbers)

# tuple 不可变元组
families = ("Dad", "Mum", "Son")
print(len(families))
one = (1,)
print(one)
print((1))

# 5. 判断和循环
number = 20
if int(number) > 18:
    print(number)
elif int(number) > 6:
    print("less than 18")

sum = 0
for x in range(101):
    sum += x
print(sum)

# 6. dict即map和Set
d = {"Dad": 38, "Mum": 37}
print(d["Mum"])
print(d.get("Son", "Yummy"))
# set 元素不重复
s1 = set([1, 2, 3, 3])
print(s1)
s2 = set([2, 3, 4])
s1.add(5)
print(s1 & s2)
print(s1 | s2)

# 7. 函数
h = hex
print(h(12))


def print_name(name):
    print("My name is", name)


def return_tuple():
    return 12, 34


x, y = return_tuple()
print(x)
print(y)
print_name("Yummy")


def power(x, n=2):
    s = 1
    while n > 0:
        s = s * x
        n -= 1
    return s


print(power(5))
print(power(5, 3))


def sums(*nums):
    result = 0
    for i in nums:
        result += i
    return result


print(sums(1, 2, 3, 4, 5))


def person(name, age, **others):
    print("Name:", name, "Age:", age, "Others: ", others)


extra = {"city": "DaLian", "gender": "Male"}
# 获得的室extra的拷贝，修改不会影响extra的值
person("Yummy", 8, **extra)


def person_two(name, age, *, city):
    print("Name:", name, "Age:", age, "City:", city)


person_two("Yummy", 8, city="DaLian")


def f1(a, b, c=1, *args, **kwargs):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kwargs)


f1(1, 2, 4, 4, 4, 4, kwargs={"5": 5})
```
