# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
import os
import thread
reload(sys)
sys.setdefaultencoding("utf-8")
import threading
import time

f = open('stock_code', 'r')
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
            oldcode = code
            #link = 'http://hq.sinajs.cn/list=%s' % (code)
            p = re.compile('sh([\d]+)')
            m = p.search(code)
            if m: 
               code = '%s.ss' % (m.group(1))
            else:
               code = '%s.sz' % (re.compile('sz([\d]+)')).search(code).group(1)

            link = 'http://table.finance.yahoo.com/table.csv\?s=%s' % (code)
            print link
            os.system('curl %s >> history_data/%s' % (link, oldcode))


def get_code():
    threadLock.acquire()
    r = f.readline()
    threadLock.release()
    return r
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

os.system("sh ./handle_data.sh")

