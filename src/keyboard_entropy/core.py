import os
import sys
import time
from pynput import keyboard
import socket


def abort_keyboard_listen():

    global timestamp_begin
    global timestamp_end
    global elapsed_time

    timestamp_end = time.time()
    elapsed_time = timestamp_end - timestamp_begin
    print("\n\n")
    print("Полученный энтропийный параметр: ", elapsed_time)
    print("\n")
    print("Суммарно было нажато клавиш: ", total_keyboard_press)
    print("\n\n---------- END module core keyboard entropy ----------\n")
    time.sleep(3)

    str_entropy = str(elapsed_time)

    # Клиент для передачи данных обратно в interface_keyboard_entropy.py

    sock = socket.socket()
    sock.connect(('localhost', 2019))
    sock.send(str_entropy.encode())
    sock.close()

    exit(0)


def on_press(key):
    try:
        global total_keyboard_press
        print('\nalphanumeric key {0} pressed'.format(key.char))
        total_keyboard_press += 1
        if total_keyboard_press == 5:
            abort_keyboard_listen()

    except AttributeError:
        print('\nspecial key {0} pressed'.format(key))


def on_release(key):
    print('\n{0} released'.format(key))

    if key == keyboard.Key.esc:
        # Stop listener
        return False


if __name__ == "__main__":

    print("\n---------- START module core keyboard entropy ----------\n\n")
    timestamp_begin = 0
    timestamp_begin = time.time()
    total_keyboard_press = 0
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
