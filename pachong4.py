#-*- coding:utf-8 -*-
import urllib
import json
import re
import sys


class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """
    def __init__(self, url):
        self.url = url
        self._response = urllib.urlopen(self.url)
        self.html = self._response.read()
        self.attrsDict = {}
        self.file = None

    def get_product(self):
        """
        获取html中，商品的描述(未对数据进行详细处理，粗略的返回str类型)
        """
        product_re = re.compile(r'compatible: true,(.*?)};', re.S)
        product_info = re.findall(product_re, self.html)[0]
        return product_info

    def get_product_skuid(self):
        """
        通过获取的商品信息，获取商品的skuid
        """
        product_info = self.get_product()
        skuid_re = re.compile(r'skuid: (.*?),')
        skuid = re.findall(skuid_re, product_info)[0]
        return skuid

    def get_product_name(self):
        """
        通过获取的商品信息，获取商品的name
        """
        #'\u4e2d\u6587'.decode('unicode-escape') （你可能需要print它才能看到结果）
        product_info = self.get_product()
        #源码中名称左右有两个',所以过滤的时候应该去掉
        name_re = re.compile(r"name: '(.*?)',")
        name = re.findall(name_re, product_info)[0]
        return name.decode('unicode-escape')#将其转换为中文

    def get_product_price(self):
        """
        根据商品的skuid信息，请求获得商品price
        :return:
        """
        price = None

        #得到产品的序号和名称，取价格的时候会用得到
        skuid = self.get_product_skuid()
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
        attrsText_re = re.compile(r'product-detail-2.*?<table(.*?)</table>',re.S)
        attrsText = re.findall(attrsText_re,self.html)[0].decode('gbk')
        attrs_re = re.compile(r'<tr><td.*?">(.*?)</td><td>(.*?)</td></tr>',re.S)
        attrs = re.findall(attrs_re,attrsText)
        for attr in attrs:
            key = attr[0]
            value = attr[1]
            self.attrsDict.update({key:value})


    def save_attrs(self):
        """
        将获得的参数信息保存到txt文件
        :return:
        """
        self.get_product_attrs()
        title = self.get_product_name()
        self.file = open(title+'.txt','w+')
        for k,v in self.attrsDict.iteritems():
            self.file.write(k+':'+v+'\n')
        self.file.close()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print "+"*20+"welcome to 京东放养的爬虫"+"+"*20
    url = 'http://item.jd.com/2174898.html'
    jp = JdPrice(url)
    print jp.get_product_name()
    print jp.get_product_price()
    print jp.url
    jp.save_attrs()
print "+"*20+"welcome to 京东放养的爬虫"+"+"*20


'''
    def get_product_brand(self):
        """
        获取html中商品的品牌
        :return:
        """
        brand_re = re.compile(r'product-detail-2.*?<td>(.*?)</td>',re.S)
        brand = re.findall(brand_re,self.html)[0]
        return brand.decode('gbk')

    def get_product_modelnumber(self):
        """
        获取html中商品型号
        :return:
        """
        modelnumber_re = re.compile(r'product-detail-2.*?<td>.*?<td>(.*?)</td>',re.S)
        modelnumber = re.findall(modelnumber_re,self.html)[0]
        return modelnumber

    def get_product_system(self):
        """
        获取html中商品系统
        :return:
        """
        system_re = re.compile(r'product-detail-2.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>(.*?)</td>',re.S)
        system = re.findall(system_re,self.html)[0]
        return system

    def get_product_cpu(self):
        """
        获取html中商品cpu
        :return:
        """
        cpu_re = re.compile(r'product-detail-2.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>(.*?)</td>',re.S)
        cpu = re.findall(cpu_re,self.html)[0]
        return cpu.decode('gbk')

    def get_product_ROM(self):
        """
        获取html中的机身内存
        :return:
        """
        ROM_re = re.compile(r'product-detail-2.*?colspan.*?colspan.*?colspan.*?<td>(.*?)</td>',re.S)
        ROM = re.findall(ROM_re,self.html)[0]
        return ROM

    def get_product_RAM(self):
        """
        获取html中的运行内存
        :return:
        """
        RAM_re = re.compile(r'product-detail-2.*?colspan.*?colspan.*?colspan.*?<td>.*?<td>(.*?)</td>',re.S)
        RAM = re.findall(RAM_re,self.html)[0]
        return RAM

    def get_product_size(self):
        """
        获取html中屏幕尺寸
        :return:
        """
        size_re = re.compile(r'product-detail-2.*?colspan.*?colspan.*?colspan.*?colspan.*?<td>(.*?)</td>',re.S)
        size = re.findall(size_re,self.html)[0]
        return size.decode('gbk')

    def get_product_dpi(self):
        """
        获取html中屏幕分辨率
        :return:
        """
        dpi_re = re.compile(r'product-detail-2.*?colspan.*?colspan.*?colspan.*?colspan.*?<td>.*?<td>.*?<td>(.*?)</td>',re.S)
        dpi = re.findall(dpi_re,self.html)[0]
        return dpi

    def get_product_weight(self):
        """
        获取机身重量
        :return:
        """
        weight_re = re.compile(r'product-detail-2.*?colspan.*?colspan.*?colspan.*?colspan.*?colspan.*?colspan.*?colspan.*?colspan.*?colspan.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>(.*?)</td>',re.S)
        weight = re.findall(weight_re,self.html)[0]
        return weight
'''


