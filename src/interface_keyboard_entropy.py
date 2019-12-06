#!/usr/bin/env python3

import os
import socket

if __name__ == "__main__":

    print("\n---------- START module interface keyboard entropy ----------\n\n")


    print("Нажмите несколько случайных клавиш на клавиатуре, это нужно для создания ключей.")
    print("Продолжайте ввод, пока не исчезнет дополнительное окно терминала...")

    # Сервер для приёма данных из core_keyboard_entropy.py

    sock = socket.socket()
    sock.bind(('', 2019))
    sock.listen(1)
    os.system("xterm -e './core_keyboard_entropy.py'") # sudo apt install xterm 
    conn, addr = sock.accept()


    #print (' (debug info) connected:', addr)

    entropy_parametr = []
    entropy_array = []
    keys_map_code = []
    key = []

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        entropy_parametr.append(data.decode())

    print("\nСпасибо!")

    conn.close()

    print(entropy_parametr[0])
    for i in entropy_parametr[0]:
        entropy_array.append(i)
    for k in range(1,10):
        entropy_array.append(k)

    print()
    print(entropy_array)

    buf = 0
    j = 0

    for i in range(2,19):
        #print(entropy_array[i])
        buf = buf + (int(entropy_array[i])+i)**3
        j = j + 1
        if (j % 3 == 0):
            keys_map_code.append(buf % 60)
            buf = 0
    print()
    print(keys_map_code)
    print()

    map = [ '0','1','2','3','4','5','6','7','8','9',
            'a','b','c','d','e','f','g','h','i','j',
            'k','l','m','n','o','p','q','r','s','t',
            'u','v','w','x','y','z','A','B','C','D',
            'E','F','G','H','I','J','K','L','M','N',
            'O','P','Q','R','S','T','U','V','W','X',
            'Y','Z' ]
        
    print(map)
    print()

    for i in keys_map_code:
        key.append(map[i])
    print()

    print("KEY:",key)

    print("\nPress for push msg to server")
    input()

    data_for_server = ""
    for i in key:
        data_for_server += i

    sock = socket.socket()
    sock.connect(('localhost', 2020))
    sock.send(data_for_server.encode())
    sock.close()


    print("\n\n---------- END module intefrace keyboard entropy ----------\n")

