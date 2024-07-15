from math_analyser import determine_intersection_of_ini_math_ranges
from tests.settings import ints_mode_using_temp_files


math_sets = [[(float('-inf'), float('inf'))],
             [(10.41, float('inf')), (float('-inf'), -10.37)],
             [(float('-inf'), 99.4)],
             [(-98, float('inf'))],
             [(float('-inf'), -32.08), (-17, 22.2), (54, 57)],
             [(float('-inf'), -41), (51, 62), (-18, 24), (103, float('inf'))],
             [(-89.11, -61.07), (-24.9, float('inf'))],
             [(-77, 54), 61.04],
             [(-89, -61), (-43, -12), (10, 27), (61, 72)]]
numeric_math_sets = [[(-18, 24), (-75, -41), (51, 62)],
                     [(-77, 61)],
                     [(-89, -61), (61, 72), (-43, -12)]]
semi_infinite_math_sets = [[(-89, -61), (-12, float('inf'))],
                           [(-97, float('inf'))],
                           [(float('-inf'), float('inf'))]]
math_sets_with_points = [[(-89, 17.8), 24, (25, float('inf'))],
                         [(-97, 2), (9.9, 24), (36.1, float('inf'))],
                         [-77, -29, 42.7, (51.1, float('inf'))]]
one_initial_math_set = ["[(10, 12), (-25, -10)]"]
one_initial_infinity_math_set = [[(float('-inf'), float('inf'))]]
initial_infinity_math_sets = [[(float('-inf'), float('inf'))],
                              [(float('-inf'), float('inf'))],
                              [(float('-inf'), float('inf'))]]
math_sets_without_intersection = [[(-89, -61), (102, float('inf'))],
                                  [(-57, 35)],
                                  [(-2, 16), (61, 72)]]
output_for_math_sets = [(-77, -61.07), (-17, -12), (10.41, 22.2)]
output_for_numeric_math_sets = [(-75, -61), (-43, -41), (-18, -12), 61]
output_for_semi_infinite_math_sets = [(-89, -61), (-12, float('inf'))]
output_for_math_sets_with_points = [-77, -29, 42.7, (51.1, float('inf'))]
output_for_one_initial_math_set = [(-25, -10), (10, 12)]
output_for_initial_infinity_math_sets = [(float('-inf'), float('inf'))]


def test_all_types_of_math_sets():
    """'INTS' mode for all types of math sets."""
    test_result = determine_intersection_of_ini_math_ranges(math_sets, 0, [])
    assert test_result == output_for_math_sets


def test_numeric_math_sets():
    """'INTS' mode for numeric math sets."""
    test_result = determine_intersection_of_ini_math_ranges(numeric_math_sets, 0, [])
    assert test_result == output_for_numeric_math_sets


def test_semi_infinite_math_sets():
    """'INTS' mode for math sets with semi-infinite ranges."""
    test_result = determine_intersection_of_ini_math_ranges(semi_infinite_math_sets, 0, [])
    assert test_result == output_for_semi_infinite_math_sets


def test_math_sets_with_points():
    """'INTS' mode for math sets with math points."""
    test_result = determine_intersection_of_ini_math_ranges(math_sets_with_points, 0, [])
    assert test_result == output_for_math_sets_with_points


def test_one_initial_math_set():
    """'INTS' mode for only one initial math set."""
    test_result = ints_mode_using_temp_files(one_initial_math_set)
    assert test_result == output_for_one_initial_math_set


def test_one_initial_infinity_math_set():
    """'INTS' mode for only one initial infinity math sets"""
    test_result = determine_intersection_of_ini_math_ranges(one_initial_infinity_math_set, 0, [])
    assert test_result == output_for_initial_infinity_math_sets


def test_initial_infinity_math_sets():
    """'INTS' mode for only one initial infinity math sets"""
    test_result = determine_intersection_of_ini_math_ranges(initial_infinity_math_sets, 0, [])
    assert test_result == output_for_initial_infinity_math_sets


def test_math_sets_without_intersection():
    """'INTS' mode for math sets without intersection."""
    test_result = determine_intersection_of_ini_math_ranges(math_sets_without_intersection, 0, [])
    assert test_result == [None]
