import RL_visual_task.helpers as hp
import csv, os, sys, glob, itertools
import pandas as pd
sys.path.append("..")
import matplotlib.pyplot as plt


class data_prep():

    def __init__(self, csv_lst):
        self.data_dir = "output/ppn/"
        self.rwrd_lst = list(itertools.permutations([5,3,1]))
        self.img_df = pd.read_pickle('pickles/BG_data.pickle')
        self.csv_lst = csv_lst
        self.get_data()


    def get_data(self):

        header = ['ppn', 'condition','rwd_lmh', 'trial_nr', 'animal', 'type','response','RT']
        df_dict = {key:[] for key in header}

        for file_name in glob.glob(self.data_dir+'*.csv'):
            ppn_lst = file_name.replace('.csv', '').replace(self.data_dir, '').split('_')
            ppn, rwrd = ppn_lst[0][3:5], self.rwrd_lst[int(ppn_lst[3])]
            rwrd_dict = {rwrd[0]:'l',rwrd[1]:'m',rwrd[2]:'h'}
            with open(file_name, 'r') as csvfile:
                csv_rd = csv.reader(csvfile, delimiter=',')

                for row in csv_rd:
                    try:
                        trial_nr = int(row[2])
                    except:
                        continue
                    if row[1] == 'control':
                        con = 'c'
                        type, resp = self.get_condi(row)
                    elif row[1] == 'learning':
                        con = 'lr'
                        trial_nr += 2000
                        resp = 'n'
                        type = rwrd_dict[int(row[7])]
                        if row[4]:
                            resp = int(row[8])


                    elif row[1] == 'test':
                        con = 't'
                        trial_nr += 3000
                        type, resp = self.get_condi(row)
                    else:
                        continue
                    if not row[5]:
                        rt = None
                    else:
                        rt = float(row[5])

                    tmp_lst = [ppn,con, rwrd,trial_nr,int(row[3]), type, resp, rt]
                    for i, val in enumerate(header):
                        df_dict[val].append(tmp_lst[i])

        self.df = pd.DataFrame(columns=header,data=df_dict)
        self.df.to_pickle('pickles/ana_set.pickle')
        self.df.to_csv('test.csv', sep=',',index=False)

    def get_condi(self, row):

        condi_l = self.img_df.loc[self.img_df['filename'] == row[6]]['condition'].values[0].split('_')[0]
        condi_r = self.img_df.loc[self.img_df['filename'] == row[7]]['condition'].values[0].split('_')[0]

        if (condi_l == 'LOW' or condi_l == 'MED') and (condi_r == 'LOW' or condi_r == 'MED'):
            condi = 'lm'
        elif (condi_l == 'LOW' or condi_l == 'HIGH') and (condi_r == 'LOW' or condi_r == 'HIGH'):
            condi = 'lh'
        elif (condi_l == 'MED' or condi_l == 'HIGH') and (condi_r == 'MED' or condi_r == 'HIGH'):
            condi = 'mh'

        if row[4] == 'slash':
            resp = condi_r[0].lower()
        elif row[4] == 'z':
            resp = condi_l[0].lower()
        else:
            resp = 'n'

        return condi, resp
