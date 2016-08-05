#!/usr/bin/python
import pandas as pd
import tushare as ts
from MyStock import *
from datetime import datetime, timedelta
from termcolor import colored

import sys, getopt
from MyStock import *

def main(argv):
    f_path = ''
    try:
        opts, args = getopt.getopt(argv,'p:', ["path"])
    except getopt.GetoptError:
        print 'test.py -p path'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -p path'
            sys.exit()
        elif opt in ("-p"):
            f_path = arg

    f = open(f_path, 'r')
    dup = []
    for line in f:
        line=line.strip('\n')
        ary = line.split(',')
        p_code = ''
        if len(ary) == 1:
            print line
        else:
            code = ary[0]
            if code in dup:
                p_code = colored(line, 'red')
            else:
                dup.append(code)
                p_code = line 
            current_data = ts.get_realtime_quotes('%s' % (code))
            pre_close = float(current_data['pre_close'].values[0])
            price = float(current_data['price'].values[0])
            rate ="%.1f" %  ((price - pre_close) * 100 / pre_close)
            ma5, ma10, ma20, ma30 = get_mas_live_qfq(code, price)
            ma_series = pd.Series(data=[ma5, ma10, ma20, ma30], index=['a', 'b', 'c', 'd'])

            print '%s: %s, price:%s, ma_mean:%s' % (p_code, rate, price, ("%.2f" % ma_series.var()))

if __name__ == "__main__":
   main(sys.argv[1:])
