from recognize_passport import Recognize
import pytest


def output_format(param):
    return f"{param[0]}"


class TestRecongnize:
    def setup(self):
        self.test_results = {
            'type':             ('PN',          'PN',           'PN',           'PN'),
            'country':          ('RUS',         'RUS',          'RUS',          'RUS'),
            'nationality':      ('RUS',         'RUS',          'RUS',          'RUS'),
            'surname':          ('БЕЛЯНЧЕВА',   'ИВАНОВА',      'КОЛОСОВ',      'ЛЕБЕДЕВ'),
            'name':             ('ОЛЬГА',       'АНАСТАСИЯ',    'ПАВЕЛ',        'АНДРЕЙ'),
            'patronymic':       ('ВИКТОРОВНА',  'ВЛАДИМИРОВНА', 'ОЛЕГОВИЧ',     'АЛЕКСЕЕВИЧ'),
            'sex':              ('ЖЕН.',        'ЖЕН.',         'МУЖ.',         'МУЖ.'),
            'birth_day':        ('05.07.1979',  '31.12.1990',   '13.03.1991',   '25.04.1981'),
            'passport_number':  ('373914',      '303532',       '822880',       '745905'),
            'passport_series':  ('4511',        '4011',         '4612',         '3914'),
            'extradition_day':  ('10.04.2012',  '21.07.2011',   '26.09.2012',   '02.12.2014'),
            'unit_code':        ('770-121',     '780-052',      '500-037',      '910-011'),
        }
        self.recongnizer = Recognize()

    @pytest.mark.parametrize(
        "file_mas",
        [
            ('./tests/passport_test0.jpg', 0),
            ('./tests/passport_test1.jpg', 1),
            ('./tests/passport_test2.jpg', 2),
            # ('./tests/passport_test3.jpg', 3),
        ],
        ids=output_format
    )
    def test(self, file_mas):
        path_file, number_file = file_mas
        data = self.recongnizer.recongize_file(path_file)
        print(data)
        for key in self.test_results:
            assert data[key] == self.test_results[key][number_file]
