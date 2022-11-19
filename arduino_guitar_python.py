#dependencies:
# !pip install pyserial
# !pip install pynput

import threading
import time
import serial
import sys
import numpy as np
import time
from threading import Thread

from pynput.keyboard import Key, Controller

# sudo chmod 666 /dev/ttys0



NUM_BUTTONS = 9
pressed = np.zeros(NUM_BUTTONS, dtype=bool)

#TIME = np.zeros(NUM_BUTTONS); 
RUNNING = True



ser = serial.Serial('COM6', baudrate = 115200, timeout = 20) # Replace the port here with Arduino's one
keyboard = Controller()

ENABLE_AUTO_WHAMMY = False

def autowhammy():
    keyboard2 = Controller()
    
    FRETS = [0, 1, 2, 3, 4] # button idsgt related to frets
    WHAMMY_TASK_TIME = 100 / 1000; #s
    WHAMMY_KEY = "w"
    WHAMMY_PRESSED = False
    
    while True:       
        if(WHAMMY_PRESSED):
            WHAMMY_PRESSED = False
            keyboard2.release(WHAMMY_KEY)
        elif(np.any(pressed[FRETS])):
            keyboard2.press(WHAMMY_KEY)
            WHAMMY_PRESSED = True
        
        time.sleep(WHAMMY_TASK_TIME)
                

if(ENABLE_AUTO_WHAMMY):
    autowhammy_thread = Thread(target=autowhammy, args=())
    autowhammy_thread.daemon = True
    autowhammy_thread.start()
    
while True:
    try:       
        code = ser.read(3)
        
        if(len(code) > 0): # sanety check implemented
            if(code[2] & (~(code[0] | code[1]))):
                for i in range(NUM_BUTTONS):
                    ispressed = 0
                    if(i < 8):
                        ispressed = code[0] & 1 << i
                    else:
                        ispressed = code[1] & 1 << (i - 8)
            
                    if(ispressed and not pressed[i]):
                        pressed[i] = 1;
                        keyboard.press(str(i));
                        # TIME[i] = time.time()                   
                    elif(pressed[i] and not ispressed):
                        pressed[i] = 0;
                        keyboard.release(str(i));    
                        # delay = (time.time() - TIME[i]) * 1000
                        # print(delay)
            else:
                print('Warning: Invalid serial code')
                print(code[0])
                print(code[1])
                print(code[2])
        else:
            print('Warning: empty serial code')
    
    except KeyboardInterrupt:
        ser.close()
        print('Interrupt')
        RUNNING = False
        
        if(ENABLE_AUTO_WHAMMY):
            autowhammy_thread.stop()
        break
    
    except:
        ser.close()
        
        RUNNING = False
        
        if(ENABLE_AUTO_WHAMMY):
            autowhammy_thread.stop()
        
        

    
    

                



                