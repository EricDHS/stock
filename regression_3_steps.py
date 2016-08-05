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
		all_data = pd.read_csv('pd_5days/%s.csv' % (code))
                if all_data.empty:
                    continue
                yesterday_close = -1
		is_target = False
                for index,row in all_data[::-1].iterrows():
                    if yesterday_close == -1:
                        yesterday_close = row['close']
                        yesterday_ma5 = row['ma5']
                        yesterday_ma10 = row['ma10']
                        yesterday_ma20 = row['ma20']
                        continue
                    today_close = row['close']
		    today_ma5 = row['ma5']
		    today_ma10 = row['ma10']
		    today_ma20 = row['ma20']
		    if is_target:
			if (today_ma5 > today_ma10) and (today_ma10 > today_ma20):
			    turnover = float(row['turnover'])
                            current_data = ts.get_realtime_quotes(code)
                            a1, b1 =  dma_qfq(code)
                            a2, b2 =  dma_live_qfq(code, current_data['price'].values[0])
                            fq = 'old ddd: %s, ama: %s, diff:%s; today: ddd: %s, ama: %s, diff: %s' % (a1, b1, a1-b1, a2, b2, a2-b2)
			    print code, row['date'], turnover, fq
			is_target = False
			continue
		    yesterday_ma_series = pd.Series(data=[yesterday_ma5, yesterday_ma10, yesterday_ma20], index=['a', 'b', 'c'])
		    yesterday_ma_var = yesterday_ma_series.var()
                    if yesterday_ma_var<=0.1 and today_close>=(yesterday_close* 1.08):
                        is_target = True
		    else:
		 	is_target = False
		     
		    yesterday_close = row['close']
		    yesterday_ma5 = row['ma5']
		    yesterday_ma10 = row['ma10']
		    yesterday_ma20 = row['ma20']
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
