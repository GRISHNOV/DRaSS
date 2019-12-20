import os
import time
from collections import OrderedDict

from recognition.recognize_passport import Recognize
from storage.user_data import load_user_data
from terminal_interface.menu import clear_terminal


class EnterData:
    def __init__(self):
        self.options = [1, 2]
        self.data_passport = OrderedDict()

        self.recognizer = Recognize()

    def data_correct(self):
        if len(self.data_passport) == 0:
            return None
        for field in Recognize.map_field_latin_to_cyrillic:
            if field not in self.data_passport:
                return False
        return True

    def _send_to_db(self, MK, storage_name):
        data_string = ""
        data_result = ""
        for key, value in self.data_passport.items():
            data_string += key + "::" + value + ";;"
        for char in data_string:
            data_result += f"{ord(char):04}"
        load_user_data(MK, storage_name, data_result)
        return True

    def check_input_data(self):
        result = None
        print("------------------------------")
        print("Проверьте правильность следующих данных: ")
        for field in self.data_passport:
            print(f"{field}: {self.data_passport[field]} (д/н)", end=" ")
            result = input()
            if result in ['н', 'нет', 'n', 'no']:
                print(f"Введите корректное поле \"{field}\": ", end="")
                self.data_passport[i] = input()

        result = True
        for field in Recognize.map_field_latin_to_cyrillic.values():
            if result:
                print("------------------------------")
                print("Введите недостающие данные:")
                result = False
            if field not in self.data_passport:
                print(f"{field}: ", end="")
                self.data_passport[field] = input()

    def _input_passport_from_file(self):
        print("Введите путь к изображению с паспортом")
        path_to_passport = input()
        self.data_passport = self.recognizer.recognize_file_tr(
            path_to_passport)

        if self.data_correct() is None:
            print("------------------------------")
            print("Изображение плохо обработалось. Введите данные вручную.")
            self._input_passport_from_terminal()
        elif not self.data_correct():
            self.check_input_data()
        return

    def _input_passport_from_terminal(self):
        print("Введите данные паспорта:")
        for field in Recognize.map_field_latin_to_cyrillic.values():
            print(f"{field}: ", end="")
            self.data_passport[field] = input()
        return

    def input_passport(self, MK, storage_name):
        if MK == "exit":
            print("Сначала подключитесь к БД (connect).")
            time.sleep(2)
            return

        print('''
В каком формате вы хотите загрузить паспорт? (выберете цифру)
{}. Распознавание данных из скана паспорта;
{}. Ввод с консоли данных паспорта.
'''.format(*self.options)
        )
        try:
            option = int(input())
            if option not in self.options:
                raise ValueError
        except ValueError:
            print("НЕПРАВИЛЬНОЕ ЗНАЧЕНИЕ")
            time.sleep(1)
            return

        clear_terminal()
        if option == 1:
            self._input_passport_from_file()
        else:
            self._input_passport_from_terminal()

        print("------------------------------")
        print("Итоговые загружаемые данные в БД:")
        enumerate
        for i, field in enumerate(self.data_passport, 1):
            print(f"{i:2}. {field}: {self.data_passport[field]}")
        print("------------------------------")
        print("Отправить данные в БД? (д/н)", end=" ")
        result_char = input()
        if result_char in ['н', 'нет', 'n', 'no']:
            print("Загрузка в БД отменена.")
            return

        if not self._send_to_db(MK, storage_name):
            print("Ошибка при загрузки в БД.")
        else:
            print("Успешно загружено в БД.")
        time.sleep(2)
        return
