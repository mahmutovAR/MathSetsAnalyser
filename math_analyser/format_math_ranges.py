def format_math_ranges(math_ranges: list | set, endpoints: list) -> set:
    """Returns a formatted copy of the initial math set,
    math ranges are determined in endpoint and math points ranges."""
    formatted_math_ranges = list()
    for subrange in math_ranges:
        if isinstance(subrange, tuple):
            formatted_math_ranges.extend(format_subrange(subrange, endpoints))
        else:
            formatted_math_ranges.append(subrange)
    return set(formatted_math_ranges)


def get_endpoints_of_two_math_ranges(range_1: list, range_2: list) -> list:
    """Defines ranges endpoints of two initial math sets."""
    endpoints = add_math_points(range_1, list())
    endpoints = add_math_points(range_2, endpoints)
    return sorted(endpoints)


def add_math_points(math_range: list, input_endpoints: list) -> list:
    """Adds ranges endpoints to inputted list."""
    for element in math_range:
        if isinstance(element, tuple):
            input_endpoints.extend(list(element))
        else:
            input_endpoints.append(element)
    return list(set(input_endpoints))


def format_subrange(subrange: tuple, endpoints: list) -> list:
    """Converts the inputted subrange into a list of sub ranges according to the entered endpoints.
    Ranges with '-inf' ('+inf') are converted according to min (max) value of numeric endpoints.
    """
    start, end = subrange
    start_index = endpoints.index(start)
    end_index = endpoints.index(end)
    formatted_subrange = list()
    while start_index != end_index:
        formatted_subrange.append((endpoints[start_index], endpoints[start_index + 1]))
        formatted_subrange.append(endpoints[start_index])
        start_index += 1
    formatted_subrange.append(endpoints[end_index])
    return formatted_subrange


def remove_duplicate_endpoints(input_subrange: set) -> set:
    """Removes math points from the inputted subrange if they are its endpoints."""
    ranges = set()
    ranges_points = set()
    endpoints = set()
    for subrange in input_subrange:
        if isinstance(subrange, tuple):
            ranges.add(subrange)
            ranges_points = ranges_points.union(subrange)
        else:
            endpoints.add(subrange)

    endpoints.difference_update(ranges_points)
    return ranges.union(endpoints)
