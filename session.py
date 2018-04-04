from __future__ import absolute_import, division, print_function
import random as rd
import helpers as hp
import copy


class session(object):
    def __init__(self, csv_lst):
        self.csv_lst = csv_lst
        self.sort_dict = hp.dict_unpickle('sorted_dict')
        # print(self.sort_dict)
        self.set_size = 100
        self.part_animals = 0.5
        self.contr_ph = []
        self.learn_ph = []
        self.test_ph = []
        self.plan_session()


    def plan_session(self, shuf_dict):

        # key_lst = ['control','learning','test']
        # ses_dict = {el:0 for el in key_lst}
        a_size = int(self.set_size * self.part_animals)
        na_size = int(self.set_size - a_size)

        print(list(shuf_dict))
        for key in shuf_dict:
            rd.shuffle(shuf_dict[key])

        lst_low, lst_med, lst_hig = [], [], []
        lst_low = rd.sample(shuf_dict['LOW_NA'], na_size) + rd.sample(shuf_dict['LOW_A'], a_size)
        lst_med = rd.sample(shuf_dict['LOW_NA'], na_size) + rd.sample(shuf_dict['LOW_A'], a_size)
        print(lst_low)
        lst_one = []
        lst_two = []

        # range_lst = range(len(self.set_size))
        # pick_LNA = rd.sample(shuf_dict[key], k)

csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
session(csv_lst)


# import random
#
# a = ['a', 'b', 'c']
# b = [1, 2, 3]
#
# c = list(zip(a, b))
#
# random.shuffle(c)
#
# a, b = zip(*c)
#
# print a
# print b
#
# [OUTPUT]
# ['a', 'c', 'b']
# [1, 3, 2]
