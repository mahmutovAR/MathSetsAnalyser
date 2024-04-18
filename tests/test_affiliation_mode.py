from settings import *

import unittest


class AffiliationModeTest(unittest.TestCase):
    """Tests the 'AFFL' mode for various initial math sets."""

    def setUp(self) -> None:
        self.semi_infinite_math_sets = [[(-89, -61), (-12, float('inf'))],
                                        [(-57, float('inf'))],
                                        [(float('-inf'), float('inf'))]]
        self.numeric_math_sets = [[(-89, -61), (-12, 28)],
                                  [(-57, 35)],
                                  [(-2, 16), (61, 72)]]
        self.two_closest_endpoints_case = [[(float('-inf'), -10), (10, float('inf'))],
                                           [(-77, 61)],
                                           [(-89, -61), (-43, -12), (10, 27), (61, 72)]]
        self.intersection_points_case = [[(-89, 17.8), 24, (25, float('inf'))],
                                         [(-97, 2), (9.9, 24), (36.1, float('inf'))],
                                         [-77, -29, 42.7, (51.1, float('inf'))]]
        self.math_sets_without_intersection = [[(-89, -61), (102, float('inf'))],
                                               [(-57, 35)],
                                               [(-2, 16), (61, 72)]]

        self.intersection_point_do_not_equal_to_given = [-77, -29]
        self.semi_infinite_math_sets_do_not_contain_point = [-12]
        self.numeric_math_sets_do_not_contain_point = [16]
        self.two_closest_endpoints_case_output = [-12, 10]

        self.infinite_math_intersection = [(float('-inf'), -674.37), (10.41, 22.2), (103, float('inf'))]
        self.numeric_math_intersection = [(-589, -65), -55, (-17.02, -12.05), (12.05, 22.2)]

        self.math_points_1 = [-782, -674.37, -505, 17.02, 62.6, 98.9, 103, 145.9]
        self.math_points_2 = [-600, -374.98, -55, -17.02, 0, 19.74, 45]

        self.test_results_1 = [[-782], [-674.37], [-674.37], [17.02], [22.2, 103], [103], [103], [145.9]]
        self.test_results_2 = [[-589], [-374.98], [-55], [-17.02], [-12.05, 12.05], [19.74], [22.2]]

    def test_semi_infinite_math_sets_contain_point(self):
        """'AFFL' mode for math sets with semi-infinite ranges
        when the predetermined point belongs to the math intersection."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.semi_infinite_math_sets,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(-1.09, math_intersection,
                                                                   0, len(math_intersection))

        self.assertEqual(test_result, [-1.09])

    def test_semi_infinite_math_sets_do_not_contain_point(self):
        """'AFFL' mode for math sets with semi-infinite ranges
        when the predetermined point does not belong to the math intersection."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.semi_infinite_math_sets,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(-15.01, math_intersection,
                                                                   0, len(math_intersection))
        self.assertEqual(test_result, self.semi_infinite_math_sets_do_not_contain_point)

    def test_numeric_math_sets_contain_point(self):
        """'AFFL' mode for the numeric math sets
        when the predetermined point belongs to the math intersection."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.numeric_math_sets,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(8.51, math_intersection,
                                                                   0, len(math_intersection))
        self.assertEqual(test_result, [8.51])

    def test_numeric_math_sets_do_not_contain_point(self):
        """'AFFL' mode for the numeric math sets
        when the predetermined point does not belong to the math intersection."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.numeric_math_sets,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(19.34, math_intersection,
                                                                   0, len(math_intersection))
        self.assertEqual(test_result, self.numeric_math_sets_do_not_contain_point)

    def test_two_closest_endpoints_case(self):
        """'AFFL' mode for the predetermined point which does not belong to the math intersection
        and has two closest endpoints."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.two_closest_endpoints_case,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(-1, math_intersection,
                                                                   0, len(math_intersection))
        self.assertEqual(test_result, self.two_closest_endpoints_case_output)

    def test_intersection_point_is_equal_to_given(self):
        """'AFFL' mode for the predetermined point which equals to the math intersection point."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.intersection_points_case,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(42.7, math_intersection,
                                                                   0, len(math_intersection))
        self.assertEqual(test_result, [42.7])

    def test_intersection_point_is_not_equal_to_given(self):
        """'AFFL' mode for the predetermined point which not equal to the math intersection point."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.intersection_points_case,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(-53, math_intersection,
                                                                   0, len(math_intersection))
        self.assertEqual(test_result, self.intersection_point_do_not_equal_to_given)

    def test_math_sets_without_intersection(self):
        """'AFFL' mode for math sets without intersection."""
        math_intersection = determine_intersection_of_ini_math_ranges(self.math_sets_without_intersection,
                                                                      0, [])
        test_result = determine_closest_point_of_math_intersection(-1, math_intersection,
                                                                   0, len(math_intersection))
        self.assertEqual(test_result, [None])

    def test_closest_endpoint_for_infinite_math_intersection(self):
        """'AFFL' mode for different math points and finite math intersection."""
        for test_data, test_result in zip(self.math_points_1, self.test_results_1):
            result = determine_closest_point_of_math_intersection(test_data,
                                                                  self.infinite_math_intersection,
                                                                  0,
                                                                  len(self.infinite_math_intersection))
            self.assertEqual(result, test_result)

    def test_closest_endpoint_for_numeric_math_intersection(self):
        """'AFFL' mode for different math points and infinite math intersection."""
        for test_data, test_result in zip(self.math_points_2, self.test_results_2):
            result = determine_closest_point_of_math_intersection(test_data,
                                                                  self.numeric_math_intersection,
                                                                  0,
                                                                  len(self.numeric_math_intersection))
            self.assertEqual(result, test_result)

