from __future__ import absolute_import, division, print_function
from psychopy import core, gui
from experiment.session import session
from experiment.img_sets import img_sets
import helpers as hp
import itertools, os, sys



def main():
    hp.del_pyc()
    csv_lst = ['HIGH_A', 'HIGH_NA','MED_A', 'MED_NA', 'LOW_A', 'LOW_NA']
    reward_schemes = list(itertools.permutations([5,3,1]))
    myDlg = gui.Dlg(title="JWP's experiment")
    myDlg.addText('Subject info')
    myDlg.addField('ppn nr.(0-99): ')
    myDlg.addField('reward scheme (0-5): ', choices=[0,1,2,3,4,5])
    myDlg.addField('animal l/r: ', choices=["left", "right"])
    ok_data = myDlg.show()
    if myDlg.OK:  # or if ok_data is not None
        if ok_data[2] is 'left':
            a_sd = 'al'
        else:
            a_sd = 'ar'

        try:
            ppn = int(ok_data[0])
        except:
            print("ppn not valid")
        rwrd = int(ok_data[1])
    else:
        print('user cancelled')
        sys.exit(0)

    set = img_sets(csv_lst=csv_lst, reward_val=reward_schemes[rwrd])
    cur_ses = session(ppn=ppn, a_side = a_sd,rwrd_sc=rwrd, control_ph=set.contr_ph, learn_ph=set.learn_ph,
                     test_ph=set.test_ph, demo_ph=set.demo_ph)
    cur_ses.create_window()
    core.quit()




main()
