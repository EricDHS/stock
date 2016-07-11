# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
import os
import os.path
import thread
import tushare as ts
reload(sys)
sys.setdefaultencoding("utf-8")
import threading
import time
import pandas as pd
from MyStock import *


f = open('pure_code', 'r')
f_out=open("result/follower_zt%s" % (datetime.today().date().strftime('%Y%m%d')), 'a')
#f = open('temp_code', 'r')
stock_hash_industry = StockHash('industry')
stock_hash_concept = StockHash('concept')
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
                current_data = ts.get_realtime_quotes('%s' % (code))
                csv_file = 'qfq_data/%s.csv' % (code)
		if not os.path.exists(csv_file):
                    continue
                peak_data = pd.read_csv(csv_file)

                if current_data.empty or peak_data.empty:
                    continue
                ph_today = float(current_data['high'].values[0])
                price = float(current_data['price'].values[0])
                pre_close = float(current_data['pre_close'].values[0])
                pl_today = float(current_data['low'].values[0])
                po_today = float(current_data['open'].values[0])
                ma5, ma10, ma20, ma30 = get_mas_live_qfq(code, price)
                if (ma5 < ma10) or (ma10 < ma20):
                    continue
                if (ma5 >= ma10) and (ma10 >= ma20) and (ma20 >= ma30):
                    perfect_mas = 1
                else:
                    perfect_mas = 0
                if price < ( pre_close * 1.08 ):
                    continue
                if is_later(get_sh_time(), '19:00:00') or is_early(get_sh_time(), '09:30:00'):
                    peak_data = peak_data.drop(peak_data.head(1).index)
                exjumps = get_exjumps(peak_data.head(5), code)
                insert_result(code, exjumps, perfect_mas)
                #if hist_zt_qfq(peak_data.head(3), code): 
                #    print code, ma5, ma10, ma20, ma30
                #    f_out.write('%s\n' % (code))
            except Exception as e:
                print 'something wrong with code: %s, %s' % (code, str(e))

def get_code():
    threadLock.acquire()
    r = f.readline()
    threadLock.release()
    return r.strip()

def insert_result(code, exjumps=0, perfect_mas=0):
    threadLock.acquire()
    stock_hash_industry.insert(code, exjumps, perfect_mas)
    stock_hash_concept.insert(code, exjumps, perfect_mas)
    threadLock.release()
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
print 'Dump industry:'
stock_hash_industry.dump(f_out)
print 'Dump concept'
stock_hash_concept.dump(f_out)
f_out.close()
f.close()
