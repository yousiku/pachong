#-*- coding:utf-8 -*-
"""
将数据库中数据标准化
"""
from __future__ import division
import sys
import MySQLdb

conn = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '4QSJQCRC',
        db = 'pcas2',
        charset = 'utf8'
    )
cur = conn.cursor()
sql = "select * from webapp_mobile"
results = cur.fetchmany(cur.execute(sql))

def listDate(date):
    """
    标准化listDate数据
    :param date:
    :return:
    """
    if '2016' in date:
        return 1
    elif '2015' in date:
        return round((2015-2008)/(2016-2008),2)
    elif '2014' in date:
        return round((2014-2008)/(2016-2008),2)
    elif '2013' in date:
        return round((2013-2008)/(2016-2008),2)
    elif '2012' in date:
        return round((2012-2008)/(2016-2008),2)
    elif '2011' in date:
        return round((2011-2008)/(2016-2008),2)
    elif '2010' in date:
        return round((2010-2008)/(2016-2008),2)
    elif '2009' in date:
        return round((2009-2008)/(2016-2008),2)
    else:
        return 0

def inputType(date):
    """
    标准化inputType数据
    :param date:
    :return:
    """
    if u'触控' in date:
        return 1
    elif u'键盘' in date:
        return 0.5
    else:
        return 0

def isSmart(date):
    if u'是' in date: return 1
    else: return 0

def mbRom(date):
    if '128G' in date: return 1
    elif '64G' in date: return round(14/15,2)
    elif '32G' in date: return round(13/15,2)
    elif '16G' in date: return round(12/15,2)
    elif '8G' in date: return round(11/15,2)
    elif '4G' in date: return round(10/15,2)
    elif '2G' in date: return round(9/15,2)
    elif '1G' in date: return round(8/15,2)
    elif '512M' in date: return round(7/15,2)
    elif '256M' in date: return round(6/15,2)
    elif '128M' in date: return round(5/15,2)
    elif '64M' in date: return round(4/15,2)
    elif '32M' in date: return round(3/15,2)
    elif '16M' in date: return round(2/15,2)
    elif '4M' in date: return round(1/15,2)
    else: return 0

def hvGPS(date):
    if u'不支持' in date: return 0
    elif u'其他' in date: return 0
    else: return 1

def reCamera(date):
    if u'2300万' in date: return 1
    elif u'2116万' in date: return round(15/16,2)
    elif u'2100万' in date: return round(14/16,2)
    elif u'2070万' in date: return round(13/16,2)
    elif u'2000万' in date: return round(12/16,2)
    elif u'1800万' in date: return round(11/16,2)
    elif u'1600万' in date: return round(10/16,2)
    elif u'1300万' in date: return round(9/16,2)
    elif u'1200万' in date: return round(8/16,2)
    elif u'800万' in date: return round(7/16,2)
    elif u'500万' in date: return round(6/16,2)
    elif u'300万' in date: return round(5/16,2)
    elif u'200万' in date: return round(4/16,2)
    elif u'130万' in date: return round(3/16,2)
    elif u'30万' in date: return round(2/16,2)
    elif u'8万' in date: return round(1/16,2)
    else: return 0

def prCamera(date):
    if u'1600万' in date: return 1
    elif u'1300万' in date: return round(15/16,2)
    elif u'1200万' in date: return round(14/16,2)
    elif u'800万' in date: return round(13/16,2)
    elif u'500万' in date: return round(12/16,2)
    elif u'490万' in date: return round(11/16,2)
    elif u'400万' in date: return round(10/16,2)
    elif u'370万' in date: return round(9/16,2)
    elif u'300万' in date: return round(8/16,2)
    elif u'210万' in date: return round(7/16,2)
    elif u'200万' in date: return round(6/16,2)
    elif u'190万' in date: return round(5/16,2)
    elif u'130万' in date: return round(4/16,2)
    elif u'120万' in date: return round(3/16,2)
    elif u'90万' in date: return round(2/16,2)
    elif u'30万' in date: return round(1/16,2)
    else: return 0

def hvWiFi(date):
    if u'不支持' in date: return 0
    else: return 1

def hvBlue(date):
    if u'不支持' in date: return 0
    else: return 1

data = [listDate(results[2][4]),inputType(results[2][5]),isSmart(results[2][6]),mbRom(results[2][8]),hvGPS(results[2][11]),
        reCamera(results[2][12]),prCamera(results[2][13]),hvWiFi(results[2][14]),hvBlue(results[2][15])]
print results[2][4],results[2][5],results[2][6],results[2][8],results[2][11],results[2][12],results[2][13],results[2][14],results[2][15]
print data
file = open('data.txt','w+')
for result in results:
    string = '%s,%r,%r,%r,%r,%r,%r,%r,%r,%r\n' % (result[0],listDate(result[4]),inputType(result[5]),
                                                   isSmart(result[6]),mbRom(result[8]),hvGPS(result[11]),
                                                   reCamera(result[12]),prCamera(result[13]),hvWiFi(result[14]),hvBlue(result[15]))
    file.write(string)
file.close()