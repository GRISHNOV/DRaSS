import argparse
import sys
import io
import pytest

from passporteye import read_mrz
from collections import OrderedDict


class Recognize:
    map_field_latin_to_cyrillic = OrderedDict({
        'surname': 'Фамилия',
        'name': 'Имя',
        'patronymic': 'Отчество',
        'sex': 'Пол',
        'birth_day': 'Дата рождения',
        'extradition_day': 'Дата выдачи',
        'passport_number': 'Номер паспорта',
        'passport_series': 'Серия паспорта',
        'unit_code': 'Код подразделения',
    })

    def __init__(self):
        self._map_latin_to_cyrillic = {
            'A': 'А', 'B': 'Б',	'V': 'В',
            'G': 'Г', 'D': 'Д', 'E': 'Е',
            '2': 'Ё', 'J': 'Ж',	'Z': 'З',
            'I': 'И', 'Q': 'Й', 'K': 'К',
            'L': 'Л', 'M': 'М',	'N': 'Н',
            'O': 'О', 'P': 'П', 'R': 'Р',
            'S': 'С', 'T': 'Т', 'U': 'У',
            'F': 'Ф', 'H': 'Х', 'C': 'Ц',
            '3': 'Ч', '4': 'Ш', 'W': 'Щ',
            'X': 'Ъ', 'Y': 'Ы', '9': 'Ь',
            '6': 'Э', '7': 'Ю', '8': 'Я',
        }
        self._map_sex = {
            'M': 'МУЖ.',
            'F': 'ЖЕН.',
        }
        self._max_year_20th = 50

    def recognize_file_tr(self, path_to_file):
        correct_data = self.recongize_file(path_to_file)

        correct_data_russia = OrderedDict()
        if correct_data is None:
            return correct_data_russia
        
        for field, value in self.map_field_latin_to_cyrillic.items():
            if field in correct_data:
                correct_data_russia[value] = correct_data[field]
        return correct_data_russia

    def recongize_file(self, path_to_file):
        try:
            fd = open(path_to_file, 'rb')
        except FileNotFoundError:
            return None
        return self.recognize_fd(fd)

    def recognize_fd(self, data):
        mrz_data = self.get_mrz(data)
        if not mrz_data:
            return None
        recogn_data = mrz_data.to_dict()

        name, patronymic = [None] * 2
        if recogn_data.get('names'):
            name, patronymic = recogn_data.get('names').split()
        
        correct_data = OrderedDict({
            'type':         recogn_data.get('type'),
            'country':      recogn_data.get('country'),
            'nationality':  recogn_data.get('nationality'),

            'surname':      self._translate_latin_to_cyrillic(recogn_data.get('surname')),
            'name':         self._translate_latin_to_cyrillic(name),
            'patronymic':   self._translate_latin_to_cyrillic(patronymic),
            'sex':          self._map_sex.get(recogn_data.get('sex')),
        })

        if recogn_data.get('valid_date_of_birth'):
            correct_data['birth_day'] = self._get_day_correct_view(
                recogn_data['date_of_birth'])

        if recogn_data.get('valid_number'):
            correct_data['passport_number'] = recogn_data['number'][3:9]

        if recogn_data.get('valid_personal_number'):
            if recogn_data.get('valid_number'):
                correct_data['passport_series'] = recogn_data['number'][0:3] + \
                    recogn_data['personal_number'][0]
            correct_data['extradition_day'] = self._get_day_correct_view(
                recogn_data['personal_number'][1:7])
            correct_data['unit_code'] = recogn_data['personal_number'][7:10] + \
                '-' + recogn_data['personal_number'][10:13]

        return correct_data

    def get_mrz(self, data):
        mrz = read_mrz(data, extra_cmdline_params='--oem 0')
        return mrz

    def _translate_latin_to_cyrillic(self, word):
        if not word:
            return None
        for char in self._map_latin_to_cyrillic:
            word = word.replace(char, self._map_latin_to_cyrillic[char])
        return word

    def _get_day_correct_view(self, day_number):
        return \
            day_number[4:] + '.' + \
            day_number[2:4] + '.' + \
            ('20' if int(day_number[:2]) < self._max_year_20th else '19') + \
            day_number[:2]


class ArgTestAction(argparse.Action):
    path_to_file_test = "./tests.py"

    def __init__(self,
                 option_strings,
                 dest='test',
                 default=False,
                 help=None):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        pytest.main(["-v", self.path_to_file_test])
        parser.exit()


def main():
    parser = argparse.ArgumentParser(
        description='Function for recognition of passport and cards'
    )
    parser.add_argument(
        'infile',
        type=argparse.FileType('rb'),
        help='input file with text for recognition'
    )
    parser.add_argument(
        '-t', '--test',
        action=ArgTestAction,
        help='test this function and exit'
    )
    args = parser.parse_args(sys.argv[1:])

    recogniser = Recognize()
    data = recogniser.recognize_fd(args.infile)
    print(data)


if __name__ == "__main__":
    main()
