---  
title: CSRF token 工作原理  
category: default  
date: 2017-06-24T09:50:55Z   
url: https://github.com/x1ah/Blog/issues/14  
---

    >[CSRF：跨站请求伪造](https://zh.wikipedia.org/zh/%E8%B7%A8%E7%AB%99%E8%AF%B7%E6%B1%82%E4%BC%AA%E9%80%A0)

--------

# 防御
## CSRF Token
工作流程如下：后端服务器生成表单时加入一个 token 字段，这个字段可根据情况调整生成算法，一般是随机字符串，用户提交表单时，该字段一并提交，后端检验 token 是否一致。攻击者可以伪造表单，但是无法在一个 session 内伪造 token。