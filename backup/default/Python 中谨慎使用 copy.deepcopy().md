---  
title: Python 中谨慎使用 copy.deepcopy()  
category: default  
date: 2017-12-24T04:14:50Z   
url: https://github.com/x1ah/Blog/issues/18  
---

    >在一次做 Benchmark 的时候，发现无论如何调代码，最后总是不尽人意，之后用 `pstats` 分析发现 `copy.deepcopy` 占了很大一部分运行时间，于是挑出来看了下，让其与 `dict.copy` 比较下，惊了
![image](https://user-images.githubusercontent.com/14919255/34324313-51777d70-e8a9-11e7-9296-109bd4461be6.png)


## 性能比较
```python
in [1]: import string
In [2]: def test_copy():
    ...:     d = {}
    ...:     for i, c in enumerate(string.ascii_letters):
    ...:         d[i] = c
    ...:     return d.copy()
    ...:
    ...:

In [3]: def test_deepcopy():
    ...:     d = {}
    ...:     for i, c in enumerate(string.ascii_letters):
    ...:         d[i] = c
    ...:     return copy.deepcopy(d)
    ...:

In [4]: %timeit -r 100 r = test_deepcopy()
96.4 µs ± 4.13 µs per loop (mean ± std. dev. of 100 runs, 10000 loops each)

In [5]: %timeit -r 100 r = test_copy()
6.55 µs ± 98.4 ns per loop (mean ± std. dev. of 100 runs, 100000 loops each)
```

96 - 6 的差异，惊+1

## 解决
- 在无需使用深拷贝时，适当的使用 浅拷贝代替。
- 序列化后再反序列化
- 实现 `__deepcopy__` 方法

## Tips
http://www.algorithmdog.com/slow-python-deepcopy