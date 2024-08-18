---
title: Python练习-常用内建模块hashlib
tags: [python]
date: 2022-10-07 21:40:24 +0800
comments: true
author: onecode
---
本部分学习Python常用内置模块hashlib。主要封装了md5、sha1等常用的摘要算法。摘要算法主要用来判断文本、代码等是否被修改，以及利用其不可逆性，用于在数据库中密文保存密码。
<!--more-->
```python
# Python中hashlib摘要算法类库
import hashlib

md5 = hashlib.md5()
md5.update('This is a python hashlib demo'.encode('utf-8'))
print(md5.hexdigest())
md5.update('this is a python hashlib demo'.encode('utf-8'))
print(md5.hexdigest())
sha1 = hashlib.sha1()
sha1.update("This is a python ".encode("utf8"))
sha1.update("hashlib demo".encode("utf8"))
print(sha1.hexdigest())
```
输出如下：
```
016109b4d87fb870e8cc61fd8075a15c
1acf688f896ee8944c8d1ae3d87f5e39
e820e61f70631375dbcf508a2a2910e9c02867e2
```
1个数据库密码密文存储和判断的小练习
```python
# 练习 设计一个验证用户登录的函数，根据用户输入的口令是否正确，返回True或False：
# -*- coding: utf-8 -*-
db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}


def login(user, password):
    md5 = hashlib.md5()
    md5.update(password.encode("utf8"))
    md5_pass = md5.hexdigest()
    if md5_pass == db.get(user):
        return True
    else:
        return False


# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')
```
考虑到对于相同的密码，摘要后的值也相同，所以可以根据用户特征，进行“加盐”。如下练习

```python
# 练习2，实现加salt的登录验证
# -*- coding: utf-8 -*-
import hashlib, random


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.salt = self.username
        self.password = get_md5(password + self.salt)


db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}


def login(username, password):
    user = db[username]
    return user.password == get_md5(password + username)


# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')
```
