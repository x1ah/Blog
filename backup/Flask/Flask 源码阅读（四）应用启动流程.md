
---
title: Flask 源码阅读（四）应用启动流程
category: Flask
date: 2017-03-04T02:46:00Z
url: https://github.com/x1ah/Blog/issues/5
---
    >结束了这些小细节，现在开始来把这些全部串起来，看看一个 Web 应用是怎么启动的，中间又触发了什么，先后顺序又是怎么样的，一个请求过来如何响应，以及 Flask 的几个特色点

在 WSGI 协议里面就已经提到过，应用程序必须是一个可调用对象，并且带两个参数，对应到 Python 里面，可以有三种实现方式：
- 可以是函数
- 可以是一个实例，它的类实现了__call__方法
- 可以是一个类，这时候，用这个类生成实例的过程就相当于调用这个类
在 Flask 里面采用了第二种，也就是 Flask 类实现了 `__call__` 方法。同时 WSGI 约定其必须返回一个可迭代对象，故先看看 `__call__` 的实现：
```python
class Flask(object):
    # ...
    def __call__(self, environ, start_response):
        """Shortcut for :attr:`wsgi_app`"""
        return self.wsgi_app(environ, start_response)
```
可见，其实是返回了一个 `WSGI` APP，跟着看看 `wsgi_app(environ, start_response)` 这个方法的实现：
```python
class Flask(object):
    def wsgi_app(self, environ, start_response):
        with self.request_context(environ):
            rv = self.preprocess_request() # 调度before_request装饰函数
            if rv is None:
                rv = self.dispatch_request() # 调度请求，调度视图函数
            response = self.make_response(rv)
            response = self.process_response(response) # 调度after_request 装饰函数
            return response(environ, start_response)
```
这段代码便是一次收到一次请求，Flask 的处理逻辑，详细解释一下，在 Flask 里面有 **上下文** 的概念，通俗的解释就是应用启动了便有了一个 **应用上下文** ，上下文可以抽象理解为一个隔离环境，必须在这个隔离环境下才能执行相关任务。同理，一个请求过来了 Flask 又给了你一个 **请求上下文**，意思就是只有在这个”请求隔离环境“内才能处理你的事务，而且，多个请求上下文执行任务是互不干扰的。暂时就先解释这些，后面在作详细阐述。
从上面代码来看，首先是在一个 **请求上下文** 内，`rv` 便是 `before_request` 列表里面逐个执行的首个返回结果。跟着，来到了 `preprocess_request()` 函数
```python
class Flask(object):
    # ...
    def preprocess_request(self):
        for func in self.before_request_funcs:
            rv = func()
            if rv is not None:
                return rv
```
*这里有个小技巧，很明显可以看出来，一旦某个函数有返回值，便会直接将返回结果传给 `rv`，然后不再去调用视图函数，直接构造 `response` ，之后无论请求哪个路由，都直接返回这个结果。这也就是我们常说的 **请求拦截** 了。所以，我们在实际开发中 `before request` 函数里很少提供返回值*

我们这里没有给返回值，于是来到了 `rv = self.dispatch_request()`，调度请求，根据URL调用视图函数。再来看看 `dispatch_request()`方法：
```python
```python
class Flask(object):
    # ...
    def dispatch_request(self):
        try:
            endpoint, values = self.match_request()
            return self.view_functions[endpoint](**values)
        except HTTPException, e:
            handler = self.error_handlers.get(e.code)
            if handler is None:
                return e
            return handler(e)
        except Exception, e:
            handler = self.error_handlers.get(500)
            if self.debug or handler is None:
                raise
            return handler(e)
```
这里有 Flask 的 HTTP 错误处理逻辑，先捕捉 `HTTPException` 错误，如果捕捉到了便通过 HTTP 状态码调用我们之前对应的 `error_handlers` 函数。并返回结果构造 `response` 对象，再调用 `after request` 函数。并且，在 `after request` 函数里面是可以修改 `response` 的（所以我们的 `after_request` 函数是需要带一个 `response` 形参的）。并且返回修改后的 `response`，实现如下：
```python
class Flask(object):
    # ...
    def process_response(self, response):
        session = _request_ctx_stack.top.session
        if session is not None:
            self.save_session(session, response)
        for handler in self.after_request_funcs:
            response = handler(response)
        return response
```
直接取栈顶会话作为当前会话。

--------------------------------------------------

再回到 `app.run()`，
```python
class Flask(object):
    # ...
    def run(self, host='localhost', port=5000, **options):
        from werkzeug import run_simple
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        return run_simple(host, port, self, **options)
```
默认参数里面给了默认的服务器就是本机，端口为 5000。首先判断了是否开了 debug 模式，因为在`werkzeug` 的 `run_simple()` 里面是没有 `debug` 参数的，而是以 `use_reloader` 参数来实现相似的功能，故先在 `options` 里 `pop` 出 `debug` 键值对，再赋值给 `use_reloader`，然后再调用 `run_simple()`,再跟着来到了 `werkzeug` 的源码，它的 `run_simple()` 实现如下：
```python
def run_simple(hostname, port, application, use_reloader=False,
               extra_files=None, threaded=False, processes=1):
    """
    Start an application using wsgiref and with an optional reloader.
    """
    def inner():
        srv = make_server(hostname, port, application, threaded,
                          processes)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass

    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        print '* Running on http://%s:%d/' % (hostname or '0.0.0.0', port)
    if use_reloader:
        # Create and destroy a socket so that any exceptions are raised before we
        # spawn a separate Python interpreter and loose this ability.
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        test_socket.bind((hostname, port))
        test_socket.close()
        run_with_reloader(inner, extra_files or [])
    else:
        inner()
```

这个 `inner` 函数便是运行开发服务器，等待我们的请求的东西。接下来的 `if` 判断便是我们每次启动开发服务器打印的第一条日志。` * Running on http://0.0.0.0:5000/`，后面的 `if use_reloader` 便是 `debug` 模式的关键所在，**这点有些不明白，什么时候创建销毁 这个套接字，有什么意义？**
然后在 `run_with_reloader` 里面开一个线程运行 `inner()`，等待请求。这便是整个流程。

------------------------------------

### 小结
整合上面的各点，再来捋一捋这整个过程
![](http://ww1.sinaimg.cn/large/005NaGmtly1fde33m2ou2j30nf0p5wgm)

---------------------

上面这些只是特别简单的捋了一遍，这个小部分就到这里了。