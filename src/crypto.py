#!/usr/bin/env python3

import hashlib
import binascii
import time



print("\n---------- START module crypto ----------\n\n")

begin = [0]
begin[0] = time.time()

hash = hashlib.sha256(b'test').hexdigest()
hash_iteration = 1
iteration_constant = 10**6

while (hash_iteration < iteration_constant):
    hash = hashlib.sha256(hash.encode()).hexdigest()
    hash_iteration = hash_iteration + 1

print(hash)
end = time.time()
elapsed = end - begin[0]
print(elapsed)

input()

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