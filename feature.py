import numpy as np
import sampling
import feature_extract as FEXT
import file_handle
import generate_target
import serial
init_state = np.array([0,0])
np.save('state.npy',init_state)
ser = serial.Serial('COM16',timeout = 1)

def car_send(state):
    np.save('state.npy',state)
    print(state)
    if state[1] == 0:
        data = 'q'
        print('I goot it')
    if state[1] == 1:
        data = 'f'
        print('I goot it')
    if state[1] == 2:
        data = 'l'
        print('I goot it')        
    if state[1] == 3:
        data = 'r'
        print('I goot it')
    if state[1] == 4:
        data = 'b'
        print('I goot it')
    ser.write(data.encode('ascii'))
    print(data)
        

from scipy import signal
from pybrain.structure import RecurrentNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

duration = 1

num_coeff = 26
max_freq = 8000
min_freq = 0
melArray = np.linspace(FEXT.freqToMel(min_freq), FEXT.freqToMel(max_freq), num_coeff + 2)
ferqArray = FEXT.melToFreq(melArray)
freqArray_bin = np.floor(513 * ferqArray / 16000)
centralPoints = freqArray_bin[1:21]
freqbank = np.zeros((26, 257))

LSTMre = RecurrentNetwork()

LSTMre.addInputModule(LinearLayer(39, name='input'))
LSTMre.addModule(LSTMLayer(50, name = 'LSTM_hidden'))
LSTMre.addOutputModule(SoftmaxLayer(5, name='out'))
LSTMre.addConnection(FullConnection(LSTMre['input'], LSTMre['LSTM_hidden'], name='c1'))
LSTMre.addConnection(FullConnection(LSTMre['LSTM_hidden'], LSTMre['out'], name='c2'))
LSTMre.addRecurrentConnection(FullConnection(LSTMre['LSTM_hidden'], LSTMre['LSTM_hidden'], name='c3'))
LSTMre.sortModules()
ds = SupervisedDataSet(39, 5)

#ser.

for i in range(1,27):
    start, center, stop = int(freqArray_bin[i-1]), int(freqArray_bin[i]), int(freqArray_bin[i+1])
    temp = np.zeros(257)
    ascending = np.linspace(0, 1, center - start + 1) 
    descending = np.linspace(1, 0, stop - center + 1)
    temp[start : center + 1] = ascending
    temp[center : stop + 1] = descending
    freqbank[i-1] = temp
print(freqbank)

state_start = input('Press any key to start:')
state_run = True
do_train = True
do_update = True
is_correct = True


while state_run == True:
    
    my_recording = sampling.record_speech(duration)
    sampling.play_speech(my_recording)

    my_recording = np.append([my_recording],[np.zeros(240)])
    window = signal.hamming(400, sym = True)

    for i in range( 0, int(len(my_recording)/160-1)):
        temp = my_recording[ 160 * i : 160 * i + 400] * window
        temp_fft = np.fft.fft(temp,n = 512)
        temp_fft = temp_fft[0:257]
        temp_mfcc = FEXT.mfcc(temp_fft, freqbank)
        temp_delta_mfcc = FEXT.delta_mfcc(temp_mfcc)
        temp_delta_delta_mfcc = FEXT.delta_mfcc(temp_delta_mfcc)
        temp_dataset = temp_mfcc
        temp_dataset = np.append(temp_dataset,temp_delta_mfcc)
        temp_dataset = np.append(temp_dataset,temp_delta_delta_mfcc)
        
        
        if i == 0:
            final = [temp]
            final_fft = [temp_fft]
            final_mfcc = [temp_mfcc]
            final_delta_mfcc = [temp_delta_mfcc]
            final_delta_delta_mfcc = [temp_delta_delta_mfcc]
            final_dataset = [temp_dataset]
            
        else:
            final = np.concatenate((final,[temp]),axis = 0)
            final_fft = np.concatenate((final_fft,[temp_fft]),axis = 0)
            final_mfcc = np.concatenate((final_mfcc,[temp_mfcc]),axis = 0)
            final_delta_mfcc = np.concatenate((final_delta_mfcc,[temp_delta_mfcc]),axis = 0)
            final_delta_delta_mfcc = np.concatenate((final_delta_delta_mfcc,[temp_delta_delta_mfcc]),axis = 0)
            final_dataset = np.concatenate((final_dataset,[temp_dataset]),axis=0)

    dataset_op = 0
    dataset_ip = 0
    ds.clear()
    parameters =np.load('parameters.npy')
    LSTMre._setParameters(parameters)

    output=np.empty((100,5))
    #print(LSTMre.params)
    print('____________>output')
    for i in range(100):
        output[i] = LSTMre.activate(final_dataset[i])
    final_op = np.mean(output,axis=0)
    print('YOU SAID--------------->')
    state = generate_target.final_output(final_op)
    
    #is_it_correct = input('Is it correct?')
    '''if is_it_correct == 'n'
        is_correct = False
    else:
        is_correct = True'''

    if is_correct:
        car_send(state)
    

    '''do_train = input('Do you want to train? Enter --> x <-- to cancel')
        
    if do_train != 'x':
        just_said = input('What did you just said??huh')
        dataset_op = generate_target.gen_output(just_said)
        file_handle.save_tofile(final_dataset,'train')
        dataset_ip = file_handle.load_fromfile('train')
        print (dataset_ip.size)
        print(dataset_ip[0])
        print(dataset_op[0])
        for i in range(39):
            ds.addSample(dataset_ip[i], dataset_op[1])
        trainer = BackpropTrainer(LSTMre, ds,batchlearning = True)
        trainer.train()
        print('trained and saving parameters')
        parameters = np.array(LSTMre.params)
        np.save('parameters.npy',parameters)'''      
        
    state_temp = input('Press x to exit')
    if (state_temp == 'x' ):
        state_run = False

print('Thank You')

    
