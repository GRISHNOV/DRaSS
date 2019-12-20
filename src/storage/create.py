import os
import sqlite3
import socket
import time

import storage.crypto
from keyboard_entropy.interface import interface_main


def check_selected_storage(path="db"):
    while(True):
        storage_name = input()

        if storage_name == "exit":
            return None
        if os.path.isfile(path + "/" + storage_name) or os.path.isfile(path + "/" + storage_name + ".drass"):
            print(
                "Хранилище с заданным именем уже существует, попробуйте использовать другое имя")
        else:
            return storage_name


def get_keyboard_entropy_data(wait=False):
    """
    Server to get client data from keyboard_entropy/interface.py
    """

    sock = socket.socket()
    sock.bind(('', 2020))
    sock.listen(1)

    interface_main(wait)  # Client part

    conn, addr = sock.accept()

    # print('(debug info) connected:', addr)

    data_from_client = []

    while True:
        data = conn.recv(1024)
        if not data:
            break
        # print(data.decode())
        data_from_client.append(data.decode())

    conn.close()
    return data_from_client


def create_selected_storage(path, storage_name):
    """
    Create database "key_data":
    user_db_name                    - storage name
    UK_hash                         - value of the (10**6 + 1) iteration of the SHA256 from UK (User Key)
    MK_encypted = MK xor UK_gamma   - UK_gamma is (10**6) iteration of the SHA256 from UK
    MK_CRC                          - CRC32 value from MK
    text_comment                    - log information
    """

    connection = sqlite3.connect(path + "/" + storage_name +
                                 ("" if storage_name.endswith(
                                     ".drass") else ".drass")
                                 )
    cursor = connection.cursor()

    cursor.execute(
        '''
        CREATE TABLE key_data(
            user_db_name text, 
            UK_hash text, 
            MK_encypted text,
            MK_CRC text, 
            text_comment text
        )
        '''
    )

    UK = ""
    MK = ""

    UK_hash = ""
    MK_encypted = ""
    MK_CRC = ""

    data_from_client = get_keyboard_entropy_data()
    for i in data_from_client:
        MK += i
    print("\nMK: ", MK)

    data_from_client = get_keyboard_entropy_data()
    for i in data_from_client:
        UK += i
    print("\nUK: ", UK)

    print("\nСохраните UK для доступа к хранилищу.")
    print("Нажмите любую клавишу чтобы продолжить...")
    input()

    UK_gamma = storage.crypto.get_sha256(UK, False)
    UK_hash = storage.crypto.get_sha256(UK_gamma, True)
    MK_encypted = storage.crypto.get_XOR_cipher(MK, UK_gamma)
    MK_CRC = storage.crypto.get_crc32(MK)

    entities = (
        storage_name,
        UK_hash,
        MK_encypted,
        MK_CRC,
        'storage_created_successfully'
    )
    cursor.execute(
        '''
        INSERT INTO key_data(
            user_db_name, 
            UK_hash, 
            MK_encypted, 
            MK_CRC, 
            text_comment
        ) VALUES(?, ?, ?, ?, ?)
        ''',
        entities
    )

    connection.commit()
    connection.close()


def create_storage(path="db"):
    # Prepare directory to create database
    if os.path.isdir(path) == False:
        os.mkdir(path)

    print("1. Введите желаемое имя для Вашего хранилища:")
    storage_name = check_selected_storage(path)
    if not storage_name:
        return
    print("------------------------------")

    print("2. Идёт создание хранилища...")
    create_selected_storage("db", storage_name)


if __name__ == "__main__":
    create_storage()
