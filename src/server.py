#!/usr/bin/env python3


import time
begin = [0]
begin[0] = time.time()
print("\n---------- START module server ----------\n\n")

import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print ('connected:', addr)
end = time.time()
elapsed = end - begin[0]
key = str(elapsed)
print(key)


while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(data.upper())
    #conn.send(data.upper())

conn.close()

print("\n\n---------- END module server ----------\n")