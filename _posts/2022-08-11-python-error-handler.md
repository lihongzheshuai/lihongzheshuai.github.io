---
title: Python练习-错误处理
tags: [python]
date: 2022-08-11 20:20:24 +0800
comments: true
author: onecode
---
本部分练习python中的异常处理，相当于Java中的try...catch...finally，不同的是：

1.Python中的语句是try....except....finally
2.Python中有try....except...else...finally语句，期中else语句是当没有异常捕获时执行；
3.Python中主动抛出异常的语句时raise。
<!--more-->
```python
# 1.try except 捕获error
import logging

try:
    print('try...')
    r = 10 / 2
    print('result:', r)
except ZeroDivisionError as e:
    print('except:', e)
else:
    print("No error")
finally:
    print('finally...')
print('END')

try:
    print('try...')
    r = 10 / 0
    print('result:', r)
except ZeroDivisionError as e:
    print('except:', e)
    # logging.exception(e)
    logging.exception("Logging Error")
else:
    print("No error")
finally:
    print('finally...')
print('END')


class myError(BaseException):
    pass


try:
    raise myError()
except myError as e:
    logging.exception(e)
    # raise

# 练习 根据异常堆栈定位错误，并修改语句
from functools import reduce


def str2num(s):
    # int(s) 根据堆栈修改
    return float(s)


def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)


def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    print('99 + 88 + 7.6 =', r)


main()
```
上述代码中，最后的练习部分，异常堆栈输出为：
<pre>
Traceback (most recent call last):
  File "C:\Users\lihongzhe\PycharmProjects\pyforwork\demo\errorHandling.py", line 63, in <module>
    main()
  File "C:\Users\lihongzhe\PycharmProjects\pyforwork\demo\errorHandling.py", line 59, in main
    r = calc('99 + 88 + 7.6')
  File "C:\Users\lihongzhe\PycharmProjects\pyforwork\demo\errorHandling.py", line 53, in calc
    return reduce(lambda acc, x: acc + x, ns)
  File "C:\Users\lihongzhe\PycharmProjects\pyforwork\demo\errorHandling.py", line 47, in str2num
    return int(s)
ValueError: invalid literal for int() with base 10: ' 7.6'
</pre>


可以看到，错误是因为用int()函数对非整数进行了强转，因此改为float()即可。改后输出如下：


<pre>
100 + 200 + 345 = 645.0
99 + 88 + 7.6 = 194.6 
</pre>
