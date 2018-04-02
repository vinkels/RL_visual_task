from __future__ import absolute_import, division, print_function

# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, prefs
import sys, csv, time
import random as rd

class window(object):
    def __init__(self, ppn, img_lst, img_time=1.0, cross_time = 1.0):
        self.img_set = img_lst
        self.w_scr = 1280
        self.h_scr = 800
        self.img_dir = 'images/'
        self.out_dir = 'output/'
        self.img_scl = 0.8
        self.x_val = 0.5
        self.cross_scl = 0.01
        self.ppn = ppn
        self.date_time = time.strftime("%y%m%d%H%M")
        self.img_time = img_time
        self.cross_time = cross_time
        self.win = visual.Window(size=(self.w_scr, self.h_scr),fullscr=True, monitor='testMonitor')
        self.fix_cros = visual.ShapeStim(win=self.win,
                   vertices=((0, -self.cross_scl), (0, self.cross_scl), (0,0),
                             (-self.cross_scl,0), (self.cross_scl, 0)),
                   lineWidth=2,closeShape=False,lineColor="black")
        self.create_window()

# Create a visual window:
    def create_window(self, condi=1):

        ttl_timer = core.Clock()
        event.globalKeys.add('q', func=core.quit)
        if condi== 2:
            trial_lst = self.set_one()
        else:
            trial_lst = self.set_two()

        # end_time = core.Clock()
        # print(end_time)
        # tot_time = ttl_timer - end_time
        self.show_end(ttl_timer)
        trial_lst = self.create_csv(trial_lst)
        self.win.close()
        core.quit()

    def set_two(self):

        trial_lst = []
        lst_one = self.img_set.condi_dict[self.img_set.csv_lst[0]]
        lst_two = self.img_set.condi_dict[self.img_set.csv_lst[1]]
        print(lst_one)
        print(lst_two)
        len_one = len(lst_one)
        len_two = len(lst_two)
        for i in range(10):
            name_one, name_two = lst_one[rd.randint(0,len_one-1)], lst_two[rd.randint(0,len_two-1)]
            img_one = self.img_dir+self.img_set.csv_lst[0]+'/'+ name_one
            img_two = self.img_dir+self.img_set.csv_lst[1]+'/'+ name_two
            key_pressed = self.show_pics(img_one, img_two)
            trial_lst.append([1]+[i] + key_pressed + [name_one, name_two])
        return trial_lst

    def set_one(self):

        trial_lst = []
        lst_one = self.img_set.condi_dict[self.img_set.csv_lst[0]]
        len_one = len(lst_one)
        for i in range(10):
            img_name = lst_one[rd.randint(0,len_one-1)]
            img_one = self.img_dir+self.img_set.csv_lst[0]+'/'+ img_name
            key_pressed = self.show_animal(img_one)
            trial_lst.append([2]+[i] + key_pressed + [img_name])
        return trial_lst

    def show_animal(self, img):

        img_show = visual.ImageStim(win=self.win, image=img,pos=(0,0))
        img_show.size *= self.img_scl
        img_show.draw()
        trial_tmr = core.Clock()
        self.win.flip()
        keys = event.waitKeys(maxWait=self.img_time, keyList=["z", "slash"],timeStamped=trial_tmr)
        return self.get_cross(keys)

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
        trial_tmr = core.Clock()
        self.win.flip()
        keys = event.waitKeys(maxWait=self.img_time, keyList=["z", "slash"],timeStamped=trial_tmr)
        return self.get_cross(keys)


    def show_end(self, ttl_timer):
        '''End slide takes window en begin time.'''
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
            csv_writer.writerow(['phase','trial_nr','key','time', 'img_l', 'img_r'])

            for row in log_lst:
                print(row)
                csv_writer.writerow(row)
