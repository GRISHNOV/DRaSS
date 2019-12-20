import os
import sqlite3
import socket
import time

from terminal_interface.menu import clear_terminal
from terminal_interface.heroes import print_man

import storage.crypto


def get_available_storages(path="db"):
    return [file for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file)) and (file.endswith(".drass"))]


def print_available_storages(path="db"):
    files = get_available_storages(path)
    if len(files):
        for file in files:
            print(file)
        return True
    else:
        print("Нет доступных хранилищ")
        return False


def get_selected_storage(path="db"):
    while(True):
        storage_name = input()

        if storage_name == "exit":
            return "exit"
        if os.path.isfile(path + "/" + storage_name):
            return storage_name
        if os.path.isfile(path + "/" + storage_name + ".drass"):
            storage_name += ".drass"
            return storage_name
        else:
            print("Хранилища с введённым именем не существует, попробуйте ещё раз")


def get_access_selected_storage(path, storage_name):  # TODO
    connection = sqlite3.connect(path + "/" + storage_name)
    cursor = connection.cursor()

    print("Соединение с хранилищем установлено!")
    # time.sleep(2)

    cursor.execute('SELECT * FROM key_data ')
    rows = cursor.fetchall()

    clear_terminal()
    while(True):

        print_man()
        print("Хранилище: ", storage_name)
        print("Введите пароль от хранилища:")
        UK_input = input()
        if UK_input == "exit":
            exit(0)
        UK_hash = storage.crypto.get_sha256(
            storage.crypto.get_sha256(UK_input, False), True)

        if UK_hash == rows[0][1]:
            clear_terminal()
            print("Принято!")
            print_man()
            break

        else:
            clear_terminal()
            print("Ошибка. Повторите ввод")

    UK_gamma = storage.crypto.get_sha256(UK_input, False)
    MK = storage.crypto.get_XOR_cipher(rows[0][2], UK_gamma)

    if str(storage.crypto.get_crc32(MK)) == rows[0][3]:
        print()
        # print("MK CRC correct")
    else:
        print("MK CRC error")
        print("Гаммирование MK завершилось ошибкой. Хранилище повреждено...")
        exit(0)

    connection.commit()
    connection.close()


def connect_storage(path="db"):
    # Prepare directory to create database
    if os.path.isdir(path) == False:
        os.mkdir(path)

    print("0. Список доступных хранилищ:")
    if not print_available_storages(path):
        time.sleep(1)
        return
    print("------------------------------")

    print("1. Введите имя хранилища, к которому Вы хотите подключиться (или exit чтобы выйти):")
    storage_name = get_selected_storage(path)
    if storage_name == "exit":
        return
    print("------------------------------")

    print("2. Идёт установка соединения с хранилищем...")
    get_access_selected_storage("db", storage_name)
    # print("------------------------------")


if __name__ == "__main__":
    connect_storage()
