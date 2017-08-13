---  
title: Flask 源码阅读（五）附：上下文  
category: Flask  
date: 2017-03-11T15:25:10Z   
url: https://github.com/x1ah/Blog/issues/7  
---

    先完全从 Flask 源码来观察上下文机制是怎样实现的

------------------------------------------------------

在 `Flask.wsgi_app` 方法内，前面解释过，是在一个请求上下文内进行一系列调度。在这个方法内的调用堆栈如下：
```
with self.request_context(environ)
    _RequestContext(self, environ）
```
实际上 ` _RequestContext` 就是一个自定义的上下文管理器，它的源码如下：
```python
class _RequestContext(object):
    def __init__(self, app, environ):
        self.app = app
        self.url_adapter = app.url_map.bind_to_environ(environ)
        self.request = app.request_class(environ)
        self.session = app.open_session(self.request)
        self.g = _RequestGlobals()
        self.flashes = None

    def __enter__(self):
        _request_ctx_stack.push(self)

    def __exit__(self, exc_type, exc_value, tb):
        if tb is None or not self.app.debug:
            _request_ctx_stack.pop()
```

----------------------

在这里，可以先提提上下文管理器，实际开发中，经常能用到的对文件 I/O 会这样写：
```python
with open("foo.txt", 'w') as f:
    f.write("hello world")
```
这样写的好处是不用我们自行去调用 `f.close()`，它会自动关闭，那么如何自己实现一个？实际上实现了 `__enter__` 和 `__exit__` 方法的类就可以作文一个上下文管理器。如下例子：
```python
 class mycontext(object):    
     def __init__(self, foo):
         self.foo = foo
     def __enter__(self):
         print("__enter__")
         print(self.foo)
     def __exit__(self, *args):
         print(self.foo)          
         print("__exit__") 

# 运行
>>> with mycontext("mycontext"):
               print("in mycontext")
>>> # output
__enter__
mycontext
in mycontext
mycontext
__exit__
```
可见，`__enter__` 和 `__exit__` 分别在 `with` 语句块前后执行。而上面的 ` _RequestContext` 类就是这样的一个上下文管理器。首先将自己（Request Context）推入 ` _request_ctx_stack` 栈中。在调度结束后又将其弹出栈。所以通过这样进栈出栈的方式，每次取栈顶作为当前请求上下文来实现隔离，而关于这个 ` _request_ctx_stack` 又是什么样的一种存在，我的理解如下：
它是一种 `Local Stack`，何为 `Local Stack`？就是对线程独立，甚至可以不妨将其看成是个映射表，键是线程 ID， 而值便是对应栈元素。同样可以应用于 **应用上下文**，应用上下文也是这样的原理，每次取栈顶元素，在推入请求上下文时会检查当前应用上下文栈是否为空，为空会自动推入当前应用上下文。
除了这些，其还有很多细节体现，没能仔细去往深处研究，个中细节也不能一一列出，然而，有一篇博客给了我很好的思路。TonySeek 的 [Flask 的 Context 机制](https://blog.tonyseek.com/post/the-context-mechanism-of-flask/)。
