# -*- coding: utf-8 -*-
#!/usr/local/bin/python

#0：”大秦铁路”，股票名字；
#1：”27.55″，今日开盘价；
#2：”27.25″，昨日收盘价；
#3：”26.91″，当前价格；
#4：”27.55″，今日最高价；
#5：”26.20″，今日最低价；
#6：”26.91″，竞买价，即“买一”报价；
#7：”26.92″，竞卖价，即“卖一”报价；
#8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
#9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
#10：”4695″，“买一”申请4695股，即47手；
#11：”26.91″，“买一”报价；
#12：”57590″，“买二”
#13：”26.90″，“买二”
#14：”14700″，“买三”
#15：”26.89″，“买三”
#16：”14300″，“买四”
#17：”26.88″，“买四”
#18：”15100″，“买五”
#19：”26.87″，“买五”
#20：”3100″，“卖一”申报3100股，即31手；
#21：”26.92″，“卖一”报价
#(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
#30：”2008-01-11″，日期；
#31：”15:05:32″，时间；

import urllib
import re
import math
import sys
from subprocess import check_output
reload(sys)
sys.setdefaultencoding("utf-8")

def peak_recent(code):
  try:
    output = check_output('sh stock_hhv.sh %s' % (code), shell=True)
    return float(output)
  except:
    return None

def read_time_stock(code):
  link = 'http://hq.sinajs.cn/list=%s' % (code)
  f = urllib.urlopen(link)
  myfile = f.read()
  f.close()
  myfile = myfile.decode('gbk')
  p = re.compile('(s[hz][\d]+)[\w\W]+\"([\w\W]+)\"')
  m = p.search(myfile)
  if not m:
     print 'can not find stock information for %s' % (code)
     return None, None
  stock_code = m.group(1)
  ns = m.group(2).split(',')

  price_now = ns[3].encode('utf-8')
  price_end = ns[5].encode('utf-8')
  return price_now, price_end

f = open('history_data/code', 'r')
for code in f.readlines():
  his_peak = peak_recent(code)
  today_now, today_low= read_time_stock(code)
  if his_peak and today_low and today_now:
    if today_low <= his_peak * 0.85:
      print "%s, peak: %s, today_low: %s, today_now: %s" % (code, his_peak, today_low, today_now)
f.close()

