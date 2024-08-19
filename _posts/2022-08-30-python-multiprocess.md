---
title: Python练习-多进程
tags: [Python]
categories: [Python技术研究]
date: 2022-08-30 20:20:24 +0800
comments: true
author: onecode
---
本部门学习Python多进程编程，若在linux环境下，可以使用fork函数，windows环境下没有该函数，可通过Process模块实现。
<!--more-->
```python
# windows没有fork调用，因此无法使用os.fork函数
# 使用multiprocessing模块

def sub_process_runner(name):
    print("I am a child process name: [%s]. PID:[%s]" % (name, os.getpid()))


if __name__ == "__main__":
    print('Parent process %s.' % os.getpid())
    sub_p = Process(target=sub_process_runner, args=("sub_proc_name",))
    print("Child proc start")
    sub_p.start()
    # 等待子线程结束再继续执行
    sub_p.join()
    print("Child proc finish")
```
其中，Process()函数，通过targe指定一个在进程中要运行的函数，通过args给函数传参。join函数用于等待创建的进程执行完成。输出如下：
```
Parent process 42896.
Child proc start
I am a child process name: [sub_proc_name]. PID:[6172]
Child proc finish
```
上述为创建一个进程，若想批量创建进程，可以使用进程池模块。Pool
```python
# 进程池
def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random() * 2)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    print('Pool parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
```
```
 Pool parent process 42896.
Waiting for all subprocesses done...
Run task 0 (51456)...
Run task 1 (42808)...
Run task 2 (10044)...
Run task 3 (29200)...
Task 1 runs 0.24 seconds.
Run task 4 (42808)...
Task 2 runs 1.13 seconds.
Task 0 runs 1.43 seconds.
Task 3 runs 2.00 seconds.
Task 4 runs 1.81 seconds.
All subprocesses done.
```
4个进程的池，执行5个任务，所以最后一个任务需要等待有任务执行完成，才能在池中去到进程去执行函数。

进程间若要进行数据交互，可以用Queue等数据结构
```python
# 进程间通信

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['Apple', 'Banana', 'Cat', 'Dog']:
        print('Put [%s] to queue...' % value)
        q.put(value)
        time.sleep(random())


# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get [%s] from queue.' % value)


if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
```
上述代码，一个进程向queue写数据，一个进程读取数据。读完后销毁。输出如下：
```
Process to write: 54176
Put [Apple] to queue...
Process to read: 38456
Get [Apple] from queue.
Put [Banana] to queue...
Get [Banana] from queue.
Put [Cat] to queue...
Get [Cat] from queue.
Put [Dog] to queue...
Get [Dog] from queue.
```
此外，通过subprocess模块，可以实现系统函数调用，如：
```python
if __name__ == '__main__':
    print('$ nslookup www.baidu.com')
    r = subprocess.call(['nslookup', 'www.baidu.com', ], text=True, encoding="utf-8")
    print('Exit code:', r)

if __name__ == '__main__':
    print('$ nslookup')
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output.decode('gbk'))
    print('Exit code:', p.returncode)
```
