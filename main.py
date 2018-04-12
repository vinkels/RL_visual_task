from __future__ import absolute_import, division, print_function
from psychopy import core
from session import session
from img_sets import img_sets
import helpers as hp
import itertools, os



def main():
    csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']

    ppn_input = input("ppn: ")
    try:
        ppn = int(ppn_input)
    except:
        print("ppn not valid")

    reward_schemes = list(itertools.permutations([5,3,1]))
    print(reward_schemes)
    reward_input = input("reward scheme (0-5): ")

    try:
        rwrd = int(reward_input)
    except:
        print("wrong input")

    if rwrd >= 0 and rwrd < 6:
        set = img_sets(csv_lst=csv_lst, reward_val=reward_schemes[rwrd])
        cur_ses = session(ppn=ppn, control_ph=set.contr_ph, learn_ph=set.learn_ph,
                         test_ph=set.test_ph, demo_ph=set.demo_ph)
        cur_ses.create_window()
        # print('dit gaat dus goed')
        core.quit()
    else:
        print("reward scheme does not exist")

    hp.del_pyc()

main()
