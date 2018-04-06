from __future__ import absolute_import, division, print_function
import random as rd
import helpers as hp
import copy as cp


class img_sets(object):
    def __init__(self, csv_lst, reward_val=(0,0,0)):
        self.csv_lst = csv_lst
        self.dict_one = hp.dict_unpickle('dict_one')
        self.dict_two = hp.dict_unpickle('dict_two')
        self.set_size = 100
        self.part_animals = 0.5
        self.reward_val = reward_val
        self.a_size = int(self.set_size * self.part_animals)
        self.na_size = int(self.set_size - self.a_size)
        # self.contr_ph = self.plan_phase(self.dict_one)
        # self.learn_ph = self.plan_animal(self.dict_one)
        # self.test_ph = self.plan_phase(self.dict_two)
        self.random_dicts(self.dict_one, self.dict_two)


    def random_dicts(self, dict_one, dict_two):
        ran_num = rd.randint(0,1)
        print(ran_num)
        if ran_num == 1:
            self.contr_ph = self.plan_phase(self.dict_one)
            self.learn_ph = self.plan_animal(self.dict_one)
            self.test_ph = self.plan_phase(self.dict_two)
        else:
            self.contr_ph = self.plan_phase(self.dict_two)
            self.learn_ph = self.plan_animal(self.dict_two)
            self.test_ph = self.plan_phase(self.dict_one)


    def plan_animal(self, unshuf_dict):
        type_list = ['LOW_A', 'MED_A', 'HIGH_A']
        # rd.shuffle(self.reward_val)
        # print(unshuf_dict)
        img_lst, val_lst = [], []
        # rd.shuffle(val_list)
        # print(val_lst)
        # val_list[0], val_list[1], val_list[2] = val_list[0], val_list[1], val_list[2]
        samp_num = self.na_size
        for value in self.csv_lst:
            # print(unshuf_dict[value])
            # print(rd.sample(unshuf_dict[value], samp_num))
            # print(img_lst)
            img_lst += rd.sample(unshuf_dict[value], samp_num)
            try:
                val_lst += ([self.reward_val[type_list.index(value)]]*samp_num)
            except:
                val_lst += ([0]*samp_num)
        img_lst, val_lst = self.shuffle_lists(img_lst, val_lst)
        print(val_lst)
        return [img_lst, val_lst]

    def plan_phase(self, unshuf_dict):

        set_dict = {}
        set_list = ['lm', 'lh', 'mh']
        shuf_dict = cp.deepcopy(unshuf_dict)

        for key in shuf_dict:
            rd.shuffle(shuf_dict[key])

        low_lm, med_lm = self.get_shuffled(shuf_dict, 'LOW', 'MED')
        low_lh, high_lh = self.get_shuffled(shuf_dict, 'LOW', 'HIGH')
        med_mh, high_mh = self.get_shuffled(shuf_dict, 'MED', 'HIGH')

        list_one = low_lm + low_lh + med_mh
        list_two = med_lm + high_lh + high_mh

        one_shuf, two_shuf = self.shuffle_lists(list_one, list_two)

        return [one_shuf, two_shuf]

    def get_shuffled(self, shuf_dict, type_one, type_two):
        lst_one = (rd.sample(shuf_dict['{}_NA'.format(type_one)], self.na_size) +
                  rd.sample(shuf_dict['{}_A'.format(type_one)], self.a_size))
        lst_two = (rd.sample(shuf_dict['{}_NA'.format(type_two)], self.na_size) +
                  rd.sample(shuf_dict['{}_A'.format(type_two)], self.a_size))
        lst_one, lst_two = self.shuffle_lists(lst_one, lst_two)
        return lst_one, lst_two

    def shuffle_lists(self, lst_one, lst_two):
        zip_lst = list(zip(lst_one, lst_two))
        rd.shuffle(zip_lst)
        lst_one, lst_two = zip(*zip_lst)
        return lst_one, lst_two

# csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
# img_sets(csv_lst,reward_val=(5,3,1))
