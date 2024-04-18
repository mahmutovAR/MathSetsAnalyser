from json import dump as json_dump
from json import load as json_load

from configparser import ConfigParser
from os.path import abspath, dirname
from os.path import join as os_path_join
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup

import run_math_sets_analyser as run_msa
from math_analyser import *


class TestConfig:
    __slots__ = ['__script_dir']

    def __init__(self, script_dir):
        self.__script_dir = script_dir

    def get_script_dir(self) -> str:
        return self.__script_dir

    def get_json_test_data_file(self) -> str:
        return os_path_join(self.__script_dir, 'data files', 'data file.json')

    def get_txt_test_data_file(self) -> str:
        return os_path_join(self.__script_dir, 'data files', 'data file.txt')

    def get_xml_test_data_file(self) -> str:
        return os_path_join(self.__script_dir, 'data files', 'data file.xml')

    def get_output_file(self) -> str:
        return os_path_join(self.__script_dir, 'output file')

    def get_invalid_file_path(self) -> str:
        return os_path_join(self.__script_dir, 'invalid dir', 'output file')


TestData = TestConfig(abspath(dirname(__file__)))


def create_config_file_for_ints_mode(input_file_path: str, input_data: dict) -> None:
    """Creates at given path config file for INTS mode."""
    test_config_ini = ConfigParser()

    test_mode = input_data['analysis_mode']
    test_input_format = input_data['data_format']
    test_input_path = input_data['data_file']
    test_output_format = input_data['output_file_format']
    test_output_path = input_data['output_file_path']

    test_config_ini['general'] = {'mode': test_mode}
    test_config_ini['input'] = {'format': test_input_format,
                                'path': test_input_path}
    test_config_ini['output'] = {'format': test_output_format,
                                 'path': test_output_path}
    with open(input_file_path, 'w') as config_file:
        test_config_ini.write(config_file)


def create_config_file_for_affl_mode(input_file_path: str, input_data: dict) -> None:
    """Creates at given path config file for AFFL mode."""
    test_config_ini = ConfigParser()

    test_mode = input_data['analysis_mode']
    test_point = input_data['math_point']
    test_input_format = input_data['data_format']
    test_input_path = input_data['data_file']
    test_output_format = input_data['output_file_format']
    test_output_path = input_data['output_file_path']

    test_config_ini['general'] = {'mode': test_mode, 'point': test_point}
    test_config_ini['input'] = {'format': test_input_format,
                                'path': test_input_path}
    test_config_ini['output'] = {'format': test_output_format,
                                 'path': test_output_path}
    with open(input_file_path, 'w') as config_file:
        test_config_ini.write(config_file)


def create_json_test_data_file(input_file: str, input_data: list) -> None:
    """Creates JSON data file at given path."""
    with open(input_file, 'w') as json_data_file:
        json_dump(input_data, json_data_file)


def read_json_file(input_file: str) -> str:
    """Returns dict object with data from inputted JSON file."""
    with open(input_file) as json_file:
        file_data = json_load(json_file)
    return file_data


def read_txt_file(input_file: str) -> str:
    """Returns dict object with data from inputted TXT file."""
    with open(input_file, 'r', newline='') as txt_file:
        file_data = txt_file.readline().rstrip()
    return file_data


def read_xml_file(input_file: str) -> str:
    """Returns dict object with data from inputted XML file."""
    with open(input_file) as xml_file:
        file_data = xml_file.read()
    bs_object = BeautifulSoup(file_data, 'lxml')
    output_xml_file = bs_object.find('outputdata')
    file_data = output_xml_file.find('value').get_text()
    return file_data


def ints_mode_using_temp_files(ini_math_sets: list) -> list:
    """Tests 'INTS' mode with given initial parameters."""
    with TemporaryDirectory() as temp_dir:
        test_config_file = os_path_join(temp_dir, 'config.ini')
        test_data_file = os_path_join(temp_dir, 'data file')
        test_config_parameters = {'analysis_mode': 'INTS',
                                  'input_point': None,
                                  'data_format': 'JSON',
                                  'data_file': test_data_file,
                                  'output_file_format': 'JSON',
                                  'output_file_path': 'test output file'}

        create_config_file_for_ints_mode(test_config_file, test_config_parameters)
        create_json_test_data_file(test_data_file, ini_math_sets)

        test_configuration_data = parse_configuration_file(test_config_file)
        sorted_math_intersection = run_msa.determine_initial_math_sets_intersection(test_configuration_data)
        return sorted_math_intersection
