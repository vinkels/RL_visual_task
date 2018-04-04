from __future__ import absolute_import, division, print_function
import pandas as pd
import numpy as np
import csv, os
import helpers as hp

class img_set(object):

    def __init__(self, csv_lst):
        self.csv_lst = csv_lst
        self.df = self.alt_type()
        self.sorted_dict = self.sort_sets()
        self.split_dict = self.split_sets()
        hp.dict_pickle(self.sorted_dict, 'sorted_dict')
        hp.dict_pickle(self.split_dict, 'split_dict')

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

    def split_sets(self):

        split_dict = {}
        for key in self.sorted_dict:
            temp_one = [img for idx, img in enumerate(self.sorted_dict[key]) if idx % 2 == 0]
            temp_two = [img for idx, img in enumerate(self.sorted_dict[key]) if idx % 2 != 0]
            print(key, len(temp_one), len(temp_two))
            dict_one[key] = temp_one
            dict_two[key] = temp_two
        return dict_one, dict_two

csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
img_set(csv_lst)
