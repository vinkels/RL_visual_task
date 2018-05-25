from __future__ import absolute_import, division, print_function
from psychopy import visual, core, event, prefs
import sys, csv, time, os,datetime, time
import random as rd


class session(object):
    def __init__(self, ppn, a_side, rwrd_sc,control_ph, learn_ph, test_ph, demo_ph,
                 img_time=1.250, cross_time = 0.5, a_time = 0.1):
        self.c_ph, self.l_ph, self.t_ph, self.demo_ph = control_ph, learn_ph, test_ph, demo_ph
        self.w_scr, self.h_scr = 1280, 800
        self.a_side = a_side
        self.rwrd_sc = rwrd_sc
        self.trial_num = 300
        self.demo_dir = 'images/demo/'
        self.img_dir = 'images/task/'
        self.out_dir = 'output/ppn/'
        self.img_scl = 0.8
        self.x_val = 0.5
        self.cross_scl = 0.08
        self.txt_scl = 0.2
        self.a_time = 0.1
        self.ppn = ppn
        self.date_time = time.strftime("%y%m%d%H%M")
        self.img_time = img_time
        self.cross_time = cross_time
        self.cur_reward = 0
        self.trial_lst = []

    def test(self):
        self.ttl_timer = datetime.datetime.now()
        self.win = visual.Window(size=(self.w_scr, self.h_scr),fullscr=True,
                                 monitor='testMonitor')
        event.globalKeys.add('q', func=self.quit_q)
        self.win.mouseVisible = False
        self.fix_cros = visual.ShapeStim(win=self.win, vertices=((0, -self.cross_scl),
                                        (0, self.cross_scl), (0,0),(-self.cross_scl*(6/8),0),
                                        (self.cross_scl*(6/8), 0)),lineWidth=4,closeShape=False,
                                         lineColor="black")
        for i in range(10):
            timer_lst = []
            in_txt = visual.ImageStim(win=self.win, image='images/instruct/exit.png', pos=(0,0))
            in_txt.draw()
            self.win.flip()
            trial_tmr = core.Clock()
            keys = event.waitKeys(maxWait=3.0, keyList=["z", "slash"], timeStamped=trial_tmr)
            self.fix_cros.draw()
            self.win.flip()
            core.wait(0.5)
            print(keys)




    def create_window(self):


        self.ttl_timer = datetime.datetime.now()
        self.win = visual.Window(size=(self.w_scr, self.h_scr),fullscr=True,
                                 monitor='testMonitor')
        self.fix_cros = visual.ShapeStim(win=self.win, vertices=((0, -self.cross_scl),
                                        (0, self.cross_scl), (0,0),(-self.cross_scl*(6/8),0),
                                        (self.cross_scl*(6/8), 0)),lineWidth=4,closeShape=False,
                                         lineColor="black")

        start_data = [str(self.ttl_timer), 'start begin']
        event.globalKeys.add('q', func=self.quit_q)
        self.win.mouseVisible = False
        print('start demo')
        self.test_phase()
        print('start phase 1')
        self.trial_lst.append([str(datetime.datetime.now() - self.ttl_timer), 'start control'])
        con_log = self.set_two('control',self.c_ph, self.trial_num)
        self.show_instruct('end_one.png')
        print('start phase 2')
        self.trial_lst.append([str(datetime.datetime.now() - self.ttl_timer), 'start learning'])
        learn_log = self.set_one('learning',self.l_ph, self.trial_num)
        self.show_instruct('end_two.png')
        print('start phase 3')
        self.trial_lst.append([str(datetime.datetime.now() - self.ttl_timer), 'start test'])
        test_log = self.set_two('test',self.t_ph, self.trial_num)
        self.show_instruct('exit.png')
        # print(self.cur_reward)
        self.create_csv()
        self.win.close()


    def test_phase(self):
        demo_two = [self.demo_ph[0], self.demo_ph[1], self.demo_ph[2]]
        demo_one = [self.demo_ph[0], self.demo_ph[3],self.demo_ph[2]]
        self.show_instruct('demo.png')
        self.show_instruct('demo_two.png')
        self.set_two('demo_two', demo_two, 10)
        if self.a_side == 'al':
            dem_name = 'demo_second_al.png'
        else:
            dem_name = 'demo_second_ar.png'
        self.show_instruct(dem_name)
        self.set_one('demo_one', demo_one, 10)
        self.cur_reward = 0
        self.show_instruct('end_demo.png')
    #

    def show_instruct(self, file_path):
        in_txt = visual.ImageStim(win=self.win, image='images/instruct/'+file_path, pos=(0,0))
        in_txt.draw()
        self.win.flip()
        event.waitKeys()

    def set_two(self, phase, img_set, reps):

        if phase.startswith('demo'):
            im_dir = self.demo_dir
        else:
            im_dir = self.img_dir

        for i in range(reps):
            ran_num = rd.randint(0, 1)
            if ran_num == 1:
                img_one = img_set[0][i]
                img_two = img_set[1][i]
            else:
                img_one = img_set[1][i]
                img_two = img_set[0][i]


            img_l = visual.ImageStim(win=self.win, image=im_dir+img_one,pos=(-self.x_val,0))
            img_r = visual.ImageStim(win=self.win, image=im_dir+img_two, pos=(self.x_val, 0))
            img_l.size *= self.img_scl
            img_r.size *= self.img_scl
            img_l.draw()
            img_r.draw()
            self.win.flip()
            trial_tmr = core.Clock()
            keys = event.waitKeys(maxWait=self.img_time, keyList=["z", "slash"],timeStamped=trial_tmr)
            if keys == None:
                key_name = [None, None]
                warn_img = 'images/instruct/warning_two.png'
                warn_txt = visual.ImageStim(win=self.win, image=warn_img, pos=(0,0))
                warn_txt.draw()
                self.win.flip()
                core.wait(0.5)
            else:
                key_name = keys[0]
            self.get_cross()
            self.trial_lst.append([str(datetime.datetime.now() - self.ttl_timer),phase, i, img_set[2][i],
                              key_name[0], key_name[1], img_one, img_two,0, 0])

    def set_one(self, phase, img_lst, reps):
        '''Function creates second phase. Shows one image for 100ms and registers keys
            Takes phasename, list with image names and number of trials as ppn_input
            adds variables [key pressed, image name, RT, reward, total reward, etc.]
            to log list of participant session'''
        if phase.startswith('demo'):
            im_dir = self.demo_dir
        else:
            im_dir = self.img_dir

        for i in range(reps):

            img_nm, img_rw, img_a = im_dir+img_lst[0][i], img_lst[1][i], img_lst[2][i]
            img_show = visual.ImageStim(win=self.win, image=img_nm,pos=(0,0))
            img_show.size *= self.img_scl
            img_show.draw()
            self.win.flip()
            core.wait(self.a_time)

            x_col = 'white'
            self.fix_cros.lineColor = x_col
            self.fix_cros.draw()
            trial_tmr = core.Clock()
            self.win.flip()
            keys = event.waitKeys(maxWait=1.150, keyList=["z", "slash"],timeStamped=trial_tmr)
            get_reward, col = 0, 'white'
            if self.a_side == 'al':
                key_na, key_a = 'slash', 'z'
            else:
                key_na, key_a = 'z','slash'
            try:
                key = keys[0]
                if (key[0] == key_na and img_a == 0) or (key[0] == key_a and img_a == 1):
                    get_reward = img_rw
                    col = 'green'
                    fb_txt = 'Correct'
                else:
                    col = 'red'
                    fb_txt = 'Incorrect'
            except:
                key = [None, None]
                col = 'yellow'
                fb_txt = 'Incorrect'

            self.cur_reward += get_reward

            stim1 = visual.TextStim(self.win, str(get_reward)+' points',
               color=col, pos=(0,0))
            stim2 = visual.TextStim(self.win, fb_txt,
               color=col, pos=(0,0.3))

            stim1.draw()
            stim2.draw()
            self.win.flip()

            self.trial_lst.append([str(datetime.datetime.now() - self.ttl_timer),phase, i, img_lst[2][i],
                              key[0],key[1], img_nm, img_rw,get_reward, self.cur_reward])

            core.wait(1.0)

            self.get_cross()
            if i in {1, 99, 199, 299}:
                rwrd_stim = visual.TextStim(self.win, 'total points: '+str(self.cur_reward),
                   color='white', pos=(0,0))
                rwrd_stim.draw()
                self.win.flip()
                core.wait(1.0)

    #
    def get_cross(self):
        '''Draws and shows black fixation cross on screen for [cross_time] time'''

        x_col = 'black'
        self.fix_cros.lineColor = x_col
        self.fix_cros.draw()
        self.win.flip()
        core.wait(self.cross_time)
    #
    #
    def create_csv(self):
        '''Creates csv output file of session from session log list
            Files can be found in output/ppn folder'''

        ppn_form = ('0'*(2-len(str(self.ppn))))+str(self.ppn)
        file_name = "PPN{}_{}_{}_{}.csv".format(ppn_form, self.date_time, self.a_side,self.rwrd_sc)
        with open(self.out_dir+file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow(['time_stamp','phase','trial_nr','animal','key','RT',
                                 'img_l', 'img_r', 'reward', 'tot_reward'])

            csv_writer.writerows(self.trial_lst)

        return True

    def quit_q(self):
        '''saves current log to csv and quits session'''
        self.create_csv()
        core.quit()

# window()
