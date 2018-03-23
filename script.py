from __future__ import absolute_import, division, print_function

# Import key parts of the PsychoPy library:
from psychopy import visual, core, event
import sys

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
        clock = core.Clock()


        img_lst = ['images/py1.jpeg', 'images/py2.jpeg', 'py3.jpeg', 'py4.jpeg']
        img_one = visual.ImageStim(win=win, image=img_lst[0],pos=(-self.x_val,0))
        img_two = visual.ImageStim(win=win, image=img_lst[0], pos=(self.x_val, 0))
        img_one.size *= self.img_scl
        img_two.size *= self.img_scl

        fix_cros = visual.ShapeStim(win,
                   vertices=((0, -self.cross_scl), (0, self.cross_scl), (0,0),
                             (-self.cross_scl,0), (self.cross_scl, 0)),
                   lineWidth=2,closeShape=False,lineColor="black")

        key = 'q'
        event.globalKeys.add(key, func=core.quit)


        for i in range(10):
            img_one.draw()
            img_two.draw()
            win.flip()
            keyList = event.waitKeys(maxWait=2.0, keyList=['z','/'])
            # core.wait(2.0)
            fix_cros.draw()
            win.flip()
            core.wait(2.0)




        # return True
