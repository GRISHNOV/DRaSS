# TODO

import hashlib
import binascii
import time

import pyAesCrypt
import io


def get_sha256(data: str, once_iteration: bool) -> str:  # Многоитерационный SHA256

    if once_iteration:  # Флаг запроса только одной итерации хеширования

        hash = hashlib.sha256(data.encode()).hexdigest()
        return hash

    else:

        # Длина цепочки хэшей. Миллион итераций обеспечивают должную задержку
        ITERATION_NUMBER = 10**6

        hash = hashlib.sha256(data.encode()).hexdigest()
        counter = 1

        while (counter < ITERATION_NUMBER):
            hash = hashlib.sha256(hash.encode()).hexdigest()
            counter = counter + 1

        return hash


def get_crc32(data: str) -> str:  # Контрольная сумма CRC32

    checksum = binascii.crc32(data.encode())

    return checksum


# Потоковый шифр гаммирования для одинаковых по длине строк
def get_XOR_cipher(data: str, gamma: str) -> str:

    # gamma является значением ключа
    result = bytes([i ^ j for i, j in zip(
        data.encode(), gamma.encode())]).decode()

    return result


def get_AES256_encrypt(data: str, password: str) -> bytes:  # Шифрование AES256

    BUFFER_SIZE = 64 * 1024  # Размер буфера

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


def get_AES256_decrypt(data: str, password: str) -> str:  # Расшифрование AES256

    BUFFER_SIZE = 64 * 1024  # Размер буфера

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
