import os
import socket


def interface_main():
    """
    Server to recieve data from keyboard_entropy/core.py
    """

    print("Нажмите несколько случайных клавиш на клавиатуре, это нужно для создания ключей.")
    print("Продолжайте ввод, пока не исчезнет дополнительное окно терминала...")

    sock = socket.socket()
    sock.bind(('', 2019))
    sock.listen(1)
    os.system("xterm -e 'python3 src/keyboard_entropy/core.py'")
    conn, addr = sock.accept()

    #print (' (debug info) connected:', addr)

    entropy_parametr = []
    entropy_array = []
    keys_map_code = []
    key = []

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"\nПолучена энтропия равная {data.decode()}.")
        entropy_parametr.append(data.decode())

    conn.close()

    # print(entropy_parametr[0])
    for i in entropy_parametr[0]:
        entropy_array.append(i)
    for k in range(1, 10):
        entropy_array.append(k)

    # print(entropy_array)

    buf = 0
    j = 0

    for i in range(2, 19):
        # print(entropy_array[i])
        buf = buf + (int(entropy_array[i])+i)**3
        j = j + 1
        if (j % 3 == 0):
            keys_map_code.append(buf % 60)
            buf = 0

    # print(keys_map_code)

    map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
           'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
           'Y', 'Z']

    for i in keys_map_code:
        key.append(map[i])

    # print("KEY:", key)

    print("\nНажмите любую клавишу чтобы продолжить...")
    input()

    data_for_server = ""
    for i in key:
        data_for_server += i

    sock = socket.socket()
    sock.connect(('localhost', 2020))
    sock.send(data_for_server.encode())
    sock.close()


if __name__ == "__main__":
    interface_main()
