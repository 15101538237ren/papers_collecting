#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2, os

pkl_dir = 'pkl'
papers_dir = 'papers'

for dir_path in [pkl_dir, papers_dir]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

paper_years = range(2013, 2018)
ip = '10.138.232.71'
port = '80'
timeout = 20

def request_url(paper_collection_name, url):
    if paper_collection_name != "icml":
        proxydict = {}
        proxydict['http'] = "http://%s:%s"%(ip, port)
        proxy_handler = urllib2.ProxyHandler(proxydict)
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Connection','keep-alive'),('Cookie','_ga=GA1.2.1314251887.1513847038; _gat=1; _gid=GA1.2.129016361.1514334078')]
        urllib2.install_opener(opener)
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req,timeout=timeout)
        return response.read()
    except urllib2.URLError, e:
        print e.reason
        return 0

def schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    # print '%.2f%%' % per
