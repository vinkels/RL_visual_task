# import RL_visual_task.helpers as hp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

class stats():

    def __init__(self):
        self.df = pd.read_pickle('pickles/ana_set.pickle')
        self.ctrl_set = self.get_stats('c')
        self.lrn_set = self.get_stats('lr')
        self.tst_set = self.get_stats('t')
        # self.get_plotsum()
        # self.get_summ()

    def get_stats(self, condi):

        ctrl_df = self.df.loc[self.df['condition'] == condi]
        f = {'response':['size'],'RT':['mean','std']}
        nm_lst = ['ppn', 'type','response','n','rt_mean','rt_sd']
        ctrl_freq = ctrl_df[['ppn', 'type', 'response','RT']].groupby(['ppn','type','response']).agg(f).reset_index()

        ctrl_freq.columns = ['_'.join(col).strip() if col[1] else col[0] for col in ctrl_freq.columns.values]

        return ctrl_freq

    def get_plot(self):
        plot_dat = {}
        ppn_dict = {}
        ppn_lst = list(self.ctrl_set.ppn.unique())
        self.df = pd.DataFrame(self.ctrl_set[['ppn','response', 'response_size']]
                               .groupby(['ppn','response'],as_index=False).sum())
        tab = self.df.pivot(columns='response',values='response_size',index='ppn').reset_index()
        print(tab)
        tab.plot(kind='bar',x='ppn',stacked=False)
        plt.show()
        # parallel_coordinates() https://pandas.pydata.org/pandas-docs/stable/visualization.html

    def get_plotsum(self):
        ppn_lst = list(self.ctrl_set.ppn.unique())
        type_lst = list(self.ctrl_set.response.unique())
        df = pd.DataFrame(self.ctrl_set[['ppn','response', 'response_size']]
                          .groupby(['ppn','response'],as_index=False).sum())
        tab = df.groupby(['response']).agg(['mean', 'sem'])
        print(tab.columns)
        tab.columns = tab.columns
        # print(tab.columns.values)
        # tab.columns = [ if col[1] else col[0] for col in tab.columns.values]
        # print(pd.DataFrame(tab))
        # tab = pd.pivot_table(self.df,columns='response',values='response_size',index='ppn',aggfunc='mean').reset_index()
        # print(tab)
        # tab.plot(kind='bar',x='ppn',stacked=False)
        # plt.show()

    def get_summ(self):

        type_lst = list(self.ctrl_set.response.unique())
        jup = pd.DataFrame(self.ctrl_set[['ppn','type','response', 'response_size']]
                           .groupby(['type','response'],as_index=False).mean())
        print(jup)
        tab = jup.pivot(columns='response',values='response_size',index='type').reset_index()
        print(tab)
        tab.plot(kind='bar', x='type',stacked=False)
        plt.show()


        # type_lst = list(self.ctrl_set.response.unique())
        # jup = self.ctrl_set[['ppn','type','response', 'response_size']].groupby(['type','response'],as_index=False).agg(['mean','std']).reset_index()
        # jup.columns = [col[1] if col[1] else col[0] for col in jup.columns.values]
        # jup = pd.DataFrame(jup.reset_index())
        #
        # jup.plot(kind='bar', x='type',y='mean')
        # plt.show()
        # tab = jup.pivot(columns='response',values='response_size',index='type').reset_index()
        # tab.plot(kind='bar', x='type', stacked=False)
        # plt.show()
        # print(jup)
stats()
