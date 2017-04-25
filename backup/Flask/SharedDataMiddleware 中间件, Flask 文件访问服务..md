
---
title: SharedDataMiddleware 中间件, Flask 文件访问服务.
category: Flask
date: 2017-01-25T13:17:34Z
url: https://github.com/x1ah/Blog/issues/1
---
    [SharedDataMiddleware](http://werkzeug.pocoo.org/docs/0.11/middlewares/#werkzeug.wsgi.SharedDataMiddleware) 是 [Werkzeug](http://werkzeug.pocoo.org/docs/0.11/) 内的一个中间件，顾名思义，用来 share data 共享数据的。经常我们能看见一些软件的安装方式是这样的:

```shell
$ curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

通过 URL 直接就能访问服务器上的文件，那么我们也可以通过 Flask 和 ShareDataMiddleware 很简单的来实现一个这样的小功能,下面看一个 Demo:

```python
#!/usr/bin/env python
# encoding: utf-8
# demo.py

# official document: http://flask.pocoo.org/docs/0.10/patterns/fileuploads/

from flask import Flask, send_from_directory
from werkzeug import SharedDataMiddleware

app = Flask(__name__)

app.config["FILE_PATH"] = "."   # The path want handdle

def prev_file(filename):
    return send_from_directory(app.config.get("FILE_PATH"), filename)

app.add_url_rule("/file/<filename>", "prev_file", build_only=True)

app.wsgi_app = SharedDataMiddleware(
    app.wsgi_app,
    {
        "/file": app.config.get("FILE_PATH")
    },
    cache = False
    # tips: http://stackoverflow.com/questions/11515804/zombie-shareddatamiddleware-on-python-heroku
)


if __name__ == "__main__":
    app.run()
```

当运行脚本之后，便可以直接通过访问 `http://localhost:8000/file/<filename>` 来直接访问该目录下的<filename>文件内容了。

除此之外，在 Flask 源码(0.1)内也有一段使用了SharedDataMiddleware，源码如下：

```python
class Flask(object):
    # balabala
    def __init__(self, package_name):
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

这段代码就是默认的为static静态文件提供访问服务，使得我们不用再去关心如何管理静态文件。