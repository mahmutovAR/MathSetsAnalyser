import json
import unittest
from configparser import ConfigParser
from os.path import abspath, dirname
from os.path import join as os_path_join
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup
from chameleon import PageTemplateLoader

import math_sets_analyser as msa
import run_math_sets_analyser as run_msa
from math_analyser import config_data, ConfigData, MathSet
from tests.errors import TestFailedError
from tests.test_params import TestData

testing_const = TestData(abspath(dirname(__file__)))


class ConfigurationFileTest(unittest.TestCase):
    """Tests the parsing of the configuration data file in case of invalid data."""

    def setUp(self) -> None:
        self.test_output_file = testing_const.get_output_file()
        self.test_config_parameters = {'analysis_mode': 'INTS',
                                       'input_point': 12.75,
                                       'data_format': 'JSON',
                                       'data_file': testing_const.get_json_test_data_file(),
                                       'output_file_format': 'TXT',
                                       'output_file_path': self.test_output_file}

    def test_no_config_file(self):
        """The configuration file does not exist."""
        not_existing_config_file = testing_const.get_invalid_file_path()
        with self.assertRaises(msa.ConfigFileNotFoundError):
            msa.parse_configuration_file(not_existing_config_file)

    def test_invalid_data_file_format(self):
        """The data file format is not valid."""
        self.test_config_parameters['data_format'] = 'PDF'
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_invalid_data_file_path(self):
        """The path to the data file is invalid."""
        self.test_config_parameters['data_file'] = testing_const.get_invalid_file_path()
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.DataFileNotFoundError):
            test_config_data.verify_config_data()

    def test_different_input_file_format_in_data_format_and_data_path(self):
        """The input data file format does not match the one specified in the path."""
        self.test_config_parameters['data_format'] = 'XML'
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_different_output_file_format_in_data_format_and_data_path(self):
        """The output data file format does not match the one specified in the path."""
        self.test_config_parameters['output_file_path'] = f'{self.test_output_file}.json'
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_invalid_output_file_format(self):
        """The output file format is invalid."""
        self.test_config_parameters['output_file_format'] = 'PDF'
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_no_output_file_path(self):
        """The path to the output file is not specified."""
        self.test_config_parameters['output_file_path'] = ''
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_invalid_output_file_path(self):
        """The directory for the output file does not exist."""
        self.test_config_parameters['output_file_path'] = testing_const.get_invalid_file_path()
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.OutputDirectoryNotFoundError):
            test_config_data.verify_config_data()

    def test_invalid_mode(self):
        """The invalid mode is specified."""
        self.test_config_parameters['analysis_mode'] = 'ERR'
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.ConfigFileParsingError):
            test_config_data.verify_config_data()

    def test_invalid_point(self):
        """The point for AFFL mode is invalid. Tested for the following cases:
            "point ="
            "point = {string}"
            "{no row}"
        """
        self.test_config_parameters['analysis_mode'] = 'AFFL'
        self.test_config_parameters['input_point'] = None
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(config_data.ConfigFileParsingError):
            test_config_data.verify_config_data()


class DataFileTest(unittest.TestCase):
    """Tests getting data from data files in case of invalid data.
    It also tests getting data from JSON TXT and XML data files."""

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

    def test_string_data_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
        a 'str' object instead of required 'list'."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', '"-inf", 57, 74')

    def test_numeric_data_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
         an 'int' object instead of required 'list'."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', 547)

    def test_no_data(self):
        """One of the initial math sets in the data file has an invalid value: an empty row."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', "")

    def test_empty_list(self):
        """One of the initial math sets in the data file has an invalid value: an empty 'list'."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', [])

    def test_invalid_string_data(self):
        """One of the initial math sets in the data file has an invalid value,
        invalid 'str' value at math range."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', [('qw', 'asd')])

    def test_range_with_less_than_two_points(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with less than two points."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', [(47,)])

    def test_range_with_more_than_two_points(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with more than two points."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', [(123, 23, 23)])

    def test_invalid_semi_infinite_range(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with invalid semi-infinite range."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', [(12, '-inf')])

    def test_set_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
        'set' object instead of required 'list'."""
        with self.assertRaises(msa.DataGettingError):
            msa.verify_ini_math_sets('invalid data', {12, 34})

    def test_all_infinity_ranges(self):
        """All initial math sets in the data file are infinite ranges, [('-inf', '+inf')]."""
        infinity_math_sets = {'set_type_1': [('-inf', '+inf')],
                              'set_type_2': [('-inf', '+inf')],
                              'set_type_3': [('-inf', '+inf')]}
        test_math_sets = [MathSet(math_set_name, math_ranges)
                          for math_set_name, math_ranges in infinity_math_sets.items()]
        with self.assertRaises(msa.InfiniteSetError):
            msa.get_all_initial_numeric_endpoints(test_math_sets)

    def test_json_data_file(self):
        """Tests getting initial math sets from JSON data files."""
        with open(testing_const.get_json_test_data_file()) as test_data_file:
            test_ini_math_sets = msa.get_data_from_json_file(test_data_file)
        extracted_math_sets = {ini_math_set.get_ini_math_set_name(): ini_math_set.get_ini_math_ranges()
                               for ini_math_set in test_ini_math_sets}
        if self.math_sets != extracted_math_sets:
            raise TestFailedError('getting data from JSON data file', None)

    def test_txt_data_file(self):
        """Tests getting initial math sets from TXT data files."""
        with open(testing_const.get_txt_test_data_file()) as test_data_file:
            test_ini_math_sets = msa.get_data_from_txt_file(test_data_file)
        extracted_math_sets = {ini_math_set.get_ini_math_set_name(): ini_math_set.get_ini_math_ranges()
                               for ini_math_set in test_ini_math_sets}
        if self.math_sets != extracted_math_sets:
            raise TestFailedError('getting data from TXT data file', None)

    def test_xml_data_file(self):
        """Tests getting initial math sets from XML data files."""
        with open(testing_const.get_xml_test_data_file()) as test_data_file:
            test_ini_math_sets = msa.get_data_from_xml_file(test_data_file)
        extracted_math_sets = {ini_math_set.get_ini_math_set_name(): ini_math_set.get_ini_math_ranges()
                               for ini_math_set in test_ini_math_sets}
        if self.math_sets != extracted_math_sets:
            raise TestFailedError('getting data from XML data file', None)


class OutputFileTest(unittest.TestCase):
    """Tests generating script output files in JSON TXT and XML format.
    It also tests raising of OutputFileGeneratingError."""

    def setUp(self) -> None:
        self.test_output_title = 'The intersection of initial math sets'
        self.test_output_data = [(-77, -61), (-17, -12), (10, 22)]

        self.reference_output = {self.test_output_title: self.test_output_data}

        self.test_config_parameters = {'analysis_mode': 'INTS',
                                       'input_point': 12.75,
                                       'data_format': 'JSON',
                                       'data_file': '/home/data file/initial math sets',
                                       'output_file_format': 'JSON',
                                       'output_file_path': '/home/script output files/report'}

    def test_OutputFileGeneratingError(self):
        """Tests raising of OutputFileGeneratingError. Tested for the following cases:
            [Errno 2] No such file or directory
            [Errno 13] Permission denied
        """
        test_config_data = ConfigData(**self.test_config_parameters)
        with self.assertRaises(msa.OutputFileGeneratingError):
            msa.output_script_data(test_config_data, 'test title', ['test', 'list'])

    def test_json_output_file(self):
        """Tests generating a JSON script output file."""
        with TemporaryDirectory() as temp_dir:
            self.test_config_parameters['output_file_format'] = 'JSON'
            test_output_file = os_path_join(temp_dir, 'output_test')
            self.test_config_parameters['output_file_path'] = test_output_file

            test_config_data = ConfigData(**self.test_config_parameters)

            msa.output_script_data(test_config_data, self.test_output_title, self.test_output_data)
            json_output = read_json_file(f'{test_output_file}.json')
            if self.reference_output != json_output:
                raise TestFailedError('creating output JSON file', None)

    def test_txt_output_file(self):
        """Tests generating a TXT script output file."""
        with TemporaryDirectory() as temp_dir:
            self.test_config_parameters['output_file_format'] = 'TXT'
            test_output_file = os_path_join(temp_dir, 'output_test')
            self.test_config_parameters['output_file_path'] = test_output_file

            test_config_data = ConfigData(**self.test_config_parameters)

            msa.output_script_data(test_config_data, self.test_output_title, self.test_output_data)
            txt_output = read_txt_file(f'{test_output_file}.txt')
            if self.reference_output != txt_output:
                raise TestFailedError('creating output TXT file', None)

    def test_xml_output_file(self):
        """Tests generating an XML script output file."""
        with TemporaryDirectory() as temp_dir:
            self.test_config_parameters['output_file_format'] = 'XML'
            test_output_file = os_path_join(temp_dir, 'output_test')
            self.test_config_parameters['output_file_path'] = test_output_file

            test_config_data = ConfigData(**self.test_config_parameters)

            msa.output_script_data(test_config_data, self.test_output_title, self.test_output_data)
            xml_output = read_xml_file(f'{test_output_file}.xml')
            if self.reference_output != xml_output:
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
        self.one_initial_infinity_math_set = {'set_type_1': [("-inf", "+inf")]}
        self.math_sets_without_intersection = {'set_type_1': [(-89, -61), (102, '+inf')],
                                               'set_type_2': [(-57, 35)],
                                               'set_type_3': [(-2, 16), (61, 72)]}

        self.math_sets_output = [(-77, -61.07), (-17, -12), (10.41, 22.2)]
        self.numeric_math_sets_output = [(-75, -61), (-43, -41), (-18, -12), 61]
        self.semi_infinite_math_sets_output = [(-89, -61), (-12, '+inf')]
        self.math_sets_with_points_output = [-77, -29, 42.7, (51.1, '+inf')]
        self.one_initial_math_set_output = [(-25, -10), (10, 12)]

    def test_all_types_of_math_sets(self):
        """'INTS' mode for all types of math sets."""
        test_ints_mode_using_msa_functions(self.math_sets, self.math_sets_output,
                                           'INTS mode (all types of initial math sets)')

    def test_numeric_math_sets(self):
        """'INTS' mode for numeric math sets."""
        test_ints_mode_using_msa_functions(self.numeric_math_sets, self.numeric_math_sets_output,
                                           'INTS mode (only numeric initial math sets)')

    def test_semi_infinite_math_sets(self):
        """'INTS' mode for math sets with semi-infinite ranges."""
        test_ints_mode_using_msa_functions(self.semi_infinite_math_sets, self.semi_infinite_math_sets_output,
                                           'INTS mode (semi-infinite math sets)')

    def test_math_sets_with_points(self):
        """'INTS' mode for math sets with math points."""
        test_ints_mode_using_msa_functions(self.math_sets_with_points, self.math_sets_with_points_output,
                                           'INTS mode (math sets with points)')

    def test_one_initial_math_set(self):
        """'INTS' mode for only one initial math set."""
        test_ints_mode_using_temp_files(self.one_initial_math_set, self.one_initial_math_set_output,
                                        'INTS mode (only one initial math set)')

    def test_one_initial_infinity_math_set(self):
        """'INTS' mode for only one initial infinity math sets"""
        with self.assertRaises(run_msa.InfiniteSetError):
            test_ints_mode_using_temp_files(self.one_initial_infinity_math_set, list(),
                                            'INTS mode (one initial infinity math sets)')

    def test_math_sets_without_intersection(self):
        """'INTS' mode for math sets without intersection."""
        with self.assertRaises(run_msa.NoIntersectionError):
            test_ints_mode_using_msa_functions(self.math_sets_without_intersection, list(),
                                               'INTS mode (initial math sets without intersection)')


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
            'The point of the initial math sets intersection is the predetermined point': [42.7]}
        self.intersection_point_do_not_equal_to_given = {
            'The nearest endpoint(s) to the predetermined point': [-77, -29]}
        self.semi_infinite_math_sets_contain_point = {
            'The subrange of the initial math sets intersection with the predetermined point': [(-12, '+inf')]}
        self.semi_infinite_math_sets_do_not_contain_point = {
            'The nearest endpoint(s) to the predetermined point': [-12]}
        self.numeric_math_sets_contain_point = {
            'The subrange of the initial math sets intersection with the predetermined point': [(-2, 16)]}
        self.numeric_math_sets_do_not_contain_point = {
            'The nearest endpoint(s) to the predetermined point': [16]}
        self.two_nearest_endpoints_case_output = {
            'The nearest endpoint(s) to the predetermined point': [-12, 10]}

    def test_semi_infinite_math_sets_contain_point(self):
        """'AFFL' mode for math sets with semi-infinite ranges
        when the predetermined point belongs to the math intersection."""
        test_affl_mode_using_msa_functions(-1.09,
                                           self.semi_infinite_math_sets,
                                           self.semi_infinite_math_sets_contain_point,
                                           'AFFL mode (semi-infinite math sets contain point)')

    def test_semi_infinite_math_sets_do_not_contain_point(self):
        """'AFFL' mode for math sets with semi-infinite ranges
        when the predetermined point does not belong to the math intersection."""
        test_affl_mode_using_msa_functions(-15.01,
                                           self.semi_infinite_math_sets,
                                           self.semi_infinite_math_sets_do_not_contain_point,
                                           "AFFL mode (semi-infinite math sets don't contain point)")

    def test_numeric_math_sets_contain_point(self):
        """'AFFL' mode for the numeric math sets
        when the predetermined point belongs to the math intersection."""
        test_affl_mode_using_msa_functions(8.51,
                                           self.numeric_math_sets,
                                           self.numeric_math_sets_contain_point,
                                           'AFFL mode (numeric math sets contain point)')

    def test_numeric_math_sets_do_not_contain_point(self):
        """'AFFL' mode for the numeric math sets
        when the predetermined point does not belong to the math intersection."""
        test_affl_mode_using_msa_functions(19.34,
                                           self.numeric_math_sets,
                                           self.numeric_math_sets_do_not_contain_point,
                                           "AFFL mode (numeric math sets don't contain point)")

    def test_two_nearest_endpoints_case(self):
        """'AFFL' mode for the predetermined point which does not belong to the math intersection
        and has two nearest endpoints."""
        test_affl_mode_using_msa_functions(-1.0,
                                           self.two_nearest_endpoints_case,
                                           self.two_nearest_endpoints_case_output,
                                           'AFFL mode (two nearest endpoints)')

    def test_intersection_point_is_equal_to_given(self):
        """'AFFL' mode for the predetermined point which equals to the math intersection point."""
        test_affl_mode_using_msa_functions(42.7,
                                           self.intersection_points_case,
                                           self.intersection_point_equal_to_given,
                                           'AFFL mode (math intersection point is equal to the given one)')

    def test_intersection_point_is_not_equal_to_given(self):
        """'AFFL' mode for the predetermined point which not equal to the math intersection point."""
        test_affl_mode_using_msa_functions(-53,
                                           self.intersection_points_case,
                                           self.intersection_point_do_not_equal_to_given,
                                           'AFFL mode (math intersection point is not equal to the given one)')

    def test_math_sets_without_intersection(self):
        """'AFFL' mode for math sets without intersection."""
        with self.assertRaises(run_msa.NoIntersectionError):
            test_affl_mode_using_msa_functions(-1.0,
                                               self.math_sets_without_intersection,
                                               dict(),
                                               'AFFL mode (initial math sets without intersection)')


class FullRunTest(unittest.TestCase):
    """Tests math_sets_analyser for INTS and AFFL modes."""

    def setUp(self) -> None:
        self.INTS_input_data = {'set_type_1': [('-inf', '+inf')],
                                'set_type_2': [('-inf', -10.37), (10.41, '+inf')],
                                'set_type_3': [('-inf', 99.4)],
                                'set_type_4': [(-98, '+inf')],
                                'set_type_5': [('-inf', -32.08), (-17, 22.2), (54, 57)],
                                'set_type_6': [('-inf', -41), (-18, 24), (51, 62), (103, '+inf')],
                                'set_type_7': [(-89.11, -61.07), (-24.9, '+inf')],
                                'set_type_8': [(-77, 61.04), 54],
                                'set_type_9': [(-89, -61), (-43, -12), (10, 27), (61, 72)]}
        self.INTS_reference_output = {
            'The intersection of initial math sets': [(-77, -61.07), (-17, -12), (10.41, 22.2)]}
        self.INTS_config_parameters = {'analysis_mode': 'INTS',
                                       'input_point': None,
                                       'data_format': 'XML',
                                       'data_file': 'test data file',
                                       'output_file_format': 'JSON',
                                       'output_file_path': 'test output file'}

        self.AFFL_input_data = {'set_type_1': [('-inf', -10), (10, '+inf')],
                                'set_type_2': [(-77, 61)],
                                'set_type_3': [(-89, -61), (-43, -12), (10, 27), (61, 72)]}
        self.AFFL_reference_output = {
            'The nearest endpoint(s) to the predetermined point': [-12, 10]}
        self.AFFL_config_parameters = {'analysis_mode': 'AFFL',
                                       'input_point': -1,
                                       'data_format': 'TXT',
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
            create_xml_test_data_file(test_data_file, self.INTS_input_data)

            test_configuration_data = msa.parse_configuration_file(test_config_file)
            run_msa.main(test_configuration_data)

            script_result_file = read_json_file(f'{test_output_file}.json')
            if self.INTS_reference_output != script_result_file:
                raise TestFailedError('script full run test for INTS mode', None)

    def test_affl_mode_full_run(self):
        """Full run test for AFFL mode."""
        with TemporaryDirectory() as temp_dir:
            test_config_file = os_path_join(temp_dir, 'config.ini')
            test_data_file = os_path_join(temp_dir, 'data file')
            test_output_file = os_path_join(temp_dir, 'output file')

            self.AFFL_config_parameters['data_file'] = test_data_file
            self.AFFL_config_parameters['output_file_path'] = test_output_file

            create_config_file_for_affl_mode(test_config_file, self.AFFL_config_parameters)
            create_txt_test_data_file(test_data_file, self.AFFL_input_data)

            test_configuration_data = msa.parse_configuration_file(test_config_file)
            run_msa.main(test_configuration_data)

            script_result_file = read_xml_file(f'{test_output_file}.xml')
            if self.AFFL_reference_output != script_result_file:
                raise TestFailedError('script full run test for AFFL mode', None)


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
    test_point = input_data['input_point']
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


def create_json_test_data_file(input_file: str, input_data: dict) -> None:
    """Creates JSON data file at given path."""
    json_data = dict()
    for math_set_name in input_data:
        json_data[math_set_name] = str(input_data[math_set_name])
    with open(input_file, 'w') as json_data_file:
        json.dump(json_data, json_data_file)


def create_txt_test_data_file(input_file: str, input_data: dict) -> None:
    """Creates TXT data file at given path."""
    with open(input_file, 'w') as txt_data_file:
        for math_set_name, math_subrange in input_data.items():
            txt_data_file.write(f'{math_set_name}\n{math_subrange}\n')


def create_xml_test_data_file(input_file: str, input_data: dict) -> None:
    """Creates XML data file at given path."""
    template = PageTemplateLoader(os_path_join(abspath(dirname(__file__)), 'tests', 'templates'))
    tmpl = template['input_temp.pt']
    with open(input_file, 'w') as xml_output_file:
        data_for_xml = tmpl(ini_data=input_data)
        xml_output_file.write(data_for_xml)


def read_json_file(input_file: str) -> dict:
    """Returns dict object with data from inputted JSON file."""
    with open(input_file) as json_file:
        json_file_data = json.load(json_file)
    output_data = {file_title: eval(file_data)
                   for file_title, file_data in json_file_data.items()}
    return output_data


def read_txt_file(input_file: str) -> dict:
    """Returns dict object with data from inputted TXT file."""
    with open(input_file, 'r', newline='') as txt_file:
        file_title = txt_file.readline().rstrip()
        file_data = txt_file.readline().rstrip()
        file_data = eval(file_data)
    return {file_title: file_data}


def read_xml_file(input_file: str) -> dict:
    """Returns dict object with data from inputted XML file."""
    with open(input_file) as xml_file:
        file_data = xml_file.read()
    bs_object = BeautifulSoup(file_data, 'lxml')
    output_data = bs_object.find('scriptoutput')
    result_title = output_data.get('title')
    result_data = output_data.find('value').get_text()
    result_data = eval(result_data)
    return {result_title: result_data}


def test_ints_mode_using_temp_files(ini_math_sets: dict, reference_output: list, test_name: str) -> None:
    """Tests 'INTS' mode with given initial parameters."""
    with TemporaryDirectory() as temp_dir:
        test_config_file = os_path_join(temp_dir, 'config.ini')
        test_data_file = os_path_join(temp_dir, 'data file')
        test_config_parameters = {'analysis_mode': 'INTS',
                                  'input_point': None,
                                  'data_format': 'XML',
                                  'data_file': test_data_file,
                                  'output_file_format': 'JSON',
                                  'output_file_path': 'test output file'}

        create_config_file_for_ints_mode(test_config_file, test_config_parameters)
        create_xml_test_data_file(test_data_file, ini_math_sets)

        test_configuration_data = msa.parse_configuration_file(test_config_file)
        sorted_math_intersection = run_msa.determine_initial_math_sets_intersection(test_configuration_data)

        if reference_output != sorted_math_intersection:
            raise TestFailedError(test_name, None)


def test_ints_mode_using_msa_functions(ini_math_sets: dict, reference_output: list, test_name: str) -> None:
    """Tests 'INTS' mode with given initial parameters."""
    test_math_sets = [MathSet(math_set_name, math_ranges)
                      for math_set_name, math_ranges in ini_math_sets.items()]

    all_ini_numeric_endpoints = msa.get_all_initial_numeric_endpoints(test_math_sets)
    msa.format_ranges_using_all_ini_numeric_endpoints(all_ini_numeric_endpoints, test_math_sets)
    intersection_result = msa.get_intersection_of_ini_math_ranges(test_math_sets, 0, set())
    sorted_math_intersection = msa.format_and_sort_math_intersection(intersection_result)

    if reference_output != sorted_math_intersection:
        raise TestFailedError(test_name, None)


def test_affl_mode_using_msa_functions(input_number: float, ini_math_sets: dict,
                                       reference_output: dict, test_name: str) -> None:
    """Tests 'INTS' mode with given initial parameters."""
    test_config_parameters = {'analysis_mode': 'AFFL',
                              'input_point': input_number,
                              'data_format': 'JSON',
                              'data_file': '/home/data file/initial math sets',
                              'output_file_format': 'JSON',
                              'output_file_path': 'test output file'}

    test_config_data = ConfigData(**test_config_parameters)
    test_math_sets = [MathSet(math_set_name, math_ranges)
                      for math_set_name, math_ranges in ini_math_sets.items()]

    all_ini_numeric_endpoints = msa.get_all_initial_numeric_endpoints(test_math_sets)
    msa.format_ranges_using_all_ini_numeric_endpoints(all_ini_numeric_endpoints, test_math_sets)
    intersection_result = msa.get_intersection_of_ini_math_ranges(test_math_sets, 0, set())
    sorted_math_intersection = msa.format_and_sort_math_intersection(intersection_result)
    result_title, result_data = msa.determine_affiliation_of_point_to_intersection(test_config_data,
                                                                                   sorted_math_intersection)

    if reference_output != {result_title: result_data}:
        raise TestFailedError(test_name, None)


if __name__ == '__main__':
    unittest.main()
