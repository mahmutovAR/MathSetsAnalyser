from settings import *

import unittest


class IntersectionModeTest(unittest.TestCase):
    """Tests the 'INTS' mode for various initial math sets."""

    def setUp(self) -> None:
        self.math_sets = [[(float('-inf'), float('inf'))],
                          [(10.41, float('inf')), (float('-inf'), -10.37)],
                          [(float('-inf'), 99.4)],
                          [(-98, float('inf'))],
                          [(float('-inf'), -32.08), (-17, 22.2), (54, 57)],
                          [(float('-inf'), -41), (51, 62), (-18, 24), (103, float('inf'))],
                          [(-89.11, -61.07), (-24.9, float('inf'))],
                          [(-77, 54), 61.04],
                          [(-89, -61), (-43, -12), (10, 27), (61, 72)]]
        self.numeric_math_sets = [[(-18, 24), (-75, -41), (51, 62)],
                                  [(-77, 61)],
                                  [(-89, -61), (61, 72), (-43, -12)]]
        self.semi_infinite_math_sets = [[(-89, -61), (-12, float('inf'))],
                                        [(-97, float('inf'))],
                                        [(float('-inf'), float('inf'))]]
        self.math_sets_with_points = [[(-89, 17.8), 24, (25, float('inf'))],
                                      [(-97, 2), (9.9, 24), (36.1, float('inf'))],
                                      [-77, -29, 42.7, (51.1, float('inf'))]]
        self.one_initial_math_set = ["[(10, 12), (-25, -10)]"]
        self.one_initial_infinity_math_set = [[(float('-inf'), float('inf'))]]
        self.initial_infinity_math_sets = [[(float('-inf'), float('inf'))],
                                           [(float('-inf'), float('inf'))],
                                           [(float('-inf'), float('inf'))]]
        self.math_sets_without_intersection = [[(-89, -61), (102, float('inf'))],
                                               [(-57, 35)],
                                               [(-2, 16), (61, 72)]]
        self.output_for_math_sets = [(-77, -61.07), (-17, -12), (10.41, 22.2)]
        self.output_for_numeric_math_sets = [(-75, -61), (-43, -41), (-18, -12), 61]
        self.output_for_semi_infinite_math_sets = [(-89, -61), (-12, float('inf'))]
        self.output_for_math_sets_with_points = [-77, -29, 42.7, (51.1, float('inf'))]
        self.output_for_one_initial_math_set = [(-25, -10), (10, 12)]
        self.output_for_initial_infinity_math_sets = [(float('-inf'), float('inf'))]

    def test_all_types_of_math_sets(self):
        """'INTS' mode for all types of math sets."""
        test_result = determine_intersection_of_ini_math_ranges(self.math_sets, 0, [])
        self.assertEqual(test_result, self.output_for_math_sets)

    def test_numeric_math_sets(self):
        """'INTS' mode for numeric math sets."""
        test_result = determine_intersection_of_ini_math_ranges(self.numeric_math_sets, 0, [])
        self.assertEqual(test_result, self.output_for_numeric_math_sets)

    def test_semi_infinite_math_sets(self):
        """'INTS' mode for math sets with semi-infinite ranges."""
        test_result = determine_intersection_of_ini_math_ranges(self.semi_infinite_math_sets, 0, [])
        self.assertEqual(test_result, self.output_for_semi_infinite_math_sets)

    def test_math_sets_with_points(self):
        """'INTS' mode for math sets with math points."""
        test_result = determine_intersection_of_ini_math_ranges(self.math_sets_with_points, 0, [])
        self.assertEqual(test_result, self.output_for_math_sets_with_points)

    def test_one_initial_math_set(self):
        """'INTS' mode for only one initial math set."""
        test_result = ints_mode_using_temp_files(self.one_initial_math_set)
        self.assertEqual(test_result, self.output_for_one_initial_math_set)

    def test_one_initial_infinity_math_set(self):
        """'INTS' mode for only one initial infinity math sets"""
        test_result = determine_intersection_of_ini_math_ranges(self.one_initial_infinity_math_set, 0, [])
        self.assertEqual(test_result, self.output_for_initial_infinity_math_sets)

    def test_initial_infinity_math_sets(self):
        """'INTS' mode for only one initial infinity math sets"""
        test_result = determine_intersection_of_ini_math_ranges(self.initial_infinity_math_sets, 0, [])
        self.assertEqual(test_result, self.output_for_initial_infinity_math_sets)

    def test_math_sets_without_intersection(self):
        """'INTS' mode for math sets without intersection."""
        test_result = determine_intersection_of_ini_math_ranges(self.math_sets_without_intersection, 0, [])
        self.assertEqual(test_result, [None])
