---
title: Python练习-正贼表达式
tags: [python]
date: 2022-09-08 13:20:24 +0800
comments: true
author: onecode
---
本部分练习通过Python使用正则表达式。正则表达式是编程里一个很常用，很基础的知识，这里不做赘述。具体规则可以查阅关于正则学习的相关资料。这里重点练习通过Python编程使用正则表达式的方法。
<!--more-->
在Python中，通过re模块来使用正则表达式，如：
```python
# Python 中正则表达式，强烈建议使用r前缀，避免转义
import re

print(re.match(r"\d{4}-\d{8}", "0411-12345678"))
print(re.match(r"\d{4}-\d{8}", "0411-1234567"))

if re.match(r"\d{4}-\d{8}", "0411-12345678"):
    print("Match, OK!")
else:
    print("Don't match.")
```
输出如下：
> <re.Match object; span=(0, 13), match='0411-12345678'>
> None
> Match, OK!

在Python中，re.match函数如果匹配则返回Match对象，如果不匹配返回None

其他使用场景包括通过正则拆分字符串，分组字符串等，代码如下：
```python
# 可以更灵活的切分字符串，例如按空格切分（1个或者多个）
print(re.split(r"\s+", "a b  c"))
# 或者更灵活的按照给定的字符串切分
print(re.split(r"[\s,;]+", "a,b;c d  e"))

# 分组
g = re.match(r"(^\d{4})-(\d{8})$", "0411-12345678")
# group(0)永远是与整个正则表达式相匹配的字符串
print(g.group(0))
print(g.group(1))
print(g.group(2))

# 贪婪匹配，也就是尽可能多的匹配字符，如果增加?则改贪婪匹配为最小化匹配。
print(re.match(r'^(\d+?)(0?)(\d+?)(0*)$', '12202300').groups())
print(re.match(r'^([1-9]+)(0*)(\d+?)(0*)$', '12202300').groups())

# 先编译表达式，反复使用
re_com = re.compile(r'^([1-9]+)(0*)(\d+?)(0*)$')
print(re_com.match("12202300").groups())
print(re_com.match("123234200233430000").groups())
```
输出如下：
> ['a', 'b', 'c']
> ['a', 'b', 'c', 'd', 'e']
> 0411-12345678
> 0411
> 12345678
> ('1', '', '22023', '00')
> ('122', '0', '23', '00')
> ('122', '0', '23', '00')
> ('1232342', '00', '23343', '0000')

最后，两个小练习：

```python
# 练习练习
# 请尝试写一个验证Email地址的正则表达式。版本一应该可以验证出类似的Email：
# someone@gmail.com
# bill.gates@microsoft.com

def is_valid_email(addr):
    re_email = re.compile(r"^[\w.]+@\w+.\w+$")
    is_match = False
    if re_email.match(addr):
        is_match = True
    return is_match


# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')


# 版本二可以提取出带名字的Email地址：
# <Tom Paris> tom@voyager.org => Tom Paris
# bob@example.com => bob
def name_of_email(addr):
    re_mail_com = re.compile(r"@")
    mailaddr = re_mail_com.split(addr)[0]
    print(mailaddr)
    name = mailaddr
    if mailaddr.startswith("<"):
        re_name = re.compile(r"^(<)([\w\s]+)([>\w\s]+)$")
        name = re_name.match(mailaddr).group(2)
        print(name)
    return name


# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')
```
