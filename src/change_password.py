#!/usr/bin/env python3

import os
import sqlite3
import socket

import crypto # github.com/marcobellaccini/pyAesCrypt -> setup.py install


if __name__ == "__main__":

    print("\n---------- START module storage creator master ----------\n\n")

    print("Сейчас Вам будет предложено сменить пароль от личного хранилища.")

    if os.path.isdir("./db") == False: # Директория для хранения базы данных
            os.mkdir("db") # Если директории не существует, то создадим
            print("Не обнаужено ни одного хранилища.")
            exit(0)

    print("Введите, пожалуйста, имя Вашего хранилища:")

    while(True): # Исключаем возможность работы, если храналища с ведённым именем не существует

        storage_name = input() # Будем запрашивать повторный ввод до тех пор, пока не получим имя существующего файла

        if os.path.isfile("./db/" + storage_name + ".drass"):
            break
        else:
            print("Хранилища с заданным именем не существует, попробуйте использовать другое имя.")

    #os.chdir("./db/")

    connection = sqlite3.connect("./db/" + storage_name + ".drass")
    cursor = connection.cursor()



    connection.commit()
    connection.close()

    print("\n\n---------- END module storage creator master ----------\n")