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
FILE_END = False

f = open('pure_code', 'r')
class myThread (threading.Thread):
    def __init__(self, name):
	threading.Thread.__init__(self)
	self.name = name
    def run(self):
        print "Starting " + self.name
        while True:
            if FILE_END:
                print 'FILE_END, %s returns' % (self.name)
                return
            code = get_code()
            print 'Code is: %s, thread: %s' % (code, self.name) 
            if not code:
                print 'Non-Code, %s returns' % (self.name)
                return
            try:
                end = datetime.date.today()
                start = datetime.date.today() - datetime.timedelta(days=200)
                ts.get_h_data(code).to_csv('qfq_data/%s.csv' % (code))
                print 'Code: %s, thread: %s is done' % (code, self.name)
            except:
                print 'something wrong with code: %s, thread: %s' % (code, self.name)

def get_code():
    global FILE_END
    threadLock.acquire()
    if FILE_END:
        threadLock.release()
        return '' 
    r = f.readline()
    if not r:
        FILE_END = True
        threadLock.release()
        return ''
    r = r.strip()
    threadLock.release()
    return r

threadLock = threading.Lock()
threads = []

# 创建新线程
i = 0
while (i<100):
    threads.append(myThread(i))
    i = i + 1 


# 开启新线程
for thread in threads:
    thread.start()

# 等待所有线程完成
for t in threads:
    t.join()

f.close()
