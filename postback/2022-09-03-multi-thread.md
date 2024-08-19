---
title: Python练习-多线程
tags: [python]
date: 2022-09-03 20:20:24 +0800
comments: true
author: onecode
---
本部门练习Python多线程操作，Python中得多线程虽然为真正得POSIX 多线程，但是由于全局进程锁GIL得存在，在计算密集型业务中，并不能发挥真正并发的作用。

Python中的多线程主要通过threading模块实现，结果操作与Java多线程和Python多进程类似。
<!--more-->
```python
# 多线程练习
import threading


def thread_run(text):
    print("Thread [%s] is running...text:[%s]" % (threading.current_thread().name, text))


print("Main thread name: %s" % threading.current_thread().name)
for i in range(4):
    t = threading.Thread(target=thread_run, args=(i,))
    t.start()
    t.join()

# 多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，
# 所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。
# 假定这是你的银行存款:
balance = 0


def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(2000000):
        change_it(n)


t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
```
多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，
所以，任何一个变量都可以被任何一个线程修改，因此需要通过锁机制保证变量修改的线程安全：
```python
# 通过锁保证线程安全
lock = threading.Lock()
balance_lock = 0


def change_it_lock(n):
    # 先存后取，结果应该为0:
    global balance_lock
    balance_lock = balance_lock + n
    balance_lock = balance_lock - n


def run_thread_with_lock(n):
    for i in range(3000000):
        lock.acquire()
        try:
            change_it_lock(n)
        finally:
            lock.release()


t1 = threading.Thread(target=run_thread_with_lock, args=(5,))
t2 = threading.Thread(target=run_thread_with_lock, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance_lock)

# 因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，
# 然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，
# 所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。
# Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。
```
代码整体输出如下：
```
Main thread name: MainThread
Thread [Thread-1 (thread_run)] is running...text:[0]
Thread [Thread-2 (thread_run)] is running...text:[1]
Thread [Thread-3 (thread_run)] is running...text:[2]
Thread [Thread-4 (thread_run)] is running...text:[3]
0（理论上会有线程安全问题，不一定为0）
0
```
多线程程序，还可以通过ThreadLocal实现线程内变量的存储、传递和线程间隔离
```python
thread_local = threading.local()


def read_thread():
    print("Thread [%s], text [%s]" % (threading.current_thread().name, thread_local.text))


def process_thread(text):
    thread_local.text = text
    read_thread()


t1 = threading.Thread(target=process_thread, args=("One",))
t2 = threading.Thread(target=process_thread, args=("Two",))
t1.start()
t2.start()
t1.join()
t2.join()
```
输出如下：
```
Thread [Thread-9 (process_thread)], text [One]
Thread [Thread-10 (process_thread)], text [Two]
```
