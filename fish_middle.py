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

f = open('pure_code', 'r')
class myThread (threading.Thread):
    def __init__(self, name):
	threading.Thread.__init__(self)
	self.name = name
    def run(self):
        print "Starting " + self.name
        f_out=open("result/fish_middle_%s" % (datetime.today().date().strftime('%Y%m%d')), 'a')
        while True:
            code = get_code()
            if not code:
                return
            try:
                current_data = ts.get_realtime_quotes('%s' % (code))
		peak_data = pd.read_csv('pd_5days/%s.csv' % (code))
                if current_data.empty or peak_data.empty:
                    continue
                ph_today = float(current_data['high'].values[0])
                price = float(current_data['price'].values[0])
                if price > 15:
                    continue
                pre_close = float(current_data['pre_close'].values[0])
                pl_today = float(current_data['low'].values[0])
                ma5, ma10, ma20, ma30 = get_mas_live(code, price)
                if (ma5 < ma10) or (ma10 < ma20):
                    continue
                if is_later(current_data['time'].values[0], '15:00:00'):
                    ma5_y, ma10_y, ma20_y, ma30_y = get_mas_yesterday(code)
                    pl_y = float(peak_data.head(2).tail(1)['low'].values[0])
                else:
                    ma5_y, ma10_y, ma20_y, ma30_y = get_mas(code)
                    pl_y = float(peak_data.head(1)['low'].values[0])
                if pl_y >= ma5_y:
                    continue

                if hist_zt(peak_data.head(6)): 
                    print code, ma5, ma10, ma20, ma30
                    f_out.write('%s\n' % (code))
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
