from __future__ import absolute_import, division, print_function

# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, prefs
import sys, csv, time
import random as rd

class window(object):
    def __init__(self, ppn, control_ph, learn_ph, test_ph,
                 img_time=1.0, cross_time = 0.5):
        self.control_ph, self.learn_ph, self.test_ph = control_ph, learn_ph, test_ph
        self.w_scr, self.h_scr = 1280, 800
        self.trial_num = 5
        self.img_dir = 'images/'
        self.out_dir = 'output/sessions/'
        self.img_scl = 0.8
        self.x_val = 0.5
        self.cross_scl = 0.01
        self.txt_scl = 0.2
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
        self.cur_reward = 0.00

    def create_window(self):

        self.intro_window()
        self.ttl_timer = core.Clock()
        self.test_phase()
        event.globalKeys.add('q', func=core.quit)
        con_log = self.set_two('control',self.control_ph[0], self.control_ph[1])
        learn_log = self.set_one('learning', self.learn_ph[0], self.learn_ph[1])
        test_log = self.set_two('test',self.test_ph[0], self.test_ph[1])
        self.show_end()
        self.win.close()

        trial_log = self.create_csv(con_log + learn_log + test_log)
        core.quit()
            print('komt ook hier')



    def intro_window(self):
        # # end_txt = visual.TextStim(win=self.win, text='This task exists of 3 parts in which \
        #                           you have to press either the [z] or [/] key. \n Press key'+
        #                           ' to start demo', color=(1, 1, 1), colorSpace='rgb')

        intro_txt = visual.ImageStim(win=self.win, image='images/instruct/text_test.png',pos=(0,0))
        intro_txt.size *= self.txt_scl
        intro_txt.draw()
        self.win.flip()
        event.waitKeys()
        instruct_txt = visual.ImageStim(win=self.win, image='images/instruct/demo.png',pos=(0,0))
        instruct_txt.draw()
        self.win.flip()
        event.waitKeys()

    def test_phase(self):
        test_na = ['test/im_571.jpg', 'test/im_2158.jpg']
        test_a = ['test/im_6664.jpg', 'test/im_303.jpg']
        for idx, val in enumerate(test_na):
            keys = self.show_pics(self.img_dir+test_na[idx], self.img_dir+test_a[idx])
            key_pressed = self.get_cross(keys=keys)
            self.show_key(key_pressed)

        instruct_txt = visual.ImageStim(win=self.win, image='images/instruct/end_demo.png',pos=(0,0))
        instruct_txt.draw()
        self.win.flip()
        event.waitKeys()


    def show_key(self, key):
        if key[0] is None:
            key_txt = 'No key was pressed'
        else:
            key_txt = 'You pressed key {}'.format(key)
        key_text = visual.TextStim(win=self.win, text=key_txt,
                                    color=(1, 1, 1), colorSpace='rgb')




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

            keys = self.show_pics(self.img_dir+img_one, self.img_dir+img_two)
            key_pressed = self.get_cross(keys)
            print('kom ik hier')
            trial_lst.append([phase, i, key_pressed[0], key_pressed[1], img_one, img_two,
                             0.00, self.cur_reward])
        return trial_lst

    def set_one(self, phase, list_one, list_reward):

        trial_lst = []

        for i in range(self.trial_num):
            img_one = self.img_dir+list_one[i]
            key_pressed, reward = self.show_animal(img_one, list_reward[i])
            trial_lst.append([phase, i, key_pressed[0], key_pressed[1], img_one, None,
                             reward, self.cur_reward])
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
        get_reward = reward
        try:
            keys = keys[0]
            col = 'white'
            if keys[0] == 'slash' and reward > 0:
                col = 'green'
            elif keys[0] == 'z' and reward == 0:
                col = 'green'
            else:
                col = 'red'
                get_reward = 0
        except:
            keys = [None, None]
            col = 'yellow'
            get_reward = 0

        self.cur_reward += get_reward
        color_scheme = ()
        try:
            eur_str = '\x80'.decode("windows-1252")
        except:
            eur_str = '€'
        stim1 = visual.TextStim(self.win, 'reward {}: '.format(eur_str)+str(get_reward/100),
           color=col, pos=(0,0))
        stim2 = visual.TextStim(self.win, 'total {}: '.format(eur_str)+str(self.cur_reward/100),
           color='white', pos=(0,-0.2))
        print('jeej',str(stim1.font))

        stim1.draw()
        stim2.draw()
        self.win.flip()
        core.wait(self.cross_time)

        return keys, get_reward


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
        return keys
        self.get_cross(keys)


    def show_end(self):
        '''End slide takes window en begin time.'''
        end_txt = visual.TextStim(win=self.win, text='Thanks for participation!\n press key to finish test',
                        color=(1, 1, 1), colorSpace='rgb')
        end_txt.draw()
        self.win.flip()
        event.waitKeys(maxWait=10.0,timeStamped=self.ttl_timer)

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
