---
layout: post
title: Httpcomponents-client 连接释放逻辑源码研究
tags: [HttpClient,Java]
categories: [Java技术研究]
date: 2017-10-11 12:59:24 +0800
comments: true
author: onecoder
thread_key: 1913
---
## 研究背景

上篇([Httpcomponents-core 从池中获取连接代码解析](http://www.coderli.com/httpclient-core-get-pool-entry-blocking-analysis/))研究中，我们知道，Httpcomponents-client底层维护了一个socket连接池，对于同一个地址，默认只可以建立2个连接。如果连接不及时释放，就会造成连接池中无可用的连接获取，从而导致请求等待（阻塞）。因此，我们需要关注连接池释放的逻辑。

<!--break-->

## 释放方式

一个比较常见的方式就通过**EntityUtils**类，比如**EntityUtils.consume**，源码如下：

```java
/**
     * Ensures that the entity content is fully consumed and the content stream, if exists,
     * is closed.
     *
     * @param entity the entity to consume.
     * @throws IOException if an error occurs reading the input stream
     *
     * @since 4.1
     */
    public static void consume(final HttpEntity entity) throws IOException {
        if (entity == null) {
            return;
        }
        if (entity.isStreaming()) {
            final InputStream instream = entity.getContent();
            if (instream != null) {
                instream.close();
            }
        }
    }
```

### 源码解析
上述代码，看上去似乎跟连接的释放没什么关系，实际上，这里的InputStream的实现类是httpcomponents-client里封装的，
**EofSensorInputStream** 。而该Inputstream在构造的时候，会添加一个watcher，该watcher会监听流的消费，从而释放连接。4.3版本以后HttpEntity的实现类变为**ResponseEntityProxy**，其从Entity中获取Content的代码逻辑如下：

``` java
 @Override
    public InputStream getContent() throws IOException {
        return new EofSensorInputStream(this.wrappedEntity.getContent(), this);
    }
```

因此，在**EofSensorInputStream**关闭流的时候会有响应的处理：

``` java
 @Override
    public void close() throws IOException {
        // tolerate multiple calls to close()
        selfClosed = true;
        checkClose();
    }

protected void checkClose() throws IOException {

        final InputStream toCloseStream = wrappedStream;
        if (toCloseStream != null) {
            try {
                boolean scws = true; // should close wrapped stream?
                if (eofWatcher != null) {
                    scws = eofWatcher.streamClosed(toCloseStream);
                }
                if (scws) {
                    toCloseStream.close();
                }
            } finally {
                wrappedStream = null;
            }
        }
    }
```

可见，在关闭流的时候，会回调watcher的streamCloased方法，在方法中会对连接进行释放：

``` java
@Override
    public boolean streamClosed(final InputStream wrapped) throws IOException {
        try {
            final boolean open = connHolder != null && !connHolder.isReleased();
            // this assumes that closing the stream will
            // consume the remainder of the response body:
            try {
                if (wrapped != null) {
                    wrapped.close();
                }
                releaseConnection();
            } catch (final SocketException ex) {
                if (open) {
                    throw ex;
                }
            }
        } catch (final IOException ex) {
            abortConnection();
            throw ex;
        } catch (final RuntimeException ex) {
            abortConnection();
            throw ex;
        } finally {
            cleanup();
        }
        return false;
    }
```
## 总结

至此，已经基本理解了HttpClient释放连接的方式，就是在他封装的Entity流上，增加一个watcher，只要调用了stream的close方法，就会自动释放连接。所以，你可见到在EntityUtil中的各种消费Entity的函数中都会去主动关闭流。这也是为什么我们强调在使用HttpClient的过程中，即使Response不使用也一定要消费掉，因为不消费会导致连接永远不会释放。最终造成连接池耗尽造成阻塞。


