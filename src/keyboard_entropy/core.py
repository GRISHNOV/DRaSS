import os
import sys
import time
from pynput import keyboard
import socket


def on_press(key):
    try:
        global total_keyboard_press
        print(
            "\nБыла нажата алфавитно-цифровая клавиша '{0}'.".format(key.char))
        total_keyboard_press += 1
        if total_keyboard_press == 21:
            abort_keyboard_listen()

    except AttributeError:
        print("\nБыла нажата специальная клавиша '{0}'.".format(key))


def abort_keyboard_listen():
    global timestamp_begin
    timestamp_end = time.time()
    elapsed_time = timestamp_end - timestamp_begin

    print("\nПолучен энтропийный параметр равный {0}.\n".format(elapsed_time))
    print("Суммарно было нажато {0} клавиш.".format(total_keyboard_press))

    str_entropy = str(elapsed_time)

    # Client to send data back to keyboard_entropy/interface.py
    sock = socket.socket()
    sock.connect(('localhost', 2019))
    sock.send(str_entropy.encode())
    sock.close()
    exit(0)


def on_release(key):
    # print('\n{0} released'.format(key))

    # Stop listener
    if key == keyboard.Key.esc:
        return False


if __name__ == "__main__":
    timestamp_begin = time.time()
    total_keyboard_press = 0

    # Collect events until released
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()
