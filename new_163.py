# -*- coding:utf-8 -*-

import os
import urllib2
import requests
import re
from lxml import etree
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename + '.txt'
    with open(path, 'w+') as f:
        for s in slist:
            f.write("%s\t\t%s\n" % (s[0].encode("utf-8"), s[1].encode("utf-8")))

# 分析一级页面
def Page_Info(myPage):
    reg = r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>'
    mypage_Info = re.findall(reg, myPage, re.S)
    return mypage_Info

# 二级页面
def New_Page_Info(new_page):
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert (len(new_items) == len(new_urls))
    return zip(new_items, new_urls)


def spider(url):
    print "Downloading:", url
    # 读取网页,解码为gbk
    myPage = requests.get(url).content.decode('gbk')
    # myPage = urllib2.urlopen(url).read().decode('gbk')

    myPageResults = Page_Info(myPage)
    save_path = u'网易新闻抓取'
    i = 0
    filename = str(i) + "_" + u'新闻排行榜'
    # 保存
    StringListSave(save_path, filename, myPageResults)
    i = 1
    for item, url in myPageResults:
        print "Downloading:", url
        new_page = requests.get(url).content.decode('gbk')
        newPageResults = New_Page_Info(new_page)
        filename = str(i) + "_" + item
        StringListSave(save_path, filename, newPageResults)
        i += 1

if __name__ == '__main__':
    start_url = 'http://news.163.com/rank'
    spider(start_url)