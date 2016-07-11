from pandas import Series
from termcolor import colored
from Util import *
class StockHash:
    name = 'default'
    data = {}
    def __init__(self, name):
        self.name = name
        self.data = {}
    def insert(self, code, exjumps=0, perfect_mas=0):
    #value is big jump before current jump
        try:
            code_class = get_code_class(code, self.name)
            if code_class.empty:
                if 'unknown' in self.data.keys():
                    self.data['unknown'].append(Series([code, 'temp', exjumps, perfect_mas], index=['code', 'name', 'exjumps', 'perfect_mas']))
                else:
                    self.data['unknown'] = []
                    self.data['unknown'].append(Series([code, 'temp', exjumps, perfect_mas], index=['code', 'name', 'exjumps', 'perfect_mas']))
                return
            code_name = code_class['name'].values[0]
            for cl in code_class['c_name'].values:
                if cl in self.data.keys():
                    self.data[cl].append(Series([code, code_name, exjumps, perfect_mas], index=['code', 'name', 'exjumps', 'perfect_mas']))
                else:
                    self.data[cl] = []
                    self.data[cl].append(Series([code, code_name, exjumps, perfect_mas], index=['code', 'name', 'exjumps', 'perfect_mas']))
        except Exception as E:
            print 'Error in StockCash with code: %s in class: %s' % (code, self.name)
            print E
    def dump(self, out):
        dup_code = []
        for k,v in self.data.items():
            if len(v) > 1:
                print k
                out.write('%s\n'% (k))
                for kv in v:
                    code = kv['code']
                    if code in dup_code:
                        code = colored(code, 'red')
                    else:
                        dup_code.append(code)
                    print code, kv['name'], kv['exjumps'], kv['perfect_mas']
                    out.write('%s, %s, %s, %s\n'  % (kv['code'], kv['name'], kv['exjumps'], kv['perfect_mas']))
