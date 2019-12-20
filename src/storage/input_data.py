import os
import time
from recognition.recognize_passport import Recognize
from collections import OrderedDict


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

    def _send_to_db(self):
        return True

    def check_input_data(self):
        result = None
        print("Верны следующие данные? (д/н)")
        for i in self.data_passport:
            print(f"{i}: {self.data_passport[i]}")
            result = input()
            if result in ['н', 'n']:
                print(f"Введите корректное {i}")
                self.data_passport[i] = input()
        
        print("Введите недостающие данные")
        for field in Recognize.map_field_latin_to_cyrillic.values():
            if field not in self.data_passport:
                print(f"{field}: ", end="")
                self.data_passport[field] = input()

    def _input_passport_from_file(self):
        print("Введите путь к изображению с паспортом")
        path_to_passport = input()
        self.data_passport = self.recognizer.recognize_file_tr(path_to_passport)

        if self.data_correct() is None:
            print("Изображение плохо обработалось")
            self._input_passport_from_terminal()
        elif not self.data_correct():
            self.check_input_data()
        return

    def _input_passport_from_terminal(self):
        print("Введите данные паспорта")
        for field in Recognize.map_field_latin_to_cyrillic.values():
            print(f"{field}: ", end="")
            self.data_passport[field] = input()
        return

    def input_passport(self):
        print('''
В каком формате вы хотите загрузить паспорт? (выберете цифру) \n
{}. Распознавание данных из скана паспорта;\n
{}. Ввод с консоли данных паспорта.
'''.format(*self.options)
        )
        try:
            option = int(input())
            if option not in self.options:
                raise ValueError
        except ValueError:
            print("Неправильное значение")
            return
        
        if option == 1:
            self._input_passport_from_file()
        else:
            self._input_passport_from_terminal()
        
        print("Загружаемые данные в БД")
        print("-----------------------")
        for field, value in self.data_passport:
            print(f"{field}: {value}")
        print("----------------------------")
        print("Отправить данные в БД? (д/н)")
        result_char = input() 
        if result_char in ['н', 'n']:
            print("Загрузка отменена")
            return

        if not self._send_to_db():
            print("Ошибка при загрузки в БД")
        else:
            print("Успешно загружено в БД")
        time.sleep(1)
        return
