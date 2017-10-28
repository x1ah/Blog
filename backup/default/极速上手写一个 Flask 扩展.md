---  
title: 极速上手写一个 Flask 扩展  
category: default  
date: 2017-10-28T13:40:16Z   
url: https://github.com/x1ah/Blog/issues/17  
---

    >假设我是一个接口贩子，专门提供各种各样的 API 给我的客户们，主要这些 API 后端是用 Python + Flask 实现的。我需要管理和监控我的这些 API 们，看看哪些更受欢迎，哪些响应慢，哪些需要改进，于是我想给我的后端服务做个 Dashboard，能看到上面那些数据，并且想把这个东西抽象出来，以后我还能卖其他 API，还能用在我的其他项目上，于是乎打算做成一个插件。

先假装有一个存数据的客户端，👇
```python
class APIDogClient:
    '''APIDog: 收集接口服务的各种信息，请求耗时，请求路径，请求 IP 等等等等'''
    def __init__(self, secret_key):
        self.host = 'x.x.x.x'   # 假装我有一些配置需要初始化
        self.port = 'xxx'
        self.secret_key = secret_key
        self.secret_id = 'xxx'
        self.bucket = []

    def storge(self, data):
        # clean data
        self.bucket.append(data)
```

现在可以开始着手插件了，给插件取名为 `flask-APIDog`，第一代打算收集每次请求的路径，每个请求的耗时，每次请求的 IP。每次请求都这些数据一起发送到我的 APIDog 服务端存起来，并展示到 Dashboard 上。
```python
import time

from flask import Flask, request, current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class APIDog:
    '''Flask-APIDog extendsion'''
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
            self.api_dog = APIDogClient(self.app.config.get('api_dog_secret_key', ''))

    def init_app(self, app=None):
        self.app = app
        self.api_dog = APIDogClient(self.app.config.get('api_dog_secret_key', ''))
        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def _before_request(self):
        ctx = stack.top
        ctx._api_dog_data = {
            'request_begin_time': time.time()
        }

    def _after_request(self, response):
        ctx = stack.top
        api_request_begin_time = ctx._api_dog_data.get('request_path', time.time())
        request_time = time.time() - api_request_begin_time
        api_data = {
            'request_time': request_time,
            'request_path': request.path,
            'request_location': request.args.get('location', ''),
            'remote_address': request.remote_addr
        }
        self.api_dog.storge(api_data)
```

👆 是第一版的 `flask-APIDog` 的代码，很简单的一些处理， Flask 扩展一般（官方建议）提供一个 `init_app` 方法，用于在实例化插件类后初始化 Flask APP，实际上这里只是简单的给 Flask APP 的 `before_request`，`after_request` 两个钩子函数提供两个具体流程，`_app_ctx_stack.top` 是 Flask
 里面上下文的概念，意思是取当前应用。更甚至完全可以直接用 `before_request`，`after_request` 装饰两个函数来实现上面那些功能，但是后面迭代版本会越来越复杂，直接写在项目里很容易污染现有代码，抽象成插件不仅提高了鲁棒性，还符合 Flask 的插件系统理念。