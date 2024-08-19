---
title: Python练习-常用内置模块datetime
tags: [Python]
categories: [Python技术研究]
date: 2022-09-12 22:10:24 +0800
comments: true
author: onecode
---
本部分学习Python常用内置模块datetime。通过datetime模块，我们可以很方便的操作日期、时间戳已经时区转换等操作。

构建datetime对象
```python
import re
from datetime import datetime, timedelta, timezone

now = datetime.now()
print(now)
print(type(now))

# 注意到datetime是模块，datetime模块还包含一个datetime类，通过from datetime import datetime导入的才是datetime这个类。
date = datetime(2022, 9, 9, 18, 53, 22)
print(date)
print(type(date))
```
注意到datetime是模块，datetime模块还包含一个datetime类，通过from datetime import datetime导入的才是datetime这个类
<!--more-->

输出如下
> 2022-09-12 22:02:09.479743  
> <class 'datetime.datetime'>  
> 2022-09-09 18:53:22  
> <class 'datetime.datetime'>  

通过datetime对象可以直接获取到时间戳，注意Python的时间戳是精确到秒的，Java、JS等的时间戳都是精确到毫秒
```python
# Python的timestamp，整数位精确到秒
tm = date.timestamp()
print(tm)

# 从秒到timestamp
print(datetime.fromtimestamp(tm))
# 转换为0时区
print(datetime.utcfromtimestamp(tm))
```
输出如下：
> 1662720802.0  
> 2022-09-09 18:53:22  
> 2022-09-09 10:53:22  

跟Java等一样，Python这类以开发效率著称的语言，自然会提供通过字符串转换为datetime的操作
```python
# 从字符串到timestamp
print(date.strptime("2022-09-12 14:46:34", "%Y-%m-%d %H:%M:%S"))
# 字符串格式标准，
# 参考https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

# 从timestamp到字符串
tm_str = date.strftime("%b-%d %a %H:%M:%S")
print("Timestamp string is:", tm_str)
```
输出：
> 2022-09-12 14:46:34  
> Timestamp string is: Sep-09 Fri 18:53:22  

具体字符串格式代码可参考：[https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)

通过datetime可方便的快速计算和转换时区
```python
# 创建时区
# 默认无时区
print(date.tzinfo)
# 创建时区
timez8 = timezone(timedelta(hours=8))
date8 = date.replace(tzinfo=timez8)
print(date8.tzinfo)
print(date8)

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)
ty_dt = bj_dt.astimezone(timezone(timedelta(hours=9)))
print(ty_dt)
```
输出
> UTC+08:00  
> 2022-09-09 18:53:22+08:00  
> 2022-09-12 14:02:09.484005+00:00  
> 2022-09-12 22:02:09.484005+08:00  
> 2022-09-12 23:02:09.484005+09:00  

最后做个练习：
> 练习
> 假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息如UTC+5:00，均是str，请编写一个函数将其转换为timestamp：

大概思路就通过字符串格式将非时区部分转化为datetime，通过正则识别出有时区部分，代码如下：
```python
def to_timestamp(dt_str, tz_str):
    r_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    utc_reg = re.compile(r"^(UTC)([+-])(\d)+(:)(00)")
    reg_match = utc_reg.match(tz_str)
    print(reg_match.groups())
    poorng = reg_match.group(2)
    tz_int = int(reg_match.group(3))
    if poorng == "+":
        r_dt = r_dt.replace(tzinfo=timezone(timedelta(hours=tz_int)))
    else:
        r_dt = r_dt.replace(tzinfo=timezone(timedelta(hours=-tz_int)))
    return r_dt.timestamp()


# 测试:
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1
t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2
print('ok')
```
