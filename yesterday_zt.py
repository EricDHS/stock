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
# f = open('test_pure_code', 'r')
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
		all_data = pd.read_csv('pd_5days/%s.csv' % (code)).head(3)
                if all_data.empty:
                    continue
                close1 = all_data.head(2).tail(1)['close'].values[0]
                close2 = all_data.tail(1)['close'].values[0]
                if close1 >= (close2*1.099) and close1<20:
                    print code
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
