from __future__ import absolute_import, division, print_function
import time, os, datetime, sys

def test():
    # from ..helpers import *
    start_time = datetime.datetime.now()
    # time.sleep( 2 )
    string_i_want=('%02d:%02d.%d'%(start_time.minute,start_time.second,start_time.microsecond))[:-4]
    print(string_i_want)
    print((start_time.minute*60)+start_time.second)
    print("difference =", datetime.datetime.now() - start_time)

    print()
    print(target_dir)
