---
title: Python练习-文件读写
tags: [python]
date: 2022-08-16 20:20:24 +0800
comments: true
author: onecode
---
本部门练习Python文件读写操作。与Java类似，需要注意文件打开后的关闭操作。
<!--more-->
```python
# 文件操作
import os

# 因为一定要关闭文件流，所以写在finally里
try:
    file = open('.\\resources\\file_demo')
    print(file.read())
finally:
    if file:
        file.close()

# 简便写法
with open('.\\resources\\file_demo') as f:
    print(f.read())

# 分批次读取，避免内存溢出
with open('.\\resources\\file_demo') as f:
    for line in f.readlines():
        print(line.strip())

with open('.\\resources\\file_demo') as f:
    buf = f.read(8)
    while buf:
        print(buf)
        buf = f.read(8)

with open('resources/chinese_file', encoding="utf-8") as f:
    for line in f.readlines():
        print(line.strip())

# 写文件，追加写入
with open('resources/write_file', "a", encoding="utf-8") as f:
    f.write("\n")
    f.write("追加写入")
```
Python中有with open的简便写法，统一关闭文件。在open方法中通过指定不同的模式决定对文件测操作，如：
```
r：代表读

w：代表写入

x：代表创建新文件

a：代表追加写入
```
