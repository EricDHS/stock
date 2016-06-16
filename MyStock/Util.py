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

def get_ma30(code):
    data = pd.read_csv('../pd_5days/%s.csv' % (code)).head(30)
    if data.empty:
        return 0
    return float(data['close'].mean())

def get_mas_live(code, current_price):
    data = pd.read_csv('pd_5days/%s.csv' % (code))
    if data.empty:
        return 0,0,0,0

    data5 = data.head(4)['close'].append(pd.Series(data=[current_price]))
    data10 = data.head(9)['close'].append(pd.Series(data=[current_price]))
    data20 = data.head(19)['close'].append(pd.Series(data=[current_price]))
    data30 = data.head(29)['close'].append(pd.Series(data=[current_price]))
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
    data10 = data.head(10)['close'].append(pd.Series(data=[close*0.9]))
    data10_1 = data.head(10)['close'].append(pd.Series(data=[close*1.1]))
    return close, close*0.9, close*1.1, float(data5.mean()), float(data5_1.mean()), float(data10.mean()), float(data10_1.mean())

def is_later(time1, time2):
    t1 = datetime.strptime(time1, '%H:%M:%S')
    t2 = datetime.strptime(time2, '%H:%M:%S')
    return t1>=t2

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
