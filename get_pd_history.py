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
                end = datetime.date.today()
                start = datetime.date.today() - datetime.timedelta(days=200)
                ts.get_hist_data(code, start='%s' % (start), end='%s' % (end)).to_csv('pd_5days/%s.csv' % (code))
            except:
                print 'something wrong with code: %s' % (code)

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
