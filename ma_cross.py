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
                if (ma10 > ma20) and \
		   (ma10-ma20)<0.3 and \
                   (datetime.datetime.now() - begin).days < 3:
              	    print code	
            except Exception as e:
                print 'something wrong with code: %s, %s' % (code, str(e))

def get_code():
    threadLock.acquire()
    r = f.readline()
    threadLock.release()
    return r.strip()

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
