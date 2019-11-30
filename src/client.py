#!/usr/bin/env python3


print("\n---------- START module client ----------\n\n")

import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send("hello, world!".encode())

data = sock.recv(1024).decode()
sock.close()

print (data)

print("\n\n---------- END module client ----------\n")