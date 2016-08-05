#!/usr/local/bin/python
import urllib
import re
import math
import sys
import os
import thread
from datetime import datetime, timedelta
import tushare as ts
reload(sys)
sys.setdefaultencoding("utf-8")
import threading
import time
import pandas as pd
from dateutil import tz

def get_ma30(code):
    data = pd.read_csv('pd_5days/%s.csv' % (code)).head(30)
    if data.empty:
        return 0
    return float(data['close'].mean())
def get_sh_time():
    from_zone = tz.tzlocal()
    to_zone = tz.gettz('Asia/Shanghai')
    local_time = datetime.now()
    local_time = local_time.replace(tzinfo=from_zone)
    sh_time = local_time.astimezone(to_zone)
    return '%s:%s:%s' % (sh_time.hour, sh_time.minute, sh_time.second)

def ama_data(data):
    i = 0
    series = pd.Series()
    while (i<36):
        if (0 == i):
            tmp_data = data
        else:
            tmp_data = tmp_data.drop(tmp_data.head(1).index)
        i += 1
        series = series.append(pd.Series(data=ddd_data(tmp_data)))
    return float(series.mean())
        
def ddd_data(data):
    data5 = data.head(5)
    data89 = data.head(89)
    ma5 = float(data5.mean())
    ma89 = float(data89.mean())
    return (ma5 - ma89)

def dma_qfq(code, prior_days=4):
    data = pd.read_csv('qfq_data/%s.csv' % (code))
    if data.empty:
        return 9999,9999

    data = data.drop(data.head(prior_days).index)
    data = data['close']
    ddd = float('%.3f' % (ddd_data(data)))
    ama = float('%.3f' % (ama_data(data)))
    return ddd, ama
def dma_live_qfq(code, current_price):
    data = pd.read_csv('qfq_data/%s.csv' % (code))
    if data.empty:
        return 9999,9999
    current_price = float(current_price)
    if is_later(get_sh_time(), '19:00:00') or is_early(get_sh_time(), '09:30:00'):
        data = data.drop(data.head(1).index)
    data = pd.Series(data=[current_price]).append(data['close'])
    data = data.reset_index(drop=True)
    ddd = float('%.3f' % (ddd_data(data)))
    ama = float('%.3f' % (ama_data(data)))
    return ddd, ama
def get_mas_live_qfq(code, current_price):
    data = pd.read_csv('qfq_data/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0

    if is_later(get_sh_time(), '19:00:00') or is_early(get_sh_time(), '09:30:00'):
        data = data.drop(data.head(1).index)
    data5 = data.head(4)['close'].append(pd.Series(data=[current_price]))
    data10 = data.head(9)['close'].append(pd.Series(data=[current_price]))
    data20 = data.head(19)['close'].append(pd.Series(data=[current_price]))
    data30 = data.head(29)['close'].append(pd.Series(data=[current_price]))
    return float(data5.mean()), float(data10.mean()), float(data20.mean()), float(data30.mean())
def get_mas_live(code, current_price):
    data = pd.read_csv('pd_5days/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0
    if is_later(get_sh_time(), '15:10:00') or is_early(get_sh_time(), '09:30:00'):
        data = data.drop(data.head(1).index)
    data5 = data.head(4)['close'].append(pd.Series(data=[current_price]))
    data10 = data.head(9)['close'].append(pd.Series(data=[current_price]))
    data20 = data.head(19)['close'].append(pd.Series(data=[current_price]))
    data30 = data.head(29)['close'].append(pd.Series(data=[current_price]))
    return float(data5.mean()), float(data10.mean()), float(data20.mean()), float(data30.mean())
def get_mas_hist(code, days=0):
    data = pd.read_csv('qfq_data/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0
    data = data.drop(data.head(days).index)
    data5 = data.head(5)['close']
    data10 = data.head(10)['close']
    data20 = data.head(20)['close']
    data30 = data.head(30)['close']
    return float(data5.mean()), float(data10.mean()), float(data20.mean()), float(data30.mean())
def get_mas_before_date(code, date):
    data = pd.read_csv('qfq_data/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0
    data = data[data.date <= date]
    data5 = data.head(5)['close']
    data10 = data.head(10)['close']
    data20 = data.head(20)['close']
    data30 = data.head(30)['close']
    return float(data5.mean()), float(data10.mean()), float(data20.mean()), float(data30.mean())
def get_mas(code):
    data = pd.read_csv('pd_5days/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0

    data5 = data.head(5)['close']
    data10 = data.head(10)['close']
    data20 = data.head(20)['close']
    data30 = data.head(30)['close']
    return float(data5.mean()), float(data10.mean()), float(data20.mean()), float(data30.mean())
def get_mas_yesterday(code):
    data = pd.read_csv('pd_5days/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0
    data = data.drop(data.head(1).index)
    data5 = data.head(5)['close']
    data10 = data.head(10)['close']
    data20 = data.head(20)['close']
    data30 = data.head(30)['close']
    return float(data5.mean()), float(data10.mean()), float(data20.mean()), float(data30.mean())
def mas_tomorrow(code):
    data = pd.read_csv('pd_5days/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0
    close = float(data.head(1)['close'].values)
    data5 = data.head(4)['close'].append(pd.Series(data=[close*0.9]))
    data5_1 = data.head(4)['close'].append(pd.Series(data=[close*1.1]))
    data10 = data.head(9)['close'].append(pd.Series(data=[close*0.9]))
    data10_1 = data.head(9)['close'].append(pd.Series(data=[close*1.1]))
    data20 = data.head(19)['close'].append(pd.Series(data=[close*0.9]))
    data20_1 = data.head(19)['close'].append(pd.Series(data=[close*1.1]))
    data30 = data.head(29)['close'].append(pd.Series(data=[close*0.9]))
    data30_1 = data.head(29)['close'].append(pd.Series(data=[close*1.1]))
    return close, close*0.9, close*1.1, float(data5.mean()), float(data5_1.mean()), float(data10.mean()), float(data10_1.mean()), float(data20.mean()), float(data20_1.mean()),float(data30.mean()), float(data30_1.mean())

def is_later(time1, time2):
    t1 = datetime.strptime(time1, '%H:%M:%S')
    t2 = datetime.strptime(time2, '%H:%M:%S')
    return t1>=t2

def is_early(time1, time2):
    t1 = datetime.strptime(time1, '%H:%M:%S')
    t2 = datetime.strptime(time2, '%H:%M:%S')
    return t1<=t2

def hist_zt(data):
    yesterday_close = -1
    is_target = False
    for index,row in data[::-1].iterrows():
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
		return True 
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
    return False
def hist_zt_qfq(data, code):
    yesterday_close = -1
    is_target = False
    for index,row in data[::-1].iterrows():
        if yesterday_close == -1:
            yesterday_close = row['close']
            yesterday_ma5, yesterday_ma10, yesterday_ma20, yesterday_ma30 = get_mas_before_date(code, row['date'])
            continue
        today_close = row['close']
        today_ma5, today_ma10, today_ma20, today_ma30 = get_mas_before_date(code, row['date'])
        if is_target:
            if (today_ma5 > today_ma10) and (today_ma10 > today_ma20):
                return True
        yesterday_ma_series = pd.Series(data=[yesterday_ma5, yesterday_ma10, yesterday_ma20], index=['a', 'b', 'c'])
        yesterday_ma_var = yesterday_ma_series.var()
        if yesterday_ma_var<=0.1 and today_close>=(yesterday_close* 1.08):
            is_target = True
        else:
            is_target = False

        yesterday_close = row['close']
        yesterday_ma5 = today_ma5
        yesterday_ma10 = today_ma10
        yesterday_ma20 = today_ma20
    return False

def get_exjumps(data, code):
    exjumps = 0
    pre_close = -1
    for index,row in data[::-1].iterrows():
        if pre_close == -1:
            pre_close = row['close']
        close = row['close']
        if close >= pre_close*1.08:
            exjumps += 1
        pre_close = close 
    return exjumps

def get_code_class(code, code_class='industry'):
    f = ''
    if 'industry' == code_class:
        f = 'data/sina_industry.csv'
    elif 'concept' == code_class:
        f = 'data/sina_concept.csv'
    else:
        return None 
    try:
        data = pd.read_csv(f)
        code = int(code)
        return data[data.code == code]

    except Exception as e:
        print "Error with Code: %s, %s" % (code, str(e))
        print os.system('pwd') 
        return None
