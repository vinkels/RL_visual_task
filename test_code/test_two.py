from __future__ import absolute_import, division, print_function
import pandas as pd
import numpy as np
import csv, os

df = pd.read_csv('../input/BG_data2.csv')

NA = []
A = []

for index, row in df.iterrows():
    if row['animal'] == 0:
        NA.append(index+1)
    elif row['animal'] == 1:
        A.append(index+1)



def create_csv(file, name):
    file_name = 'all_{}'.format(name)
    with open(file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        # csv_writer.writerow(['phase','trial_nr','key','time', 'img_l', 'img_r'])

        for line in file:
            print(line)
            csv_writer.writerow([line])

    csvfile.close()

create_csv(NA, 'NA')
create_csv(A, 'A')
