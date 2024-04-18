import unittest

from errors import *
from settings import *


class ConfigurationFileTest(unittest.TestCase):
    """Tests the parsing of the configuration data file in case of invalid data."""

    def setUp(self) -> None:
        self.test_output_file = TestData.get_output_file()
        self.test_config_parameters = {'analysis_mode': 'INTS',
                                       'math_point': 12.75,
                                       'data_format': 'JSON',
                                       'data_file': TestData.get_json_test_data_file(),
                                       'output_file_format': 'TXT',
                                       'output_file_path': self.test_output_file}

    def test_no_config_file(self):
        """The configuration file does not exist."""
        not_existing_config_file = TestData.get_invalid_file_path()
        with self.assertRaises(ConfigFileNotFoundError):
            parse_configuration_file(not_existing_config_file)

    def test_invalid_data_file_format(self):
        """The data file format is not valid."""
        self.test_config_parameters['data_format'] = 'PDF'
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_invalid_data_file_path(self):
        """The path to the data file is invalid."""
        self.test_config_parameters['data_file'] = TestData.get_invalid_file_path()
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(DataFileNotFoundError):
            test_config_data.verify_config_data()

    def test_different_input_file_format_in_data_format_and_data_path(self):
        """The input data file format does not match the one specified in the path."""
        self.test_config_parameters['data_format'] = 'XML'
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_different_output_file_format_in_data_format_and_data_path(self):
        """The output data file format does not match the one specified in the path."""
        self.test_config_parameters['output_file_path'] = f'{self.test_output_file}.json'
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_invalid_output_file_format(self):
        """The output file format is invalid."""
        self.test_config_parameters['output_file_format'] = 'PDF'
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_no_output_file_path(self):
        """The path to the output file is not specified."""
        self.test_config_parameters['output_file_path'] = ''
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_invalid_output_file_path(self):
        """The directory for the output file does not exist."""
        self.test_config_parameters['output_file_path'] = TestData.get_invalid_file_path()
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(OutputDirectoryNotFoundError):
            test_config_data.verify_config_data()

    def test_invalid_mode(self):
        """The invalid mode is specified."""
        self.test_config_parameters['analysis_mode'] = 'ERR'
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_no_point(self):
        """The point for AFFL mode is invalid: point = {None}"""
        self.test_config_parameters['analysis_mode'] = 'AFFL'
        self.test_config_parameters['math_point'] = None
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_string_point(self):
        """The point for AFFL mode is invalid: point = {string}"""
        self.test_config_parameters['analysis_mode'] = 'AFFL'
        self.test_config_parameters['math_point'] = 'asd'
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_infinity_point(self):
        """The point for AFFL mode is invalid: point = -inf"""
        self.test_config_parameters['analysis_mode'] = 'AFFL'
        self.test_config_parameters['math_point'] = float('-inf')
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_infinity_point_2(self):
        """The point for AFFL mode is invalid: point = +inf"""
        self.test_config_parameters['analysis_mode'] = 'AFFL'
        self.test_config_parameters['math_point'] = float('inf')
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(ConfigFileParsingError):
            test_config_data.verify_config_data()
