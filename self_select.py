# -*- coding: utf-8 -*-
#!/usr/local/bin/python`
import urllib
import re
import math
import sys
import tushare as ts
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

def get_5days_data(code):
    end = datetime.date.today()
    start = datetime.date.today() - datetime.timedelta(days=16)
    return ts.get_hist_data(code, start='%s' % (start), end='%s' % (end)).head(5)

f = open('pure_code', 'r')
for code in f.readlines():
    code = code.strip()
    data = get_5days_data(code)
    if data is None: 
        print 'can not find stock information for %s' % (code)
        continue
    current_data = data.head(1)
    peak_data = data.sort_values('high', ascending=False).head(1)
    if (peak_data['high'].values > peak_data['ma5'].values) and \
       (peak_data['high'].values > peak_data['ma10'].values) and \
       (peak_data['high'].values > peak_data['ma20'].values) and \
       (current_data['low'].values < (peak_data['high'].values * 0.84)):
       print code

f.close()

