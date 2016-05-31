# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
import os
import thread
import datetime
import tushare as ts
reload(sys)
sys.setdefaultencoding("utf-8")
import threading
import time
import pandas as pd

f = open('pure_code', 'r')
class myThread (threading.Thread):
    def __init__(self, name):
	threading.Thread.__init__(self)
	self.name = name
    def run(self):
        print "Starting " + self.name
        f_out=open("result/upsidedown_%s" % (datetime.datetime.today().date().strftime('%Y%m%d')), 'a')
        while True:
            code = get_code()
            if not code:
                return
            try:
                current_data = ts.get_realtime_quotes('%s' % (code))
		peak_data = pd.read_csv('pd_5days/%s.csv' % (code)).head(5).sort_values('high', ascending=False).head(1)
                if current_data.empty or peak_data.empty:
                    continue
                ph = float(peak_data['high'].values[0])
                cl = float(current_data['low'].values[0])
                ma5 = float(peak_data['ma5'].values[0])
                ma10 = float(peak_data['ma10'].values[0])
                if (peak_data['high'].values > peak_data['ma5'].values) and \
		   (peak_data['high'].values > peak_data['ma10'].values) and \
		   (peak_data['high'].values > peak_data['ma20'].values) and \
		   ((ph*0.89) > cl) and \
                   (cl > 0) and (cl < 18) and \
                   (ma5*0.96 >= ma10):
              	    print code
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
