# -*- coding=utf8 -*-

import urllib2
import urllib
import socket
from bs4 import BeautifulSoup


User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

# 获取代理IP,并存进proxy.txt文件下
url = 'http://www.xicidaili.com/nn/1'
req = urllib2.Request(url,headers=header)
res = urllib2.urlopen(req).read()
soup = BeautifulSoup(res, 'lxml')
ips = soup.findAll('tr')
f = open("./src/proxy.txt","w")
for x in range(1,len(ips)):
    ip = ips[x]
    tds = ip.findAll("td")
    ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
    f.write(ip_temp.encode('utf-8'))

# 验证代理是否有效
socket.setdefaulttimeout(3)         #设置超时时间为3s，一个请求3s内还没有响应，就结束访问，并返回timeout
f = open("./src/proxy.txt")
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    ip = lines[i].strip("\n").split("\t")   #strip("\n")--->去除换行符,split("\t")--->分割字符串为字符串数组
    proxy_host = "http://"+ip[0]+":"+ip[1]
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)
url = "http://ip.chinaz.com/getip.aspx"
for proxy in proxys:
    try:
        res = urllib.urlopen(url,proxies=proxy).read()      #proxies是代理,以代理模式访问目标网址
        print res
    except Exception,e:
        print proxy, e
        continue