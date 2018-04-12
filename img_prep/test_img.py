from __future__ import absolute_import, division, print_function
from shutil import copyfile as cf
import csv, os, sys
sys.path.append("..")
from RL_visual_task.helpers import dict_pickle


class test_img():
    def __init__(self):
        self.img_dir = '/Users/yannick/Desktop/code/stage/image_sets/allstimuli_recoded/'
        self.img_data = '/output/table_check.csv'
        self.tar_dir = '/images/demo/'
        self.dir_path = sys.path[0].split('/')
        self.get_img()

    def get_img(self):
        a_lst, n_lst = [], []
        test_dct = {}

        path = '/'+'/'.join(self.dir_path[:-1])
        with open((path+self.img_data)) as csvfile:
            csv_read = csv.reader(csvfile, delimiter=',')
            idx = 0
            for idx, row in enumerate(csv_read):
                if row[12] == '' and int(row[1].strip('.jpg').strip('im_')) < 8401:
                    if row[8] == '1.0':
                        a_lst.append(row[1])
                    elif row[8] == '0.0':
                        n_lst.append(row[1])
                    cf(self.img_dir+row[1], path+self.tar_dir+row[1])
        print('succesfull {} files copied'.format(idx))
        test_dct['A'], test_dct['NA'] = a_lst, n_lst
        print(test_dct)
        dict_pickle(test_dct, 'demo_dict')

test_img()
