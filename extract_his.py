# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

fin = sys.argv[1]
p= re.compile('([\d]+)\.pht[\w\W]+year=([\d]+)[\w\W]+jidu=([\d]+)')

fcode = p.search(fin)



fout = '%s-Y%s-Q%s.txt' % (fcode.group(1), fcode.group(2), fcode.group(3))


print fout

sys.exit(0)


f_in = open(fin, 'r')
f_out = open(fout, 'w')

flag = 0

for lin in f.readlines():
   if (0 == flag) and (re.match('FundHoldSharesTable', line)):
      flag += 1
      continue
   else:
      continue

   if (1 == flag) and (re.match('FundHoldSharesTable', line)):
      break

      
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



