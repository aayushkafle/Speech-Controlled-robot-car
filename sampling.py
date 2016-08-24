import sounddevice as sd
import numpy as np


def record_speech(duration):
    fs = 16000
    sd.default.samplerate= fs
    sd.default.channels=1
    myrecording = sd.rec(duration * fs)
    print("Recording")
    sd.wait()
    rec=np.reshape(myrecording,-1)
    return rec
def play_speech(rec):
    print('Playing')
    sd.play(rec)

