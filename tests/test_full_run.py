from settings import *

import unittest


class FullRunTest(unittest.TestCase):
    """Tests math_sets_analyser for INTS and AFFL modes."""

    def setUp(self) -> None:
        self.INTS_input_data = ["[(float('-inf'), float('inf'))]",
                                "[(float('-inf'), -10.37), (10.41, float('inf'))]",
                                "[(float('-inf'), 99.4)]",
                                "[(-98, float('inf'))]",
                                "[(float('-inf'), -32.08), (-17, 22.2), (54, 57)]",
                                "[(float('-inf'), -41), (-18, 24), (51, 62), (103, float('inf'))]",
                                "[(-89.11, -61.07), (-24.9, float('inf'))]",
                                "[(-77, 54), 61.04]",
                                "[(-89, -61), (-43, -12), (10, 27), (61, 72)]"]
        self.INTS_reference_output = '[(-77, -61.07), (-17, -12), (10.41, 22.2)]'
        self.INTS_config_parameters = {'analysis_mode': 'INTS',
                                       'input_point': None,
                                       'data_format': 'JSON',
                                       'data_file': 'test data file',
                                       'output_file_format': 'TXT',
                                       'output_file_path': 'test output file'}

        self.AFFL_input_data = ["[(float('-inf'), -10), (10, float('inf'))]",
                                "[(-77, 61)]",
                                "[(-89, -61), (-43, -12), (10, 27), (61, 72)]"]
        self.AFFL_reference_output = '[-12, 10]'
        self.AFFL_config_parameters = {'analysis_mode': 'AFFL',
                                       'math_point': -1,
                                       'data_format': 'JSON',
                                       'data_file': 'test data file',
                                       'output_file_format': 'XML',
                                       'output_file_path': 'test output file'}

    def test_ints_mode_full_run(self):
        """Full run test for INTS mode."""
        with TemporaryDirectory() as temp_dir:
            test_config_file = os_path_join(temp_dir, 'config.ini')
            test_data_file = os_path_join(temp_dir, 'data file')
            test_output_file = os_path_join(temp_dir, 'output file')

            self.INTS_config_parameters['data_file'] = test_data_file
            self.INTS_config_parameters['output_file_path'] = test_output_file

            create_config_file_for_ints_mode(test_config_file, self.INTS_config_parameters)
            create_json_test_data_file(test_data_file, self.INTS_input_data)

            test_configuration_data = parse_configuration_file(test_config_file)
            run_msa.main(test_configuration_data)

            script_result_file = read_txt_file(f'{test_output_file}.txt')

            self.assertEqual(script_result_file, self.INTS_reference_output)

    def test_affl_mode_full_run(self):
        """Full run test for AFFL mode."""
        with TemporaryDirectory() as temp_dir:
            test_config_file = os_path_join(temp_dir, 'config.ini')
            test_data_file = os_path_join(temp_dir, 'data file')
            test_output_file = os_path_join(temp_dir, 'output file')

            self.AFFL_config_parameters['data_file'] = test_data_file
            self.AFFL_config_parameters['output_file_path'] = test_output_file

            create_config_file_for_affl_mode(test_config_file, self.AFFL_config_parameters)
            create_json_test_data_file(test_data_file, self.AFFL_input_data)

            test_configuration_data = parse_configuration_file(test_config_file)
            run_msa.main(test_configuration_data)

            script_result_file = read_xml_file(f'{test_output_file}.xml')
            self.assertEqual(script_result_file, self.AFFL_reference_output)
