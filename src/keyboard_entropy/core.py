import os
import sys
import time
from pynput import keyboard
import socket


def on_press(key):
    try:
        global total_keyboard_press
        print(
            f"\nБыла нажата алфавитно-цифровая клавиша '{key.char}'.")
        total_keyboard_press += 1
        if total_keyboard_press == 21:
            abort_keyboard_listen()

    except AttributeError:
        print(f"\nБыла нажата специальная клавиша '{key}'.")


def abort_keyboard_listen():
    global timestamp_begin
    timestamp_end = time.time()
    elapsed_time = timestamp_end - timestamp_begin

    print(f"\nПолучен энтропийный параметр равный {elapsed_time}.\n")
    print(f"Суммарно было нажато {total_keyboard_press} клавиш.")
    time.sleep(2)

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
