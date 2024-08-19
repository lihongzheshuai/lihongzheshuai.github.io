---
title: Python练习-常用内建模块struct
tags: [python]
date: 2022-09-28 22:00:24 +0800
comments: true
author: onecode
---
本部分学习Python内置模块struct。struct模块可以方便快速的处理字节，如将一个整数转化为字节数组的表示等。

传统情况下，如果我们想将一个32位的整数，用1个由4个字节组成的字节数组表示的话，需编写如下代码：
```python
n = 12345678
b1 = (n & 0xff000000) >> 24
b2 = (n & 0xff0000) >> 16
b3 = (n & 0xff00) >> 8
b4 = n & 0xff
bs = bytes([b1, b2, b3, b4])
print(b1, b2, b3, b4)
print(bin(b1))
print(bin(b2))
print(bin(b3))
print(bin(b4))
```
<!--more-->

输出
```
0 188 97 78
0b0
0b10111100
0b1100001
0b1001110
```

而且上述代码仅针对整型有效，当涉及到浮点数转化的时候，就很困难了。通过struct模块，可以快速实现二进制数据类型和bytes转换，兼容整型、浮点型。

```python
s_bytes = struct.pack('>I', 12345678)
print(s_bytes.hex('-'))
s_bytes = struct.pack('>f', 1234.5678)
print(s_bytes.hex('-'))
for b in s_bytes:
    print(b)
```
输出
```
00-bc-61-4e
44-9a-52-2b
68
154
82
43
```
其中00-bc-61-4e和44-9a-52-2b是字节对应的十六进制表示，后四行是44-9a-52-2b对应的十进制表示。

从bytes数据还原代码如下
```python
print(struct.unpack('>f', s_bytes))
```
这里的s_bytes，我们直接使用的是上面代码的输出结果，输出如下
```
(1234.5677490234375,)
```
精度还是有丢失的。

最后做一个有趣的练习，

```
请编写一段代码，检查任意文件是否是位图文件，如果是，打印出图片大小和颜色数。
# BMP格式采用小端方式存储数据，文件头的结构按顺序如下：
# 两个字节：'BM'表示Windows位图，'BA'表示OS/2位图； 一个4字节整数：表示位图大小； 一个4字节整数：保留位，始终为0；
# 一个4字节整数：实际图像的偏移量； 一个4字节整数：Header的字节数； 一个4字节整数：图像宽度；
# 一个4字节整数：图像高度； 一个2字节整数：始终为1； 一个2字节整数：颜色数。
```

```python
import base64, struct

bmp_data = base64.b64decode('Qk1oAgAAAAAAADYAAAAoAAAAHAAAAAoAAAABABAAAAAAADICAAASCwAAEgsAA' +
                            'AAAAAAAAAAA/3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3/' +
                            '/f/9//3//f/9//3//f/9/AHwAfAB8AHwAfAB8AHwAfP9//3//fwB8AHwAfAB8/3//f/9/A' +
                            'HwAfAB8AHz/f/9//3//f/9//38AfAB8AHwAfAB8AHwAfAB8AHz/f/9//38AfAB8/3//f/9' +
                            '//3//fwB8AHz/f/9//3//f/9//3//f/9/AHwAfP9//3//f/9/AHwAfP9//3//fwB8AHz/f' +
                            '/9//3//f/9/AHwAfP9//3//f/9//3//f/9//38AfAB8AHwAfAB8AHwAfP9//3//f/9/AHw' +
                            'AfP9//3//f/9//38AfAB8/3//f/9//3//f/9//3//fwB8AHwAfAB8AHwAfAB8/3//f/9//' +
                            '38AfAB8/3//f/9//3//fwB8AHz/f/9//3//f/9//3//f/9/AHwAfP9//3//f/9/AHwAfP9' +
                            '//3//fwB8AHz/f/9/AHz/f/9/AHwAfP9//38AfP9//3//f/9/AHwAfAB8AHwAfAB8AHwAf' +
                            'AB8/3//f/9/AHwAfP9//38AfAB8AHwAfAB8AHwAfAB8/3//f/9//38AfAB8AHwAfAB8AHw' +
                            'AfAB8/3//f/9/AHwAfAB8AHz/fwB8AHwAfAB8AHwAfAB8AHz/f/9//3//f/9//3//f/9//' +
                            '3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//3//f/9//38AAA==')


def bmp_info(data):
    print(data)
    bmp_info_tuple = struct.unpack('<ccIIIIIIHH', data[0:30])
    for b in bmp_info_tuple:
        print(b)
    return {
        'width': bmp_info_tuple[-4],
        'height': bmp_info_tuple[-3],
        'color': bmp_info_tuple[-1]
    }


# 测试
bi = bmp_info(bmp_data)
assert bi['width'] == 28
assert bi['height'] == 10
assert bi['color'] == 16
print('ok')
```
