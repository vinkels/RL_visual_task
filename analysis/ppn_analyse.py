# import RL_visual_task.helpers as hp
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class stats():

    def __init__(self):
        self.df = pd.read_pickle('pickles/ana_set.pickle')
        self.rt_lr = 0.050
        self.rt_ct = 0.150
        self.clean_trials()


    def clean_trials(self):
        self.invalid_trials(True)
        self.lrn_raw = self.get_stats('lr')
        self.cor_outliers()
        self.ctrl_set = self.get_stats('c')
        self.tst_set = self.get_stats('t')
        self.plot_prefer()
        # self.interact_plot()
        self.valid_trials.to_csv('output/clean_data.csv',sep=',',index=False)
        self.ctrl_set.to_csv('output/ctrl_set.csv',sep=',',index=False)
        self.tst_set.to_csv('output/tst_set.csv',sep=',',index=False)

    def invalid_trials(self, plot=False):

        inval_trials = self.df.loc[(((self.df["condition"] != 'lr') & (self.df["RT"] < self.rt_ct)) |
                                  ((self.df["condition"] == 'lr') & (self.df["RT"] < self.rt_lr)))]
        self.valid_trials = self.df.loc[(((self.df["condition"] != 'lr') & (self.df["RT"] >= self.rt_ct)) |
                                   ((self.df["condition"] == 'lr') & (self.df["RT"] >= self.rt_lr)))]

        inval_trials.to_csv('output/invalid_RT_trials.csv',sep=',')

        jup = self.valid_trials.groupby(['ppn','condition'],as_index=False).count()
        jup['percent'] = (jup['lr'] / 300)*100
        print(jup)
        jup2 = jup[np.abs(jup.percent-jup.percent.mean())>(3*jup.percent.std())]
        print('mean', jup.percent.mean(),'sd', jup.percent.std())
        exclus_ppn = list(jup2['ppn'].unique())
        self.valid_trials = self.valid_trials[-self.valid_trials.ppn.isin(exclus_ppn)]
        print(exclus_ppn)
        if plot == True:
            ax = sns.boxplot(x="condition", y="percent", order=['c','lr','t'], data=jup)
            ax.set_title('Valid RT (>150ms) trials for all experimental phases')
            ax.set(xlabel='Experimental phase', ylabel='% valid trials')
            plt.savefig('output/plots/RT_bxplt.png',dpi=300)
            plt.close()
        # print(jup2)
        return exclus_ppn

    def cor_outliers(self, plot=False):
        '''Extracts ppn's considered outliers (3*sd) based on number correct in learning phase'''
        # print(self.lrn_set)
        temp_df = (self.lrn_raw[['ppn', 'type', 'response','response_size']]
                   .loc[(self.lrn_raw['response'] != 0)])

        clean_df = temp_df.groupby(['ppn','type'],as_index=False).sum()
        # print(clean_df)

        if plot == True:
            ax = sns.boxplot(x="type", y="response_size", order=['l','m','h'], data=clean_df)
            ax.set_title('Correct responses for learning phase')
            ax.set(xlabel='CE/SC classes', ylabel="% responses")
            plt.savefig('output/plots/bxplt_incorrect.png',dpi=300)
            plt.close()
        # #keep only the ones that are within +3 to -3 standard deviations in the column 'response_size'.
        lrn_clean = clean_df[np.abs(clean_df.response_size-clean_df.response_size.mean())<=(3*clean_df.response_size.std())]
        incor_lr = clean_df[np.abs(clean_df.response_size-clean_df.response_size.mean())>(3*clean_df.response_size.std())]
        incor_lr.to_csv('output/incorrect_learning_trials.csv',sep=',')
        print('mean', clean_df.response_size.mean(),'sd', clean_df.response_size.std())
        exclus_ppn = list(incor_lr['ppn'].unique())
        print(exclus_ppn)
        self.valid_trials = self.valid_trials[-self.valid_trials.ppn.isin(exclus_ppn)]
        self.lrn_set = clean_df[-clean_df.ppn.isin(exclus_ppn)]
        self.lrn_set.to_csv('output/lr_set.csv',sep=',',index=False)


    def get_stats(self, condi):

        ctrl_df = self.valid_trials.loc[self.valid_trials['condition'] == condi]
        f = {'response':['size'],'RT':['mean','std']}
        nm_lst = ['ppn', 'type','response','n','rt_mean','rt_sd']
        ctrl_freq = ctrl_df[['ppn', 'type', 'response','RT']].groupby(['ppn','type','response']).agg(f).reset_index()

        ctrl_freq.columns = ['_'.join(col).strip() if col[1] else col[0] for col in ctrl_freq.columns.values]
        return ctrl_freq

    def plot_prefer(self,plot=False):
        ctrl_count = self.ctrl_set.groupby(['type','response','ppn','response_size'],as_index=False).count()
        if plot == True:
            g = sns.factorplot(x="type", y="response_size", hue="response", data=ctrl_count,size=6, kind="bar",dodge=0.2,order=['lm','lh','mh'],hue_order=['l','m','h'])
            # # ax = sns.swarmplot(x="type", y="response_size", hue="response", data=ctrl_count)
            g.ax.set_title('average CE/SC class preference for complexity sets')
            g.ax.set(xlabel='m/l/h CE/SC subsets', ylabel='% responses per subset')
            plt.savefig('output/plots/barplot_preference.png',dpi=300)
            plt.close()

    def interact_plot(self):
        sns.set_style("darkgrid")
        # print(self.lrn_set)
        ax = sns.pointplot(x="response", y="response_size", hue="type", data=self.lrn_set, dodge=True, yerr='sem',errwidth=0.9,capsize=0.1,order=[1,3,5],hue_order=['l','m','h'])
        ax.set_title('No significant effects of image complexity \n and reward on percentage correct')
        ax.set(xlabel='reward value (points)', ylabel='% responses per subset')
        plt.ylim(80, 100)
        leg_handles = ax.get_legend_handles_labels()[0]
        ax.legend(leg_handles,['low','medium','high'],loc='lower right',title='CE/SC classes')
        plt.savefig('output/plots/learn_effects.png',dpi=300)
        # plt.show()
stats()
