from __future__ import absolute_import, division, print_function
from psychopy import core
from experiment.session import session
from experiment.img_sets import img_sets
import helpers as hp
import itertools, os



def main():
    hp.del_pyc()
    csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']

    ppn_input = 1
    # ppn_input = input("participant number (1-99): ")
    if ppn_input > -1:
        ppn = int(ppn_input)
    else:
        print("ppn not valid")
        sys.exit(0)

    reward_schemes = list(itertools.permutations([5,3,1]))
    print(reward_schemes)

    reward_input = 0
    # reward_input = input("reward scheme (0-5): ")
    if reward_input > -1:
        rwrd = int(reward_input)
    else:
        print("wrong input")
        sys.exit(0)

    a_sd = 'ar'
    # a_sd = input("give animal side ('ar'/'al'): ")
    if a_sd not in ['ar', 'al']:
        print('animal side not valid')
        sys.exit(0)

    if rwrd >= 0 and rwrd < 6:
        set = img_sets(csv_lst=csv_lst, reward_val=reward_schemes[rwrd])
        cur_ses = session(ppn=ppn, a_side = a_sd,rwrd_sc=rwrd, control_ph=set.contr_ph, learn_ph=set.learn_ph,
                         test_ph=set.test_ph, demo_ph=set.demo_ph)
        cur_ses.create_window()
        # print('dit gaat dus goed')
        core.quit()
    else:
        print("reward scheme does not exist")



main()
