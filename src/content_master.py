#!/usr/bin/env python3

import os
import sqlite3
import socket
import time

import crypto # github.com/marcobellaccini/pyAesCrypt -> download repository and run setup.py install
import ascii_interface


if __name__ == "__main__":

    print("\n---------- START module storage creator master ----------\n\n")

    if os.path.isdir("./db") == False:
            os.mkdir("db")

    print("Список доступных хранилищ:")
    print()
    print("==============================")
    os.system("ls ./db/ -1")
    print("==============================")
    print()
    print("Введите, пожалуйста, имя хранилища, к которому Вы хотите подключиться:")

    while(True):

        storage_name = input()

        if storage_name == "exit":
            exit(0)
        if os.path.isfile("./db/" + storage_name + ".drass"):
            break
        else:
            print("Хранилища с введённым именем не существует, попробуйте ещё раз")

    connection = sqlite3.connect("./db/" + storage_name + ".drass")
    cursor = connection.cursor()

    print("Соединение с хранилищем установлено...")
    time.sleep(2)
    
    connection.commit()
    connection.close()

    print("\n\n---------- END module storage creator master ----------\n")