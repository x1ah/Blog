---  
title: Flask 源码阅读（二）创建应用以及请求钩子  
category: Flask  
date: 2017-03-01T13:09:57Z   
url: https://github.com/x1ah/Blog/issues/3  
---

    >看优秀项目的源码有个技巧，那就是从最初的版本开始看，这样能更快的理解作者的思想，所以，下面的例子以及源码均为 flask 0.1 版本的源码，flask 0.1 版本代码总共也才600+行，非常短小精悍。

### 从例子开始
下面给一个特别简单的例子，从而来理解一个Web程序是如何启动并工作的
```python
#!/usr/bin/python
#coding: utf-8

# demo.py

from flask import Flask, g, request

app = Flask(__name__)

@app.before_request
def preprocess():
    print("======preprocess======")

@app.after_request
def afterprocess(response):
    global times
    print("=====afterprocess====== ")
    return response

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found"

@app.route("/", methods=["GET"])
def index():
    g.user = 'test'
    headers = request.headers
    return """
        Hello world!<br />
        g.user = {0}<br />
        headers={1}
    """.format(g.user, headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
```

先一句一句看，首先执行了`app = Flask(__name__)`，这过程发生了什么？怎么就创建了一个 app ？先看看 `Flask` 类里面到底有什么内容,部分解释如下

```python
class Flask(object):
    request_class = Request # 请求对象，继承于werkzeug.Request类，并做了一些定制化
    response_class = Response # 返回对象，是继承于werkzeug.Response 类，可以看作就是 werkzeug.Response
    static_path = '/static' # 静态文件目录
    secret_key = None # 默认secret_key 为空
    def __init__(self, package_name):
        self.debug = True # 默认开启 debug 模式
        self.package_name = package_name # 包名，也就是传入的__name__
        self.root_path = _get_package_path(self.package_name) # app 的根目录
        self.view_functions = {} # 视图函数
        self.error_handlers = {} # 也就是我们上面写过的错误处理函数
        self.before_request_funcs = [] # 同样的，里面用来存before_request装饰过的函数，顾名思义是在每次请求前执行的，这里还有一个小的注意点
        self.after_request_funcs = [] # 同理用after_request装饰过的函数，在后面版本更多用teardown_request了，在每次请求结束后执行
        self.url_map = Map() # 这里存放我们的URL映射关系

        if self.static_path is not None:
            self.url_map.add(Rule(self.static_path + '/<filename>',
                                  build_only=True, endpoint='static'))
            if pkg_resources is not None:
                target = (self.package_name, 'static')
            else:
                target = os.path.join(self.root_path, 'static')
            self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
                self.static_path: target
            })
```

这里就用到了前面谈到的 `werkzeug` 里的 [SharedDataMiddleware中间件](https://github.com/x1ah/Blog/issues/1)，初始化了我们的静态文件，以至于我们不用去在针对静态目录，为了访问静态文件而特意写一个视图函数处理，而只需要在同目录下建一个`static/`目录，这就方便多了。


之后便是这些请求钩子了，`before_request`, `after_request`, `errorhandler`，做的工作也仅仅是把这些装饰过的函数加到前面的列表/字典的，等待调用。具体实现如下

```python
class Flask(object):

    # ...
    
    def before_request(self, f):
        """Registers a function to run before each request."""
        self.before_request_funcs.append(f)
        return f

    def after_request(self, f):
        """Register a function to be run after each request."""
        self.after_request_funcs.append(f)
        return f
    def errorhandler(self, code):
        def decorator(f):
            self.error_handlers[code] = f
            return f
        return decorator
```

这些钩子函数都是用来干嘛的？
- `before_request` 在每次请求前执行，也可用来请求拦截，在后面会谈到
- `after_request` 在每次请求完成后执行
- 在后面的 flask 版本甚至还有 `before_first_request`, `teardown_request`之类。分别为第一次请求前，每次请求后无论出错不出错都执行
- `errorhandler`，这其实不应该叫做钩子，这是错误处理，其带的`code`参数正好对应 `HTTP` 状态码，对不同的状态码执行不同的错误处理逻辑
-------------------------------

于此，我们便创建了一个 `Web application`，正如前面谈 `WSGI` 说道，应用程序必须是可调用的，并且带两个位置参数，所以，在 Flask 类里面实现了 `__call__(self, environ, start_response)` 如下，恰好符合 `WSGI` 标准，

```python
class Flask(object):
    # ...
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
```