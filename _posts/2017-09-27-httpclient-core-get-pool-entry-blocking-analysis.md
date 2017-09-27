---
layout: post
title: Httpcomponents-core 从池中获取连接代码解析
tags: [HttpClient,Java]
date: 2017-09-27 20:18:24 +0800
comments: true
author: onecoder
thread_key: 1912
---
最近使用Httpcomponents-client过程中遇到一个线程阻塞的问题。通过jstack dump线程发现，是block在AbstractConnPool的getPoolEntryBlocking中，于是决定研究一下Httpcomponents-client的源码。

<!--break-->

# Httpcomponents-client连接池

Apache Httpcomponents-client是一个常用的Http客户端工具包，其底层通过socket绑定到指定目标，通过socket的io流发送和接受http协议相关信息。

出于效率考虑，httpclient底层利用一个连接池将socket连接缓存起来便于复用。本次研究的代码，就是关于httpcomponents-core 从池中获取连接的逻辑判断部分。代码如下：

```java
private E getPoolEntryBlocking(
            final T route, final Object state,
            final long timeout, final TimeUnit tunit,
            final Future<E> future) throws IOException, InterruptedException, TimeoutException {

        Date deadline = null;
        if (timeout > 0) {
            deadline = new Date(System.currentTimeMillis() + tunit.toMillis(timeout));
        }
        this.lock.lock();
        try {
            final RouteSpecificPool<T, C, E> pool = getPool(route);
            E entry;
            for (; ; ) {
                Asserts.check(!this.isShutDown, "Connection pool shut down");
                for (; ; ) {
                    entry = pool.getFree(state);
                    if (entry == null) {
                        break;
                    }
                    if (entry.isExpired(System.currentTimeMillis())) {
                        entry.close();
                    }
                    if (entry.isClosed()) {
                        this.available.remove(entry);
                        pool.free(entry, false);
                    } else {
                        break;
                    }
                }
                if (entry != null) {
                    this.available.remove(entry);
                    this.leased.add(entry);
                    onReuse(entry);
                    return entry;
                }

                // New connection is needed
                final int maxPerRoute = getMax(route);
                MyLogFactory.getPoolEntryBlockingLog().debug("Max conn count per route, default is 2. [" + maxPerRoute + "].");
                // Shrink the pool prior to allocating a new connection
                final int excess = Math.max(0, pool.getAllocatedCount() + 1 - maxPerRoute);
                MyLogFactory.getPoolEntryBlockingLog().debug("excess conn count [" + excess + "]. " +
                        "getAllocatedCount means: available + leased.");
                if (excess > 0) {
                    for (int i = 0; i < excess; i++) {
                        final E lastUsed = pool.getLastUsed();
                        if (lastUsed == null) {
                            break;
                        }
                        lastUsed.close();
                        this.available.remove(lastUsed);
                        pool.remove(lastUsed);
                    }
                }

                if (pool.getAllocatedCount() < maxPerRoute) {
                    final int totalUsed = this.leased.size();
                    final int freeCapacity = Math.max(this.maxTotal - totalUsed, 0);
                    MyLogFactory.getPoolEntryBlockingLog().debug("Free capacity is: [" + freeCapacity + "]. MaxTotal(default 20) - leased.size");
                    if (freeCapacity > 0) {
                        final int totalAvailable = this.available.size();
                        if (totalAvailable > freeCapacity - 1) {
                            if (!this.available.isEmpty()) {
                                final E lastUsed = this.available.removeLast();
                                lastUsed.close();
                                final RouteSpecificPool<T, C, E> otherpool = getPool(lastUsed.getRoute());
                                otherpool.remove(lastUsed);
                            }
                        }
                        final C conn = this.connFactory.create(route);
                        entry = pool.add(conn);
                        this.leased.add(entry);
                        return entry;
                    }
                }

                boolean success = false;
                try {
                    if (future.isCancelled()) {
                        throw new InterruptedException("Operation interrupted");
                    }
                    pool.queue(future);
                    this.pending.add(future);
                    if (deadline != null) {
                        success = this.condition.awaitUntil(deadline);
                    } else {
                        this.condition.await();
                        success = true;
                    }
                    if (future.isCancelled()) {
                        throw new InterruptedException("Operation interrupted");
                    }
                } finally {
                    // In case of 'success', we were woken up by the
                    // connection pool and should now have a connection
                    // waiting for us, or else we're shutting down.
                    // Just continue in the loop, both cases are checked.
                    pool.unqueue(future);
                    this.pending.remove(future);
                }
                // check for spurious wakeup vs. timeout
                if (!success && (deadline != null && deadline.getTime() <= System.currentTimeMillis())) {
                    break;
                }
            }
            throw new TimeoutException("Timeout waiting for connection");
        } finally {
            this.lock.unlock();
        }
    }
```

# 流程分析

![](/images/post/httpcomponents-core-get-pool-entry/httpcore-getPoolEntryBlocking.png)    

# 关于源码学习

我fork了一份httpcomponents的源码，增加了一些学习标记用的log。如需要可自行fork。  

**httpcomponents-core**  
[https://github.com/lihongzheshuai/httpcomponents-core](https://github.com/lihongzheshuai/httpcomponents-core)  
**httpcomponents-client** 
[https://github.com/lihongzheshuai/httpcomponents-client](https://github.com/lihongzheshuai/httpcomponents-client)


