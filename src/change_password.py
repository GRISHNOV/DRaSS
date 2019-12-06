#!/usr/bin/env python3

import os
import sqlite3
import socket

import crypto # github.com/marcobellaccini/pyAesCrypt -> download repository and run setup.py install


if __name__ == "__main__":

    print("\n---------- START module change password master ----------\n\n")

    print("Сейчас Вам будет предложено сменить пароль от личного хранилища.")

    if os.path.isdir("./db") == False: # Директория для хранения базы данных
            os.mkdir("db") # Если директории не существует, то создадим
            print("Не обнаужено ни одного хранилища.")
            print("\n\n---------- END module change password master ----------\n")
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

    print("\nПроизведено подключение к хранилищу: " + storage_name)

    cursor.execute('SELECT * FROM key_data ')
    rows = cursor.fetchall()
    
    ################################
    # rows[0][0] ==> user_db_name  #
    # rows[0][1] ==> UK_hash       #
    # rows[0][2] ==> MK_encypted   #
    # rows[0][3] ==> MK_CRC        #
    # rows[0][4] ==> text_comment  #
    ################################

    print("\nВведите свой текущий пароль:")
    
    while(True):

        UK_input = input() # e3IaK
        UK_gamma = crypto.get_sha256( UK_input, False)
        UK_hash = crypto.get_sha256( UK_gamma , True )

        if UK_hash == rows[0][1]:
            print("Совпадение")
            break
        else:
            print("Ошибка. Повторите ввод")


    new_UK = ""

    new_UK_hash = ""
    new_MK_encypted = ""

    # Работа сервера для получение данных от клиентского модуля interface_keyboard_entropy.py
    # Диалог между модулями разыгрывается для генерации нового значения UK
    sock = socket.socket()
    sock.bind(('', 2020))
    sock.listen(1)
    
    os.system("./interface_keyboard_entropy.py")

    conn, addr = sock.accept()

    print ('(debug info) connected:', addr)

    data_from_client = []

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        data_from_client.append(data.decode())

    conn.close()

    for i in data_from_client:
        new_UK += i

    print("\nnew UK:", new_UK)

    # UK_gamma = crypto.get_sha256( new_UK, False)
    # new_UK_hash = crypto.get_sha256( UK_gamma , True )
    # MK_encypted = crypto.get_XOR_cipher( MK, UK_gamma )
    # MK_CRC = crypto.get_crc32(MK)

    # entities = (storage_name, new_UK_hash, MK_encypted, MK_CRC, 'storage_created_successfully')
    # cursor.execute('''INSERT INTO key_data(user_db_name, UK_hash, MK_encypted, MK_CRC, text_comment) VALUES(?, ?, ?, ?, ?)''', entities)


    connection.commit()
    connection.close()

    print("\n\n---------- END module change password master ----------\n")