#-*- coding:utf-8 -*-
import urllib
import json
import re
import sys
import time


class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """
    def __init__(self, url):
        self.url = url
        self.flag = True
        try:
            self._response = urllib.urlopen(self.url)
            self.html = self._response.read()
        except Exception,e:
            print 'init error:{0}'.format(e.message)
            self.flag = False
        self.attrsDict = {}
        self.file = None

    def get_product(self):
        """
        获取html中，商品的描述(未对数据进行详细处理，粗略的返回str类型)
        """
        try:
            product_re = re.compile(r'compatible: true,(.*?)};', re.S)
            product_info = re.findall(product_re, self.html)[0]
        except IndexError,e:
            print 'get_product error:{0}'.format(e.message)
            return None
        return product_info

    def get_product_skuid(self):
        """
        通过获取的商品信息，获取商品的skuid
        """
        product_info = self.get_product()
        if not product_info:
            return None
        try:
            skuid_re = re.compile(r'skuid: (.*?),')
            skuid = re.findall(skuid_re, product_info)[0]
        except IndexError,e:
            print 'get_product error：' + e.message
            return None
        return skuid

    def get_product_name(self):
        """
        通过获取的商品信息，获取商品的name
        """
        #'\u4e2d\u6587'.decode('unicode-escape') （你可能需要print它才能看到结果）
        product_info = self.get_product()
        if not product_info:
            return None
        #源码中名称左右有两个',所以过滤的时候应该去掉
        try:
            name_re = re.compile(r"name: '(.*?)',")
            name = re.findall(name_re, product_info)[0]
        except IndexError,e:
            print 'get_product_name error:' + e.message
            return None
        return name.decode('unicode-escape')#将其转换为中文

    def get_product_price(self):
        """
        根据商品的skuid信息，请求获得商品price
        :return:
        """
        price = None

        #得到产品的序号和名称，取价格的时候会用得到
        skuid = self.get_product_skuid()
        if not skuid:
            return None
        #name = self.get_product_name()
        #print name

        #通过httpfox检测得知，每次网页都会访问这个网页去提取价格嵌入到html中
        url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'

        #json调整格式，并将其转化为utf-8，列表中只有一个字典元素所以取出第一个元素就转化为字典
        price_json = json.load(urllib.urlopen(url))[0]

        #p对应的价格是我们想要的
        if price_json['p']:
            price = price_json['p']
        return price

    def get_product_attrs(self):
        """
        获取商品的参数并保存到字典attrsDict中
        :return:
        """
        try:
            attrsText_re = re.compile(r'product-detail-2.*?<table(.*?)</table>',re.S)
            attrsText = re.findall(attrsText_re,self.html)[0].decode('gbk')
            attrs_re = re.compile(r'<tr><td.*?">(.*?)</td><td>(.*?)</td></tr>',re.S)
            attrs = re.findall(attrs_re,attrsText)
        except IndexError,e:
            print "get_product_attrs error:" + e.message
            return None
        for attr in attrs:
            key = attr[0]
            value = attr[1]
            self.attrsDict.update({key:value})
        return True

    def save_attrs(self):
        """
        将获得的参数信息保存到txt文件
        :return:
        """
        if not self.flag:
            print "访问失败，跳过"
            return None
        if not self.get_product_attrs():
            print "1"
            return None
        if not self.get_product_name():
            print"2"
            return None
        title = self.get_product_name()
        try:
            self.file = open('products\\'+title+'.txt','w+')

            for k,v in self.attrsDict.iteritems():
                self.file.write(k+':'+v+'\n')
            self.file.close()
        except IOError,e:
            print "写入异常，原因：" + e.message


if __name__ == '__main__':
    start = time.clock()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    url = "http://item.jd.com/1861098.html"
    jp = JdPrice(url)
    jp.save_attrs()
    """
    print "+"*20+"welcome to 京东放养的爬虫"+"+"*20
    i=0
    file = open("urls.txt")

    for line in file.readlines():
        url = 'http:'+ line
        jp = JdPrice(url)
        jp.save_attrs()
        i += 1
        print i

    print i
    end = time.clock()
    print end-start
    """


print "+"*20+"welcome to 京东放养的爬虫"+"+"*20



