def get_imglst(self):
    condi_dict = {}
    for name in self.csv_lst:
        temp_part = self.df.loc[self.df['condi'] == name]
        condi_dict[name] = list(temp_part['filename'])
    return condi_dict

def get_type(self):
    BG_table = pd.read_csv('input/BG_data2.csv')
    type_lst = [None]*len(BG_table)
    csv_dir = 'input/'
    error_lst = []
    count = 0
    for csv_name in self.csv_lst:
        with open(csv_dir+csv_name+'.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if type_lst[int(row[0])-1] is None:
                    type_lst[int(row[0])-1] = csv_name
                else:
                    error_lst.append(int(row[0])+1)
                    type_lst[int(row[0])-1] = None

    BG_table['condi'] = pd.Series(type_lst, index=BG_table.index)
    # print(error_lst, len(error_lst))
    return BG_table, error_lst
