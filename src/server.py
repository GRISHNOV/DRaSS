#!/usr/bin/env python3

print("\n---------- START module server ----------\n\n")

import socket

sock = socket.socket()
sock.bind(('', 6662))
sock.listen(1)
conn, addr = sock.accept()

print ('connected:', addr)

# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     conn.send(data.upper())

rec_key = []
data_key = []
pas_code = []

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(data.decode())
    rec_key.append(data.decode())

print(rec_key[0])
for i in rec_key[0]:
    data_key.append(i)

print()
print(data_key)

buf = 0
j = 0

for i in range(2,19):
    #print(data_key[i])
    buf = buf + (int(data_key[i])+i)**3
    j = j + 1
    if (j % 3 == 0):
        pas_code.append(buf % 60)
        buf = 0
print()
print(pas_code)
print()

map = ['0','1','2','3','4','5','6','7','8','9',
       'a','b','c','d','e','f','g','h','i','j',
       'k','l','m','n','o','p','q','r','s','t',
       'u','v','w','x','y','z','A','B','C','D',
       'E','F','G','H','I','J','K','L','M','N',
       'O','P','Q','R','S','T','U','V','W','X',
       'Y','Z']
    
print(map)
print()

pas = []

for i in pas_code:
    pas.append(map[i])

print(pas)


conn.close()

print("\n\n---------- END module server ----------\n")