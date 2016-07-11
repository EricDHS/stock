#!/usr/bin/python
import pandas as pd
import tushare as ts
from MyStock import *
from datetime import datetime, timedelta

import sys, getopt
from MyStock import *
current_data = ts.get_realtime_quotes('600135')

def main(argv):
   try:
      opts, args = getopt.getopt(argv,'c:', ["code"])
   except getopt.GetoptError:
      print 'test.py -c code'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
      	 print 'test.py -c code'
         sys.exit()
      elif opt in ("-c"):
         code = arg
   c,tl,th,ma5l,ma5h,ma10l,ma10h,ma20l,ma20h,ma30l,ma30h =  mas_tomorrow(str(code))
   print 'close:%s, t_l:%s, t_h: %s, ma5_l:%s, ma5_h:%s, ma10_l:%s, ma10_h:%s, ma20_l:%s, ma20_h: %s, ma30_l:%s, ma30_h:%s' % (c, tl, th, ma5l, ma5h, ma10l, ma10h, ma20l, ma20h, ma30l, ma30h)
   
if __name__ == "__main__":
   main(sys.argv[1:])
