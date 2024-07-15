from bisect import bisect_left

from math_analyser import format_math_ranges, get_endpoints_of_two_math_ranges, remove_duplicate_endpoints


def determine_intersection_of_ini_math_ranges(ini_math_sets: list, set_index: int, math_intersection: list) -> list:
    """Recursive function to determine the intersection of the initial math sets by comparing all sets step by step.
    Function arguments are
    - list of initial math sets;
    - index of math set;
    - result of the previous math sets comparison.
    On initial run, the function gets a list of math sets, index 0, and an empty list.
    Returns list of math sub ranges."""
    if len(ini_math_sets) == 1:
        math_intersection = determine_intersection_of_two_math_ranges(ini_math_sets[0], list())
        return sorted(list(math_intersection), key=sorting_criterion)

    elif set_index == 0:
        math_intersection = determine_intersection_of_two_math_ranges(ini_math_sets[0], ini_math_sets[1])
        if not math_intersection:
            return [None]
        return determine_intersection_of_ini_math_ranges(ini_math_sets, set_index + 2, list(math_intersection))

    elif set_index < len(ini_math_sets):
        math_intersection = determine_intersection_of_two_math_ranges(math_intersection, ini_math_sets[set_index])
        if not math_intersection:
            return [None]
        return determine_intersection_of_ini_math_ranges(ini_math_sets, set_index + 1, list(math_intersection))

    else:
        math_intersection = remove_duplicate_endpoints(set(math_intersection))
        return sorted(list(math_intersection), key=sorting_criterion)


def determine_intersection_of_two_math_ranges(range_1: list, range_2: list) -> set:
    """Returns math intersection of two math ranges."""
    if not range_2:
        math_ranges_endpoints = get_endpoints_of_two_math_ranges(range_1, list())
        range_1_formatted = format_math_ranges(range_1, math_ranges_endpoints)
        return remove_duplicate_endpoints(set(range_1_formatted))

    math_ranges_endpoints = get_endpoints_of_two_math_ranges(range_1, range_2)
    range_1_formatted = format_math_ranges(range_1, math_ranges_endpoints)
    range_2_formatted = format_math_ranges(range_2, math_ranges_endpoints)
    return remove_duplicate_endpoints(range_1_formatted.intersection(range_2_formatted))


def sorting_criterion(input_subrange):
    """Returns the starting endpoint for a numeric math range,
    or the numeric endpoint for a semi-infinite math range and a number for a math point."""
    if isinstance(input_subrange, tuple):
        return input_subrange[0]
    else:
        return input_subrange


def start_point(subrange: tuple | float) -> float:
    """Returns the start (left) endpoint of a subrange or the range point itself."""
    if isinstance(subrange, tuple):
        return subrange[0]
    else:
        return subrange


def end_point(subrange: tuple | float) -> float:
    """Returns the end (right) endpoint of a subrange or the range point itself."""
    if isinstance(subrange, tuple):
        return subrange[1]
    else:
        return subrange


def closest_point_of_two_ranges(point: float, range_1: tuple | float, range_2: tuple | float) -> list:
    """Returns the closest endpoint(s) of a subrange (or range point) to a math point."""
    if round(abs(point - end_point(range_1)), 3) < round(abs(point - start_point(range_2)), 3):
        return [end_point(range_1)]
    elif round(abs(point - end_point(range_1)), 3) == round(abs(point - start_point(range_2)), 3):
        return [end_point(range_1), start_point(range_2)]
    else:
        return [start_point(range_2)]


def determine_closest_point_of_math_intersection(math_point: float, math_intersection: list) -> list:
    """Returns a math point if it is at the intersection of the initial math ranges
    or the closest endpoint(s) to the math point."""
    if not math_intersection or math_intersection == [None]:
        return [None]

    all_endpoints = list()
    for endpoint in math_intersection:
        if isinstance(endpoint, tuple):
            if endpoint[0] == float('-inf'):
                all_endpoints.append(endpoint[1])
            else:
                all_endpoints.append(endpoint[0])
        else:
            all_endpoints.append(endpoint)

    index = bisect_left(all_endpoints, math_point)

    if index == 0:
        subrange = math_intersection[0]
        if (math_point == subrange or
                (math_point >= start_point(subrange) and math_point <= end_point(subrange))):
            return [math_point]
        return [start_point(subrange)]

    elif index > len(math_intersection) - 1:
        subrange = math_intersection[-1]
        if (math_point == subrange or
                (math_point >= start_point(subrange) and math_point <= end_point(subrange))):
            return [math_point]
        elif math_point > end_point(subrange):
            return [end_point(subrange)]
        elif len(math_intersection) > 1:
            subrange = math_intersection[-2]
            if (math_point == subrange or
                    (math_point >= start_point(subrange) and math_point <= end_point(subrange))):
                return [math_point]
            return closest_point_of_two_ranges(math_point, math_intersection[-2], math_intersection[-1])

    else:
        subrange = math_intersection[index]

        if (math_point == subrange or
                (math_point >= start_point(subrange) and math_point <= end_point(subrange))):
            return [math_point]

        elif len(math_intersection) > 1:
            subrange = math_intersection[index - 1]
            if (math_point == subrange or
                    (math_point >= start_point(subrange) and math_point <= end_point(subrange))):
                return [math_point]

            return closest_point_of_two_ranges(math_point, math_intersection[index - 1], math_intersection[index])
