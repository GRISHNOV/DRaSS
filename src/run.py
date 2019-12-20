from terminal_interface.menu import clear_terminal, print_welcome, print_menu
from storage.connect import connect_storage
from storage.create import create_storage

from storage.input_data import EnterData
from storage.out_data import output_data

if __name__ == "__main__":
    result = "ОЖИДАЕТСЯ ВВОД КОМАНДЫ"

    MK = "exit"
    storage_name = ""

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
            MK, storage_name = connect_storage()
            if MK == "exit":
                result = "НЕУСПЕШНОЕ ПОДКЛЮЧЕНИЕ К ХРАНИЛИЩУ"
            else:
                result = "УСПЕШНОЕ ПОДКЛЮЧЕНИЕ К ХРАНИЛИЩУ"
        elif user_input_command == "load":
            clear_terminal()
            enter_data = EnterData()
            enter_data.input_passport(MK, storage_name)
            result = "УСПЕШНАЯ ЗАГРУЗКА ДОКУМЕНТА"
        elif user_input_command == "get":
            clear_terminal()
            output_data(MK, storage_name)
            result = "УСПЕШНОЕ ПОЛУЧЕНИЕ ДОКУМЕНТА"
        elif user_input_command == "exit":
            clear_terminal()
            exit(0)
        else:
            result = "ВВЕДЕНА НЕКОРРЕКТНАЯ КОМАНДА"

    clear_terminal()
