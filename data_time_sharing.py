# -*- coding: utf-8 -*-
#!/usr/bin/python`
import urllib
import re
import math
import sys
from time import time, sleep

import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

pre_cal_price='pre_cal_price'
pre_vol='pre_vol'
pre_capital='pre_capital'
income = 'income'
total_income='total_income'

codes=[]
codes_info={}
f =open('stock_code_followed', 'r')
for tmp in f.readlines():
   tmp = tmp.strip('\n')
   codes.append(tmp)
   codes_info[tmp] = {}

f.close()

#print "股票名称", "当前价格", "计算价格", "当前资金流入", "资金总流入", "阶段交易量","阶段交易金额","时间"

def code_info(code, info):
       
   p = re.compile('(s[hz][\d]+)[\w\W]+\"([\W\w]+)\"')
   m = p.search(info)
   if not m:
      print 'can not find stock information for %s' % (code)
      return
   stock_code = m.group(1)
   ns = m.group(2).split(',')
   stock_name = ns[0].decode('gbk')
   price_yesterday = float(ns[2].encode('utf-8'))
   price_present = float(ns[3].encode('utf-8'))
   vol_present=float(ns[8].encode('utf-8'))
   capital_present=float(ns[9].encode('utf-8'))
   date=ns[30]
   if datetime.datetime.strptime(date , '%Y-%m-%d').date() != datetime.datetime.now().date():
      print "Get yesterday's stock information"
      return
   #print code, price_present, vol_present, capital_present, date, stock_name
   #print info
   #return 
   f_out=open("time_sharing/%s_%s_%s" % (code, stock_name, date), 'a')
   time="%s-%s" % (date, ns[31])

   code_info=codes_info[code]
   if not code_info:
      if vol_present == 0:
         f_out.close()
         return
      code_info[pre_vol]=vol_present
      code_info[pre_capital]=capital_present
      code_info[pre_cal_price]=round(code_info[pre_capital]/code_info[pre_vol],2)
      code_info[income]=round((code_info[pre_cal_price] - price_yesterday)*code_info[pre_vol]/10000, 2)
      code_info[total_income]=code_info[income]
      
      f_out.write( "%s, %s, %s, %s, %s, %s, %s, %s\n" % (stock_name, 
                      price_present, code_info[pre_cal_price],code_info[income], 
                      code_info[total_income],code_info[pre_vol], code_info[pre_capital],
                      time))
      f_out.close()
      return
   
   in_vol=vol_present-code_info[pre_vol]
   in_capital=capital_present -code_info[ pre_capital]
   if 0==in_vol or 0==in_capital:
      print in_vol, in_capital
      f_out.close()
      return

   cal_price=in_capital/in_vol
   code_info[income]=round((cal_price-code_info[pre_cal_price])*in_vol / 10000, 2)
   cal_price = round(cal_price, 2)
   code_info[total_income]+=code_info[income]
   f_out.write("%s, %s, %s, %s, %s, %s, %s, %s\n" % (stock_name, 
                  price_present, cal_price,code_info[income], 
                  code_info[total_income], in_vol, in_capital,
                  time))
   f_out.close()

   code_info[pre_vol] = vol_present
   code_info[pre_capital] = capital_present
   code_info[pre_cal_price]=cal_price


def fetch_codes_info():

   code_list = ",".join(codes)
   link = 'http://hq.sinajs.cn/list=%s' % (code_list)
   print "%s: Fetch all code info" % (datetime.datetime.now())
   f = urllib.urlopen(link)
   myfile = f.readlines()
   f.close()
   i=0
   for info in myfile:
      info.decode('gbk')
      code_info(codes[i], info)
      i += 1


#fetch_codes_info()
got_time=False


while True:
   try:
      now = datetime.datetime.now().time()
      if not got_time:
         open_time_1 = now.replace(hour=9, minute=20, second=0, microsecond=0)
         end_time_1 = now.replace(hour=11, minute=30, second=0, microsecond=0)
         open_time_2 = now.replace(hour=13, minute=0, second=0, microsecond=0)
         end_time_2 = now.replace(hour=15, minute=3, second=0, microsecond=0)
         recycle_time_1 = now.replace(hour=15, minute=36, second=0, microsecond=0)
         recycle_time_2 = now.replace(hour=15, minute=37, second=0, microsecond=0)
         got_time = True

      if now >= recycle_time_1 and now <= recycle_time_2:
         print "End one trade day!"
         for (k,v) in codes_info.items():
            codes_info[k]={}

      if (((now >= open_time_1) and (now <= end_time_1)) or ((now >=open_time_2) and (now <= end_time_2))): 
         fetch_codes_info()
         sleep(1)
      else:
         print "Not trade time, sleeping"
         sleep(60)
   except Exception:
      print sys.exc_info()
