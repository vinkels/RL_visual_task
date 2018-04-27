import RL_visual_task.helpers as hp
import csv, os, sys, glob, itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class stats():

    def __init__(self):
        self.df = pd.read_pickle('pickles/ana_set.pickle')
        self.get_stats()

    def get_stats(self):

        ctrl_df = self.df.loc[self.df['condition'] == 'c']
        lrn_df = self.df.loc[self.df['condition'] == 'lr']
        tst_df = self.df.loc[self.df['condition'] == 't']
        ctrl_freq = ctrl_df[['ppn', 'type', 'response']].groupby(['ppn','type','response']).size().reset_index(name='freq')
        lrn_freq = lrn_df[['ppn', 'type', 'response']].groupby(['ppn','type','response']).size().reset_index(name='freq')
        tst_freq = tst_df[['ppn', 'type', 'response']].groupby(['ppn','type','response']).size().reset_index(name='freq')
