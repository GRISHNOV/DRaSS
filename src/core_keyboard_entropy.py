#!/usr/bin/env python3

import os
import sys
import time
from pynput import keyboard

print("\n---------- START module core keyboard entropy ----------\n\n")

begin = [0]
begin[0] = time.time()
i = [0]

def abort():
    end = time.time()
    elapsed = end - begin[0]
    print("\n\n")
    print ("Полученный энтропийный параметр: ",elapsed)
    print("\n")
    print ("Суммарно было нажато клавиш: ",i[0])
    print("\n\n---------- END module core keyboard entropy ----------\n")
    time.sleep(3)

    import socket

    str_entropy = str(elapsed)

    # socket server

    sock = socket.socket()
    sock.connect(('localhost', 6662))
    sock.send(str_entropy.encode())
    sock.close()

    exit(0)
    

def on_press(key):
    try:
        print('\nalphanumeric key {0} pressed'.format(key.char))
        #nonlocal i
        i[0] = i[0] + 1
        if i[0] == 5:
            abort()
            #keyboard.send('ctrl+c')
            

    except AttributeError:
        print('\nspecial key {0} pressed'.format(key))

def on_release(key):
    print('\n{0} released'.format(key))

    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
    
#f = open('/dev/null', 'w')
#sys.stdout = f