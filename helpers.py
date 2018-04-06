from __future__ import absolute_import, division, print_function
import os

try:
   import cPickle as pickle
except:
   import pickle

def dict_pickle(dict, name):
    with open('pickles/{}.pickle'.format(name), 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()

def dict_unpickle(pickle_file):
    with open('pickles/{}.pickle'.format(pickle_file), 'rb') as file:
        pickle_dict = pickle.load(file)
        file.close()
    return pickle_dict

def del_pyc():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith(".pyc")]:
            os.remove(os.path.join(dirpath, filename))
#find . -name '*.pyc' -delete
