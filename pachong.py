import urllib2
import urllib
import re


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
