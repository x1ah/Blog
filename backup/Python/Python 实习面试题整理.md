
---
title: Python 实习面试题整理
category: Python
date: 2017-04-08T14:50:16Z
url: https://github.com/x1ah/Blog/issues/9
---
    >下面的内容均为最近几周找 Python 实习遇见的各种面试题，记录备用。其中有 bat 之类大厂也有十几个人的初创公司～（斜体的为遇见两次以上的。）

# Python 语法
- *说说你平时 Python 都用哪些库*

- `==` 和 `is` 区别。
    - `==` 是比较两对象的值，`is` 是比较在内存中的地址(id)， `is` 相当于 `id(objx) == id(objy)`。

- *深拷贝和浅拷贝。*
```python
# 浅拷贝操作只会拷贝被拷贝对象的第一层对象，对于更深层级的只不过是拷贝其引用，如下例中 `a[2]`
# 和 `lst[2]` 这两个对象为第二层，实际上浅拷贝之后，这两个还是一个对象。深拷贝会完全的拷贝被拷
# 贝对象的所有层级对象，也就是一个真正意义上的拷贝。
>>> from copy import copy, deepcopy
>>> lst = [1, 2, [3, 4]]
>>> a, b = copy(lst), deepcopy(lst)
>>> a, b
([1, 2, [3, 4]], [1, 2, [3, 4]])
>>> id(lst[2]), id(a[2]), id(b[2])
(139842737414224, 139842737414224, 139842737414584)
>>> lst[0] = 10
>>> a
[1, 2, [3, 4]]
>>> b
[1, 2, [3, 4]]
>>> lst[2][0] = 'test'
>>> lst
[10, 2, ['test', 4]]
>>> a
[1, 2, ['test', 4]]
>>> b
[1, 2, [3, 4]]
```

- `__init__` 和 `__new__`。
    - `__init__` 只是单纯的对实例进行某些属性的初始化，以及执行一些需要在新建对象时的必要自定义操作，无返回值。而 `__new__` 返回的是用户创建的实例，这个才是真正用来创建实例的，所以 `__new__` 是在 `__init__` 之前执行的，先创建再初始化。

- *Python 2 和 Python 3 有哪些区别？*
    - lz 当时只是简单的说了几点：
        - Python2 和 Python3 的默认字符串不一样，Python3 默认为 Unicode 形式。
        - `raw_input()`, `input()`
        - 捕捉异常/错误的写法，Python2 除了后面的写法还支持：`except Exception, e`， 而 Python3 只支持 `except Exception as e`
        - Python3 中没有了 `xrange`， 而使用 `range` 代替它，在 Python3 中，`range` 返回的是一个可迭代对象，而不是 Python2 那样直接返回列表。
        - Python3 中 `map` 如果需要立即执行必须以 `list(map())` 这样的方式。
        - Python3 中，`print` 改成了函数，而在 Python2 中，`print` 是一个关键字。使用上有所差异。
        - Python3 中，`3/2 == 1.5`；Python2 中，`3/2 == 1`。
        - 上面知识列了几点比较常见的，这里有一篇 [Blog](http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html) 写的详细写。

- 连接字符串都有哪些方式？
    - 格式化字符连接（`%s`)
    - `format`
    - `join`
    - `+`

- 如何判断某个对象是什么类型？
    - `type(obj)`
    - `isinstance(obj)`

- *生成器是什么？*
    - 一言难尽，推荐看这个 [stackoverflow 答案的翻译](https://taizilongxu.gitbooks.io/stackoverflow-about-python/content/1/README.html)

- Python 中的 GIL 是什么？全称？举个例子说说其具体体现。
    - GIL 全称 Global Interpreter Lock（全局解释器锁），任何 Python 线程执行前，必须先获得 GIL 锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。要避免这种“现象”利用操作系统的多核优势可以有下面几种方法：
        - 使用 C 语言编写扩展，创建原生线程，摆脱 GIL，但是即使是扩展，在 Python 代码内，任意一条Python 代码还是会有 GIL 限制
        - 使用多进程代替多线程，使用多进程时，每个进程都有自己的 GIL。故不存在进程与进程之间的 GIL 限制。但是多进程不能共享内存。

- `s = 'abcd', s[2] = 'e'` 运行结果是什么？
    - 报错，字符串是不可变对象

- Python 中，`sorted` 函数内部是什么算法？
    - 在 [官方文档](https://docs.python.org/3/howto/sorting.html?highlight=Timsort) 里面有提到，用的是 [Timsort](https://en.wikipedia.org/wiki/Timsort) 算法

- 编码是一个什么样的过程？
    - 编码是二进制到字符的过程

- *Python 里面怎么实现协程？*
    - lz 当时也就简单说了下可以用 yield 关键字实现，举了个小例子，还说了用户控制调度，加上一些第三方框架，Gevent，tornado 之类的，可怜。这里安利一下 [驹哥](http://ajucs.com) 的一篇文章 [说清道明：协程是什么](http://mp.weixin.qq.com/s/TKrb0i5fF0pJdRIgGC9qQQ )

- `requests` 包新建一个 `session` 再 `get` 和普通的 `requests.get` 有什么区别？（tcp长连接）
    - 维持一个会话，** 建立一个tcp长连接** ，cookie 自动保存，下次请求还是一个会话。

- *Python 都有哪些数据结构？可变对象，不可变对象分别有哪些？*
    - 可变对象：列表，字典
    - 字符串，数字，元组，集合

- *在 Python 内，函数传参是引用传递还是值传递？*
    - 在 Python 内，如果形参是可变参数，更像是引用传递，如果是不可变参数，更像是值传递。面试只要说到了这个点，基本就没问题了。

- 你会对你的项目写测试么？用哪些方法哪些库？
    - 只说了用 unitest......需要自行寻找答案。

- 请新建一个只有一个元素 `1` 的列表和元组。
    - `lst = [1]`
    - `tup = (1,)`

- *函数默认参数是可变对象情况。*
```python
>>> def foo(a, b=[1, 2]):
        print(b)
        b.append(a)
        print(b)
>>> val = 4
>>> foo(val)
# [1, 2]
# [1, 2, 4]
>>> foo(val)
# [1, 2, 4]
# [1, 2, 4, 4]
# 这里可以看到，第二次执行函数时，默认参数 b 的值已经变成 `[1, 2, 4]` 了，原因是，默认参数只在第
# 一次执行时会进行初始化，后面就默认使用 **初始化后的这个对象(引用)**，但是这里 b 是可变对象，
#添加了一个元素还是之前的对象，所以，引用没变，不过是值变了而已。
```



- *Flask 的 Route 是怎么实现的？* 你认为 Flask 框架有什么优缺点？
    - 实际上在 Flask 类里面，`route` 可以简单理解为不过是把对应的路由规则作为键，装饰的视图函数作为值，存到 `werkzeug.routing.Map` 对象（可以看成是和字典类似的数据结构）里。这里是 [源码](https://github.com/pallets/flask/blob/master/flask/app.py#L1076-L1120)，好理解些。这是之前写的一篇 [笔记](https://github.com/x1ah/Blog/issues/4)
    - Flask 优点是轻量，灵活，可高度定制，插件化。缺点也是过于轻量，功能必须通过第三方插件实现，插件质量参差不齐，也不能完全保证后期维护。
    - 这几点都只是个人之见，更详细标准的还需自行寻找答案。

- *WSGI 是什么？uWSGI， nginx 这些都是什么用途？*
    - 这里有[维基百科](https://zh.wikipedia.org/wiki/Web%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%BD%91%E5%85%B3%E6%8E%A5%E5%8F%A3) 的解释，WSGI 就是一个通用的标准，遵守这个标准，我们能让我们的 Web 框架更加通用，编写更加简单。
    - uwsgi 和 Nginx 都是 Web Server，不同的是 Nginx 负责 外网请求 ---(转换)--> 内网请求，uwsgi 负责的是 内网请求 -> Python Web 程序。

- nginx 和 Apache 的区别？(参考 [interview_python](https://github.com/taizilongxu/interview_python#7-apache和nginx的区别))
    - nginx 相对 apache 的优点：
        - 轻量级，同样起web 服务，比apache 占用更少的内存及资源
        - 抗并发，nginx 处理请求是异步非阻塞的，支持更多的并发连接，而apache 则是阻塞型的，在高并发下nginx 能保持低资源低消耗高性能
        - 配置简洁
        - 高度模块化的设计，编写模块相对简单
        - 社区活跃
    - apache 相对nginx 的优点：
        - rewrite ，比nginx 的rewrite 强大
        - 模块超多，基本想到的都可以找到
        - 少bug ，nginx 的bug 相对较多
        - 超稳定

- 你部署 Python 项目时用的是 uWSGI 的哪个模式？
    - 默认模式
    - 这个应该问的可能性极小了，可翻阅 [uwsgi 文档](http://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/WSGIquickstart.html) 查找更详细的资料


# 数据结构，算法
- 层次遍历二叉树用什么方法？（参考
```python
class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

btree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))

def level_trav(tree):
    queue = [tree]
    while queue:
        current = queue.pop(0)
        print(current.data)
        if current.left:
            queue.append(current.left)
        if queue.right:
            stack.append(current.right)
```

- 非平衡二叉数如何变成平衡二叉数？
    - 参考 [AVL平衡二叉树详解与实现](https://segmentfault.com/a/1190000006123188)

- 先，中，后序遍历二叉数。完全二叉数是什么？
    - 完全二叉树：深度为k有n个节点的二叉树，当且仅当其中的每一节点，都可以和同样深度k的满二叉树，序号为1到n的节点一对一对应时，称为“完全二叉树”。（摘自维基百科）
    - 先序：先根后左再右
    - 中序：先左后中再右
    - 后序：先左后右再根

- 如何判断两个单链表是否相交于某个节点，包括 X 型，Y 型，V 型。
    - X 型不可能存在，一个单链表节点不存在两个不同的后继。
```python
# 存在 V 型和 Y 型，如果交叉，则最后一个节点肯定是相同的，故直接从最后一个节点进行反向遍历。
# 反转单链表
def reverse_single_link_lst(link_lst):
    if not link_lst:
        return link_lst
    pre = link_lst
    cur = link_lst.next
    pre.next = None
    while cur:
        tmp = cur.next
        cur.next = pre
        pre = cur
        cur = tmp
    return pre

# 寻找交叉点
def point(node_a, node_b):
    if node_a is None or node_b is None:
        return None
    next_a, next_b = node_a, node_b
    while next_a or next_b:
        if next_a.val == next_b.val:
            if next_a.next and next_b.next and (next_a.next.val == next_b.next.val):
                next_a, next_b = next_a.next, next_b.next
                continue
            return next_a.val
        next_a, next_b = next_a.next, next_b.next
    return None

# 构造单链表
class Node(object):
    def __init__(self, value, next=None):
        self.val = value
        self.next = next

a = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
b = ListNode(7, ListNode(9, ListNode(4, ListNode(5))))

ra = reverse_single_link_lst(a)
rb = reverse_single_link_lst(b)
point(ra, rb)
# output:
# 4
```

- 如何判断两个单链表是否是同一个链表。
    - 直接判断第一个节点即可。

- 单链表逆转。
    - 见上面判断交叉链表内的 `reverse_single_link_lst()` 函数。

- *堆，栈，队列。*
    - [堆](https://zh.wikipedia.org/wiki/%E5%A0%86_(%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84))， [栈](https://zh.wikipedia.org/zh-hans/%E5%A0%86%E6%A0%88)， [队列](https://zh.wikipedia.org/wiki/%E9%98%9F%E5%88%97)

- *说说你知道的排序算法以及其时间复杂度。*
![](http://ww1.sinaimg.cn/large/005NaGmtly1fenoomcn03j30iz07874f.jpg)

- *手写快速排序。画画堆排序的原理及过程。*
```python
# 快速排序，lz 当时写的比较复杂，但是是最常见的写法（紧张导致有几个小bug），如下
def quick_sort(lst, start, stop):
    if start < stop:
        i, j, x= start, stop, start
        while i < j:
            while (i < j) and (lst[j] > x):
                j -= 1
            if (i < j):
                lst[i] = lst[j]
                i += 1
            while (i < j) and (lst[i] < x):
                i += 1
            if (i < j):
                lst[j] = lst[i]
                j -= 1
        lst[i] = x
        quick_sort(lst, start, i-1)
        quick_sort(lst, i+1, stop)
    return lst
```

之后面试官 [akun](https://github.com/akun) 大哥给了个特别简洁的写法，三路复用，地址在 [Gist](https://gist.github.com/akun/d90998068f4e1f3eb169)
```python
def qsort(alist):
    """
    quick sort(easy way, but more memory)
    test: python -m doctest qsort.py
    >>> import math
    >>> import random
    >>> size = 100
    >>> alist = [random.randint(0, size * 10) for i in range(size)]
    >>> qlist = qsort(alist)
    >>> alist.sort()
    >>> assert qlist == alist
    """

    if len(alist) <= 1:
        return alist

    key = alist[0]
    left_list, middle_list, right_list = [], [], []

    [{i < key: left_list, i == key: middle_list, i > key: right_list}[
        True
    ].append(i) for i in alist]

    return qsort(left_list) + middle_list + qsort(right_list)
```

- 说说你所了解的加密算法，编码算法，以及压缩算法。了解 base64 的原理么？
    - 只说了听过 base64, md5 这几种编码。。。。。自行搜索吧，考的概率极小。

# 数据库
- 索引是什么原理？有什么优缺点？
    - 参考 [数据库索引的实现原理](http://blog.csdn.net/kennyrose/article/details/7532032)

- 乐观锁和悲观锁是什么？
    - [深入理解乐观锁与悲观锁](http://www.hollischuang.com/archives/934) 

- 你为什么选择 Redis 而不是 MongoDB 或者其他的？（有个项目用了 Redis）
    - [redis、memcache、mongoDB有哪些区别？](https://segmentfault.com/q/1010000002588088/a-1020000002589415)

- SQL 和 NoSQL 区别？
    - [SQL 和 NoSQL 的区别](http://www.jianshu.com/p/b32fe4fe45a3)

# 网络
- 从浏览器输入网址到网页渲染完毕这过程发生了什么？
    - [这里](https://github.com/skyline75489/what-happens-when-zh_CN) 说的非常详细，看面的岗位不同，回答的侧重点不一样。如面的 Web ，可以侧重说说 nginx -> uwsgi -> Python -> uwsgi -> nginx 这个过程，（WSGI 标准）

- *TCP 三次握手四次挥手详细说下。*
    - [TCP协议中的三次握手和四次挥手(图解)](http://blog.csdn.net/whuslei/article/details/6667471)

- 为什么是三次握手？两次不行么？
    - [TCP连接建立过程中为什么需要“三次握手”](http://www.cnblogs.com/techzi/archive/2011/10/18/2216751.html)

- *说说 TCP 和 UDP 的区别。*
    - TCP（传输层）
        - 优点：TCP 面向连接，可靠，稳定，传输数据前需要建立连接，故有三次握手四次挥手，还有拥塞控制，重传等
        - 缺点：慢，占用系统资源，有确认机制，三次握手，所以容易被攻击，DDos
    - UDP
        - 优点：快，无状态传输协议
        - 缺点：不稳定，不可靠，容易丢包

- 谈谈你对 SQL 注入、 XSS 、 CSRF 的理解。以及如何防范。
    - [关于XSS（跨站脚本攻击）和CSRF（跨站请求伪造)](https://cnodejs.org/topic/50463565329c5139760c34a1)
    - [SQL 注入](https://zh.m.wikipedia.org/zh-hans/SQL%E8%B3%87%E6%96%99%E9%9A%B1%E7%A2%BC%E6%94%BB%E6%93%8A)，现在多数采用 ORM，以及参数化查询，很少再出现。

- *说说 DNS 是什么东西。*
    - 根据域名寻找 主机 IP 的协议。

- HTTP 是工作在七层模型的哪一层？DNS 又是哪一层？TCP 和 IP 呢？
    - HTTP，DNS 应用层，TCP 传输层，IP 网络层。

- *说说你知道的 HTTP 方法和 状态码。*
    - [状态码](https://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81)，这里只需要大概说说，以 1××，2××，3×× 这样的层面说，没有必要细到每一个状态码。
    - [HTTP 请求方法](https://zh.wikipedia.org/wiki/%E8%B6%85%E6%96%87%E6%9C%AC%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE#.E8.AF.B7.E6.B1.82.E6.96.B9.E6.B3.95)

- *HTTP 的 GET 和 POST 有什么区别？*
    - 本质上，GET 和 POST 只不过是 **发送机制不同** 。

- HTTP 和 HTTPS 的区别？
    - HTTPS = HTTP + SSL
    - HTTP 默认使用 80 端口，HTTPS 使用 443 端口。
    - [更详细](https://zh.wikipedia.org/wiki/%E8%B6%85%E6%96%87%E6%9C%AC%E4%BC%A0%E8%BE%93%E5%AE%89%E5%85%A8%E5%8D%8F%E8%AE%AE#.E4.B8.8EHTTP.E7.9A.84.E5.B7.AE.E5.BC.82)

- 说说你知道的 HTTP 包头部信息里都有哪些字段。
    - 这个随便抓下包就知道了，就不说了～

- *HTTP 包头部信息里面的 `Host` 字段是什么作用？*
    - 表示当前请求服务器的主机名

- 说说 cookie 里面你都知道哪些字段。
    - [Cookie](http://javascript.ruanyifeng.com/bom/cookie.html)

- Session 是什么东西？
    - [Cookie/Session的机制与安全](http://harttle.com/2015/08/10/cookie-session.html)

- 在写爬虫过程中，如果遇见需要加载 js 的情况你是如何处理的。
    - Selenium，PhantomJS

- 普通匿名代理和高匿代理有什么区别？
    - 来自普通匿名代理的请求在服务端能看见真实 IP， 而高匿代理在服务端看不见真实 IP，只能看见代理服务器 IP。

- 你知道哪些反爬措施？
    - 加代理，加头部，爬取速度控制，随机 UA，模拟真实用户的点击习惯去请求。

# 操作系统
- *进程和线程以及协程的区别？*
- *多线程和多进程的区别？*
- 信号量和互斥量的区别？
- 堆内存是干嘛的？
- 如何检验当前机器是大端模式还是小端模式？
- 如何让某个程序在后台运行？（Linux）
- sed, awk 用法（Linux）

# 编程题

- 手写二分查找，*快速排序*。
- ~还有一个 SQL 语句的，一条 SQL 语句打印某张表某个 group count  TOP 5。~
- Python 中正则模块 `re` 里 `match` 函数 和 `search` 函数有什么区别？举例说明。
- 一条语句求 0 - 999999 内能被 7 整除的所有数的和。
- 实现一个链表结构，要求其插入第一个节点，删除最后一个节点的复杂度为 O(1)。
- 实现一个 `retry` 装饰器，使用如下：
```python
# 可以指定重试次数，直到函数返回正确结果。
@retry(retries=3)
def func(*args, **kw):
    try:
        # some action
        return True
    except:
        return False
```
大概可以像下面这样写，
```python
from functools import wraps

def retry(retries=3):
    def timesf(func):
        @wraps(func)
        def wrap(*args, **kw):
            i = 0
            status = True
            while status and i < times:
                status = func(*args, **kw)
                i += 1
            return status
        return wrap
    return timesf
```

- 有一个4G 的文本文件，存储的是酒店信息，每行存的是一个酒店ID，可以重复。请编写程序输出一个新文件，新文件内容为每行一条数据，每行的数据格式如下：`酒店ID + 出现次数`（最后提到了其他想法，如文件切片，bitmap 之类）
- 实现一个函数，根据字典序比较两字符串大小，不允许用库函数，尽量越底层实现越好。（手写）
- 实现一个函数，检验一个字符串是否符合 `xxxx-xx-xx` 这样的日期格式，注意润年，大小月，不允许用库函数，尽量越底层实现越好。（手写）
- 假设有一个 9 x 9 的[数独](https://zh.wikipedia.org/wiki/%E6%95%B8%E7%8D%A8)，里面只有 n 个空格没有填写数字，试讲讲你会用什么方法去填上数字，复杂度如何？
- 我们是做地图相关工作的，现在给你提供一个三维的数据，数据描述的是不同时间一些地图上的一些地点坐标，分别有时间，x轴坐标，y轴坐标，请你设计一个算法，能够得到一天内地图上的 TOP 10 热点地区，地区大小也相应的自己作合适调整，开放性题目。

# 概率论
- 一副扑克除去大小王，共 52 张排，随机取三张扑克，求同花（三张扑克同一种花色）和顺子的概率。
- 其他忘了 Orz

# 总结
- 如果目标是大公司，多刷题，多刷题，多刷题，基础知识（操作系统，计算机网络，数据结构，算法之类）一定要劳靠，如果只是想写业务，这些将会是加分项。但是，作为一个有理想的程序猿，基础不劳，地动山摇，出来混迟早要还的。

>最后顺利拿到了自己喜欢的 offer，而且个人也建议，不要一味追求大厂，选择一个自己喜欢的，技术栈符合自己的，也符合自己职业发展的公司/岗位～