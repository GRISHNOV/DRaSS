#!/usr/bin/env python3

import os
import socket

if __name__ == "__main__":

    print("\n---------- START module interface keyboard entropy ----------\n\n")


    print("Нажмите несколько случайных клавиш на клавиатуре, это нужно для создания ключей.")
    print("Продолжайте ввод, пока не исчезнет дополнительное окно терминала...")

    import socket

    # socket server

    sock = socket.socket()
    sock.bind(('', 6662))
    sock.listen(1)
    os.system("xterm -e './core_keyboard_entropy.py'") # sudo apt install xterm 
    conn, addr = sock.accept()


    print (' (debug info) connected:', addr)

    rec_key = []
    data_key = []
    pas_code = []

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        rec_key.append(data.decode())

    print("\nСпасибо!")

    conn.close()

    print(rec_key[0])
    for i in rec_key[0]:
        data_key.append(i)
    for k in range(1,10):
        data_key.append(k)

    print()
    print(data_key)

    buf = 0
    j = 0

    for i in range(2,19):
        #print(data_key[i])
        buf = buf + (int(data_key[i])+i)**3
        j = j + 1
        if (j % 3 == 0):
            pas_code.append(buf % 60)
            buf = 0
    print()
    print(pas_code)
    print()

    map = ['0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g','h','i','j',
        'k','l','m','n','o','p','q','r','s','t',
        'u','v','w','x','y','z','A','B','C','D',
        'E','F','G','H','I','J','K','L','M','N',
        'O','P','Q','R','S','T','U','V','W','X',
        'Y','Z']
        
    print(map)
    print()

    pas = []

    for i in pas_code:
        pas.append(map[i])

    print(pas)

    print("\n\n---------- END module intefrace keyboard entropy ----------\n")