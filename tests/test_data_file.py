from pytest import raises

from errors import DataFileError
from math_analyser import (
    verify_ini_math_sets, get_data_from_json_file, get_data_from_txt_file, get_data_from_xml_file)
from tests.settings import TestData


math_sets = [[(float('-inf'), float('inf'))],
             [(float('-inf'), -10.37), (10.41, float('inf'))],
             [(float('-inf'), 99.4)],
             [(-98, float('inf'))],
             [(float('-inf'), -32.08), (-17, 22.2), (54, 57)],
             [(float('-inf'), -41), (-18, 24), (51, 62), (103, float('inf'))],
             [(-89.11, -61.07), (-24.9, float('inf'))],
             [(-77, 54), 61.04],
             [(-89, -61), (-43, -12), (10, 27), (61, 72)]]


def test_string_data_instead_of_list():
    """One of the initial math sets in the data file has an invalid value,
    a 'str' object instead of required 'list'."""
    with raises(DataFileError):
        verify_ini_math_sets('"-inf", 57, 74')


def test_numeric_data_instead_of_list():
    """One of the initial math sets in the data file has an invalid value,
     an 'int' object instead of required 'list'."""
    with raises(DataFileError):
        verify_ini_math_sets(547)


def test_no_data():
    """One of the initial math sets in the data file has an invalid value: an empty row."""
    with raises(DataFileError):
        verify_ini_math_sets("")


def test_empty_list():
    """One of the initial math sets in the data file has an invalid value: an empty 'list'."""
    with raises(DataFileError):
        verify_ini_math_sets(list())


def test_invalid_string_data():
    """One of the initial math sets in the data file has an invalid value,
    invalid 'str' value at math range."""
    with raises(DataFileError):
        verify_ini_math_sets([('qw', 'asd')])


def test_range_with_less_than_two_points():
    """One of the initial math sets in the data file has an invalid value,
    math range with less than two points."""
    with raises(DataFileError):
        verify_ini_math_sets([(47,)])


def test_range_with_more_than_two_points():
    """One of the initial math sets in the data file has an invalid value,
    math range with more than two points."""
    with raises(DataFileError):
        verify_ini_math_sets([(123, 23, 23)])


def test_invalid_semi_infinite_range_1():
    """One of the initial math sets in the data file has an invalid value,
    math range with invalid semi-infinite range."""
    with raises(DataFileError):
        verify_ini_math_sets([(12, float('-inf'))])


def test_invalid_semi_infinite_range_2():
    """One of the initial math sets in the data file has an invalid value,
    math range with invalid semi-infinite range."""
    with raises(DataFileError):
        verify_ini_math_sets([(12, '+inf')])


def test_set_instead_of_list():
    """One of the initial math sets in the data file has an invalid value,
    'set' object instead of required 'list'."""
    with raises(DataFileError):
        verify_ini_math_sets({12, 34})


def test_json_data_file():
    """Tests getting initial math sets from JSON data files."""
    with open(TestData.get_json_test_data_file()) as test_data_file:
        test_ini_math_sets = get_data_from_json_file(test_data_file)
    assert math_sets == test_ini_math_sets


def test_txt_data_file():
    """Tests getting initial math sets from TXT data files."""
    with open(TestData.get_txt_test_data_file()) as test_data_file:
        test_ini_math_sets = get_data_from_txt_file(test_data_file)
    assert math_sets == test_ini_math_sets


def test_xml_data_file():
    """Tests getting initial math sets from XML data files."""
    with open(TestData.get_xml_test_data_file()) as test_data_file:
        test_ini_math_sets = get_data_from_xml_file(test_data_file)
    assert math_sets == test_ini_math_sets
