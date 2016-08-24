import numpy as np
from scipy import fftpack

def mfcc(fft, freqbank):
    temp = abs(fft) ** 2
    temp = temp / 400
    #print(freqArray_bin[0])
    for i in range (0, 26):
        temp1 = np.sum(freqbank[i] * temp)
        
        if i == 0:
            final = temp1
        else:
            final = np.append(final,temp1)
            
    final = np.log(final)
    final = fftpack.dct(final,type=2)
    return final[0:13]

def delta_mfcc(mfcc):
    for i in range(13):
        if i == 0:
            c1 = mfcc[0]
            c2 = mfcc[0]
            c3 = mfcc[i+1]
            c4 = mfcc[i+2]
        elif i == 1:
            c1 = mfcc[0]
            c2 = mfcc[i-1]
            c3 = mfcc[i+1]
            c4 = mfcc[i+2]
        elif i == 11:
            c1 = mfcc[i-2]
            c2 = mfcc[i-1]
            c3 = mfcc[i+1]
            c4 = mfcc[11]
        elif i == 12:
            c1 = mfcc[i-2]
            c2 = mfcc[i-1]
            c3 = mfcc[12]
            c4 = mfcc[12]
        else:
            c1 = mfcc[i-2]
            c2 = mfcc[i-1]
            c3 = mfcc[i+1]
            c4 = mfcc[i+2]
        #print(i,'=',c1,',',c2,',',c3,',',c4,',')
        temp_coeff = (c3 - c2 + 2 * ( c4 - c1)) / 10
        #print(temp_coeff)
        if i==0:
            final =  temp_coeff
        else:
            final = np.append(final,temp_coeff)

    return final[0:13]
    
    
    
def freqToMel(lala):
    return 1127 * np.log(1 + lala / 700)

def melToFreq(lala):
    return 700 * (np.exp(lala / 1127) - 1)

#mfcc(20)
