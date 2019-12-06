import argparse
import sys
import io

from passporteye import read_mrz
from collections import OrderedDict


def translate(name):
    slovar = {
        'A': 'А', 'B': 'Б',	'V': 'В', 'G': 'Г',	
        'D': 'Д', 'E': 'Е',	'2': 'Ё', 'J': 'Ж',	
        'Z': 'З', 'I': 'И',	'Q': 'Й', 'K': 'К',	
        'L': 'Л', 'M': 'М',	'N': 'Н', 'O': 'О',	
        'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т',
        'U': 'У', 'F': 'Ф', 'H': 'Х', 'C': 'Ц',
        '3': 'Ч', '4': 'Ш', 'W': 'Щ', 'X': 'Ъ',
        'Y': 'Ы', '9': 'Ь', '6': 'Э', '7': 'Ю',
        '8': 'Я'
    }
        
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


def get_correct_day(day):
    return day[4:] + '.' + day[2:4] + '.' + \
        ('20' if int(day[:2]) < 50 else '19') + day[:2]


def recognize_data(data):
    mrz = read_mrz(data, extra_cmdline_params='--oem 0')
    recogn_data = mrz.to_dict()
    print(recogn_data)

    name, patronymic = recogn_data['names'].split()
    correct_data = OrderedDict({
        'type': recogn_data['type'],
        'country': recogn_data['country'],
        'nationality': recogn_data['nationality'],
        'surname': translate(recogn_data['surname']),
        'name': translate(name),
        'patronymic': translate(patronymic),
        'sex': 'МУЖ.' if recogn_data['sex'] == 'M' else 'ЖЕН.'
    })

    if recogn_data['valid_date_of_birth']:
        correct_data['birth_day'] = get_correct_day(recogn_data['date_of_birth']) 
    
    if recogn_data['valid_number']:
        correct_data['passport_number'] = recogn_data['number'][3:9]

    if recogn_data['valid_personal_number']:
        if recogn_data['valid_number']:
            correct_data['passport_series'] = recogn_data['number'][0:3] + recogn_data['personal_number'][0]
        correct_data['extradition_day'] = get_correct_day(recogn_data['personal_number'][1:7])
        correct_data['unit_code'] = recogn_data['personal_number'][7:10] + '-' + recogn_data['personal_number'][10:13]
    
    print(correct_data)
    return recogn_data


def main():
    parser = argparse.ArgumentParser(description='Function for recognition of passport and cards')
    parser.add_argument('infile', type=argparse.FileType('rb'), help='input file with text for recognition')
    parser.add_argument('-t', '--test', action='store_true', help='provide testing this function and exit')

    args = parser.parse_args()

    recognize_data(args.infile)


if __name__=="__main__":
    main()
