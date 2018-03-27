import pandas as pd
import numpy as np
import csv

class img_set(object):
    def __init__(self):
        self.BG_table, self.error_lst = self.get_type()

    def get_type(self):
        BG_table = pd.read_csv('input/BG_data.csv')

        type_lst = [None]*len(BG_table)
        csv_dir = 'input/'
        error_lst = []
        csv_lst = ['HIGH_A', 'HIGH_NA', 'LOW_A', 'LOW_NA', 'MED_A', 'MED_NA']
        count = 0
        for csv_name in csv_lst:
            with open(csv_dir+csv_name+'.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                for row in csv_reader:
                    if type_lst[int(row[0])-1] is None:
                        type_lst[int(row[0])-1] = csv_name
                    else:
                        error_lst.append(int(row[0])+1)
                        type_lst[int(row[0])-1] = None

        BG_table['condi'] = pd.Series(type_lst, index=BG_table.index)
        return BG_table, error_lst

jup = img_set()
