#!/usr/bin/env python3

import hashlib
import binascii


print("\n---------- START module crypto ----------\n\n")

hash = hashlib.sha256(b'test').hexdigest()
print(hash)

hash_crc = binascii.crc32(hash.encode())
print(hash_crc)

import pyAesCrypt

def crypt(dir):
    print('-----------------------------------')
    password = input('Enter key: ') 
    bufferSize = 512*1024 
    pyAesCrypt.encryptFile(str(dir),str(dir)+'.aes',password, bufferSize) 
    print('[Crypted] '+str(dir)+'.aes')

dir = input('Enter file name: ')
crypt(dir)

input()
password = input('Enter key: ') 
bufferSize = 512*1024
pyAesCrypt.decryptFile("test.txt.aes","data.txt",password,bufferSize) 

msg = "test"
gamma = "1234"
result = bytes([i^j for i,j in zip(msg.encode(),gamma.encode())]).decode()
print(result)
decrypt = bytes([i^j for i,j in zip(result.encode(),gamma.encode())]).decode()
print(decrypt)




print("\n\n---------- END module crypto ----------\n")