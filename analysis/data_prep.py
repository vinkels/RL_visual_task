# import RL_visual_task.helpers as hp
import csv, os, sys, glob, itertools
import pandas as pd
sys.path.append("..")
import matplotlib.pyplot as plt


class data_prep():

    def __init__(self):
        self.data_dir = "../output/ppn/"
        self.rwrd_lst = list(itertools.permutations([5,3,1]))
        self.img_df = pd.read_pickle('../pickles/BG_data.pickle')
        self.csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
        self.get_data()
        # self.get_reward()


    def get_data(self):

        header = ['ppn', 'trial_nr', 'phase','animal','reward','condition','response','RT','lr']
        df_dict = {key:[] for key in header}

        for file_name in glob.glob(self.data_dir+'*.csv'):
            ppn_lst = file_name.replace('.csv', '').replace(self.data_dir, '').split('_')
            ppn, rwrd = int(ppn_lst[0][3:5]), self.rwrd_lst[int(ppn_lst[3])]
            rwrd_dict = {'l':rwrd[0],'m':rwrd[1],'h':rwrd[2],rwrd[0]:'l',rwrd[1]:'m',rwrd[2]:'h','n':0}
            print('ppn',ppn)
            with open(file_name, 'r') as csvfile:
                csv_rd = csv.reader(csvfile, delimiter=',')

                for row in csv_rd:
                    try:
                        trial_nr = int(row[2])
                    except:
                        continue

                    if row[1] == 'learning':
                        con = 'lr'
                        rwrd_val = int(row[7])
                        type = rwrd_dict[rwrd_val]
                        side_key = self.get_balance(ppn,row[4],con)
                        if not row[4]:
                            resp = 'n'
                        else:
                            resp = int(row[8])

                    elif row[1] in ['control', 'test']:
                        con = row[1][0]
                        type, resp = self.get_condi(row)
                        rwrd_val = rwrd_dict[resp]
                        side_key = self.get_balance(ppn,row[4],con)
                    else:
                        continue

                    if not row[5]:
                        rt = 0.0
                    else:
                        rt = float(row[5])

                    side_key = self.get_balance(ppn,row[4],con)

                    tmp_lst = [ppn,trial_nr,con,int(row[3]),rwrd_val, type, resp, rt, side_key]
                    for i, val in enumerate(header):
                        df_dict[val].append(tmp_lst[i])

        self.df = pd.DataFrame(columns=header,data=df_dict)
        self.df.to_pickle('pickles/ana_set.pickle')
        self.df.to_csv('output/ana_set.csv', sep=',',index=False)
        print('done!')


    def get_balance(self, ppn, key, condi):
        if key == 'slash':
            return 'r'
        elif key == 'z':
            return 'l'
        else:
            return 'n'


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

data_prep()
