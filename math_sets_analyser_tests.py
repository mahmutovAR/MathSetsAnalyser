import unittest
from tempfile import NamedTemporaryFile

import math_sets_analyser
import math_sets_analyser_run
from math_analyser import config_data
from math_sets_analyser_run import *
from tests.errors import TestFailedError


def create_config_file_for_affl_mode(input_file_path: str, input_data: dict) -> None:
    """Creates at given path config file for AFFL mode."""
    test_config_ini = ConfigParser()

    test_mode = input_data['mode']
    test_point = input_data['point']
    test_input_format = input_data['data_format']
    test_input_path = input_data['data_path']
    test_output_format = input_data['output_format']
    test_output_path = input_data['output_path']

    test_config_ini['general'] = {'mode': test_mode, 'point': test_point}
    test_config_ini['input'] = {'format': test_input_format,
                                'path': test_input_path}
    test_config_ini['output'] = {'format': test_output_format,
                                 'path': test_output_path}
    with open(input_file_path, 'w') as config_file:
        test_config_ini.write(config_file)


def create_config_file_for_ints_mode(input_file_path: str, input_data: dict) -> None:
    """Creates at given path config file for INTS mode."""
    test_config_ini = ConfigParser()

    test_mode = input_data['mode']
    test_input_format = input_data['data_format']
    test_input_path = input_data['data_path']
    test_output_format = input_data['output_format']
    test_output_path = input_data['output_path']

    test_config_ini['general'] = {'mode': test_mode}
    test_config_ini['input'] = {'format': test_input_format,
                                'path': test_input_path}
    test_config_ini['output'] = {'format': test_output_format,
                                 'path': test_output_path}
    with open(input_file_path, 'w') as config_file:
        test_config_ini.write(config_file)


def create_json_test_data_file(input_file_path: str, input_data: dict) -> None:
    """Creates JSON data file at given path."""
    json_data = dict()
    for math_set_name in input_data:
        json_data[math_set_name] = str(input_data[math_set_name])
    with open(input_file_path, 'w') as json_data_file:
        json.dump(json_data, json_data_file)


def create_txt_test_data_file(input_file_path: str, input_data: dict) -> None:
    """Creates TXT data file at given path."""
    with open(input_file_path, 'w') as txt_data_file:
        for math_set_name, math_subrange in input_data.items():
            txt_data_file.write(f'{math_set_name}\n{math_subrange}\n')


def create_xml_test_data_file(input_file_path: str, input_data: dict) -> None:
    """Creates XML data file at given path."""
    template = PageTemplateLoader(os_path_join(abspath(dirname(__file__)), 'tests', 'templates'))
    tmpl = template['input_temp.pt']
    with open(input_file_path, 'w') as xml_output_file:
        data_for_xml = tmpl(ini_data=input_data)
        xml_output_file.write(data_for_xml)


def get_data_from_json_file(input_file: str) -> dict:
    """Returns dict object with data from inputted JSON file."""
    with open(input_file) as json_file:
        json_file_data = json.load(json_file)

    return json_file_data


def get_data_from_txt_file(input_file: str) -> dict:
    """Returns dict object with data from inputted TXT file."""
    with open(input_file, 'r', newline='') as txt_file:
        file_title = txt_file.readline().rstrip()
        file_data = txt_file.readline().rstrip()

    return {file_title: file_data}


def get_data_from_xml_file(input_file: str) -> dict:
    """Returns dict object with data from inputted XML file."""
    with open(input_file) as xml_file:
        file_data = xml_file.read()
    bs_object = BeautifulSoup(file_data, 'lxml')
    output_data = bs_object.find('scriptoutput')

    result_title = output_data.get('title')
    result_data = output_data.find('value').get_text()

    return {result_title: result_data}


class ConfigurationFileTest(unittest.TestCase):
    """Tests the parsing of the configuration data file in case of invalid data."""
    def setUp(self) -> None:
        self.math_sets = {'set_type_1': [('-inf', '+inf')],
                          'set_type_2': [('-inf', -10.37), (10.41, '+inf')],
                          'set_type_3': [('-inf', 99.4)],
                          'set_type_4': [(-98, '+inf')],
                          'set_type_5': [('-inf', -32.08), (-17, 22.2), (54, 57)],
                          'set_type_6': [('-inf', -41), (-18, 24), (51, 62), (103, '+inf')],
                          'set_type_7': [(-89.11, -61.07), (-24.9, '+inf')],
                          'set_type_8': [(-77, 61.04), 54],
                          'set_type_9': [(-89, -61), (-43, -12), (10, 27), (61, 72)]}

        self.invalid_math_sets = {'set_type_1': '-inf',
                                  'set_type_2': [(10, '+asd')],
                                  'set_type_3': 547,
                                  'set_type_4': '',
                                  'set_type_5': {47, 211}}

        self.test_output_file = os_path_join('home', 'user', 'script output')

    def test_no_config_file(self):
        """The configuration file does not exist."""
        not_existing_config_file = os_path_join('home', 'user', 'invalid config.ini')
        with self.assertRaises(math_sets_analyser.ConfigFileNotFoundError):
            math_sets_analyser.parse_configuration_data_file(not_existing_config_file)

    def test_invalid_data_file_format(self):
        """The data file format is not valid."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'INTS',
                                    'data_format': 'PDF',
                                    'data_path': temp_data_file.name,
                                    'output_format': 'TXT',
                                    'output_path': self.test_output_file}
                create_config_file_for_ints_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.math_sets)

                with self.assertRaises(config_data.ConfigFileParsingError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_invalid_data_file_path(self):
        """The path to the data file is invalid."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'INTS',
                                    'data_format': 'PDF',
                                    'data_path': f'{temp_data_file.name}-err',
                                    'output_format': 'TXT',
                                    'output_path': self.test_output_file}
                create_config_file_for_ints_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.math_sets)

                with self.assertRaises(config_data.ConfigFileParsingError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_different_file_format_in_data_format_and_data_path(self):
        """The data file format does not match the one specified in the path."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'INTS',
                                    'data_format': 'XML',
                                    'data_path': f'{temp_data_file.name}.txt',
                                    'output_format': 'TXT',
                                    'output_path': self.test_output_file}
                create_config_file_for_ints_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.invalid_math_sets)

                with self.assertRaises(config_data.ConfigFileParsingError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_invalid_output_file_format(self):
        """The output file format is invalid."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'INTS',
                                    'data_format': 'TXT',
                                    'data_path': temp_data_file.name,
                                    'output_format': 'PDF',
                                    'output_path': self.test_output_file}
                create_config_file_for_ints_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.math_sets)

                with self.assertRaises(config_data.ConfigFileParsingError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_no_output_file_path(self):
        """The path to the output file is not specified."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'INTS',
                                    'data_format': 'TXT',
                                    'data_path': temp_data_file.name,
                                    'output_format': 'TXT',
                                    'output_path': ''}
                create_config_file_for_ints_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.math_sets)

                with self.assertRaises(config_data.ConfigFileParsingError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_invalid_output_file_path(self):
        """The directory for the output file does not exist."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'INTS',
                                    'data_format': 'TXT',
                                    'data_path': temp_data_file.name,
                                    'output_format': 'TXT',
                                    'output_path': self.test_output_file}
                create_config_file_for_ints_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.math_sets)

                with self.assertRaises(config_data.OutputDirectoryNotFoundError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_invalid_mode(self):
        """The invalid mode is specified."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'ERR',
                                    'data_format': 'TXT',
                                    'data_path': temp_data_file.name,
                                    'output_format': 'TXT',
                                    'output_path': self.test_output_file}
                create_config_file_for_ints_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.math_sets)

                with self.assertRaises(config_data.ConfigFileParsingError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_invalid_point(self):
        """The point for AFFL mode is invalid. Tested for the following cases:
            "point ="
            "point = {string}"
            "{no row}"
        """
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                config_file_data = {'mode': 'AFFL',
                                    'point': '',
                                    'data_format': 'TXT',
                                    'data_path': temp_data_file.name,
                                    'output_format': 'TXT',
                                    'output_path': self.test_output_file}
                create_config_file_for_affl_mode(temp_config_file.name, config_file_data)
                create_txt_test_data_file(temp_data_file.name, self.math_sets)

                with self.assertRaises(config_data.ConfigFileParsingError):
                    math_sets_analyser.parse_configuration_data_file(temp_config_file.name)


class DataFileTest(unittest.TestCase):
    """Tests getting data from data files in case of invalid data.
    It also tests getting data from JSON TXT and XML data files."""
    def setUp(self) -> None:
        self.math_sets = {'set_type_1': [('-inf', '+inf')],
                          'set_type_2': [('-inf', -10), (10, '+inf')],
                          'set_type_3': [('-inf', 99)],
                          'set_type_4': [(-98, '+inf')],
                          'set_type_5': [('-inf', -32), (-17, 22)],
                          'set_type_6': [('-inf', -41), (-18, 24), (51, 62), (103, '+inf')],
                          'set_type_7': [(-89, -61), (-24, '+inf')],
                          'set_type_8': [(-77, 61)],
                          'set_type_9': [(-89, -61), (-43, -12), (10, 27), (61, 72)]}

        self.math_set_is_point = {'set_type_1': [('-inf', 57)],
                                  'set_type_2': [('-inf', -10), (10, '+inf')],
                                  'set_type_3': [57],
                                  'set_type_4': [(57, '+inf')]}

        self.invalid_math_sets = {'set_type_1': [(-25, -10), (10, 12)],
                                  'set_type_2': [(-89, -61), (-43, -12)]}

        self.infinity_math_sets = {'set_type_1': [('-inf', '+inf')],
                                   'set_type_2': [('-inf', '+inf')],
                                   'set_type_3': [('-inf', '+inf')]}

        self.ranges_and_point = {'set_type_1': [('-inf', 10), (68, '+inf')],
                                 'set_type_2': [('-inf', -3), (10, 15), 72, (85, 99)],
                                 'set_type_3': [('-inf', -12), (-25, 10), 72, 87, (90, 120)]}

        self.config_file_data = {'mode': 'INTS',
                                 'output_format': 'TXT'}

        self.math_sets_intersection = [(-77, -61), (-17, -12), (10, 22)]
        self.math_sets_intersection_at_point = [57]
        self.math_sets_intersection_for_ranges_and_points = [('-inf', -12), 10, 72, 87, (90, 99)]

        self.test_output_file = os_path_join('home', 'user', 'script output')

    def test_no_data_file(self):
        """No data file."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            self.config_file_data['data_path'] = '/home/data/dir/path'
            self.config_file_data['output_path'] = '/home/output/dir/path/'
            self.config_file_data['data_format'] = 'TXT'

            create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)

            with self.assertRaises(math_sets_analyser.DataFileNotFoundError):
                math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

    def test_string_data_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
        a 'str' object instead of required 'list'."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'JSON'
                    self.invalid_math_sets['err_set'] = '"-inf", 57, 74'

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_json_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_numeric_data_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
         an 'int' object instead of required 'list'."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'TXT'
                    self.invalid_math_sets['err_set'] = 547

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_no_data(self):
        """One of the initial math sets in the data file has an invalid value: an empty row."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'XML'
                    self.invalid_math_sets['err_set'] = ""

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_xml_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_empty_list(self):
        """One of the initial math sets in the data file has an invalid value: an empty 'list'."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'JSON'
                    self.invalid_math_sets['err_set'] = []

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_json_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_invalid_string_data(self):
        """One of the initial math sets in the data file has an invalid value,
        invalid 'str' value at math range."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'TXT'
                    self.invalid_math_sets['err_set'] = [('qw', 'asd')]

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_range_with_less_than_two_points(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with less than two points."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'XML'
                    self.invalid_math_sets['err_set'] = [(47,)]

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_xml_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_range_with_more_than_two_points(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with more than two points."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'JSON'
                    self.invalid_math_sets['err_set'] = [(123, 23, 23)]

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_json_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_invalid_semi_infinite_range(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with invalid semi-infinite range."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'TXT'
                    self.invalid_math_sets['err_set'] = [(12, '-inf')]

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_set_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
        'set' object instead of required 'list'."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'XML'
                    self.invalid_math_sets['err_set'] = {12, 34}

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_xml_test_data_file(temp_data_file.name, self.invalid_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.DataGettingError):
                        math_sets_analyser_run.main(config_file_data)

    def test_all_infinity_ranges(self):
        """All initial math sets in the data file are infinite ranges, [('-inf', '+inf')]."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['data_format'] = 'XML'

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_xml_test_data_file(temp_data_file.name, self.infinity_math_sets)
                    config_file_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.InfiniteSetError):
                        math_sets_analyser_run.main(config_file_data)

    def test_math_set_with_point(self):
        """Tests getting initial math sets with math point from data files."""
        with NamedTemporaryFile('w+t') as temp_data_file:
            create_txt_test_data_file(temp_data_file.name, self.math_set_is_point)
            json_config = ConfigData('TXT', temp_data_file.name, 'JSON', self.test_output_file, 'INTS', None)
            intersection_result = math_sets_analyser_run.determine_initial_math_sets_intersection(json_config)

            if self.math_sets_intersection_at_point != intersection_result:
                raise TestFailedError('getting data from JSON data file in case of initial math point instead of set',
                                      None)

    def test_json_data_file(self):
        """Tests getting initial math sets from JSON data files."""
        with NamedTemporaryFile('w+t') as temp_data_file:
            create_json_test_data_file(temp_data_file.name, self.math_sets)
            json_config = ConfigData('JSON', temp_data_file.name, 'JSON', self.test_output_file, 'INTS', None)
            intersection_result = math_sets_analyser_run.determine_initial_math_sets_intersection(json_config)

            if self.math_sets_intersection != intersection_result:
                raise TestFailedError('getting data from JSON data file', None)

    def test_txt_data_file(self):
        """Tests getting initial math sets from TXT data files."""
        with NamedTemporaryFile('w+t') as temp_data_file:
            create_txt_test_data_file(temp_data_file.name, self.math_sets)
            txt_config = ConfigData('TXT', temp_data_file.name, 'JSON', self.test_output_file, 'INTS', None)
            intersection_result = math_sets_analyser_run.determine_initial_math_sets_intersection(txt_config)

            if self.math_sets_intersection != intersection_result:
                raise TestFailedError('getting data from TXT data file', None)

    def test_xml_data_file(self):
        """Tests getting initial math sets from XML data files."""
        with NamedTemporaryFile('w+t') as temp_data_file:
            create_xml_test_data_file(temp_data_file.name, self.math_sets)
            xml_config = ConfigData('XML', temp_data_file.name, 'XML', self.test_output_file, 'INTS', None)
            intersection_result = math_sets_analyser_run.determine_initial_math_sets_intersection(xml_config)

            if self.math_sets_intersection != intersection_result:
                raise TestFailedError('getting data from XML data file', None)


class OutputFileTest(unittest.TestCase):
    """Tests generating script output files in JSON TXT and XML format.
    It also tests raising of OutputFileGeneratingError."""

    def setUp(self) -> None:
        self.test_output_title = 'The intersection of initial math sets'
        self.test_output_data = [(-77, -61), (-17, -12), (10, 22)]

        self.script_output_data = {
            'The intersection of initial math sets': '[(-77, -61), (-17, -12), (10, 22)]'}

    def test_OutputFileGeneratingError(self):
        """Tests raising of OutputFileGeneratingError. Tested for the following cases:
            [Errno 2] No such file or directory
            [Errno 13] Permission denied
        """
        with NamedTemporaryFile('w+t') as temp_data_file:
            output_file = '/home/err/file/path'
            test_config = ConfigData('TXT', temp_data_file.name, 'JSON', output_file, 'INTS', None)
            with self.assertRaises(math_sets_analyser.OutputFileGeneratingError):
                math_sets_analyser.output_script_data(test_config, 'test title', ['test', 'list'])

    def test_json_output_file(self):
        """Tests generating a JSON script output file."""
        with NamedTemporaryFile('w+t') as temp_output_file:
            math_sets_analyser.generate_json_output_file(temp_output_file.name,
                                                         self.test_output_title, self.test_output_data)
            json_output = get_data_from_json_file(temp_output_file.name)

            if self.script_output_data != json_output:
                raise TestFailedError('creating output JSON file', None)

    def test_txt_output_file(self):
        """Tests generating a TXT script output file."""
        with NamedTemporaryFile('w+t') as temp_output_file:
            math_sets_analyser.generate_txt_output_file(temp_output_file.name,
                                                        self.test_output_title, self.test_output_data)
            txt_output = get_data_from_txt_file(temp_output_file.name)

            if self.script_output_data != txt_output:
                raise TestFailedError('creating output TXT file', None)

    def test_xml_output_file(self):
        """Tests generating an XML script output file."""
        with NamedTemporaryFile('w+t') as temp_output_file:
            math_sets_analyser.generate_xml_output_file(temp_output_file.name,
                                                        self.test_output_title, self.test_output_data)
            xml_output = get_data_from_xml_file(temp_output_file.name)

            if self.script_output_data != xml_output:
                raise TestFailedError('creating output XML file', None)


class IntersectionModeTest(unittest.TestCase):
    """Tests the 'INTS' mode for various initial math sets."""
    def setUp(self) -> None:
        self.math_sets = {'set_type_1': [('-inf', '+inf')],
                          'set_type_2': [('-inf', -10.37), (10.41, '+inf')],
                          'set_type_3': [('-inf', 99.4)],
                          'set_type_4': [(-98, '+inf')],
                          'set_type_5': [('-inf', -32.08), (-17, 22.2), (54, 57)],
                          'set_type_6': [('-inf', -41), (-18, 24), (51, 62), (103, '+inf')],
                          'set_type_7': [(-89.11, -61.07), (-24.9, '+inf')],
                          'set_type_8': [(-77, 61.04), 54],
                          'set_type_9': [(-89, -61), (-43, -12), (10, 27), (61, 72)]}

        self.numeric_math_sets = {'set_type_1': [(-75, -41), (-18, 24), (51, 62)],
                                  'set_type_2': [(-77, 61)],
                                  'set_type_3': [(-89, -61), (-43, -12), (61, 72)]}

        self.semi_infinite_math_sets = {'set_type_1': [(-89, -61), (-12, "+inf")],
                                        'set_type_2': [(-97, "+inf")],
                                        'set_type_3': [("-inf", "+inf")]}

        self.math_sets_with_points = {'set_type_1': [(-89, 17.8), 24, (25, "+inf")],
                                      'set_type_2': [(-97, 2), (9.9, 24), (36.1, "+inf")],
                                      'set_type_3': [-77, -29, 42.7, (51.1, "+inf")]}

        self.one_initial_math_set = {'set_type_1': [(-25, -10), (10, 12)]}

        self.math_sets_without_intersection = {'set_type_1': [(-89, -61), (102, '+inf')],
                                               'set_type_2': [(-57, 35)],
                                               'set_type_3': [(-2, 16), (61, 72)]}

        self.config_file_data = {'mode': 'INTS',
                                 'data_format': 'TXT',
                                 'output_format': 'JSON'}

        self.math_sets_output = {
            'The intersection of initial math sets': '[(-77, -61.07), (-17, -12), (10.41, 22.2)]'}
        self.numeric_math_sets_output = {
            'The intersection of initial math sets': '[(-75, -61), (-43, -41), (-18, -12), 61]'}
        self.semi_infinite_math_sets_output = {
            'The intersection of initial math sets': "[(-89, -61), (-12, '+inf')]"}
        self.math_sets_with_points_output = {
            'The intersection of initial math sets': "[-77, -29, 42.7, (51.1, '+inf')]"}
        self.one_initial_math_set_output = {
            'The intersection of initial math sets': '[(-25, -10), (10, 12)]'}

    def test_all_types_of_math_sets(self):
        """'INTS' mode for all types of math sets."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.math_sets)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    intersection_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.math_sets_output != intersection_result:
                        raise TestFailedError('INTS mode for all types of initial math sets', None)

    def test_numeric_math_sets(self):
        """'INTS' mode for numeric math sets."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.numeric_math_sets)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    intersection_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.numeric_math_sets_output != intersection_result:
                        raise TestFailedError('INTS mode for only numeric initial math sets', None)

    def test_semi_infinite_math_sets(self):
        """'INTS' mode for math sets with semi-infinite ranges."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.semi_infinite_math_sets)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    intersection_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.semi_infinite_math_sets_output != intersection_result:
                        raise TestFailedError('INTS mode for semi-infinite math sets', None)

    def test_math_sets_with_points(self):
        """'INTS' mode for math sets with math points."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.math_sets_with_points)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    intersection_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.math_sets_with_points_output != intersection_result:
                        raise TestFailedError('INTS mode for math sets with points', None)

    def test_one_initial_math_set(self):
        """'INTS' mode for only one initial math sets."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.one_initial_math_set)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    intersection_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.one_initial_math_set_output != intersection_result:
                        raise TestFailedError('INTS mode for only one initial math set', None)

    def test_math_sets_without_intersection(self):
        """'INTS' mode for math sets without intersection."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name

                    create_config_file_for_ints_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.math_sets_without_intersection)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.NoIntersectionError):
                        math_sets_analyser_run.main(test_config_data)


class AffiliationModeTest(unittest.TestCase):
    """Tests the 'AFFL' mode for various initial math sets."""
    def setUp(self) -> None:
        self.semi_infinite_math_sets = {'set_type_1': [(-89, -61), (-12, '+inf')],
                                        'set_type_2': [(-57, '+inf')],
                                        'set_type_3': [('-inf', '+inf')]}

        self.numeric_math_sets = {'set_type_1': [(-89, -61), (-12, 28)],
                                  'set_type_2': [(-57, 35)],
                                  'set_type_3': [(-2, 16), (61, 72)]}

        self.two_nearest_endpoints_case = {'set_type_1': [('-inf', -10), (10, '+inf')],
                                           'set_type_2': [(-77, 61)],
                                           'set_type_3': [(-89, -61), (-43, -12), (10, 27), (61, 72)]}

        self.intersection_points_case = {'set_type_1': [(-89, 17.8), 24, (25, "+inf")],
                                         'set_type_2': [(-97, 2), (9.9, 24), (36.1, "+inf")],
                                         'set_type_3': [-77, -29, 42.7, (51.1, "+inf")]}

        self.math_sets_without_intersection = {'set_type_1': [(-89, -61), (102, '+inf')],
                                               'set_type_2': [(-57, 35)],
                                               'set_type_3': [(-2, 16), (61, 72)]}

        self.intersection_point_equal_to_given = {
            'The point of the initial math sets intersection is the predetermined point': '42.7'}

        self.intersection_point_do_not_equal_to_given = {
            'The nearest endpoint(s) to the predetermined point': '[-77, -29]'}

        self.config_file_data = {'mode': 'AFFL',
                                 'data_format': 'TXT',
                                 'output_format': 'JSON'}

        self.semi_infinite_math_sets_contain_point = {
            'The subrange of the initial math sets intersection with the predetermined point': "[(-12, '+inf')]"}
        self.semi_infinite_math_sets_do_not_contain_point = {
            'The nearest endpoint(s) to the predetermined point': '[-12]'}
        self.numeric_math_sets_contain_point = {
            'The subrange of the initial math sets intersection with the predetermined point': '[(-2, 16)]'}
        self.numeric_math_sets_do_not_contain_point = {
            'The nearest endpoint(s) to the predetermined point': '[16]'}
        self.two_nearest_endpoints_case_output = {
            'The nearest endpoint(s) to the predetermined point': '[-12, 10]'}

    def test_semi_infinite_math_sets_contain_point(self):
        """'AFFL' mode for math sets with semi-infinite ranges
        when the predetermined point belongs to the math intersection."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = -1.09

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.semi_infinite_math_sets)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    test_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.semi_infinite_math_sets_contain_point != test_result:
                        raise TestFailedError('INTS mode for all types of ini math sets', None)

    def test_semi_infinite_math_sets_do_not_contain_point(self):
        """'AFFL' mode for math sets with semi-infinite ranges
        when the predetermined point does not belong to the math intersection."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = -15.01

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.semi_infinite_math_sets)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    test_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.semi_infinite_math_sets_do_not_contain_point != test_result:
                        raise TestFailedError('INTS mode for all types of ini math sets', None)

    def test_numeric_math_sets_contain_point(self):
        """'AFFL' mode for the numeric math sets
        when the predetermined point belongs to the math intersection."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = 8.51

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.numeric_math_sets)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    test_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.numeric_math_sets_contain_point != test_result:
                        raise TestFailedError('INTS mode for only numeric ini math sets', None)

    def test_numeric_math_sets_do_not_contain_point(self):
        """'AFFL' mode for the numeric math sets
        when the predetermined point does not belong to the math intersection."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = 19.34

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.numeric_math_sets)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    test_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.numeric_math_sets_do_not_contain_point != test_result:
                        raise TestFailedError('INTS mode for only numeric ini math sets', None)

    def test_two_nearest_endpoints_case(self):
        """'AFFL' mode for the predetermined point which does not belong to the math intersection
        and has two nearest endpoints."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = -1

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.two_nearest_endpoints_case)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    test_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.two_nearest_endpoints_case_output != test_result:
                        raise TestFailedError('INTS mode for only numeric ini math sets', None)

    def test_intersection_point_equal_to_given(self):
        """'AFFL' mode for the predetermined point which equals to the math intersection point."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = 42.7

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.intersection_points_case)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    test_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.intersection_point_equal_to_given != test_result:
                        raise TestFailedError('INTS mode for only numeric ini math sets', None)

    def test_intersection_point_do_not_equal_to_given(self):
        """'AFFL' mode for the predetermined point which not equal to the math intersection point."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = -53

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.intersection_points_case)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)
                    math_sets_analyser_run.main(test_config_data)
                    test_result = get_data_from_json_file(f'{temp_output_file.name}.json')

                    if self.intersection_point_do_not_equal_to_given != test_result:
                        raise TestFailedError('INTS mode for only numeric ini math sets', None)

    def test_math_sets_without_intersection(self):
        """'AFFL' mode for math sets without intersection."""
        with NamedTemporaryFile('w+t') as temp_config_file:
            with NamedTemporaryFile('w+t') as temp_data_file:
                with NamedTemporaryFile('w+t') as temp_output_file:
                    self.config_file_data['data_path'] = temp_data_file.name
                    self.config_file_data['output_path'] = temp_output_file.name
                    self.config_file_data['point'] = 12.4

                    create_config_file_for_affl_mode(temp_config_file.name, self.config_file_data)
                    create_txt_test_data_file(temp_data_file.name, self.math_sets_without_intersection)
                    test_config_data = math_sets_analyser.parse_configuration_data_file(temp_config_file.name)

                    with self.assertRaises(math_sets_analyser.NoIntersectionError):
                        math_sets_analyser_run.main(test_config_data)


if __name__ == '__main__':
    unittest.main()
