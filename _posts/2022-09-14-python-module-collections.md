---
title: Python练习-常用内建模块collections
tags: [Python]
categories: [Python技术研究]
date: 2022-09-14 22:30:24 +0800
comments: true
author: onecode
---
本部分学习Python常用内建模块collections。collections模块中提供了很多集合相关的类，如namedtuple、OrderDict、ChainMap以及Count等。便于针对特定使用场景，高效的进行集合操作。

# 一、namedtuple
namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来使用tuple的某个元素。主要的作用是增强了使用tuple时的可读性

```python
# namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
Boys = namedtuple("Boy", ["name", "age"])
boy_one = Boys("One", 20)
print(boy_one)
print(boy_one.name)
print(isinstance(boy_one, tuple))
```
<!--more-->
输出如下：
> Boy(name='One', age=20)  
> One  
> True

# 二、deque

deque是一个双向列表，可以高效实现插入和删除操作
```python
dq = deque(['a', 'b', 'c'])
dq.append("zz")
dq.appendleft("XX")
print(dq)
dq.popleft()
print(dq)
```
输出如下：
> deque(['XX', 'a', 'b', 'c', 'zz'])  
> deque(['a', 'b', 'c', 'zz'])

# 三、defualdict
defualdict是一个当key不存在返回默认值的dict

```python
dd = defaultdict(lambda: "Key does not exist")
dd["k1"] = "val1"
print(dd["k1"])
print(dd["k2"])
```
输出如下：
> val1  
> Key does not exist

# 四、OrderedDict
OrderedDict是key按照插入顺序的dict
```python
od = OrderedDict()
od["a"] = 1
od["c"] = 3
od["b"] = 2
print(od.keys())
```
输出如下：
> odict_keys(['a', 'c', 'b'])

# 五、ChainMap
ChainMap可以把一组dict串起来并组成一个逻辑上的dict。ChainMap本身也是一个dict，但是查找的时候，会按照顺序在内部的dict依次查找。适合于例如：多处设置同一变量值，存在变量值覆盖，但是有取值优先级的场景。

```python
dict_one = {"A": "AOne"}
dict_two = {"A": "BOne", "B": "Two"}
dic_three = {"C": "CThree"}
cm = ChainMap(dict_one, dict_two, dic_three)
print(cm.get("A"))
print(cm.get("B"))
print(cm.get("C"))
```
输出如下：
> AOne  
> Two  
> CThree

# 六、Counter
Counter计数器用于统计字符出现的次数
```python
c = Counter("Javajavascriptpython")
print(c)
```
输出如下：
> Counter({'a': 4, 'v': 2, 'p': 2, 't': 2, 'J': 1, 'j': 1, 's': 1, 'c': 1, 'r': 1, 'i': 1, 'y': 1, 'h': 1, 'o': 1, 'n': 1})
