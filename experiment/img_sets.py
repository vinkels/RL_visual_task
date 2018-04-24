from __future__ import absolute_import, division, print_function
import random as rd
import sys, os
sys.path.append("..")
import RL_visual_task.helpers as hp
import copy as cp


class img_sets(object):
    def __init__(self, ppn,csv_lst, reward_val,demo_num=30):
        self.demo_num = demo_num
        self.csv_lst = csv_lst
        self.ppn = ppn
        self.dict_one = hp.dict_unpickle('dict_one')
        self.dict_two = hp.dict_unpickle('dict_two')
        self.demo_dict = hp.dict_unpickle('demo_dict')
        self.set_size = 100
        self.part_animals = 0.5
        self.reward_val = reward_val
        self.a_size = int(self.set_size * self.part_animals)
        self.na_size = int(self.set_size - self.a_size)
        self.random_dicts(self.dict_one, self.dict_two, ran_num = rd.randint(0,1))


    def random_dicts(self, dict_one, dict_two, ran_num=0):
        self.demo_ph = self.plan_demo()
        if ran_num == 1:
            self.contr_ph = self.plan_phase(self.dict_one)
            self.learn_ph = self.plan_animal(self.dict_one)
            self.test_ph = self.plan_phase(self.dict_two)
        else:
            self.contr_ph = self.plan_phase(self.dict_two)
            self.learn_ph = self.plan_animal(self.dict_two)
            self.test_ph = self.plan_phase(self.dict_one)

    def plan_animal(self, unshuf_dict):

        type_list = ['LOW', 'MED', 'HIGH']
        img_lst, val_lst, a_lst = [], [], []

        samp_num = self.na_size
        for value in self.csv_lst:
            for idx, name in enumerate(type_list):
                if value.startswith(name):

                    img_lst += rd.sample(unshuf_dict[value], samp_num)
                    val_lst += ([self.reward_val[idx]]*samp_num)
                    if value.endswith('NA'):
                        a_lst += [0]*samp_num
                    else:
                        a_lst += [1]*samp_num

                        break
        tot_lst = [img_lst, val_lst, a_lst]
        [img_lst, val_lst, a_lst] = self.shuffle_lists(tot_lst)
        return [img_lst, val_lst, a_lst]

    def plan_phase(self, unshuf_dict):

        a_lst = []
        set_dict = {}
        set_list = ['lm', 'lh', 'mh']
        shuf_dict = cp.deepcopy(unshuf_dict)

        for key in shuf_dict:
            rd.shuffle(shuf_dict[key])

        low_lm, med_lm, a_lm = self.get_shuffled(shuf_dict, 'LOW', 'MED')
        low_lh, high_lh, a_lh = self.get_shuffled(shuf_dict, 'LOW', 'HIGH')
        med_mh, high_mh, a_mh = self.get_shuffled(shuf_dict, 'MED', 'HIGH')

        list_one = low_lm + high_lh + med_mh
        list_two = med_lm + low_lh + high_mh
        list_a = a_lm + a_lh + a_mh

        type_dct = {}
        for idx, value in enumerate(low_lm):
            type_dct[value] = 'low_lm'
            type_dct[high_lh[idx]] = 'high_lh'
            type_dct[med_mh[idx]] = 'med_mh'
            type_dct[med_lm[idx]] = 'med_lm'
            type_dct[low_lh[idx]] = 'low_lh'
            type_dct[high_mh[idx]] = 'high_mh'
        hp.dict_pickle(type_dct, 'PPN{}_{}'.format(self.ppn, self.reward_val))

        print(type_dct)



        list_tot = [list_one, list_two, list_a]
        one_shuf, two_shuf, a_shuf = self.shuffle_lists(list_tot)

        return [one_shuf, two_shuf, a_shuf]

    def get_shuffled(self, shuf_dict, type_one, type_two):
        lst_one = (rd.sample(shuf_dict['{}_NA'.format(type_one)], self.na_size) +
                  rd.sample(shuf_dict['{}_A'.format(type_one)], self.a_size))
        lst_two = (rd.sample(shuf_dict['{}_NA'.format(type_two)], self.na_size) +
                  rd.sample(shuf_dict['{}_A'.format(type_two)], self.a_size))
        lst_a = [0]*self.na_size+[1]*self.a_size
        lst_tot = [lst_one, lst_two, lst_a]
        [lst_one, lst_two, lst_a] = self.shuffle_lists(lst_tot)
        return lst_one, lst_two, lst_a

    def shuffle_lists(self, lst_lsts):
        shuf_lsts = []
        list_shuf = list(range(len(lst_lsts[0])))
        rd.shuffle(list_shuf)
        for lst in lst_lsts:
            temp_lst = [lst[idx] for idx in list_shuf]
            shuf_lsts.append(temp_lst)

        return shuf_lsts

    def plan_demo(self):
        a_len = len(self.demo_dict['A'])/2
        na_len = len(self.demo_dict['NA'])/2
        r_num =int(self.demo_num/2)
        print(r_num)
        a_lst = rd.sample(self.demo_dict['A'], self.demo_num)
        na_lst = rd.sample(self.demo_dict['NA'], self.demo_num)
        l_lst = na_lst[:r_num]+a_lst[r_num:]
        r_lst = na_lst[r_num:]+a_lst[:r_num]
        a_lst = [0]*r_num + [1]*r_num
        rwd_lst = [3]*len(l_lst)
        [l_shuf, r_shuf, a_shuf] = self.shuffle_lists([l_lst,r_lst,a_lst])
        return [l_shuf, r_shuf, a_shuf, rwd_lst]


# csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
# img_sets(csv_lst,reward_val=(5,3,1))
