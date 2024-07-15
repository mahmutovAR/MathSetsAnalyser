from os.path import join as os_path_join

import run_math_sets_analyser as run_msa
from math_analyser import parse_configuration_file
from tests.settings import (TemporaryDirectory,
                            create_config_file_for_affl_mode,
                            create_config_file_for_ints_mode,
                            create_json_test_data_file,
                            read_txt_file,
                            read_xml_file)

INTS_input_data = ["[(float('-inf'), float('inf'))]",
                   "[(float('-inf'), -10.37), (10.41, float('inf'))]",
                   "[(float('-inf'), 99.4)]",
                   "[(-98, float('inf'))]",
                   "[(float('-inf'), -32.08), (-17, 22.2), (54, 57)]",
                   "[(float('-inf'), -41), (-18, 24), (51, 62), (103, float('inf'))]",
                   "[(-89.11, -61.07), (-24.9, float('inf'))]",
                   "[(-77, 54), 61.04]",
                   "[(-89, -61), (-43, -12), (10, 27), (61, 72)]"]
INTS_reference_output = '[(-77, -61.07), (-17, -12), (10.41, 22.2)]'
INTS_config_parameters = {'analysis_mode': 'INTS',
                          'input_point': None,
                          'data_format': 'JSON',
                          'data_file': 'test data file',
                          'output_file_format': 'TXT',
                          'output_file_path': 'test output file'}

AFFL_input_data = ["[(float('-inf'), -10), (10, float('inf'))]",
                   "[(-77, 61)]",
                   "[(-89, -61), (-43, -12), (10, 27), (61, 72)]"]
AFFL_reference_output = '[-12, 10]'
AFFL_config_parameters = {'analysis_mode': 'AFFL',
                          'math_point': -1,
                          'data_format': 'JSON',
                          'data_file': 'test data file',
                          'output_file_format': 'XML',
                          'output_file_path': 'test output file'}


def test_ints_mode_full_run():
    """Full run test for INTS mode."""
    with TemporaryDirectory() as temp_dir:
        test_config_file = os_path_join(temp_dir, 'config.ini')
        test_data_file = os_path_join(temp_dir, 'data file')
        test_output_file = os_path_join(temp_dir, 'output file')

        INTS_config_parameters['data_file'] = test_data_file
        INTS_config_parameters['output_file_path'] = test_output_file

        create_config_file_for_ints_mode(test_config_file, INTS_config_parameters)
        create_json_test_data_file(test_data_file, INTS_input_data)

        test_configuration_data = parse_configuration_file(test_config_file)
        run_msa.main(test_configuration_data)

        script_result_file = read_txt_file(f'{test_output_file}.txt')

        assert script_result_file == INTS_reference_output


def test_affl_mode_full_run():
    """Full run test for AFFL mode."""
    with TemporaryDirectory() as temp_dir:
        test_config_file = os_path_join(temp_dir, 'config.ini')
        test_data_file = os_path_join(temp_dir, 'data file')
        test_output_file = os_path_join(temp_dir, 'output file')

        AFFL_config_parameters['data_file'] = test_data_file
        AFFL_config_parameters['output_file_path'] = test_output_file

        create_config_file_for_affl_mode(test_config_file, AFFL_config_parameters)
        create_json_test_data_file(test_data_file, AFFL_input_data)

        test_configuration_data = parse_configuration_file(test_config_file)
        run_msa.main(test_configuration_data)

        script_result_file = read_xml_file(f'{test_output_file}.xml')
        assert script_result_file == AFFL_reference_output
