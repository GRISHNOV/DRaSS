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
        (storage.crypto.get_AES256_encrypt(user_data, MK),)
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

    decrypted_user_data = []
    for doc in user_data:
        decrypted_user_data.append(
            storage.crypto.get_AES256_decrypt(doc[0], MK))

    connection.commit()
    connection.close()

    return decrypted_user_data
