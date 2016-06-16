# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
import os
import thread
import tushare as ts
reload(sys)
sys.setdefaultencoding("utf-8")
import threading
import time
import pandas as pd
from MyStock import *

f = open('selected_code', 'r')
class myThread (threading.Thread):
    def __init__(self, name):
	threading.Thread.__init__(self)
	self.name = name
    def run(self):
        print "Starting " + self.name
        f_out=open("result/live_hit_line_%s" % (datetime.today().date().strftime('%Y%m%d')), 'a')
        while True:
            code = get_code()
            if not code:
                return
            try:
                current_data = ts.get_realtime_quotes('%s' % (code))
		peak_data = pd.read_csv('pd_5days/%s.csv' % (code)).head(1)
                if current_data.empty or peak_data.empty:
                    continue
                ph = float(current_data['high'].values[0])
                cl = float(current_data['low'].values[0])
                price = float(current_data['price'].values[0])
                #ma5 = float(peak_data['ma5'].values[0])
                #ma10 = float(peak_data['ma10'].values[0])
                #ma20 = float(peak_data['ma20'].values[0])
		#ma30 = get_ma30(code)
                ma5, ma10, ma20, ma30 = get_mas_live(code, price)
                if (ma5 > ma10) and (ma10 > ma20) and (ma20 > ma30) and (ph < 20):
	            if ((cl<=ma10) or (cl<=ma20) or (abs(cl-ma10)<(ma10*0.01)) or (abs(cl-ma20)<(ma20*0.01))): 
              	#    print code
                        print code, ma5, ma10, ma20, ma30, ph, cl
            except Exception as e:
                print 'something wrong with code: %s, %s' % (code, str(e))
        f_out.close()

def get_code():
    threadLock.acquire()
    r = f.readline()
    threadLock.release()
    return r.strip()
threadLock = threading.Lock()
threads = []

# 创建新线程
i = 0
while (i<10):
    threads.append(myThread(i))
    i = i + 1 


# 开启新线程
for thread in threads:
    thread.start()

# 等待所有线程完成
for t in threads:
    t.join()

f.close()
