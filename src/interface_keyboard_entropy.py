#!/usr/bin/env python3

import os
import socket

print("\n---------- START module interface keyboard entropy ----------\n\n")


print("Нажмите несколько случайных клавиш на клавиатуре, это нужно для создания ключей.")
print("Продолжайте ввод, пока не исчезнет дополнительное окно терминала...")
os.system("xterm -e './core_keyboard_entropy.py'") # sudo apt install xterm
print("\nСпасибо!")


print("\n\n---------- END module intefrace keyboard entropy ----------\n")