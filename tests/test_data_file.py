import unittest

from errors import *
from settings import *


class DataFileTest(unittest.TestCase):
    """Tests getting data from data files in case of invalid data.
    It also tests getting data from JSON TXT and XML data files."""

    def setUp(self) -> None:
        self.math_sets = [[(float('-inf'), float('inf'))],
                          [(float('-inf'), -10.37), (10.41, float('inf'))],
                          [(float('-inf'), 99.4)],
                          [(-98, float('inf'))],
                          [(float('-inf'), -32.08), (-17, 22.2), (54, 57)],
                          [(float('-inf'), -41), (-18, 24), (51, 62), (103, float('inf'))],
                          [(-89.11, -61.07), (-24.9, float('inf'))],
                          [(-77, 54), 61.04],
                          [(-89, -61), (-43, -12), (10, 27), (61, 72)]]

    def test_string_data_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
        a 'str' object instead of required 'list'."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets('"-inf", 57, 74')

    def test_numeric_data_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
         an 'int' object instead of required 'list'."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets(547)

    def test_no_data(self):
        """One of the initial math sets in the data file has an invalid value: an empty row."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets("")

    def test_empty_list(self):
        """One of the initial math sets in the data file has an invalid value: an empty 'list'."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets(list())

    def test_invalid_string_data(self):
        """One of the initial math sets in the data file has an invalid value,
        invalid 'str' value at math range."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets([('qw', 'asd')])

    def test_range_with_less_than_two_points(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with less than two points."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets([(47,)])

    def test_range_with_more_than_two_points(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with more than two points."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets([(123, 23, 23)])

    def test_invalid_semi_infinite_range_1(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with invalid semi-infinite range."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets([(12, float('-inf'))])

    def test_invalid_semi_infinite_range_2(self):
        """One of the initial math sets in the data file has an invalid value,
        math range with invalid semi-infinite range."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets([(12, '+inf')])

    def test_set_instead_of_list(self):
        """One of the initial math sets in the data file has an invalid value,
        'set' object instead of required 'list'."""
        with self.assertRaises(DataGettingError):
            verify_ini_math_sets({12, 34})

    def test_json_data_file(self):
        """Tests getting initial math sets from JSON data files."""
        with open(TestData.get_json_test_data_file()) as test_data_file:
            test_ini_math_sets = get_data_from_json_file(test_data_file)
        self.assertEqual(self.math_sets, test_ini_math_sets)

    def test_txt_data_file(self):
        """Tests getting initial math sets from TXT data files."""
        with open(TestData.get_txt_test_data_file()) as test_data_file:
            test_ini_math_sets = get_data_from_txt_file(test_data_file)
        self.assertEqual(self.math_sets, test_ini_math_sets)

    def test_xml_data_file(self):
        """Tests getting initial math sets from XML data files."""
        with open(TestData.get_xml_test_data_file()) as test_data_file:
            test_ini_math_sets = get_data_from_xml_file(test_data_file)
        self.assertEqual(self.math_sets, test_ini_math_sets)
