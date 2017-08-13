#!/usr/bin/env python
# coding:utf-8

import os

import requests


def all_issues():
    api = "https://api.github.com/repos/x1ah/Blog/issues"
    res = requests.get(api).json()
    for issue in res:
        yield issue


def backup(issue):
    title = issue.get('title')
    # 默认一篇博客只打一个标签
    label = issue.get('labels')
    label = label[0].get('name') if label else 'default'
    url = issue.get('html_url')
    create_at = issue.get('created_at')
    body = issue.get('body')
    head_text = """---  \r\ntitle: {title}  \r\ncategory: {label}  \r\ndate: {time}   \r\nurl: {url}  \r\n---\r\n
    """.format(title=title, label=label, time=create_at, url=url)
    backup_path = os.path.join('backup', label)
    if not os.path.isdir(backup_path):
        os.mkdir(backup_path)
    path = os.path.join(backup_path, title) + '.md'
    print("备份 {} ing".format(path))
    with open(path, 'w') as mkd:
        mkd.write(head_text + body)


def run():
    issues = all_issues()
    for issue in issues:
        backup(issue)


if __name__ == "__main__":
    run()
