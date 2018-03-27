from __future__ import absolute_import, division, print_function

# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, prefs
import sys, csv, time
import random as rd

class session(object):
    def __init__(self, ppn):
        self.w_scr = 1280
        self.h_scr = 800
        self.img_dir = 'images/'
        self.out_dir = 'output/'
        self.img_scl = 0.4
        self.x_val = .5
        self.cross_scl = 0.01
        self.ppn = ppn
        self.date_time = time.strftime("%y%m%d%H%M")
        self.create_window()


# Create a visual window:
    def create_window(self):

        trial_lst = []
        win = visual.Window(size=(self.w_scr, self.h_scr),fullscr=True, monitor='testMonitor')
        ttl_timer = core.Clock()


        img_lst = [self.img_dir+'py1.jpeg', self.img_dir+'py2.jpeg', self.img_dir+'py3.jpeg', self.img_dir+'py4.jpeg']
        num_img = len(img_lst)

        # prefs.general['shutdownKey'] = 'q'
        event.globalKeys.add('q', func=core.quit)

        for i in range(10):
            key_pressed = self.show_pics(img_lst[rd.randint(0,num_img-1)], img_lst[rd.randint(0,num_img-1)], win)
            trial_lst.append([i] + key_pressed)
            # print(trial_lst)

        self.show_end(win, ttl_timer)
        win.close()
        core.quit()
        self.create_csv(trial_lst)

    # def get_ppn(self):

    def show_pics(self, img_one, img_two, win):
        # event.globalKeys.add('q', func=core.quit)
        img_one = visual.ImageStim(win=win, image=img_one,pos=(-self.x_val,0))
        img_two = visual.ImageStim(win=win, image=img_two, pos=(self.x_val, 0))
        img_one.size *= self.img_scl
        img_two.size *= self.img_scl
        fix_cros = visual.ShapeStim(win=win,
                   vertices=((0, -self.cross_scl), (0, self.cross_scl), (0,0),
                             (-self.cross_scl,0), (self.cross_scl, 0)),
                   lineWidth=2,closeShape=False,lineColor="black")

        img_one.draw()
        img_two.draw()
        trial_tmr = core.Clock()
        win.flip()
        keys = event.waitKeys(maxWait=1.0, keyList=["z", "slash"],timeStamped=trial_tmr)
        # print(keys)
        fix_cros.draw()
        win.flip()
        core.wait(0.5)
        if keys is not None:
            return keys[0]
        else:
            return [None, None]

    def show_end(self, win, ttl_timer):
        '''End slide takes window en begin time.'''
        end_txt = visual.TextStim(win=win, text='Thanks for participation!\n press key to finish test',
                        color=(1, 1, 1), colorSpace='rgb')
        end_txt.draw()
        win.flip()
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
