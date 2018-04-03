from __future__ import absolute_import, division, print_function
from window import window
from img_set import img_set

def main():
    csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
    ppn_input = input("proefpersoon nummer: ")
    try:
        ppn = int(ppn_input)
    except ValueError:
        print("That's not an int!")
    img_files = img_set(csv_lst)
    cur_ses = window(ppn, img_files)
main()
