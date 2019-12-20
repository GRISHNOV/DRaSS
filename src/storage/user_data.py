import sqlite3
import json

import time

import storage.crypto


def load_user_data(MK, storage_name, user_data, path="db"):
    connection = sqlite3.connect(
        path + "/" + storage_name +
        ("" if storage_name.endswith(".drass") else ".drass")
    )
    cursor = connection.cursor()

    cursor.execute(
        '''
        INSERT INTO user_data(
            document
        ) VALUES(?)
        ''',
        (storage.crypto.get_AES256_encrypt(json.dumps(user_data), MK),)
    )

    connection.commit()
    connection.close()


def get_user_data(MK, storage_name, path="db"):
    connection = sqlite3.connect(
        path + "/" + storage_name +
        ("" if storage_name.endswith(".drass") else ".drass")
    )
    cursor = connection.cursor()

    cursor.execute('SELECT document FROM user_data')
    user_data = cursor.fetchall()

    connection.commit()
    connection.close()

    for document in user_data:
        print(storage.crypto.get_AES256_decrypt(
            str(document)[1:-2], MK))  # TODO
    # storage.crypto.get_AES256_decrypt(document, MK)
    # storage.crypto.get_AES256_decrypt(user_data, MK)
    # for document in json.loads(storage.crypto.get_AES256_decrypt(user_data, MK)):

    time.sleep(10)

    return user_data
