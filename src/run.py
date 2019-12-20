from terminal_interface.menu import clear_terminal, print_welcome, print_menu
from storage.connect import connect_storage
from storage.create import create_storage

if __name__ == "__main__":
    result = "ОЖИДАЕТСЯ ВВОД КОМАНДЫ"
    while(True):
        clear_terminal()
        print_welcome()
        print_menu(result)

        user_input_command = input()
        if user_input_command == "create":
            clear_terminal()
            create_storage()
            result = "УСПЕШНОЕ СОЗДАНИЕ ХРАНИЛИЩА"
        elif user_input_command == "connect":
            clear_terminal()
            connect_storage()
            result = "УСПЕШНОЕ ПОДКЛЮЧЕНИЕ К ХРАНИЛИЩУ"
        elif user_input_command == "exit":
            clear_terminal()
            exit(0)
        else:
            result = "ВВЕДЕНА НЕКОРРЕКТНАЯ КОМАНДА"

    clear_terminal()
