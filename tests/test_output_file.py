import unittest

from errors import *
from settings import *


class OutputFileTest(unittest.TestCase):
    """Tests generating script output files in JSON TXT and XML format.
    It also tests raising of OutputFileGeneratingError."""

    def setUp(self) -> None:
        self.test_output_data = [(-77, -61), (-17, -12), (10, 22), (75, float('inf'))]
        self.test_config_parameters = {'analysis_mode': 'INTS',
                                       'math_point': 12.75,
                                       'data_format': 'JSON',
                                       'data_file': '/home/data file/initial math sets',
                                       'output_file_format': 'JSON',
                                       'output_file_path': '/home/script output files/report'}

    def test_OutputFileGeneratingError(self):
        """Tests raising of OutputFileGeneratingError. Tested for the following cases:
            [Errno 2] No such file or directory
            [Errno 13] Permission denied
        """
        test_config_data = ConfigFileData(**self.test_config_parameters)
        with self.assertRaises(OutputFileGeneratingError):
            output_script_data(test_config_data, ['test', 'list'])

    def test_json_output_file(self):
        """Tests generating a JSON script output file."""
        with TemporaryDirectory() as temp_dir:
            self.test_config_parameters['output_file_format'] = 'JSON'
            test_output_file = os_path_join(temp_dir, 'output_test')
            self.test_config_parameters['output_file_path'] = test_output_file

            test_config_data = ConfigFileData(**self.test_config_parameters)

            output_script_data(test_config_data, self.test_output_data)
            json_output = read_json_file(f'{test_output_file}.json')
            self.assertEqual(str(self.test_output_data), json_output)

    def test_txt_output_file(self):
        """Tests generating a TXT script output file."""
        with TemporaryDirectory() as temp_dir:
            self.test_config_parameters['output_file_format'] = 'TXT'
            test_output_file = os_path_join(temp_dir, 'output_test')
            self.test_config_parameters['output_file_path'] = test_output_file

            test_config_data = ConfigFileData(**self.test_config_parameters)

            output_script_data(test_config_data, self.test_output_data)
            txt_output = read_txt_file(f'{test_output_file}.txt')
            self.assertEqual(str(self.test_output_data), txt_output)

    def test_xml_output_file(self):
        """Tests generating an XML script output file."""
        with TemporaryDirectory() as temp_dir:
            self.test_config_parameters['output_file_format'] = 'XML'
            test_output_file = os_path_join(temp_dir, 'output_test')
            self.test_config_parameters['output_file_path'] = test_output_file

            test_config_data = ConfigFileData(**self.test_config_parameters)

            output_script_data(test_config_data, self.test_output_data)
            xml_output = read_xml_file(f'{test_output_file}.xml')
            self.assertEqual(str(self.test_output_data), xml_output)
