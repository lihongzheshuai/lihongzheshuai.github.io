---
title: TensorFlow's Hello World Mnist数据集下载错误问题解决 
tags: [TensorFlow, Python]
categories: [知识扩展]
date: 2017-12-05 16:56:24 +0800
comments: true
author: onecode
---
部署Anaconda 科学计算包，并通过

```shell
conda install -c conda-forge tensorflow
```

部署tensorflow相关包。在ipython环境下执行下列命令下载训练数据包

```shell
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
```

结果报错, 

> [Errno 104] Connection reset by peer

![错误信息][1]


  <!--break-->
  
  从错误信息看，应该网络问题。仔细查看错误堆栈，找到了
 
 anaconda3/lib/python3.6/site-packages/tensorflow/contrib/learn/python/learn/datasets/mnist.py
 
 这个文件。
 
 发现里面的数据文件是从storage.googleapis.com下载的，自然访问不通。改成上面的镜像地址，即可：
 
 ![网址替换][2]

再次执行命令，一切ok

![正常][3]


  [1]: /images/post/tensorflow-mnist-data/error.jpg
  [2]: /images/post/tensorflow-mnist-data/url.jpg
  [3]: /images/post/tensorflow-mnist-data/success.jpg

