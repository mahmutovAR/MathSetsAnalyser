from copy import deepcopy


class MathSet:
    __slots__ = ['__math_set_name', '__ini_math_ranges', '__numeric_endpoints',
                 '__infinite_endpoints', '__formatted_ini_math_set']

    def __init__(self, math_set_name, ini_math_ranges):
        """Creates an object of the MathSet class, assigns values to the math set and its name.
        The math set given in the data file is called the initial math set."""
        self.__math_set_name = math_set_name
        self.__ini_math_ranges = ini_math_ranges
        self.__numeric_endpoints = set()
        self.__infinite_endpoints = set()
        self.__formatted_ini_math_set = deepcopy(ini_math_ranges)

    def get_ini_math_set_name(self) -> str:
        """Returns math set name."""
        return self.__math_set_name

    def get_ini_math_ranges(self) -> list:
        """Returns initial math set."""
        return self.__ini_math_ranges

    def define_endpoints(self) -> None:
        """Defines endpoints of the initial math set."""
        add_endpoint(self.__ini_math_ranges, self.__numeric_endpoints, self.__infinite_endpoints)

    def get_numeric_endpoints(self) -> set:
        """Returns numeric endpoints of the initial math set."""
        return self.__numeric_endpoints

    def format_ranges_using_all_endpoints(self, all_numeric_endpoints: set,
                                          min_endpoint: float, max_endpoint: float) -> None:
        """Formats a copy of the initial math set,
        all math ranges are determined in endpoint ranges of all initial math sets from data file."""
        edit_with_min_and_max_value(self.__formatted_ini_math_set, min_endpoint, max_endpoint)
        self.__formatted_ini_math_set = edit_with_all_ini_numeric_endpoints(self.__formatted_ini_math_set,
                                                                            all_numeric_endpoints)
        if self.__infinite_endpoints:
            self.__formatted_ini_math_set = add_infinite_endpoints(self.__formatted_ini_math_set,
                                                                   self.__infinite_endpoints,
                                                                   min_endpoint, max_endpoint)

    def get_formatted_math_set(self) -> set:
        """Returns formatted math set."""
        return set(self.__formatted_ini_math_set)


def add_endpoint(input_math_ranges: list or set, numeric_endpoints: set, infinite_endpoints: set) -> None:
    """Adds endpoints of each subrange into the list of the all endpoints of math set."""
    for endpoint in input_math_ranges:
        if isinstance(endpoint, tuple):
            add_endpoint(endpoint, numeric_endpoints, infinite_endpoints)
        else:
            if isinstance(endpoint, str):
                infinite_endpoints.add(endpoint)
            else:
                numeric_endpoints.add(endpoint)


def edit_with_min_and_max_value(input_math_set: list, min_range_value: float, max_range_value: float) -> None:
    """Formats initial math set. The value '-inf' is replaced by the min endpoint
    and the value '+inf' is replaced by the max endpoint.
    Minimal and maximal values are determined from endpoints of all initial math sets.
    All sub ranges are reduced to the set of ranges from all endpoints."""
    if input_math_set == [('-inf', '+inf')]:
        formatted_subrange = (min_range_value, max_range_value)
        input_math_set.remove(('-inf', '+inf'))
        input_math_set.append(formatted_subrange)

    for index, subrange in enumerate(input_math_set):
        if isinstance(subrange, tuple):
            endpoint_1, endpoint_2 = subrange
            if isinstance(endpoint_1, str):
                formatted_subrange = (min_range_value, endpoint_2)
                input_math_set[index] = formatted_subrange

            elif isinstance(endpoint_2, str):
                formatted_subrange = (endpoint_1, max_range_value)
                input_math_set[index] = formatted_subrange


def edit_with_all_ini_numeric_endpoints(input_math_set: list, numeric_endpoints: set) -> list:
    """Inputted math sub ranges are determined in ranges of given numeric endpoints."""
    if len(input_math_set) == 1 and not isinstance(input_math_set[0], tuple):
        return input_math_set
    formatted_math_set = list()
    numeric_endpoints = sorted(list(numeric_endpoints))
    for subrange in input_math_set:
        if isinstance(subrange, tuple):
            subrange_beginning, subrange_ending = subrange
            converted_subrange = convert_subrange(numeric_endpoints, subrange_beginning, subrange_ending)
            formatted_math_set.extend(converted_subrange)
        else:
            formatted_math_set.append(subrange)

    return formatted_math_set


def convert_subrange(numeric_endpoints: list, range_beginning: float, range_ending: float) -> list:
    """The initial math subrange given by (range_beginning to range_ending) is converted
    to the set of tuples of endpoints contained in this subrange. Endpoints are also added."""
    start_index = numeric_endpoints.index(range_beginning)
    end_index = numeric_endpoints.index(range_ending)
    output_subrange = list()
    while start_index != end_index:
        temp_subrange = (numeric_endpoints[start_index], numeric_endpoints[start_index + 1])
        output_subrange.append(temp_subrange)
        output_subrange.append(numeric_endpoints[start_index])
        start_index += 1
    output_subrange.append(numeric_endpoints[end_index])

    return output_subrange


def add_infinite_endpoints(input_subset: list, infinite_endpoints: set,
                           min_range_value: float, max_range_value: float) -> list:
    """Adds ranges with '-inf' and '+inf' to the formatted set of initial math set."""
    if '-inf' in infinite_endpoints:
        infinite_range = ('-inf', min_range_value)
        input_subset.append(infinite_range)
    if '+inf' in infinite_endpoints:
        infinite_range = (max_range_value, '+inf')
        input_subset.append(infinite_range)
    return input_subset
