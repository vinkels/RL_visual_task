from __future__ import absolute_import, division, print_function

import numpy as np
import scipy.io as spio
import matplotlib.pyplot as plt

matfile = 'wrkspc_img.mat'
matdata = spio.loadmat(matfile)
print matdata.keys()

def get_files():
    mat_contents = sio.loadmat('wrkspc_img.mat')
    # print mat_contents
    img_name = mat_contents['filenames']
    img_type = img_name.dtype
    print(img_type)
    # gam_values = mat_contents['Gamma']
    # print list(img_name)
    # print list(mat_contents.keys())

def print_mat_nested(d, indent=0, nkeys=0):
    """Pretty print nested structures from .mat files
    Inspired by: `StackOverflow <http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python>`_
    """

    # Subset dictionary to limit keys to print.  Only works on first level
    if nkeys>0:
        d = {k: d[k] for k in d.keys()[:nkeys]}  # Dictionary comprehension: limit to first nkeys keys.

    if isinstance(d, dict):
        for key, value in d.iteritems():         # iteritems loops through key, value pairs
          print '\t' * indent + 'Key: ' + str(key)
          print_mat_nested(value, indent+1)

    if isinstance(d,np.ndarray) and d.dtype.names is not None:  # Note: and short-circuits by default
        for n in d.dtype.names:    # This means it's a struct, it's bit of a kludge test.
            print '\t' * indent + 'Field: ' + str(n)
            print_mat_nested(d[n], indent+1)

print_mat_nested(matdata, nkeys=0)
print matdata['filenames']
dict = {}
for value, row in enumerate(matdata['filenames']):
    row[0][0])
