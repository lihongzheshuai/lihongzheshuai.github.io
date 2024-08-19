---
title: Python练习-IO操作 StringIO、BytesIO
tags: [Python]
categories: [Python技术研究]
date: 2022-08-21 20:20:24 +0800
comments: true
author: onecode
---
本部分学习Python的IO操作，包括StringIO、BytesIO以及文件（夹）操作3个部分。
<!--more-->

# 一、StringIO
StringIO用于在内存中生成并操作字符串。操作模式和之前练习的文件内存操作类似，是通过IO流的模式进行操作。代码如下：

```python
# 1. string io
import os
from datetime import datetime
from io import StringIO, BytesIO

str_io = StringIO()
str_io.write("Hello")
str_io.write(" ")
str_io.write("world")
print(str_io.getvalue())
str_io.seek(0, 0)
while True:
    str = str_io.readline()
    if str == "":
        break
    print(str.strip())
# 移动指针
str_io.seek(2, 0)
print(str_io.readline())
str_io_two = StringIO("What's this ?\nThis is a boy.")
while True:
    str = str_io_two.readline()
    if str == "":
        break
    print(str.strip())

print(str_io_two.getvalue())
```
需要注意的是，通过IO操作字符串，当使用write和read方法时，实际上是有一个指针在移动指向当前操作的位置的。因此，上面代码中
```python
# 移动指针
str_io.seek(2, 0)
```
是为了将指针移回到从开头两个字符的位置。否则，你直接通过read函数读取，是读不到任何信息的。移动后，通过read读取，输出为：
```
llo world
```

# 二、BytesIO
与StringIO类似，区别仅是BytesIO是在内存中操作字节，因此存在字节编码的问题。
```python
# 2. BytesIO，内存中操作字节
byte_io = BytesIO()
byte_io.write('这是中文'.encode())
print(byte_io.getvalue())
byte_io_two = BytesIO(b'\xe8\xbf\x99')
print(byte_io_two.getvalue())
print(byte_io_two.read().decode())
```
这里encode和decode函数是可以指定编码类型的。如utf-8、gbk等

# 三、操作文件和目录
Python中，主要通过os/os.path模块操作文件和目录
```python
# 3. 操作文件和目录
# 通过os变量获取一些信息
print(os.name)
# print(os.uname()) windows 不支持
print(os.environ)
# 通过os操作目录
# 获取当前目录
cur_path = os.path.abspath(".")
print(cur_path)
# 字符串操作，拼接路径
new_dir_path = os.path.join(cur_path, "dirdemo")
print(new_dir_path)
if not os.path.exists(new_dir_path):
# 创建目录
    os.mkdir(new_dir_path)
cur_file_path = os.path.join(cur_path, "io_demo.py")
# 字符串操作，提取后缀名
print(os.path.splitext(cur_file_path))
new_file_path = os.path.join(cur_path, "test.txt")
if not os.path.exists(new_file_path):
    with open(new_file_path, "x") as new_file:
        print(new_file)
# 重命名文件、删除文件
os.rename(new_file_path, "text.py")
os.remove(os.path.join(cur_path, "text.py"))
os.rmdir(new_dir_path)
```
最后，完成两个练习题：
```
# 练习 
# 1.利用os模块编写一个能实现dir -l输出的程序。 
# 2.编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。
```
样例代码如下：
```python
# 答1. dir命令
pwd = os.path.abspath('.')
print('      Size     Last Modified  Name')
print('------------------------------------------------------------')
for f in os.listdir(pwd):
    filesize = os.path.getsize(f)
    l_mod_time = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M')
    flag = '/' if os.path.isdir(f) else ''
    print("%10d %s %s%s" % (filesize, l_mod_time, f, flag))
# 答2，查找文件
search_file_name = input("Input file name:")
print("File name is: [%s]" % search_file_name)

def searchfile_in_dir(filename, dirpath):
    result = []
    for f in os.listdir(dirpath):
        if os.path.isdir(f):
            _tmp_result = searchfile_in_dir(filename, f)
            if  len(_tmp_result) > 0:
                result.extend(_tmp_result)
        else:
            if f.find(filename) != -1:
                result.append(f)
    return result


print(searchfile_in_dir(search_file_name, pwd))
```
