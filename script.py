
from __future__ import absolute_import, division, print_function

# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, prefs
import sys
import random as rd

class window(object):
    def __init__(self):
        self.w_scr = 1280
        self.h_scr = 800
        self.img_dir = 'images/'
        self.img_scl = 0.4
        self.x_val = .5
        self.cross_scl = 0.01


        self.create_window()


# Create a visual window:
    def create_window(self):

        win = visual.Window(size=(self.w_scr, self.h_scr),fullscr=True, monitor='testMonitor')
        # clock = core.Clock()


        img_lst = ['images/py1.jpeg', 'images/py2.jpeg', 'images/py3.jpeg', 'images/py4.jpeg']
        num_img = len(img_lst)

        prefs.general['shutdownKey'] = 'q'
        event.globalKeys.add('q', func=core.quit)

        for i in range(10):
            key_pressed = self.show_pics(img_lst[rd.randint(0,num_img-1)], img_lst[rd.randint(0,num_img-1)], win)

    def show_pics(self, img_one, img_two, win):
        trial_tmr = core.Clock()
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
        win.flip()
        keys = event.waitKeys(maxWait=2.0, keyList=["z", "slash"],timeStamped=Clock)
        # keyList = event.waitKeys(, keyList=['z','/'], timeStamped=True)
        # core.wait(2.0)
        # print keys
        fix_cros.draw()
        win.flip()
        core.wait(2.0)
        return keys



        # return True
