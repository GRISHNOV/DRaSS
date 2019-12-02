#!/usr/bin/env python3

import time
begin = [0]
begin[0] = time.time()

print("\n---------- START module client ----------\n\n")

import socket

end = time.time()
elapsed = end - begin[0]
key = str(elapsed)
print(key)


sock = socket.socket()
sock.connect(('localhost', 6662))
#sock.send("hello, world!".encode())
sock.send(key.encode())

#data = sock.recv(1024).decode()
sock.close()

#print (data)

#for iterator in data:
#    print(iterator)

print("\n\n---------- END module client ----------\n")