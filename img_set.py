from __future__ import absolute_import, division, print_function
import pandas as pd
import numpy as np
import csv, os

class img_set(object):
    def __init__(self):
        self.csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
        # self.df = self.get_table()
        # self.df, self.error_lst = self.get_type()
        # self.condi_dict = self.get_imglst()
        self.df, self.condi_dict = self.alt_type()
        print(self.condi_dict)
        # self.set_bounds()

    def get_imglst(self):
        condi_dict = {}
        for name in self.csv_lst:
            temp_part = self.df.loc[self.df['condi'] == name]
            condi_dict[name] = list(temp_part['filename'])
        return condi_dict

    def get_type(self):
        BG_table = pd.read_csv('input/BG_data.csv')
        type_lst = [None]*len(BG_table)
        csv_dir = 'input/'
        error_lst = []
        count = 0
        for csv_name in self.csv_lst:
            with open(csv_dir+csv_name+'.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                for row in csv_reader:
                    if type_lst[int(row[0])-1] is None:
                        type_lst[int(row[0])-1] = csv_name
                    else:
                        error_lst.append(int(row[0])+1)
                        type_lst[int(row[0])-1] = None

        BG_table['condi'] = pd.Series(type_lst, index=BG_table.index)
        print(error_lst, len(error_lst))
        return BG_table, error_lst

    def alt_type(self):
        BG_table = pd.read_csv('input/BG_data.csv')
        BG_table['condition'] = None
        type_dict = {}
        error_lst = []
        count = 0

        for value in self.csv_lst:
            type_dict[value] = os.listdir('images/'+value)
            for img in type_dict[value]:
                BG_table.loc[BG_table['filename'] == img, 'condition'] = value
                count += 1

        print(BG_table[['filename', 'condition']])
        error_lst = []
        print(type_dict)
        return BG_table, type_dict

    def get_table(self):
        BG_table = pd.read_csv('input/BG_data.csv')
        BG_table['condition'] = None
        return BG_table




img_set()
