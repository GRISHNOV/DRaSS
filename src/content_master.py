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

    cursor.execute('SELECT * FROM key_data ')
    rows = cursor.fetchall()

    ################################
    # rows[0][0] ==> user_db_name  #
    # rows[0][1] ==> UK_hash       #
    # rows[0][2] ==> MK_encypted   #
    # rows[0][3] ==> MK_CRC        #
    # rows[0][4] ==> text_comment  #
    ################################

    ascii_interface.clr_terminal()    
    while(True):

        ascii_interface.man()
        print("\t\t\t\tХранилище: ", storage_name)
        print("\t\t\t\tВведите пароль от хранилища:")
        UK_input = input() # pUoSi
        if UK_input == "exit":
            exit(0)
        UK_hash = crypto.get_sha256( crypto.get_sha256( UK_input, False) , True )

        if UK_hash == rows[0][1]:
            ascii_interface.clr_terminal()
            print("\t\t\t\t\t\tПринято!")
            ascii_interface.man()
            break
            
        else:
            ascii_interface.clr_terminal()
            print("\t\t\t\t\t\t\tОшибка. Повторите ввод")


    UK_gamma = crypto.get_sha256( UK_input, False)
    MK = crypto.get_XOR_cipher( rows[0][2], UK_gamma )
  
    if str(crypto.get_crc32(MK)) == rows[0][3]:
        print()
        #print("MK CRC correct")
    else:
        print("MK CRC error")
        print("Гаммирование MK завершилось ошибкой. Хранилище повреждено...")
        exit(0)

    connection.commit()
    connection.close()

    print("\n\n---------- END module storage creator master ----------\n")