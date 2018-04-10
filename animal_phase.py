from __future__ import absolute_import, division, print_function
from session import session
# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, prefs
import sys, csv, time
import random as rd

class animal_phase(session):

    def __init__(self, ppn, img_set, RT=1.150, img_time = 0.1):
        super(animal_phase, self).__init__(ppn)
        self.ph_name = 'learning'
        self.img_set = img_set
        self.nm_lst = img_set[0]
        self.rwd_lst = img_set[1]
        self.a_lst = img_set[2]
        self.RT = RT
        self.img_time = img_time
        self.cur_reward = 0
        self.trial_lst = self.set_one()



    def set_one(self):

        trial_lst = []

        for i in range(self.trial_num):

            img_nm, img_rw, img_a = self.img_dir+self.nm_lst[i], self.rwd_lst[i], self.a_lst[i]
            img_show = visual.ImageStim(win=self.win, image=img_nm,pos=(0,0))
            img_show.size *= self.img_scl
            img_show.draw()
            self.win.flip()
            core.wait(0.1)
            stim_l = visual.TextStim(self.win, 'animal',
               color=col, pos=(-1,0))
            stim_r = visual.TextStim(self.win, 'no animal',
               color='white', pos=(1,0))
            stim_l.draw()
            stim_r.draw()
            trial_tmr = core.Clock()
            self.win.flip()
            keys = event.waitKeys(maxWait=self.img_time, keyList=["z", "slash"],timeStamped=trial_tmr)

            get_reward, col = 0, 'white'
            if keys[0] == None:
                key = [None, None]
                col = 'yellow'
            elif (keys[0] == 'slash' and img_a == 0) or (keys[0] == 'z' and img_a == 1):
                get_reward = img_rw
                col = 'green'
            else:
                col = 'red'
            self.cur_reward += get_reward

            stim1 = visual.TextStim(self.win, 'reward: '+str(get_reward),
               color=col, pos=(0,0))
            stim2 = visual.TextStim(self.win, 'total points: '+str(self.cur_reward),
               color='white', pos=(0,-0.2))

            stim1.draw()
            stim2.draw()
            self.win.flip()

            self.trial_lst.append([self.ttl_timer,self.ph_name, i, img_set[2][i],key_name[0],
                              key_name[1], img_one, None,reward, self.cur_reward])

            core.wait(0.5)

            self.get_cross()

        return trial_lst
