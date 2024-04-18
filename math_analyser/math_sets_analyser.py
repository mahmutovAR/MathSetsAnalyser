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


def determine_closest_point_of_math_intersection(math_point: float, math_intersection: list,
                                                 subrange_index: int = 0, slice_length: int = 0) -> list:
    """Recursive function returns a math point if it is at the intersection of the initial math ranges
    or the closest endpoint(s) to the math point.
    Function arguments are
    - math point
    - math ranges list;
    - math range list index;
    - math ranges list length.
    On initial run, the function gets a math point, math ranges list, index 0, and math ranges list length."""
    if not math_intersection or math_intersection == [None]:
        return [None]

    first_subrange = math_intersection[0]
    last_subrange = math_intersection[-1]

    mid_index = subrange_index + slice_length // 2
    mid_subrange = math_intersection[mid_index]

    sub_ranges = math_intersection[subrange_index: subrange_index + slice_length + 1]

    if len(sub_ranges) == 1:
        one_subrange = sub_ranges[0]
        if (math_point == one_subrange or
            (math_point >= start_point(one_subrange) and math_point <= end_point(one_subrange))):
            return [math_point]
        elif math_point < start_point(one_subrange):
            if one_subrange == first_subrange:
                return [start_point(one_subrange)]
            else:
                return closest_point_of_two_ranges(math_point,
                                                   math_intersection[subrange_index - 1],
                                                   math_intersection[subrange_index])
        elif math_point > start_point(one_subrange):
            if one_subrange == last_subrange:
                return [end_point(one_subrange)]
            else:
                return closest_point_of_two_ranges(math_point,
                                                   math_intersection[subrange_index],
                                                   math_intersection[subrange_index + 1])

    if (math_point == mid_subrange or
            (math_point >= start_point(mid_subrange) and math_point <= end_point(mid_subrange))):
        return [math_point]

    elif math_point < start_point(mid_subrange):
        if mid_subrange == first_subrange:
            return [start_point(mid_subrange)]
        else:
            prev_subrange = math_intersection[mid_index - 1]
            if (round(abs(math_point - end_point(prev_subrange)), 3)
                    == round(abs(math_point - start_point(mid_subrange)), 3)):
                return [end_point(prev_subrange), start_point(mid_subrange)]
            elif round(abs(math_point - end_point(prev_subrange)), 3) > round(abs(math_point - start_point(mid_subrange)), 3):
                return [start_point(mid_subrange)]
            else:
                return determine_closest_point_of_math_intersection(math_point,
                                                                    math_intersection,
                                                                    subrange_index,
                                                                    slice_length // 2 - 1)

    elif math_point > start_point(mid_subrange):
        if mid_subrange == last_subrange:
            return [end_point(mid_subrange)]
        else:
            next_subrange = math_intersection[mid_index + 1]
            if (round(abs(math_point - end_point(mid_subrange)), 3)
                    == round(abs(math_point - start_point(next_subrange)), 3)):
                return [end_point(mid_subrange), start_point(next_subrange)]
            elif round(abs(math_point - end_point(mid_subrange)), 3) < round(abs(math_point - start_point(next_subrange)), 3):
                return [end_point(mid_subrange)]
            else:
                return determine_closest_point_of_math_intersection(math_point,
                                                                    math_intersection,
                                                                    mid_index + 1,
                                                                    slice_length - slice_length // 2 - 1)
