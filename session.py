from __future__ import absolute_import, division, print_function
from psychopy import visual, core, event, prefs
import sys, csv, time, os,datetime, time
import random as rd


class session(object):
    def __init__(self, ppn, control_ph, learn_ph, test_ph, demo_ph,
                 img_time=1.250, cross_time = 1, a_time = 0.1):
        self.c_ph, self.l_ph, self.t_ph, self.demo_ph = control_ph, learn_ph, test_ph, demo_ph
        self.w_scr, self.h_scr = 1280, 800
        self.trial_num = 5
        self.img_dir = 'images/task/'
        self.out_dir = 'output/sessions/'
        self.img_scl = 0.8
        self.x_val = 0.5
        self.cross_scl = 0.01
        self.txt_scl = 0.2
        self.a_time = 0.1
        self.ppn = ppn
        self.date_time = time.strftime("%y%m%d%H%M")
        self.img_time = img_time
        self.cross_time = cross_time
        self.cur_reward = 0


    def create_window(self):


        self.ttl_timer = datetime.datetime.now()
        self.win = visual.Window(size=(self.w_scr, self.h_scr),screen=0,fullscr=False,
                                 monitor='testMonitor')
        self.fix_cros = visual.ShapeStim(win=self.win, vertices=((0, -self.cross_scl),
                                        (0, self.cross_scl), (0,0),(-self.cross_scl,0),
                                        (self.cross_scl, 0)),lineWidth=2,closeShape=False,
                                         lineColor="black")

        start_data = [str(self.ttl_timer), 'start begin']
        event.globalKeys.add('q', func=core.quit)
        # self.win.mouseVisible = False
        print('start demo')
        self.test_phase()
        print('start phase 1')
        con_data = [str(datetime.datetime.now() - self.ttl_timer), 'start control']
        con_log = self.set_two('control',self.c_ph)
        print('start phase 2')
        learn_data = [str(datetime.datetime.now() - self.ttl_timer), 'start learning']
        learn_log = self.set_one(self.l_ph)
        print('start phase 3')
        test_data = [str(datetime.datetime.now() - self.ttl_timer), 'start test']
        test_log = self.set_two('test',self.t_ph)
        self.show_instruct('exit.png')
        trial_log = self.create_csv([[start_data]+[con_data]+con_log+[learn_data]+learn_log
                                     +[test_data]+test_log])
        self.win.close()


    def test_phase(self):
        self.show_instruct('intro.png')
        self.show_instruct('demo.png')


        self.show_instruct('end_demo.png')
    #

    def show_instruct(self, file_path):
        in_txt = visual.ImageStim(win=self.win, image='images/instruct/'+file_path, pos=(0,0))
        in_txt.draw()
        self.win.flip()
        event.waitKeys()

    def set_two(self, phase, img_set):
        trial_lst = []

        for i in range(self.trial_num):
            ran_num = rd.randint(0, 1)
            if ran_num == 1:
                img_one = img_set[0][i]
                img_two = img_set[1][i]
            else:
                img_one = img_set[1][i]
                img_two = img_set[0][i]

            img_l = visual.ImageStim(win=self.win, image=self.img_dir+img_one,pos=(-self.x_val,0))
            img_r = visual.ImageStim(win=self.win, image=self.img_dir+img_two, pos=(self.x_val, 0))
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
            trial_lst.append([str(datetime.datetime.now() - self.ttl_timer),phase, i, img_set[2][i],
                              key_name[0], key_name[1], img_one, img_two,0, 0])
        return trial_lst

    def set_one(self, img_lst):

        trial_lst = []

        for i in range(self.trial_num):

            img_nm, img_rw, img_a = self.img_dir+img_lst[0][i], img_lst[1][i], img_lst[2][i]
            img_show = visual.ImageStim(win=self.win, image=img_nm,pos=(0,0))
            img_show.size *= self.img_scl
            img_show.draw()
            self.win.flip()
            core.wait(0.1)
            stim_l = visual.TextStim(self.win, 'animal',
               color='white', pos=(-0.6,-0.6))
            stim_r = visual.TextStim(self.win, 'no animal',
               color='white', pos=(0.6,-0.6))
            stim_l.draw()
            stim_r.draw()
            trial_tmr = core.Clock()
            self.win.flip()
            keys = event.waitKeys(maxWait=1.150, keyList=["z", "slash"],timeStamped=trial_tmr)

            get_reward, col = 0, 'white'
            try:
                key = keys[0]
                if (key[0] == 'slash' and img_a == 0) or (key[0][0] == 'z' and img_a == 1):
                    get_reward = img_rw
                    col = 'green'
                else:
                    col = 'red'
            except:
                key = [None, None]
                col = 'yellow'

            self.cur_reward += get_reward

            stim1 = visual.TextStim(self.win, 'reward: '+str(get_reward),
               color=col, pos=(0,0))
            stim2 = visual.TextStim(self.win, 'total points: '+str(self.cur_reward),
               color='white', pos=(0,-0.2))

            stim1.draw()
            stim2.draw()
            self.win.flip()

            trial_lst.append([str(datetime.datetime.now() - self.ttl_timer),'learning', i, img_lst[2][i],
                              key[0],key[1], img_nm, img_rw,get_reward, self.cur_reward])

            core.wait(0.5)

            self.get_cross()

        return trial_lst

    #
    def get_cross(self):

        self.fix_cros.draw()
        self.win.flip()
        core.wait(self.cross_time)
    #
    #
    def create_csv(self, log_lst):

        ppn_form = ('0'*(2-len(str(self.ppn))))+str(self.ppn)
        file_name = "PPN{}_{}.csv".format(ppn_form, self.date_time)
        with open(self.out_dir+file_name, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow(['time_stamp','phase','trial_nr','animal','key','RT',
                                 'img_l', 'img_r', 'reward', 'tot_reward'])


            for row in log_lst:
                csv_writer.writerows(row)

        return True

# window()
