#-*- coding:utf-8 -*-
import urllib2
import urllib
import re

url = "http://item.jd.com/2385655.html"
request = urllib2.Request(url)
response = urllib2.urlopen(request)
result = response.read()
file = open("test.txt","w+")
file.write(result)