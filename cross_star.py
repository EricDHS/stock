# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

f = open('stock_code', 'r')
for code in f.readlines():

   link = 'http://hq.sinajs.cn/list=%s' % (code)
   f = urllib.urlopen(link)
   myfile = f.read()
   myfile = myfile.decode('gbk')

   p = re.compile('(s[hz][\d]+)[\w\W]+\"([\W\w]+)\"')
   m = p.search(myfile)
   if not m:
      print 'can not find stock information for %s' % (code)
      continue
   stock_code = m.group(1)
   ns = m.group(2).split(',')
   stock_name = ns[0]
   price_start = ns[1].encode('utf-8')
   price_end = ns[3].encode('utf-8')
   #print stock_name, stock_code, price_start, price_end
   if (math.fabs(float(price_end) - float(price_start)) < 0.02): 
      print stock_name, stock_code, price_start, price_end



