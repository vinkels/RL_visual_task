from ppn_analyse import stats as ppn
import pandas as pd
# from pandas.core import datetools
# import statsmodels.api as sm
from scipy import stats
import itertools as it
# import pyvttbl as pt
from collections import namedtuple
from rpy2.robjects import r, pandas2ri
pandas2ri.activate()

class statistics():

    def __init__(self):
        self.ppn = ppn()
        self.check_normal()

    def check_normal(self):

        groups = self.ppn.ctrl_set.groupby(['type','response'],as_index=False)['response_size'].apply(list)
        group_dict = {}
        for k, v in groups.items():
            print(v)
            statistic, pvalue = stats.shapiro(v)
            group_dict[k] = v
            print(k, statistic, pvalue)
        self.group_dict = group_dict
        print(groups)
        # groups.box_plot('rt', factors=['iv1', 'iv2'])
        print(groups.anova('rt', sub='response_size', wfactors=['type', 'response']))

statistics()
