#!/usr/bin/env python3

import os

import ascii_interface


if __name__ == "__main__":

    result = "ОЖИДАЕТСЯ ВВОД КОМАНДЫ"
    while(True):
        ascii_interface.clr_terminal()
        ascii_interface.welcom()
        ascii_interface.main_welcom(result)
        
        user_input_command = input()
        if user_input_command == "create":
            ascii_interface.clr_terminal()
            os.system("./create_storage.py")
            print("Нажмите любую клавишу для возвращения в основное меню")
            input()
            result = "ОЖИДАЕТСЯ ВВОД КОМАНДЫ"
        elif user_input_command == "connect":
            ascii_interface.clr_terminal()
            os.system("./content_master.py")
            print("Нажмите любую клавишу для возвращения в основное меню")
            input()
            result = "ОЖИДАЕТСЯ ВВОД КОМАНДЫ"
        elif user_input_command == "exit":
            ascii_interface.clr_terminal()
            exit(0)
        else:
            result = "НЕКОРРЕКТНАЯ КОМАНДА"

    

    ascii_interface.clr_terminal()