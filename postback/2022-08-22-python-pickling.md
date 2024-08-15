---
title: Python练习-序列化
tags: [python]
date: 2022-08-22 20:20:24 +0800
comments: true
author: onecode
---
本部分学习Python序列化相关操作。序列化主要是为了将内存中的对象持久化到磁盘（文件）以便于后续从文件中恢复对象。可用于对象持久化和网络传输。

本文主要学习字节流序列化操作。Python中用字节流序列化对象用pickle模块。
<!--more-->
# 一、对象转字节（序列化）
通过pickle.dumps()方法，可以直接生成序列化后的字节流，如：
```python
import json
import os.path
import pickle

d = dict(name='Bob', age=18)
# 转换为字节流
print(pickle.dumps(d))
```
```
输出为：
b'\x80\x04\x95\x1a\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04name\x94\x8c\x03Bob\x94\x8c\x03age\x94K\x12u.'
```
也可以通过 pickle.dumps(对象，文件)方法，直接持久化到文件中，如：
```python
# 直接序列化到文件
pwd = os.path.abspath(".")
pickle_file_path = os.path.join(pwd, "resources", "pickle_demo")
with open(pickle_file_path, "wb") as pfile:
    pickle.dump(d, pfile)
```
上述代码会在当前目录下的resources目录下生成一个pickle_demo序列化文件，并保存相应值

# 二、字节转对象（反序列化）
也是两种方式：

1、直接通过pickle.loads()方法，从字节值（刚才的输出结果）转换成对象，如：
```python
unpickle_from_bytes = pickle.loads(
    b'\x80\x04\x95\x1a\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04name\x94\x8c\x03Bob\x94\x8c\x03age\x94K\x12u.')
print(unpickle_from_bytes)
```
得到：
```
{'name': 'Bob', 'age': 18}
```
2、从文件（刚才生成的）直接反序列化成对象
```python
# 直接从文件读取反序列化对象
unpickle_from_file = None
with open(pickle_file_path, "rb") as pfile:
    unpickle_from_file = pickle.load(pfile)
print(unpickle_from_file)
```
同样输出：
```
{'name': 'Bob', 'age': 18}
```
上述两个对象值相同，但是为不同对象：
```python
# 只是值相同，不同对象
print(unpickle_from_bytes == unpickle_from_file)
print(unpickle_from_bytes is unpickle_from_file)
```
得到：
```
True
False
```
