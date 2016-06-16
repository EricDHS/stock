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
        f_out=open("result/hit_line_%s" % (datetime.datetime.today().date().strftime('%Y%m%d')), 'a')
        while True:
            code = get_code()
            if not code:
                return
            try:
		peak_data = pd.read_csv('pd_5days/%s.csv' % (code)).head(1)
                if peak_data.empty:
                    continue
                begin = datetime.datetime.strptime(peak_data['date'].values[0] , '%Y-%m-%d')
                ma5 = float(peak_data['ma5'].values[0])
                ma10 = float(peak_data['ma10'].values[0])
                ma20 = float(peak_data['ma20'].values[0])
                close = float(peak_data['close'].values[0])
                turnover = float(peak_data['turnover'].values[0]) if 'turnover' in peak_data.columns else 0 
                low = float(peak_data['low'].values[0])
                ma30 = get_ma30(code)
                if (ma10 > ma20) and \
		   (ma5 > ma10) and \
                   (ma20 > ma30) and \
                   ((low<=ma10) or (abs(low -ma20) < (close*0.01))) and \
                   close<15 and close >3 and \
                   (datetime.datetime.now() - begin).days < 3:
              	    print code, turnover
                    f_out.write('%s, %s\n' % (code, turnover))
            except Exception as e:
                print 'something wrong with code: %s, %s' % (code, str(e))
        f_out.close()

def get_code():
    threadLock.acquire()
    r = f.readline()
    threadLock.release()
    return r.strip()
def get_ma30(code):
    data = pd.read_csv('pd_5days/%s.csv' % (code)).head(30)
    if data.empty:
        return 0
    return float(data['close'].mean())
threadLock = threading.Lock()
threads = []

# 创建新线程
i = 0
while (i<1):
    threads.append(myThread(i))
    i = i + 1 


# 开启新线程
for thread in threads:
    thread.start()

# 等待所有线程完成
for t in threads:
    t.join()

f.close()
