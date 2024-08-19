---
title: Python练习-常用内建模块hmac
tags: [Python]
categories: [Python技术研究]
date: 2022-10-11 22:00:24 +0800
comments: true
author: onecoder
---
本部分学习Python内置模块hmac。实际hmac是承接hashlib中的md5等摘要算法加salt的操作。对该操作进行了封装，使用起来更加通用方便。在学些了之前内容的基础上，本部分内容比较简单直接。直接看代码即可。
<!--more-->
```python
# hmac 学习
message = b"This is a python"
key = b" hashlib demo"
h = hmac.new(key, message, digestmod='MD5')
print(h.hexdigest())

#练习 将上一节的salt改为标准的hmac算法，验证用户口令
# -*- coding: utf-8 -*-
import hmac, random

def hmac_md5(key, s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = hmac_md5(self.key, password)

db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}

def login(username, password):
    user = db[username]
    return user.password == hmac_md5(user.key, password)

# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')
```
唯一需要注意的是，在hmac.new中，传入的都是bytes。
