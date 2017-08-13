---  
title: Flask 源码阅读（三）路由  
category: Flask  
date: 2017-03-01T13:15:13Z   
url: https://github.com/x1ah/Blog/issues/4  
---

    在我们请求某个 URL 时，应用程序是如何对不同的 URL 作出不同的响应的？在 Flask 里面又是怎么实现的？在前面看见 Flask 类里面初始化了一个实例变量 `url_map`，这是个 `werkzeug.routing.Map` 对象，实际上可以把它看作是个 **路由映射规则** ，类似于字典这样的数据结构，里面存的都是 Web 应用的各种路由规则，供我们使用。

 在 Flask 里面`route`装饰器估计是最常用最熟悉的了，下面就来看看这个神奇的东西背后都有哪些幺娥子，先找到了`Flask.route`方法实现，如下
```python
class Flask(object)
    # ...
    def route(self, rule, **options):
        """
        By default a variable part
        in the URL accepts any string without a slash however a different
        converter can be specified as well by using ``<converter:name>``.   
        =========== ===========================================
        `int`       accepts integers
        `float`     like `int` but for floating point values
        `path`      like the default but also accepts slashes
        =========== ===========================================

        An important detail to keep in mind is how Flask deals with trailing
        slashes.  The idea is to keep each URL unique so the following rules
        apply:

        1. If a rule ends with a slash and is requested without a slash
           by the user, the user is automatically redirected to the same
           page with a trailing slash attached.
        2. If a rule does not end with a trailing slash and the user request
           the page with a trailing slash, a 404 not found is raised.


        The :meth:`route` decorator accepts a couple of other arguments
        as well:

        :param rule: the URL rule as string
        :param methods: a list of methods this rule should be limited
                        to (``GET``, ``POST`` etc.).  By default a rule
                        just listens for ``GET`` (and implicitly ``HEAD``).
        :param subdomain: specifies the rule for the subdoain in case
                          subdomain matching is in use.
        :param strict_slashes: can be used to disable the strict slashes
                               setting for this rule.  See above.
        :param options: other options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.
        """

        def decorator(f):
            self.add_url_rule(rule, f.__name__, **options)
            self.view_functions[f.__name__] = f
            return f
        return decorator
```
这里还能观察到一点小技巧：如果添加的路由规则由`/`结尾，当用户请求该URL时会自动重定向至带`/`的URL，相反如果添加的没有`/`结尾，当请求`/`结尾的URL时直接返回404，还说明了这个版本的路由匹配规则里`converter`一共有三种类系，`int`，`float`，`path`。实际上发现，在`route`内部也是通过`Flask.add_url_rule` 方法来实现路由规则添加，（*所以我们大可以使用 `add_url_rule` 来实现与`route`装饰器一样的功能，但是，为了使代码更 `Pythonic` 更简洁，兼顾可读性，在两种方法都可行的情况下更建议使用`route`装饰器来添加路由规则*）。跟踪到 `Flask.add_url_rule`：
```python
class Flask(object):
    # ...
    def add_url_rule(self, rule, endpoint, **options):
        """Connects a URL rule.  Works exactly like the :meth:`route`
        decorator but does not register the view function for the endpoint.

        Basically this example::

            @app.route('/')
            def index():
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_url_rule('index', '/')
            app.view_functions['index'] = index

        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object
        """
        options['endpoint'] = endpoint
        options.setdefault('methods', ('GET',))
        self.url_map.add(Rule(rule, **options))
```
除了给了一些常规用法外，最关键的是方法的最后一句 `self.url_map.add(Rule(rule, **options))`，所以最后都是添加到 `url_map` 里面，那么这个 `url_map` 和 `Rule` 又是什么东西？跟踪到 `werkzeug.routing`，他们的代码都相对比较长，可以看看这里 [Rule](https://github.com/pallets/werkzeug/blob/master/werkzeug/routing.py#L483L917)，[Map](https://github.com/pallets/werkzeug/blob/master/werkzeug/routing.py#L1103L1357)，先直接看看他们的 demo 吧。
```python
>>> m = Map([
...     Rule('/', endpoint="index"),
...     Rule('/about/', endpoint="/about"),
...     Rule('/help', endpoint="help")
... ])
>>> c = m.bind("example.com", '/')
>>> c.build('index')
'/'
>>> c.match("/")
('index', {})
>>> c.match('/about')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python2.7/dist-packages/werkzeug/routing.py", line 1524, in match
    safe='/:|+') + '/', query_args))
werkzeug.routing.RequestRedirect: 301: Moved Permanently
>>> c.match('/help')
('help', {})
>>> m.add(Rule('/view/<int:post>/<int:page>', endpoint="view"))
>>> c.match('/view/22/33')
('view', {'post': 22, 'page': 33})
>>> 
```
从这几个例子里面便可以看见 `werkzeug` 的 `Map`，`Rule` 主要功能了，先添加路由规则，再绑定，之后便可以进行匹配了。重现了前面提到的 URL 带不带反斜杠问题。 `werkzeug` 的路由过程最后都是转换到 `endpoint`，再返回给用户。关于路由暂时先说这些，后面还有一些更重要的细节。
欲知后事如何，请听下回分解。