import pandas as pd
import numpy as np
from ggplot import *
import matplotlib.pyplot as plt
# GGPLOT

df = pd.read_pickle('pickles/percent_df.pickle')
df_c = df.loc[df['phase'] == 'c']
fig, ax = plt.subplots(1, 1, figsize=(7.5, 5))
print(df)

# g = ggplot(df_c, aes(x='condition', fill='factor(response)', weight='percent',
#                                   y='percent')) + \
#         geom_bar() + \
#         ylab('Avg. Fare') + \
#         xlab('Class') + \
#         ggtitle('Fare by survival and class')
# g
#
g = ggplot(df_c, aes(x='condition', y='percent', color='response', weight='percent')) + \
        geom_bar(size=2.0) + \
        xlab('Date') + \
        ylab('Value') + \
        ggtitle('Random Timeseries')
print(g)
