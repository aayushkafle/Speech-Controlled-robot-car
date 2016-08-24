import numpy as np
from random import randrange as rrge
generate = np.empty((100,5))
def gen_output(target):
    if target == 'start':
        for i in range(100):
            generate[i] = np.array([1,0,0,0,0])
        return generate
    if target == 'stop':
        for i in range(100):
            generate[i] = np.array([0,1,0,0,0])
        return generate
    if target == 'left':
        for i in range(100):
            generate[i] = np.array([0,0,1,0,0])
        return generate
    if target == 'right':
        for i in range(100):
            generate[i] = np.array([0,0,0,1,0])
        return generate
    if target == 'back':
        for i in range(100):
            generate[i] = np.array([0,0,0,0,1])
        return generate
#target = gen_output('back')
#print(target)
#print('mean------------------>')
#print(np.mean(target,axis=0))

def final_output(op):
    a = np.dot(op,[1,0,0,0,0])
    b = np.dot(op,[0,1,0,0,0])
    c = np.dot(op,[0,0,1,0,0])
    d = np.dot(op,[0,0,0,1,0])
    e = np.dot(op,[0,0,0,0,1])
    output=np.array([a,b,c,d,e])
    '''if output.argmax() == 0:
        #return 'start'
    if output.argmax() == 1:
        #return 'stop'
    if output.argmax() == 2:
        #return 'left'
    if output.argmax() == 3:
        #return 'right'
    if output.argmax() == 4:
        #return 'back'''

    state = np.load('state.npy')
    if state[0] == 0.0:
        num = (rrge(1,100))%10
        if num <= 6:
            print('start')
            state[1] = 1
            state[0] = 1.0
        else:
            print('back')
    elif state[0] == 0.1:
        num = (rrge(1,100))%10
        if num <= 5:
            print('back')
            state[0] = 0.1
            state[1] = 4
        else:
            print('start')
            state[0] = 1.0
            state[1] = 1
    elif state[0] == 1.0:
        num = (rrge(1,100))%10
        if num <= 6:
            print('stop')
            state[0] = 0.1
            state[1] = 0
        elif num%2 == 0:
            print('left')
        else :
            print ('right')
    elif state[0] == 1.1:
        num = (rrge(1,100))%10
        if num <= 6:
            print('left')
            state[0] = 1.2
            state[1] = 2
        elif num%2 == 0:
            print('right')
        else :
            print ('stop')
    elif state[0] == 1.2:
        num = (rrge(1,100))%10
        if num <= 6:
            print('right')
            state[0] = 1.2
            state[1] = 3
        elif num%2 == 0:
            print('stop')
        else :
            print ('left')
    return state


    

##data = np.array([0.06,0.4,0.43,0.7,0.9])
##print(final_output(data))
    
    
