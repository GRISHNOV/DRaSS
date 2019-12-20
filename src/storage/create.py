import os
import sqlite3
import socket

import storage.crypto


def check_selected_storage(path="db"):
    while(True):
        storage_name = input()

        if storage_name == "exit":
            return "exit"
        if os.path.isfile(path + "/" + storage_name) or os.path.isfile(path + "/" + storage_name + ".drass"):
            print(
                "Хранилище с заданным именем уже существует, попробуйте использовать другое имя")
        else:
            return storage_name


def create_selected_storage(path, storage_name):  # TODO
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
    # for row in rows:
    # print(row)

    # os.chdir("./../")

    # Работа сервера для получение данных от клиентского модуля interface_keyboard_entropy.py
    # Диалог между модулями разыгрывается для генерации значения MK
    sock = socket.socket()
    sock.bind(('', 2020))
    sock.listen(1)

    os.system("./src/keyboard_entropy/interface.py")

    conn, addr = sock.accept()

    print('(debug info) connected:', addr)

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

    os.system("./src/keyboard_entropy/interface.py")

    conn, addr = sock.accept()

    print('(debug info) connected:', addr)

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

    UK_gamma = storage.crypto.get_sha256(UK, False)
    UK_hash = storage.crypto.get_sha256(UK_gamma, True)
    MK_encypted = storage.crypto.get_XOR_cipher(MK, UK_gamma)
    MK_CRC = storage.crypto.get_crc32(MK)

    entities = (storage_name, UK_hash, MK_encypted,
                MK_CRC, 'storage_created_successfully')
    cursor.execute(
        '''INSERT INTO key_data(user_db_name, UK_hash, MK_encypted, MK_CRC, text_comment) VALUES(?, ?, ?, ?, ?)''', entities)

    connection.commit()
    connection.close()


def create_storage(path="db"):
    # Prepare directory to create database
    if os.path.isdir(path) == False:
        os.mkdir(path)

    print("1. Введите желаемое имя для Вашего хранилища:")
    storage_name = check_selected_storage(path)
    if storage_name == "exit":
        return
    print("------------------------------")

    print("2. Идёт создание хранилища...")
    create_selected_storage("db", storage_name)
    # print("------------------------------")


if __name__ == "__main__":
    create_storage()
