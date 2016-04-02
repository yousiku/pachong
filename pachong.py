#-*- coding:utf-8 -*-
import urllib2
import urllib
import re


#京东爬虫类
class JDPC:

    #初始化
    def __init__(self):
        self.pageCodes = []
        self.mobileUrls = []

    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url = "http://list.jd.com/list.html?cat=9987,653,655&page=%s&go=0&JL=6_0_0" %pageIndex
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接失败，错误原因",e.reason
                return None

    #传入某页代码，保存所有商品的地址到列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print u"页面加载失败"
            return None
        pattern = re.compile('<div.*?j-sku-item.*?<a.*?href="(.*?)" >',re.S)
        items = re.findall(pattern,pageCode)
        for item in items:
            self.mobileUrls.append(item)

    #获取总页数
    def getPageCnt(self):
        pageCode = self.getPage(1)
        if not pageCode:
            print u"页面加载失败"
            return None
        pattern = re.compile('p-skip.*?<b>(.*?)</b>.*?</em>',re.S)
        result = re.search(pattern,pageCode)
        if result:
            return result.group(1).strip()
        else:
            return None

    #获取所有商品地址
    def getAllUrl(self):
        for pageIndex in range(1,int(self.getPageCnt())+1):
            self.getPageItems(pageIndex)

    #打印所有商品地址
    def printUrl(self):
        self.getAllUrl()
        for url in self.mobileUrls:
            print url



spider = JDPC()
spider.printUrl()



"""
values = {}
values['cat'] = "9987,653,655"
values['page'] = "2"
values['go'] = "0"
values['JL'] = "6_0_0"
data = urllib.urlencode(values)
url = "http://list.jd.com/list.html"
geturl = url + '?' + data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
content = response.read()
pattern = re.compile('<div.*?j-sku-item.*?<a.*?href="(.*?)" >',re.S)
items = re.findall(pattern,content)
print items[0]
for item in items:
    print item
"""