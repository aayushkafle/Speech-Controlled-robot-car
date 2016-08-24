import numpy as np
def save_tofile(mfcc_array,savetype):
    if savetype== 'train':
        filename = 'trainbuffer'
    if savetype == 'weight':
        filename = 'weightbuffer'
    np.save(filename, mfcc_array)

def load_fromfile(savetype):
    if savetype== 'train':
        filename = 'trainbuffer.npy'
    if savetype == 'weight':
        filename = 'weightbuffer.npy'
    return np.load(filename)
