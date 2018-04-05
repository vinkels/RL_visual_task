import csv, os
list_lna = os.listdir('images/LOW_NA')
list_la = os.listdir('images/LOW_A')
list_mna = os.listdir('images/MED_NA')
list_ma = os.listdir('images/MED_A')
list_hna = os.listdir('images/HIGH_NA')
list_ha = os.listdir('images/HIGH_A')

with open('input/type_csv/LOW_NA.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\n')
    csv_writer.writerow(list_lna)
    csvfile.close()
with open('input/type_csv/LOW_A.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\n')
    csv_writer.writerow(list_la)
    csvfile.close()
with open('input/type_csv/MED_NA.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\n')
    csv_writer.writerow(list_mna)
    csvfile.close()
with open('input/type_csv/MED_A.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\n')
    csv_writer.writerow(list_ma)
    csvfile.close()
with open('input/type_csv/HIGH_NA.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\n')
    csv_writer.writerow(list_hna)
    csvfile.close()
with open('input/type_csv/HIGH_A.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\n')
    csv_writer.writerow(list_ha)
    csvfile.close()
