#!/usr/bin/env python3

import os
import sqlite3

import crypto # Модуль crypto.py

if __name__ == "__main__":

    print("\n---------- START module storage creator master ----------\n\n")

    print("Сейчас Вам будет предложено создать личное хранилище.")

    print("Введите, пожалуйста, желаемое имя для Вашего хранилища:")

    if os.path.isdir("./db") == False: # Директория для хранения базы данных
            os.mkdir("db") # Если директории не существует, то создадим

    while(True): # Исключаем возможность создать хранилище с уже занятым именем

        storage_name = input() # Будем запрашивать повторный ввод до тех пор, пока не получим свободное имя

        if os.path.isfile("./db/" + storage_name + ".drass"):
            print("Хранилище с заданным именем уже существует, попробуйте использовать другое имя.")
        else:
            break

    os.chdir("./db/")

    connection = sqlite3.connect(storage_name + ".drass")
    cursor = connection.cursor()

    #   Ниже создадим таблицу для хранения ключевой информации (хэши и прочее)
    cursor.execute("""CREATE TABLE key_data     
                    (user_db_name text, 
                    UK_hash text, 
                    MK_gamma text,
                    MK_CRC text, 
                    text_comment text)
                """)

    #entities = (storage_name, '-\\-', '-\\-', '-\\-', '-\\-')
    #cursor.execute('''INSERT INTO key_data(user_db_name, UK_hash, MK_gamma, MK_CRC, text_comment) VALUES(?, ?, ?, ?, ?)''', entities)

    #cursor.execute('SELECT * FROM key_data ')
    #rows = cursor.fetchall()
    #for row in rows:
    #print(row)

    connection.commit()
    connection.close()

    print("\n\n---------- END module storage creator master ----------\n")