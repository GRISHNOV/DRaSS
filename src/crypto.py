#!/usr/bin/env python3

import hashlib
import binascii
import time
import pyAesCrypt # Если проблемы с импортированием (или отдельными функциями внутри модуля), то попробуй с sudo
import io


def get_sha256( data:str ) -> str: # Многоитерационный SHA256

    ITERATION_NUMBER = 10**6 # Длина цепочки хэшей. Миллион итераций обеспечивают должную задержку
    
    hash = hashlib.sha256(data.encode()).hexdigest()
    counter = 1
    
    while (counter < ITERATION_NUMBER):
        hash = hashlib.sha256(hash.encode()).hexdigest()
        counter = counter + 1

    return hash


def get_crc32 ( data:str ) -> str: # Контрольная сумма CRC32

    checksum = binascii.crc32(data.encode())
    
    return checksum


def get_XOR_cipher ( data:str, gamma:str ) -> str: # Потоковый шифр гаммирования для одинаковых по длине строк

    result = bytes([i^j for i,j in zip(data.encode(),gamma.encode())]).decode() # gamma является значением ключа

    return result


def get_AES256_encrypt( data:str , password:str ) -> bytes: # Шифрование AES256 

    BUFFER_SIZE = 64 * 1024 # Размер буфера

    # Битовый набор данных для шифрования (открытый текст)
    pbdata = data.encode() + b" \x00\x01"
    print(pbdata)

    # Входной битовый поток для открытого текста
    fIn = io.BytesIO(pbdata)

    # Инициализация битового потока для шифротекста
    fCiph = io.BytesIO()

    # Поток шифрования
    pyAesCrypt.encryptStream(fIn, fCiph, password, BUFFER_SIZE)

    return fCiph.getvalue()


def get_AES256_decrypt( data:str , password:str ) -> str: # Расшифрование AES256

    BUFFER_SIZE = 64 * 1024 # Размер буфера

    # Инициализация битового потока для шифротекста
    fCiph = io.BytesIO(data)

    # Инициализация битового потока для расшированного текста
    fDec = io.BytesIO()

    # Длина шифротекста
    ctlen = len(fCiph.getvalue())

    # Поток расшифрования
    pyAesCrypt.decryptStream(fCiph, fDec, password, BUFFER_SIZE, ctlen)

    # Печать расшифрованных данных
    #print("Decrypted data:\n" + str(fDec.getvalue()))
    
    return str(fDec.getvalue())


if __name__ == "__main__":

    print("\n---------- START module crypto ----------\n\n")
    pass
    print("\n\n---------- END module crypto ----------\n")