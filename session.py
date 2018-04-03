from __future__ import absolute_import, division, print_function
import random as rd
import copy

class session(object):
    def __init__(self, sorted_dict, csv_lst):
        self.csv_lst = csv_lst
        self.sort_dict = sorted_dict
        self.set_size = 100
        self.part_animals = 0.5
        self.contr_ph = []
        self.learn_ph = []
        self.test_ph = []


    def plan_session(self):

        a_size = self.set_size * self.part_animals
        na_size = self.set_size - a_size
        shuf_dict = self.sort_dict
        for key in self.sorted_dict:
            rd.shuffle(shuf_dict[key])

        range_lst = range(len(self.set_size))
        

        rd.sample(range(len(self.sorted_dict[key])), a_size)

        rd.shuffle(x[, random])
