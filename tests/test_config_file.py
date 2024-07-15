from pytest import fixture, raises

from errors import ConfigFileError, DataFileError, OutputDataError
from math_analyser import ConfigFileData, parse_configuration_file
from tests.settings import TestData


@fixture
def test_config_parameters():
    return {'analysis_mode': 'INTS',
            'math_point': 12.75,
            'data_format': 'JSON',
            'data_file': TestData.get_json_test_data_file(),
            'output_file_format': 'TXT',
            'output_file_path': TestData.get_output_file()}


def test_no_config_file():
    """The configuration file does not exist."""
    not_existing_config_file = TestData.get_invalid_file_path()
    with raises(ConfigFileError):
        parse_configuration_file(not_existing_config_file)


def test_invalid_data_file_format(test_config_parameters):
    """The data file format is not valid."""
    test_config_parameters['data_format'] = 'PDF'
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_invalid_data_file_path(test_config_parameters):
    """The path to the data file is invalid."""
    test_config_parameters['data_file'] = TestData.get_invalid_file_path()
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(DataFileError):
        test_config_data.verify_config_data()


def test_different_input_file_format_in_data_format_and_data_path(test_config_parameters):
    """The input data file format does not match the one specified in the path."""
    test_config_parameters['data_format'] = 'XML'
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_different_output_file_format_in_data_format_and_data_path(test_config_parameters):
    """The output data file format does not match the one specified in the path."""
    test_config_parameters['output_file_path'] = f'{TestData.get_output_file()}.json'
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_invalid_output_file_format(test_config_parameters):
    """The output file format is invalid."""
    test_config_parameters['output_file_format'] = 'PDF'
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_no_output_file_path(test_config_parameters):
    """The path to the output file is not specified."""
    test_config_parameters['output_file_path'] = ''
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_invalid_output_file_path(test_config_parameters):
    """The directory for the output file does not exist."""
    test_config_parameters['output_file_path'] = TestData.get_invalid_file_path()
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(OutputDataError):
        test_config_data.verify_config_data()


def test_invalid_mode(test_config_parameters):
    """The invalid mode is specified."""
    test_config_parameters['analysis_mode'] = 'ERR'
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_no_point(test_config_parameters):
    """The point for AFFL mode is invalid: point = {None}"""
    test_config_parameters['analysis_mode'] = 'AFFL'
    test_config_parameters['math_point'] = None
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_string_point(test_config_parameters):
    """The point for AFFL mode is invalid: point = {string}"""
    test_config_parameters['analysis_mode'] = 'AFFL'
    test_config_parameters['math_point'] = 'asd'
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_infinity_point(test_config_parameters):
    """The point for AFFL mode is invalid: point = -inf"""
    test_config_parameters['analysis_mode'] = 'AFFL'
    test_config_parameters['math_point'] = float('-inf')
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()


def test_infinity_point_2(test_config_parameters):
    """The point for AFFL mode is invalid: point = +inf"""
    test_config_parameters['analysis_mode'] = 'AFFL'
    test_config_parameters['math_point'] = float('inf')
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(ConfigFileError):
        test_config_data.verify_config_data()
