import csv,os,sys, glob, itertools
import pandas as pd
sys.path.append("..")
import RL_visual_task.helpers as hp

class analysis():

    def __init__(self):
        self.data_dir = "../output/ppn/"
        self.rwrd_lst = list(itertools.permutations([5,3,1]))
        self.img_df = pd.read_pickle('../pickles/BG_table')
        self.get_data()
        self.csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']

    def get_data(self):

        head_two = ['ppn', 'lA_lm', 'mA_lm', 'lA_lh', 'hA_lh', 'mA_mh', 'hA_mh','lNA_lm', 'mNA_lm', 'lNA_lh', 'hNA_lh', 'mNA_mh', 'hNA_mh']

        head_one = ['ppn', 'a_side', 'rwd_l','rwd_m','rwd_h']

        self.df_control = pd.DataFrame(columns=head_two)
        self.df_learn = pd.DataFrame(columns=head_one)
        self.df_test = pd.DataFrame(columns=head_two)

        for file_name in glob.glob(self.data_dir+'*.csv'):
            ppn_lst = file_name.replace('.csv', '').replace(self.data_dir, '')\
                               .split('_')
            print(ppn_lst)
            ppn, rwrd = int(ppn_lst[0][3:5]), self.rwrd_lst[int(ppn_lst[3])]
            temp_ctrl = [ppn]
            temp_lrn = [ppn, ppn_lst[2], rwrd[0], rwrd[1], rwrd[2]]
            temp_tst = [ppn]
            # slash is right, z is left
            cor_dict = dict.fromkeys(self.csv_lst, 0)
            scr_lst = ['LOW','MED', 'HIGH']
            with open(file_name, 'r') as csvfile:
                csv_rd = csv.reader(csvfile, delimiter=',')
                for row in csv_rd:
                    key = row[4]
                    # if row[4] == 'slash':
                    if row[1] == 'control':
                        condi_l = self.img_df.loc[self.img_df['filename'] == row[6], 'condition'].split('_')
                        condi_r = self.img_df.loc[self.img_df['filename'] == row[7], 'condition'].split('_')
                        if row[4] == 'slash':
                            +condi_r[1]
                    elif row[1] == 'learning':
                        if row[7] > 0:
                            condi = self.img_df.loc[self.img_df['filename'] == row[6], 'condition']
                            cor_dict[condi] += 1
                    elif row[1] == 'test':

    def get_combo(img_one, img_two, key):

        if key == 'slash':

analysis()
