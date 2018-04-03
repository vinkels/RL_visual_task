from __future__ import absolute_import, division, print_function
import pandas as pd
import numpy as np
import csv, os

class img_set(object):
    def __init__(self):
        self.csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
        self.df = self.alt_type()
        self.sorted_dict = self.sort_sets()


    def alt_type(self):

        BG_table = pd.read_csv('input/BG_data2.csv')
        BG_table['condition'] = None
        count = 0
        for value in self.csv_lst:
            type_files = os.listdir('images/'+value)
            for img in type_files:
                BG_table.loc[BG_table['filename'] == img, 'condition'] = value
                count += 1

        return BG_table

    def sort_sets(self):

        df_sorted = self.df.sort_values('BG')
        df_sorted.to_csv('output/table_check.csv')
        sort_dict = {}
        for type in self.csv_lst:
            sort_dict[type] = list(df_sorted.loc[df_sorted['condition'] == type, 'filename'])

        return sort_dict

img_set()
