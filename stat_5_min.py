# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding("utf-8")

sum = 0
tmp_sum =0
vols = {}
time1 = None
time2 = None
f = open(sys.argv[1], 'r')
for data in f.readlines():
   data = data.rstrip()
   datas = data.split(",")
   if len(datas) < 8:
      print "data: %s is illegal!" % (data)
      continue
   
   vol = float(datas[5])
   sum += vol
   tmp_sum += vol
   t = datas[7].lstrip()
   t = time.strptime(t,'%Y-%m-%d-%H:%M:%S')
   if not time1:
      time1 = datetime.datetime(* t[:7])
   else:
      time2 = datetime.datetime(* t[:7])
    
      if (time2-time1).seconds >= 300 or 0 == (t.tm_min % 5):
         vols[datas[7]] = tmp_sum
         tmp_sum = 0
         time1 = None
   
f.close()
#keys = vols.keys().sort()
#for key in keys:
#print key, vols[key] / sum * 100

#for (key, value) in vols.items():
#   print key, value/sum *  100

results =  sorted(vols.items(), key=lambda d:d[0])
t_sum = 0
for k,v in results:
   t_sum += v
   print k,"%.2f" % (v/sum*100), "%.2f" % (t_sum/sum*100)
