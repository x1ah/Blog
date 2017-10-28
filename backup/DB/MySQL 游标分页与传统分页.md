---  
title: MySQL 游标分页与传统分页  
category: DB  
date: 2017-08-20T12:18:42Z   
url: https://github.com/x1ah/Blog/issues/15  
---

    >现在很多后端服务使用的翻页方式都是使用传统的 `limit`, `offset` 分页，但是这样的分页方式一旦偏移量大了，便会产生一些性能问题以及数据重复或缺失问题。

# 传统分页

通常在分页时（以 HTTP 协议 GET 方法举例），会携带两个可选参数，`limit`和`offset`。或者是携带一个 `page` 参数，如果是 `limit`，`offset` 参数，在后端从数据库获取数据时，便是直接的使用 `LIMIT` 关键字查询，如下
```mysql
mysql> SELECT * FROM TEST_TABLE LIMIT offset, limit;
mysql> ;;或
mysql> SELECT * FROM TEST_TABLE LIMIT limit, OFFSET offset;
```
使用 `page` 参数控制翻页的实现方式与上面大同小异，无非是 `offset = (page-1) * size`
这样完全可以实现翻页，但是在数据量和偏移量上去之后，查询性能便会直线下降。

### 数据缺失

除了性能问题，上面提到的数据缺失，假设有这样情况，先前表里有10条数据，如下

```shell
+---------------------------+
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
+-------------------
        || 参数：limit=3&offset=0，得到

+-----------+
| 1 | 2 | 3 |
+-----------+

       || 删除一条数据（2）

+-----------------------+
| 1 | 3 | 4 | 5 | 6 | 7 |
+-----------------------+

       || 参数：limit=3&offset=3

期望：在上次取出 1，2，3 的基础上，这次取出4，5，6
实际：取出的是 5，6，7，这就导致4这条记录没有被取到
```

### 数据重复

还是上面的例子

```shell
+---------------------------+
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
+---------------------------+

        || 参数：limit=3&offset=0，得到

+-----------+
| 1 | 2 | 3 |
+-----------+
       || 插入一条数据（8）

+-------------------------------+
| 1 | 8 | 2 | 3 | 4 | 5 | 6 | 7 |
+-------------------------------+

       || 参数：limit=3&offset=3

期望：在 1，2，3 的基础上取出4，5，6，（这里甚至取出的结果很奇怪）
实际：3，4，5，与第一次取出的1，2，3 重复了 3 这条数据
```

# 游标分页

游标分页是通过 `cursor` 和 `size` 这样的类似两个参数来控制翻页，简单的 SQL 语句如下

```sql
mysql> select * from data where id>cursor limit size
```

这样再来看上面的两个问题，第一个参数变为 `cursor=3&size=3`，结果为 4，5，6，符合预期
第二个参数取出结果为 4，5，6，也符合预期。看来数据缺失和数据重复的问题得到了解决 🎉

# 性能对比
>用 Docker 启动了一个 MySQL 镜像的容器。MySQL 镜像为 DockerHub 最近版。查询时间为三次查询取平均值

```
$ docker run --name cursor_paged -e MYSQL_ROOT_PASSWORD=x1ah -itd mysql:latest
$ mysql -d 127.0.0.1 -P 3306 -u root -p
mysql> select version();
+-----------+
| version() |
+-----------+
| 5.7.19    |
+-----------+
1 row in set (0.00 sec)
```

测试的表结构如下
```sql
mysql> desc data;
+---------+------------------+------+-----+---------+----------------+
| Field   | Type             | Null | Key | Default | Extra          |
+---------+------------------+------+-----+---------+----------------+
| id      | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| content | varchar(128)     | NO   |     | NULL    |                |
+---------+------------------+------+-----+---------+----------------+
```

向表内事先插入 3000000 条记录

```sql
mysql> delimiter //
mysql> create procedure fake_data(in num int)
-> begin
-> declare string char(62) default 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
-> declare rand_str char(2);
-> declare i int default 0;
-> while i<num do
-> set rand_str=concat(substring(string,1+floor(rand()*61),1),substring(string,1+floor(rand()*61),1));
-> set i=i+1;
-> insert into data (content) values (rand_str);
-> end while;
-> end;
-> //
mysql> call fake_data(3000000);
Query OK, 1 row affected (24 min 42.63 sec)
```

## 使用 `limit`,`offset` 翻页

```shell
mysql> select * from data limit 2000000, 10;
+---------+---------+
| id      | content |
+---------+---------+
| 2000001 | RP      |
| 2000002 | m8      |
| 2000003 | tN      |
| 2000004 | rE      |
| 2000005 | MQ      |
| 2000006 | GI      |
| 2000007 | oG      |
| 2000008 | 37      |
| 2000009 | iU      |
| 2000010 | xL      |
+---------+---------+
10 rows in set (0.36 sec)

mysql> explain select * from data limit 2000000, 10\G;
***************************[ 1. row ]***************************
id            | 1
select_type   | SIMPLE
table         | data
partitions    | <null>
type          | ALL
possible_keys | <null>
key           | <null>
key_len       | <null>
ref           | <null>
rows          | 2712992
filtered      | 100.0
Extra         | <null>

1 row in set
Time: 0.017s
```

## 使用游标翻页

```shell
mysql> select * from data where id > 2000000 limit 10;
+---------+---------+
| id      | content |
+---------+---------+
| 2000001 | RP      |
| 2000002 | m8      |
| 2000003 | tN      |
| 2000004 | rE      |
| 2000005 | MQ      |
| 2000006 | GI      |
| 2000007 | oG      |
| 2000008 | 37      |
| 2000009 | iU      |
| 2000010 | xL      |
+---------+---------+
10 rows in set (0.00 sec)

mysql> explain select * from data where id > 2000000 limit 10\G
***************************[ 1. row ]***************************
id            | 1
select_type   | SIMPLE
table         | data
partitions    | <null>
type          | range
possible_keys | PRIMARY
key           | PRIMARY
key_len       | 4
ref           | <null>
rows          | 1356496
filtered      | 100.0
Extra         | Using where

1 row in set
Time: 0.019s
```

这里从查询时间还是从 `explain` 看，都是第二种方式性能要好，第一种直接扫全表了，

# 附
举一个游标翻页例子🌰 ，通常在设计接口时，并不会直接把 `cursor` 值直接明文暴露，而是服务端使用某些加密算法，像 base64 之类的，使用加密后的结果在服务端和客户端进行传递。在服务端拿到 `cursor` 参数时，会进行解码，得到可被接受的值后，再去数据库取，在取数据时会特意多取一个，以此结果长度和期望长度相比，便可得知是否还有下一页，如果存在下一页，将下一页的游标经过编码之后再返回给客户端，以此便实现了游标翻页。


