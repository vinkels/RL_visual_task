import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

class ppn_analysis():

    def __init__(self):
        self.df = pd.read_pickle('pickles/ana_set.pickle')
        self.rt_lr = 0.050
        self.rt_ct = 0.150
        self.invalid_trials()
        self.adjust_percent()
        self.get_incorrect()
        self.plot_prefer()

        # self.data_fried()

    def invalid_trials(self, plot = True):
        '''Invalid trials based on reaction time < 150 ms and missed response
        if plot = True a boxplot for all conditions with excluded ppns is saved'''

        inval_trials = self.df.loc[(((self.df["condition"] != 'lr') &
                                     (self.df["RT"] < self.rt_ct)) |
                                    ((self.df["condition"] == 'lr') &
                                     (self.df["RT"] < self.rt_lr)))]

        self.valid_trials = self.df.loc[(((self.df["condition"] != 'lr') &
                                          (self.df["RT"] >= self.rt_ct)) |
                                         ((self.df["condition"] == 'lr') &
                                          (self.df["RT"] >= self.rt_lr)))]

        inval_trials.to_csv('output/invalid_RT_trials.csv',sep=',')

        self.trial_count = pd.DataFrame(self.valid_trials[['ppn','phase','response']].groupby(['ppn','phase'],as_index=False).count()).reset_index()
        ex_out = self.trial_count[np.abs(self.trial_count.response-self.trial_count.response.mean())
                                  >(3*self.trial_count.response.std())]
        self.exclus_ppn = list(ex_out['response'].unique())

        self.trial_count["out"] = self.trial_count['response'].isin(self.exclus_ppn)
        ex_out['percent'] = (ex_out['response'].astype(float))/3.0
        self.valid_trials = self.valid_trials[-self.valid_trials.ppn.isin(self.exclus_ppn)]

        ex_out.to_csv('output/excluded_invalid.csv', index=False)
        self.valid_trials.to_csv('output/clean_data.csv', index=False)

        self.trial_count['percent'] = (self.trial_count['response'].astype(float))/3.0

        if plot:
            sns.set_style("darkgrid")
            y_pos = [1,2,3]
            ph_ord = ['c','lr','t']
            sns.boxplot(x="phase", y="percent", order=ph_ord, data=self.trial_count, width=0.5)
            sns.stripplot(x="phase", y="percent", data=self.trial_count[self.trial_count['out'] == True],
                          color='red',order=ph_ord,marker='d',size=7)
            sns.stripplot(x="phase", y="percent", data=self.trial_count, color='red',alpha=0,order=ph_ord)
            plt.tight_layout()
            plt.savefig("output/plots/percent_valid.png", dpi=300)
            plt.close()


    def adjust_percent(self):
        ''' gets percentage for all phases, conditions adjusted to valid trials'''
        tot_lst = []
        count_lst = ['ppn','phase','condition','response','reward','animal']
        resp_count = self.valid_trials[count_lst].groupby(count_lst[:-1],as_index=False)\
                                                 .count().reset_index()
        sum_df = resp_count.groupby(['ppn','phase','condition'],as_index=False)\
                           .agg({'animal': 'sum'}).rename(columns = {'animal':'animal_sum'}).reset_index()

        for index, row in resp_count.iterrows():
            jup = int(sum_df['animal_sum'].loc[(sum_df['ppn'] == row['ppn']) &
                             (sum_df['phase'] == row['phase']) &
                             (sum_df['condition'] == row['condition'])])
            tot_lst.append(jup)
        resp_count['sum'] = tot_lst
        resp_count["percent"] = (resp_count["animal"] / resp_count["sum"]) * 100
        self.percent_df = resp_count.rename(columns = {'animal':'count'}).drop('index', axis=1)
        print(self.percent_df)
        self.percent_df.to_pickle('pickles/percent_df.pickle')

    def plot_prefer(self):
        ctrl_df = self.percent_df.loc[self.percent_df['phase'] == 'c']

        g = sns.factorplot(x="condition", y="percent",hue="response", data=ctrl_df,
                           size=4, kind="bar",order=['lm','lh','mh'],
                           sharex=False,hue_order=['l','m','h'],alpha=0.9)
        g.set(ylabel='% of condition trials')
        plt.savefig("output/plots/percent_pref_ctrl.png", dpi=300)
        plt.close()


    def get_incorrect(self,plot=True):
        cor_lr = self.percent_df.loc[(self.percent_df['phase'] == 'lr') &
                                     (self.percent_df['response'] != 0)]
        incor_lr = cor_lr[np.abs(cor_lr.percent-cor_lr.percent.mean())>(3*cor_lr.percent.std())]
        ppn_ex = list(incor_lr['ppn'].unique())
        # cor_lrn["out"] = self.trial_count['response'].isin(ppn_ex)

        if plot == True:
            sns.set_style("darkgrid")
            ax = sns.boxplot(x="condition", y="percent", order=['l','m','h'], data=cor_lr)
            # ax.set_title('Correct responses for learning phase')
            ax.set(xlabel='CE/SC classes', ylabel="% correct responses")
            plt.tight_layout()
            plt.savefig('output/plots/bxplt_incorrect.png',dpi=300)
            plt.close()


        self.percent_df = self.percent_df[-self.percent_df.ppn.isin(ppn_ex)]
        self.percent_df.to_csv('output/data_percent_clean.csv',index=False)



        # incor_lr = cor_lr[np.abs(cor_lr.response_size-cor_lr.response_size.mean())>(3*cor_lr.response_size.std())]

    def data_fried(self):
        # jup = self.percent_df.loc[self.percent_df['phase'] == 't']
        group = []
        for idx, row in self.percent_df.iterrows():
            group.append(row['condition']+str(row['response']))
        self.percent_df['group'] = group
        self.percent_df.to_csv('data_grouped.csv', index=False)

    # def learn_plot(self):




ppn_analysis()
