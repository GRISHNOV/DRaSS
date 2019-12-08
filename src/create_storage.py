#!/usr/bin/env python3

import os
import sqlite3
import socket

import crypto # github.com/marcobellaccini/pyAesCrypt -> download repository and run setup.py install


if __name__ == "__main__":

    print("\n---------- START module storage creator master ----------\n\n")

    print("Сейчас Вам будет предложено создать личное хранилище.")

    print("Введите, пожалуйста, желаемое имя для Вашего хранилища:")

    if os.path.isdir("./db") == False: # Директория для хранения базы данных
            os.mkdir("db") # Если директории не существует, то создадим

    while(True): # Исключаем возможность создать хранилище с уже занятым именем

        storage_name = input() # Будем запрашивать повторный ввод до тех пор, пока не получим свободное имя

        if storage_name == "exit":
            exit(0)
        if os.path.isfile("./db/" + storage_name + ".drass"):
            print("Хранилище с заданным именем уже существует, попробуйте использовать другое имя.")
        else:
            break

    #os.chdir("./db/")

    connection = sqlite3.connect("./db/" + storage_name + ".drass")
    cursor = connection.cursor()

    #   Ниже создадим таблицу key_data для хранения ключевой информации (хэши и прочее)
    cursor.execute("""CREATE TABLE key_data     
                    (user_db_name text, 
                    UK_hash text, 
                    MK_encypted text,
                    MK_CRC text, 
                    text_comment text)
                """)
    
    ###########################################################################################
    # user_db_name -- имя хранилища, заданное пользователем при его создании                  #
    # UK_hash -- значение (10**6 + 1)-ой итерации sha256 от UK (User Key)                     #
    # MK_encypted = MK xor UK_gamma, UK_gamma равен (10**6)-ой итерации sha256 от UK          #
    # MK_CRC -- значение CRC32 от MK                                                          #
    # text_comment -- отладочная информация                                                   #
    ###########################################################################################

    UK = ""
    MK = ""

    UK_hash = ""
    MK_encypted = ""
    MK_CRC = ""


    #entities = (storage_name, '-\\-', '-\\-', '-\\-', '-\\-')
    #cursor.execute('''INSERT INTO key_data(user_db_name, UK_hash, MK_encypted, MK_CRC, text_comment) VALUES(?, ?, ?, ?, ?)''', entities)

    #cursor.execute('SELECT * FROM key_data ')
    #rows = cursor.fetchall()
    #for row in rows:
    #print(row)

    #os.chdir("./../")

    # Работа сервера для получение данных от клиентского модуля interface_keyboard_entropy.py
    # Диалог между модулями разыгрывается для генерации значения MK
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
        MK += i

    print("\nMK:", MK)

    # Работа сервера для получение данных от клиентского модуля interface_keyboard_entropy.py
    # Диалог между модулями разыгрывается для генерации значения UK
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
        UK += i

    print("\nUK:", UK)


    
    UK_gamma = crypto.get_sha256( UK, False)
    UK_hash = crypto.get_sha256( UK_gamma , True )
    MK_encypted = crypto.get_XOR_cipher( MK, UK_gamma )
    MK_CRC = crypto.get_crc32(MK)

    entities = (storage_name, UK_hash, MK_encypted, MK_CRC, 'storage_created_successfully')
    cursor.execute('''INSERT INTO key_data(user_db_name, UK_hash, MK_encypted, MK_CRC, text_comment) VALUES(?, ?, ?, ?, ?)''', entities)


    connection.commit()
    connection.close()

    print("\n\n---------- END module storage creator master ----------\n")