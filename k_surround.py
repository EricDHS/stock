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
        f_out=open("result/k_surround_%s" % (datetime.today().date().strftime('%Y%m%d')), 'a')
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
                pre_close = float(current_data['pre_close'].values[0])
                if is_later(current_data['time'].values[0], '15:00:00'):
                    ma5, ma10, ma20, ma30 = get_mas_yesterday(code)
                    peak_data = peak_data.drop(peak_data.head(1).index)
                else:
                    ma5, ma10, ma20, ma30 = get_mas(code)
                ph = float(peak_data.head(1)['high'].values[0])
                cl = float(peak_data.head(1)['low'].values[0])
                ma_series = pd.Series(data=[ma5, ma10, ma20, ma30], index=['a', 'b', 'c', 'd'])
                ma_var = ma_series.var()
                ma_max = ma_series.max()
                ma_min = ma_series.min()
                overlap = 0
                if (cl > ma_max) or (ph < ma_min):
                    continue
                if (ma_max >= ph) and (ma_min <= cl):
                    overlap = 1
                if (ph >= ma_max) and (cl >= ma_min) and (not overlap):
                    overlap = (ma_max - cl) / (ph - cl)
                if (ph <= ma_max) and (cl <= ma_min) and (not overlap):
                    overlap = (ph - ma_min) / (ph -cl)
                if (ph >= ma_max) and (cl <= ma_min) and (not overlap):
                    overlap = (ma_max - ma_min) / (ph - cl)
                if (ma_var <= 0.02) and (overlap > 0.5) and (ph_today >=(1.06 * pre_close)):
                    print code, ma5, ma10, ma20, ma30,ma_var, ph, cl
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
