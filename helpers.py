from __future__ import absolute_import, division, print_function
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
    # pickle.load(open('pickles/{}.pickle'.format(pickle_file), 'rb'))
