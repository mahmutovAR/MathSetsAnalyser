from errors import OutputDataError
from pytest import fixture, raises

from tests.settings import TemporaryDirectory, read_json_file, read_txt_file, read_xml_file
from os.path import join as os_path_join
from math_analyser import ConfigFileData, output_script_data


TEST_DATA = [(-77, -61), (-17, -12), (10, 22), (75, float('inf'))]


@fixture
def test_config_parameters():
    return {'analysis_mode': 'INTS',
            'math_point': 12.75,
            'data_format': 'JSON',
            'data_file': '/home/data file/initial math sets',
            'output_file_format': 'JSON',
            'output_file_path': '/home/script output files/report'}


def test_output_file_generating_error(test_config_parameters):
    """Tests raising of OutputFileGeneratingError. Tested for the following cases:
        [Errno 2] No such file or directory
        [Errno 13] Permission denied
    """
    test_config_data = ConfigFileData(**test_config_parameters)
    with raises(OutputDataError):
        output_script_data(test_config_data, ['test', 'list'])


def test_json_output_file(test_config_parameters):
    """Tests generating a JSON script output file."""
    with TemporaryDirectory() as temp_dir:
        test_config_parameters['output_file_format'] = 'JSON'
        test_output_file = os_path_join(temp_dir, 'output_test')
        test_config_parameters['output_file_path'] = test_output_file

        test_config_data = ConfigFileData(**test_config_parameters)

        output_script_data(test_config_data, TEST_DATA)
        json_output = read_json_file(f'{test_output_file}.json')
        assert str(TEST_DATA) == json_output


def test_txt_output_file(test_config_parameters):
    """Tests generating a TXT script output file."""
    with TemporaryDirectory() as temp_dir:
        test_config_parameters['output_file_format'] = 'TXT'
        test_output_file = os_path_join(temp_dir, 'output_test')
        test_config_parameters['output_file_path'] = test_output_file

        test_config_data = ConfigFileData(**test_config_parameters)

        output_script_data(test_config_data, TEST_DATA)
        txt_output = read_txt_file(f'{test_output_file}.txt')
        assert str(TEST_DATA) == txt_output


def test_xml_output_file(test_config_parameters):
    """Tests generating an XML script output file."""
    with TemporaryDirectory() as temp_dir:
        test_config_parameters['output_file_format'] = 'XML'
        test_output_file = os_path_join(temp_dir, 'output_test')
        test_config_parameters['output_file_path'] = test_output_file

        test_config_data = ConfigFileData(**test_config_parameters)

        output_script_data(test_config_data, TEST_DATA)
        xml_output = read_xml_file(f'{test_output_file}.xml')
        assert str(TEST_DATA) == xml_output
