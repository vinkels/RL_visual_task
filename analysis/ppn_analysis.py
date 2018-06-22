import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys, math

class ppn_analysis():

    def __init__(self):
        self.df = pd.read_pickle('pickles/ana_set.pickle')
        self.rt_lr = 0.050
        self.rt_ct = 0.150
        self.col_cesc = ['#f21d2c','#67bc58','#3c559f']
        self.lg_name = ['low', 'medium', 'high']
        self.invalid_trials()
        self.adjust_percent()
        # self.plot_prefer()
        self.get_incorrect()
        self.data_fried()
        self.get_summary()
        self.get_ct()

        self.learn_plot()
        # self.learn_bars()
        # # self.plot_prefer()
        # self.test_reward()

        #

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
        print('mean',self.trial_count.response.mean(), 'sd', self.trial_count.response.std())

        self.trial_count['per'] =  self.trial_count['response']/3.0
        print(self.trial_count)
        print('mean',self.trial_count.per.mean(), 'sd', self.trial_count.per.std())

        ex_out = self.trial_count[np.abs(self.trial_count.per-self.trial_count.per.mean())
                                  >(3*self.trial_count.per.std())]
        self.exclus_trial = list(ex_out['index'].unique())
        self.exclus_ppn = list(ex_out['ppn'].unique())
        self.trial_count["out"] = self.trial_count['index'].isin(self.exclus_trial)
        ex_out['percent'] = (ex_out['response'].astype(float))/3.0
        self.valid_trials = self.valid_trials[-self.valid_trials.ppn.isin(self.exclus_ppn)]
        ex_out.to_csv('output/excluded_invalid.csv', index=False)
        self.trial_count['percent'] = (self.trial_count['response'].astype(float))/3.0
        self.valid_trials.to_csv('output/clean_data.csv', index=False)

        if plot:
            sns.set_style("darkgrid")
            y_pos = [1,2,3]
            ph_ord = ['c','lr','t']
            sns.boxplot(x="phase", y="percent", order=ph_ord, data=self.trial_count, width=0.5, palette='Set3')
            sns.stripplot(x="phase", y="percent", data=self.trial_count[self.trial_count['out'] == True],
                          color='red',order=ph_ord,marker='d',size=7)
            ax = sns.stripplot(x="phase", y="percent", data=self.trial_count, color='red',alpha=0,order=ph_ord)
            # ax.set_title('Valid trials for control, learning and test phase')
            ax.set_xticklabels(['Control','Learning','Test'],fontsize=20)
            ax.set_xlabel('Experimental phases', fontsize=20)
            ax.set_ylabel("% valid trials",fontsize=20)
            ax.tick_params(labelsize=18)
            plt.tight_layout()
            plt.savefig("output/plots/percent_valid2.png", dpi=300)
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
        g.set_xticklabels(['LowMed','LowHigh','MedHigh'],fontsize=20)
        g.set_xlabel('CE/SC class pairs', fontsize=20)
        g.set_ylabel("'% trials'",fontsize=20)
        g.tick_params(labelsize=18)
        g.legend(lg_name)
        plt.tight_layout()
        plt.savefig("output/plots/percent_pref_ctrl2.png", dpi=300)
        plt.close()


    def get_incorrect(self,plot=True):
        cor_lr = self.percent_df.loc[(self.percent_df['phase'] == 'lr') &
                                     (self.percent_df['response'] != 0)]
        incor_lr = cor_lr[np.abs(cor_lr.percent-cor_lr.percent.mean())>(3*cor_lr.percent.std())]
        count_ex = list(incor_lr['count'].unique())
        cor_lr["out"] = cor_lr['count'].isin(count_ex)
        ppn_ex = list(incor_lr['ppn'].unique())
        lr_ord = ['l','m','h']

        if plot == True:
            sns.set_style("darkgrid")
            ax = sns.boxplot(x="condition", y="percent", order=lr_ord, data=cor_lr,
                             palette = self.col_cesc)
            sns.stripplot(x="condition", y="percent", data=cor_lr[cor_lr["out"] == True],
                          color='red',order=lr_ord,marker='d',size=7)
            ax = sns.stripplot(x="condition", y="percent", data=cor_lr, color='white',alpha=0,order=lr_ord)
            # ax.set_title('Correct responses for learning phase')
            ax.set_ylabel("% correct responses",fontsize=20)
            ax.set_xlabel('CE/SC class pairs', fontsize=20)
            ax.set_xticklabels(['low','medium','high'],fontsize=20)
            ax.tick_params(labelsize=18)
            plt.tight_layout()
            plt.savefig('output/plots/bxplt_incorrect.png',dpi=300)
            plt.close()

        self.percent_df = self.percent_df[-self.percent_df.ppn.isin(ppn_ex)]
        self.percent_df = self.percent_df.loc[self.percent_df['response'] != 0]
        self.percent_df.to_pickle('pickles/clean_df2.pickle')
        self.percent_df.to_csv('output/data_percent_clean.csv',index=False)

    def get_summary(self):
        se_lst = []
        se_after = []
        mean_lst = []
        mean_after = []
        for i, row in self.percent_df.iterrows():
            serie = self.percent_df.loc[(self.percent_df['group'] == row['group']) &
                            (self.percent_df['response'] == row['response'])]
            serie_af = self.percent_df.loc[(self.percent_df['group'] == row['group']) &
                            (self.percent_df['response'] == row['response']) &
                            (self.percent_df['reward'] == row['reward'])]

            se_lst.append(serie['percent'].std()/math.sqrt(len(serie['percent'])))
            se_after.append(serie_af['percent'].std()/math.sqrt(len(serie_af['percent'])))
            mean_lst.append(serie['percent'].mean())
            mean_after.append(serie_af['percent'].mean())
        self.percent_df['se'] = se_lst
        self.percent_df['se_af'] = se_after
        self.percent_df['mean'] = mean_lst
        self.percent_df['mean_af'] = mean_after
        print(self.percent_df)
        self.percent_df.to_csv('output/data_percent_clean.csv',index=False)



    def data_fried(self):
        group = []
        for idx, row in self.percent_df.iterrows():
            group.append(row['condition']+str(row['response']))
        self.percent_df['group'] = group
        self.percent_df.to_csv('data_grouped.csv', index=False)

    def learn_plot(self):
        sns.set_style("darkgrid")
        df_set = self.percent_df.loc[(self.percent_df['phase'] == 'lr') &
                                     (self.percent_df['response'] != 0)]
        ax = sns.pointplot(x='reward', y="percent", hue="condition", data=df_set,
                           dodge=True, yerr='sem',errwidth=0.9,capsize=0.1,order=[1,3,5],
                           hue_order=['l','m','h'],palette = self.col_cesc)
        ax.set_xlabel('reward value', fontsize=20)
        ax.set_ylabel('% correct trials', fontsize=20)
        ax.set_xticklabels([1, 3, 5], fontsize=20)
        ax.tick_params(labelsize=18)
        # ax.legend(, color=self.col_cesc)
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles, self.lg_name, title='CE/SC classes')
        plt.setp(ax.get_legend().get_texts(), fontsize='18') # for legend text
        plt.setp(ax.get_legend().get_title(), fontsize='20') # for legend title
        plt.tight_layout()
        # plt.show()
        plt.savefig('output/plots/lrn_inter.png',dpi=300)
        plt.close()

    def learn_bars(self):
        df_set = self.percent_df.loc[(self.percent_df['phase'] == 'lr') &
                                     (self.percent_df['response'] != 0)]
        g = sns.factorplot(x="condition", y="percent",hue="reward", data=df_set,
                           size=4, kind="bar",order=['l','m','h'],
                           hue_order=[1,3,5], palette = self.col_cesc)
        g.set(ylabel='% correct trials',ylim=(80,100))
        plt.savefig("output/plots/lrn_bar_condi.png", dpi=300)
        plt.close()
        ax = sns.factorplot(x="reward", y="percent",hue="condition", data=df_set,
                           size=4, kind="bar",order=[1,3,5],
                           hue_order=['l','m','h'])
        ax.set(ylabel='% correct trials',ylim=(80,100))
        ax.legend(lg_name)
        plt.savefig("output/plots/lrn_bar_reward.png", dpi=300)
        plt.close()

    def test_reward(self):
        df_tst = self.percent_df.loc[(self.percent_df['phase'] == 't')]
        ax = sns.barplot(x="reward", y="percent", data=df_tst)
        ax.set(ylabel='% preference')
        plt.savefig("output/plots/tst_bar_reward.png", dpi=300)
        plt.close()

    def get_ct(self):
        df = pd.read_pickle('pickles/clean_df2.pickle')
        ct_df = df.loc[(df['reward'] != 3) & (df['phase'] != 'lr')]
        print(ct_df)
        ct_c = ct_df.loc[ct_df.groupby(['ppn','phase','condition'])['response'].transform('count')>=2]
        ct_jup = ct_c.loc[ct_c['reward'] == 5]
        ct_jup.to_csv('output/clean_ctrl_tst.csv')
        ct_ctrl = ct_jup.loc[(ct_jup['phase'] == 'c')]
        ct_tst = ct_jup.loc[(ct_jup['phase'] == 't')]
        dif_lst = []
        for index, row in ct_ctrl.iterrows():
            tst = float(ct_tst['percent'].loc[ct_tst['ppn'] == row['ppn']])
            dif_lst.append(tst-float(row['percent']))
        ct_ctrl['dif'] = dif_lst
        ct_tst['dif'] = dif_lst
        pd.concat([ct_ctrl, ct_tst]).to_csv('output/dif_ct.csv')
        print(len(list(self.percent_df.ppn.unique())))

        # print(ct_jup)


if __name__ == '__main__':
    ppn_analysis()
