---
title: Python练习-分布式任务
tags: [python]
date: 2022-09-06 07:57:24 +0800
comments: true
author: onecode
---
本部分练习Python分布式任务。在Python的multiprocessing模块中，提供了BaseManager类，可以非常简单快速的创建分布式调度任务。

思想也很简单，服务端开启端口，注册信息传递的队列，接收端链接对应地址和端口，拿到队列，获取其中传递的信息，进行对应处理即可。
如果有结果传回，可以在注册一个队列用于传递结果即可。样例代码如下：
<!--more-->

服务端
```python
# 分布实任务样例
import random, time, queue
from multiprocessing.managers import BaseManager

# 发送任务的队列:
work_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


def workqueue():
    return work_queue


def resultqueue():
    return result_queue


# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_work_queue', callable=workqueue)
QueueManager.register('get_result_queue', callable=resultqueue)

if __name__ == '__main__':
    # 绑定端口9000, 设置验证码'abcdefg':
    manager = QueueManager(address=('127.0.0.1', 9000), authkey=b'abcdefg')
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_work_queue()
    result = manager.get_result_queue()
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d: %d...' % (i, n))
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result for task %s: %s' % (i, r))
    # 关闭:
    manager.shutdown()
    print('master exit.')

```

接收端
```python
# task_worker.py

import time, sys, queue
from multiprocessing.managers import BaseManager


# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass


# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_work_queue')
QueueManager.register('get_result_queue')

if __name__ == '__main__':
    # 连接到服务器，也就是运行task_master.py的机器:
    server_addr = '127.0.0.1'
    print('Connect to server %s...' % server_addr)
    # 端口和验证码注意保持与task_master.py设置的完全一致:
    m = QueueManager(address=(server_addr, 9000), authkey=b'abcdefg')
    # 从网络连接:
    m.connect()
    # 获取Queue的对象:
    task = m.get_work_queue()
    result = m.get_result_queue()
    # 从task队列取任务,并把结果写入result队列:
    for i in range(10):
        try:
            n = task.get(timeout=1)
            print('run task %d * %d...' % (n, n))
            r = '%d * %d = %d' % (n, n, n * n)
            time.sleep(1)
            result.put(r)
        except queue.Queue.Empty:
            print('task queue is empty.')
    # 处理结束:
    print('worker exit.')
```

运行后，服务端输出如下：
> Put task 0: 5070...
> Put task 1: 6275...
> Put task 2: 8098...
> Put task 3: 410...
> Put task 4: 5582...
> Put task 5: 5498...
> Put task 6: 1595...
> Put task 7: 4307...
> Put task 8: 7980...
> Put task 9: 5601...
> Try get results...
> Result for task 0: 5070 * 5070 = 25704900
> Result for task 1: 6275 * 6275 = 39375625
> Result for task 2: 8098 * 8098 = 65577604
> Result for task 3: 410 * 410 = 168100
> Result for task 4: 5582 * 5582 = 31158724
> Result for task 5: 5498 * 5498 = 30228004
> Result for task 6: 1595 * 1595 = 2544025
> Result for task 7: 4307 * 4307 = 18550249
> Result for task 8: 7980 * 7980 = 63680400
> Result for task 9: 5601 * 5601 = 31371201
> master exit.

客户端输出如下：
> Connect to server 127.0.0.1...
> run task 5070 * 5070...
> run task 6275 * 6275...
> run task 8098 * 8098...
> run task 410 * 410...
> run task 5582 * 5582...
> run task 5498 * 5498...
> run task 1595 * 1595...
> run task 4307 * 4307...
> run task 7980 * 7980...
> run task 5601 * 5601...
> worker exit.

由此可见，通过Python的高度封装，实现一个分布式调度任务还是非常方便快捷的，这也是Python这类语言的优势所在。
