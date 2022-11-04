---
title: Python练习-常用内建模块contextlib
tags: [python]
date: 2022-11-04 22:20:24 +0800
comments: true
author: onecoder
---
最近很忙，距离上一篇博文过去已经10多天了，不想荒废。今天继续学习Python常用内置模块contextlib。其实主要是学习了contextlib这个模块中@contextmanager这个注解的使用。

<!--more-->

前面学习过，在Python可以使用with语句自动的进行如文件处理时的打开和关闭操作。其实从原理上讲，在Python任何实现了__enter__和__exit__方法的类都可以使用with语句进行自动操作。例如：

```python
# 本部分练习contextlib 内置模块

class ContextDemo(object):

    def __init__(self, name):
        self.jobname = name
        print("Init")

    def __enter__(self):
        print("Open")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exit")

    def dowork(self):
        print("Do %s here." % self.jobname)


with ContextDemo("DemoJob") as cd:
    cd.dowork()
```

输出如下：
```
Init
Open
Do DemoJob here.
Exit
```

每次编写enter和exit会很犯错，可通过contextlib中的contextmanager注解快速实现同样的功能，如：

```python
# 写enter和exit仍然繁琐，通过contextlib有更简便的写法
from contextlib import contextmanager


class ContextManagerDemo(object):

    def __init__(self, name):
        self.name = name

    def dowork(self):
        print('Do %s here....' % self.name)


@contextmanager
def do_cmd_job(name):
    print('Open')
    q = ContextManagerDemo(name)
    # 通过yield把q输出
    yield q
    print('Exit')


with do_cmd_job("CMDemoJob") as cmd:
    cmd.dowork()
```
输入如下：
```
Open
Do CMDemoJob here....
Exit
```
这里contextmanager注解，有点像Java中的切片编程，可以讲真正要执行的函数“夹”在事前和事后处理中间。

 如果一个对象没有实现上下文，我们就不能把它用于with语句。这个时候，可以用closing()来把该对象变为上下文对象。例如，用with语句使用urlopen()，这里其实closing也是利用contextmanager实现的，会默认调用传入对象的close方法，因此未实现close方法的类是无法使用closing函数的，会报错。这里通过源码可以看到urlopen对象是有close方法的。

```python
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen("http://www.coderli.com")) as page:
    for line in page:
        print(line)
```
输出如下：
```
Init
Do Closing here.
```
