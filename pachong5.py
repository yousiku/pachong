#-*- coding:utf-8 -*-
import urllib
import json
import re


class ProductInfo(object):
    """
    获取某件商品的信息
    """
    def __init__(self,url):
        self.url = url
        self.html = urllib.urlopen(self.url).read()
