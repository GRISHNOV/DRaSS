#!/usr/bin/env python3

import socket

print("\n---------- START module client ----------\n\n")

# Клиент для передачи данных обратно в interface_keyboard_entropy.py

data_for_server = "echo!"

sock = socket.socket()
sock.connect(('localhost', 2019))
sock.send(data_for_server.encode())
sock.close()


print("\n\n---------- END module client ----------\n")