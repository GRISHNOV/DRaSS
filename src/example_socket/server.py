#!/usr/bin/env python3

import socket

print("\n---------- START module server ----------\n\n")

# Сервер для приёма данных

sock = socket.socket()
sock.bind(('', 2019))
sock.listen(1)

##################
# Работа клиента #
# В данном месте #
##################
    
conn, addr = sock.accept()

print ('(debug info) connected:', addr)

data_from_client = []

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(data.decode())
    data_from_client.append(data.decode())

conn.close()

print("\n\n---------- END module server ----------\n")