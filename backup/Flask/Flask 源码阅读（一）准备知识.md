
---
title: Flask 源码阅读（一）准备知识
category: Flask
date: 2017-02-25T16:03:49Z
url: https://github.com/x1ah/Blog/issues/2
---
    ### 首先为什么要看 flask 源码？
- 加强 flask 基础，熟悉 flask 的各种用法以及设计哲学
- 还能学习大牛们怎么写代码，一些技巧

### flask 简介
 [flask](http://flask.pocoo.org/) 是一个易扩展，使用简单的微Python web开发**框架**，这里需要区别 `Web framework` 和 `Web Server`，一个是框架一个是服务器，在使用 `flask` 开发时，常常都需要直接运行项目来测试以及方便开发，实际上这也是启动了一个 `Web Server`，但是这只是一个简单的开发服务器，并不能用到生产环境中，生产环境大多用 [uWSGI](https://uwsgi-docs.readthedocs.io/)，[Gunicorn](http://gunicorn.org/)，[Tornado](http://www.tornadoweb.org/en/stable/)之类。

### flask 周边
 `flask` 的两个主要依赖分别是 [werkzeug](https://github.com/pallets/werkzeug) 和 [Jinja](https://github.com/pallets/jinja)，并且 100% 兼容 [WSGI](http://legacy.python.org/dev/peps/pep-0333/)。其中 `Jinja` 是模板引擎，如果只是用来写 API 服务器大可不必关心 `Jinja`，而 `werkzeug` 便是 `flask` 的关键了，并且可以说 `flask` 是一个 `werkzeug` 的一个封装，来实现 Python 程序（Web应用）和 Web 服务器，服务器和客户端的交互。而 `WSGI` 便是 Python 程序和 Web 服务器之间交互的一个接口标准，或者说“协议”。所以需要先了解了解 `WSGI` 是个怎么回事儿。关于 `WSGI`，有很多文章已经介绍/解读过了，便不再造轮子了，下面几篇都是挺不错的几篇文章：
- 首先是 [PEP333](http://legacy.python.org/dev/peps/pep-0333/),在这里面有详细的关于 WSGI 标准的介绍。
- 除此之外还有 [YangZ_405](http://my.csdn.net/YangZ_XX) 的这篇 [Python的WSGI简介](http://blog.csdn.net/yangz_xx/article/details/37508909) 也很不错，建议仔细阅读。

