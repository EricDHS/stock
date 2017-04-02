import pandas as pd
import tushare as ts
from MyStock import *
from datetime import datetime, timedelta

code = '600460'
current_data = ts.get_realtime_quotes(code)
a1, b1 =  dma_qfq(code)
a2, b2 =  dma_live_qfq(code, current_data['price'].values[0])

print a1, b1, a1-b1
print a2, b2, a2-b2




#current_data = ts.get_realtime_quotes('600135')

#peak_data = pd.read_csv('pd_5days/150020.csv').head(1)
#aa = float(peak_data['turnover'].values[0]) if 'turnover' in peak_data.columns else 0
#print aa
#def parse_time(s):
#    ''' Parse 12-hours format '''
#    return datetime.strptime(s, '%H:%M:%S')

#time = parse_time('14:00:01')
#print mas_tomorrow('600392')
#cur = ts.get_realtime_quotes('600392')
#print str(cur['time'].values[0])
#endtime = parse_time(str(cur['time'].values[0]))
#print time >= endtime
#print peak_data['close'].mean()
#peak_data = pd.read_csv('pd_5days/600135.csv').sort_values('high', ascending=False).head(1)
#if not peak_data.empty:
#    p= peak_data['high']
#    c = current_data['low']
#    print p
#    print c
#else:
#    print "none"
#pp = float(p.values[0])
#cc = float(c.values[0])
#print p
#print pp>cc 
#c = pd.concat([a,b])
#print peak_data['high'].gt(current_data['low'])
