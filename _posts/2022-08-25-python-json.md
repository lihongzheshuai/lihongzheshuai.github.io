---
title: Python练习-json操作
tags: [python]
date: 2022-08-25 20:20:24 +0800
comments: true
author: onecode
---
本部门学习Python的json转换操作。跟之前学的通过bytes的序列化接口非常类似。只是在类转换的时候略有不同。
<!--more-->
# 一、dict对象转换
对于dict对象，可直接进行通过json.dumps/json.dump接口转换字符串或保存到文件中。
```python
d = dict(name='Bob', age=18)
print(json.dumps(d))
json_file_path = os.path.join(pwd, "resources", "json_demo")
with open(json_file_path, "w") as jfile:
    json.dump(d, jfile)
```
输出为：
```
{"name": "Bob", "age": 18}
```
文件内内容为：
![json文件内容图片](/images/post/2022-09-05_14-46-20-python-json-demo-1.png "Json文件内容")

同样，从json或文件转换为json对象代码如下：
```python
obj_from_json_str = json.loads('{"name": "Bob", "age": 18}')
print(obj_from_json_str)
obj_from_json_file = None
with open(json_file_path, "r") as jfile:
    obj_from_json_file = json.load(jfile)
print(obj_from_json_file)
print(obj_from_json_str == obj_from_json_file)
print(obj_from_json_str is obj_from_json_file)
```
同样，两次转换结果只是值相同，为不同的对象。

# 二、类对象的json转换
对于一般类对象的json转换，需要指定属性处理的方法，一般来说类对象默认有__dict__属性，处理属性转换：
```python
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }


s = Student('Bob', 20, 88)
print(json.dumps(s, default=student2dict))
print(json.dumps(s, default=lambda obj: obj.__dict__))
```
从json到类对象，一样需要指定处理函数
```python
# 转换为类对象
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])


print(json.loads('{"age": 20, "score": 88, "name": "Bob"}'))
print(json.loads('{"age": 20, "score": 88, "name": "Bob"}', object_hook=dict2student))
```
# 三、小练习
```python
# 练习：对中文进行JSON序列化时，json.dumps()提供了一个ensure_ascii参数，观察该参数对结果的影响：
obj = dict(name='小明', age=20)
s = json.dumps(obj, ensure_ascii=True)
print(s)
s_false = json.dumps(obj, ensure_ascii=False)
print(s_false)
print(json.dumps(dict(name='小明大虎', age=20), ensure_ascii=True))
```
输出为：
```
{"name": "\u5c0f\u660e", "age": 20}
{"name": "小明", "age": 20}
{"name": "\u5c0f\u660e\u5927\u864e", "age": 20}
```
