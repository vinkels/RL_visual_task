from __future__ import absolute_import, division, print_function

# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, prefs
import sys, csv, time
import random as rd

class window(object):
    def __init__(self, ppn, control_ph, learn_ph, test_ph,
                 img_time=1.0, cross_time = 1.0):
        self.control_ph, self.learn_ph, self.test_ph = control_ph, learn_ph, test_ph
        self.w_scr, self.h_scr = 1280, 800
        self.trial_num = 5
        self.img_dir = 'images/'
        self.out_dir = 'output/sessions/'
        self.img_scl = 0.8
        self.x_val = 0.5
        self.cross_scl = 0.01
        self.ppn = ppn
        self.date_time = time.strftime("%y%m%d%H%M")
        self.img_time = img_time
        self.cross_time = cross_time
        self.win = visual.Window(size=(self.w_scr, self.h_scr),fullscr=True,
                                 monitor='testMonitor')
        self.fix_cros = visual.ShapeStim(win=self.win, vertices=((0, -self.cross_scl),
                                        (0, self.cross_scl), (0,0),(-self.cross_scl,0),
                                        (self.cross_scl, 0)),lineWidth=2,closeShape=False,
                                         lineColor="black")
        self.cur_reward = 0
        self.create_window()

    def create_window(self):

        ttl_timer = core.Clock()
        event.globalKeys.add('q', func=core.quit)
        con_log = self.set_two('control',self.control_ph[0], self.control_ph[1])
        learn_log = self.set_one('learning', self.learn_ph[0], self.learn_ph[1])
        test_log = self.set_two('test',self.test_ph[0], self.test_ph[1])
        self.show_end(ttl_timer)
        rial_log = self.create_csv(con_log + learn_log + test_log)

        self.win.close()
        core.quit()

    def set_two(self, phase, lst_one, lst_two):

        trial_lst = []

        for i in range(self.trial_num):
            ran_num = rd.randint(0, 1)
            # name_one, name_two = lst_one[rd.randint(0,len_one-1)], lst_two[rd.randint(0,len_two-1)]
            if ran_num == 1:
                img_one = lst_one[i]
                img_two = lst_two[i]
            else:
                img_one = lst_two[i]
                img_two = lst_one[i]

            key_pressed = self.show_pics(self.img_dir+img_one, self.img_dir+img_two)

            trial_lst.append([phase, i, key_pressed[0], key_pressed[1], img_one, img_two,
                             0, self.cur_reward])
        return trial_lst

    def set_one(self, phase, list_one, list_reward):

        trial_lst = []

        for i in range(self.trial_num):
            img_one = self.img_dir+list_one[i]
            key_pressed = self.show_animal(img_one, list_reward[i])
            print('key', key_pressed)
            trial_lst.append([phase, i, key_pressed[0], key_pressed[1], img_one, None,
                             0, self.cur_reward])
        return trial_lst

    def show_animal(self, img, reward):

        img_show = visual.ImageStim(win=self.win, image=img,pos=(0,0))
        img_show.size *= self.img_scl
        img_show.draw()
        trial_tmr = core.Clock()
        self.win.flip()
        keys = event.waitKeys(maxWait=self.img_time, keyList=["z", "slash"],timeStamped=trial_tmr)

        return self.get_score(keys, reward)

    def get_score(self, keys, reward):
        if keys is not None and keys[0][0] == 'slash':
            keys = keys[0]
            self.cur_reward += reward
            get_reward = reward
        else:
            if keys is None:
                keys = [None, None]
            else:
                keys = keys[0]
            get_reward = 0
        stim1 = visual.TextStim(self.win, 'reward: '+str(get_reward),
           color=(1, 1, 1), colorSpace='rgb', pos=(0,0))
        stim2 = visual.TextStim(self.win, 'total cents: '+str(self.cur_reward),
           color=(1, 1, 1), colorSpace='rgb', pos=(0,-0.1))


        stim1.draw()
        stim2.draw()
        self.win.flip()
        core.wait(self.cross_time)
        return keys
    # def reward_screen(self, keys, reward):
    #     if keys ==

    def get_cross(self, keys):
        self.fix_cros.draw()
        self.win.flip()
        core.wait(self.cross_time)
        if keys is not None:
            keys = keys[0]
        else:
            keys = [None, None]
        return keys

    def show_pics(self, img_one, img_two):

        img_one = visual.ImageStim(win=self.win, image=img_one,pos=(-self.x_val,0))
        img_two = visual.ImageStim(win=self.win, image=img_two, pos=(self.x_val, 0))
        img_one.size *= self.img_scl
        img_two.size *= self.img_scl
        img_one.draw()
        img_two.draw()
        self.win.flip()
        trial_tmr = core.Clock()
        keys = event.waitKeys(maxWait=self.img_time, keyList=["z", "slash"],timeStamped=trial_tmr)
        print(keys)
        return self.get_cross(keys)


    def show_end(self, ttl_timer):
        '''End slide takes window en begin time.'''
        print("kom ik hier")
        end_txt = visual.TextStim(win=self.win, text='Thanks for participation!\n press key to finish test',
                        color=(1, 1, 1), colorSpace='rgb')
        end_txt.draw()
        self.win.flip()
        event.waitKeys(maxWait=10.0,timeStamped=ttl_timer)

    def create_csv(self, log_lst):
        ppn_form = ('0'*(2-len(str(self.ppn))))+str(self.ppn)
        file_name = "PPN{}_{}.csv".format(ppn_form, self.date_time)
        with open(self.out_dir+file_name, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow(['phase','trial_nr','key','time', 'img_l', 'img_r', 'reward', 'tot_reward'])

            for row in log_lst:
                # print(row)
                csv_writer.writerow(row)

# window()
