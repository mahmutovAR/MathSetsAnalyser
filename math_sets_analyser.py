import json
from configparser import ConfigParser
from os.path import abspath, dirname, isfile, splitext
from os.path import join as os_path_join

from bs4 import BeautifulSoup
from chameleon import PageTemplateLoader

from errors import *
from math_analyser import ConfigData, MathSet


def parse_configuration_data_file(input_file: str) -> 'ConfigData object':
    """Checks for the presence of 'config.ini', if the file is not found ConfigFileNotFoundError will be raised.
    Validates the configuration data from the given configuration file.
    Returns ConfigData class object with the main configuration arguments."""
    if not isfile(input_file):
        raise ConfigFileNotFoundError(input_file)
    try:
        data_from_config_ini = ConfigParser()
        data_from_config_ini.read(input_file)

        section_general = data_from_config_ini['general']
        section_input = data_from_config_ini['input']
        section_output = data_from_config_ini['output']

        analysis_mode = section_general.get('mode')
        input_point = section_general.getfloat('point')
        data_format = section_input.get('format')
        data_file = section_input.get('path')
        output_file_format = section_output.get('format')
        output_file_path = section_output.get('path')
    except KeyError as err:
        raise ConfigFileParsingError(f'section [{err}]')
    except ValueError:
        raise ConfigFileParsingError('"point" in the section [general]')
    except Exception:
        print(f'Error! The parsing of the configuration file raised an exception:')
        raise
    else:
        config_data = ConfigData(data_format, data_file, output_file_format,
                                 output_file_path, analysis_mode, input_point)
        config_data.verify_config_data()
    return config_data


def define_data_source_and_get_data(config_data: 'ConfigData object') -> list:
    """Defines type of the data file and returns the initial data as the list of objects MathSet class.
    If the data is invalid or cannot be determined, a DataGettingError is raised."""
    data_file_path = config_data.get_data_file()
    data_format = config_data.get_data_format()
    try:
        if data_format == 'JSON':
            ini_math_sets = get_data_from_json_file(data_file_path)
        elif data_format == 'TXT':
            ini_math_sets = get_data_from_txt_file(data_file_path)
        else:  # elif data_format == 'XML'
            ini_math_sets = get_data_from_xml_file(data_file_path)
    except DataGettingError:
        raise
    except Exception as err:
        raise DataGettingError(data_file_path, err)
    return ini_math_sets


def get_data_from_json_file(input_path: str) -> list:
    """Returns initial math sets from JSON file."""
    with open(input_path) as json_data_file:
        json_data = json.load(json_data_file)
    ini_math_sets = list()
    for math_set_name, math_ranges in json_data.items():
        math_ranges = eval(math_ranges)
        verify_ini_math_sets(input_path, math_set_name, math_ranges)
        ini_math_sets.append(MathSet(math_set_name, math_ranges))
    return ini_math_sets


def get_data_from_txt_file(input_path: str) -> list:
    """Returns initial math sets from TXT file."""
    ini_math_sets = list()
    with open(input_path) as txt_data_file:
        math_set_name = txt_data_file.readline().rstrip()
        while math_set_name != '':
            math_ranges = txt_data_file.readline().rstrip()
            math_ranges = eval(math_ranges)
            verify_ini_math_sets(input_path, math_set_name, math_ranges)
            ini_math_sets.append(MathSet(math_set_name, math_ranges))
            math_set_name = txt_data_file.readline().rstrip()

    return ini_math_sets


def get_data_from_xml_file(input_path: str) -> list:
    """Returns initial math sets from XML file."""
    with open(input_path) as xml_data_file:
        data_xml = xml_data_file.read()
    bs_object = BeautifulSoup(data_xml, 'lxml')
    all_math_sets = bs_object.find_all('mathset')
    ini_math_sets = list()
    for line in all_math_sets:
        math_set_name = line.get('math_set_name')
        math_ranges = line.find('value').get_text()
        math_ranges = eval(math_ranges)
        verify_ini_math_sets(input_path, math_set_name, math_ranges)
        ini_math_sets.append(MathSet(math_set_name, math_ranges))
    return ini_math_sets


def verify_ini_math_sets(data_file_path: str, input_set_name: str, input_ranges: list) -> None:
    """Validates input subset. There are two kinds of invalid data.
    Invalid syntax:
        - math set is not presented as a "list"
        - math range not specified as "tuple"
        - math range does not consist of two endpoints
        - math point is not specified as "int" or "float"

    Invalid math range:
        - the presence of any ranges, if ("-inf", "+inf") is given
        - invalid semi-infinite or numeric math range (start point is not less than the end point)
    If the check fails, DataGettingError is raised."""
    if not input_ranges:
        error_report = f'No data for math set:\n\t{input_set_name}'
        raise DataGettingError(data_file_path, error_report)

    elif not isinstance(input_ranges, list):
        error_report = f'Math set is not represented as a list of ranges and points:\n' \
                       f'\t{input_set_name}\n\t{input_ranges}'
        raise DataGettingError(data_file_path, error_report)

    for subrange in input_ranges:
        if subrange == ('-inf', '+inf') and len(input_ranges) != 1:
            error_report = f'Math set must not contain any ranges if ("-inf", "+inf") is given:\n' \
                           f'\t{input_set_name}\n\t{input_ranges}'
            raise DataGettingError(data_file_path, error_report)
        
        elif not isinstance(subrange, tuple) and not isinstance(subrange, int) and not isinstance(subrange, float):
            error_report = f'Math ranges and math points must be given as "tuple" and "int"("float"):\n' \
                           f'\t{input_set_name}\n\t{input_ranges}'
            raise DataGettingError(data_file_path, error_report)

        elif isinstance(subrange, tuple) and len(subrange) != 2:
            error_report = f'Math range must contain two endpoints::\n' \
                           f'\t{input_set_name}\n\t{input_ranges}'
            raise DataGettingError(data_file_path, error_report)

        elif isinstance(subrange, tuple):
            endpoint_1, endpoint_2 = subrange
            if endpoint_2 == '-inf':
                error_report = f'Semi-infinite math range must be given as ("-inf", 12) or (23, "+inf"):\n' \
                               f'\t{input_set_name}\n\t{input_ranges}'
                raise DataGettingError(data_file_path, error_report)

            elif endpoint_1 == '+inf':
                error_report = f'Semi-infinite math range must be given as ("-inf", 12) or (23, "+inf"):\n' \
                               f'\t{input_set_name}\n\t{input_ranges}'
                raise DataGettingError(data_file_path, error_report)

            elif isinstance(endpoint_1, str) and endpoint_1 not in ['-inf', '+inf']:
                error_report = f'Math ranges must not contain string values other than "-inf" or "+inf":\n' \
                               f'\t{input_set_name}\n\t{input_ranges}'
                raise DataGettingError(data_file_path, error_report)

            elif isinstance(endpoint_2, str) and endpoint_2 not in ['-inf', '+inf']:
                error_report = f'Math ranges must not contain string values other than "-inf" or "+inf":\n' \
                               f'\t{input_set_name}\n\t{input_ranges}'
                raise DataGettingError(data_file_path, error_report)

            elif not isinstance(endpoint_1, str) and not isinstance(endpoint_2, str) and endpoint_1 >= endpoint_2:
                error_report = f'Start point in the math set must be less than the end point:\n' \
                               f'\t{input_set_name}\n\t{input_ranges}'
                raise DataGettingError(data_file_path, error_report)


def get_all_initial_numeric_endpoints(ini_math_sets: list) -> set:
    """Returns set with all numeric endpoints of inputted math sets."""
    all_numeric_endpoints = set()

    for math_set in ini_math_sets:
        math_set.define_endpoints()
        math_set_numeric_endpoints = math_set.get_numeric_endpoints()
        all_numeric_endpoints.update(math_set_numeric_endpoints)

    if not all_numeric_endpoints:
        raise InfiniteSetError

    return all_numeric_endpoints


def format_ranges_using_all_ini_numeric_endpoints(all_numeric_endpoints: set, ini_math_sets: list) -> None:
    """Changes in math subrange value '-inf' to min endpoint and '+inf' to max endpoint.
    Minimal and maximal values are defined from endpoints of all initial math sets."""
    min_value = min(all_numeric_endpoints)
    max_value = max(all_numeric_endpoints)
    for math_set in ini_math_sets:
        math_set.format_ranges_using_all_endpoints(all_numeric_endpoints, min_value, max_value)


def get_intersection_of_ini_math_ranges(ini_math_sets: list, set_index: int, subrange_of_intersection: set) -> set:
    """Recursive function to determine the intersection of the initial math sets by comparing all sets step by step.
    Function arguments are
    - list of initial math sets;
    - index of math set;
    - result of the previous math sets comparison.
    On initial run, the function gets a list of math sets, index 0, and an empty set."""
    if set_index == 0:
        math_range_1 = ini_math_sets[set_index].get_formatted_math_set()
        math_range_2 = ini_math_sets[set_index + 1].get_formatted_math_set()
        subrange_of_intersection = math_range_1.intersection(math_range_2)
        if not subrange_of_intersection:
            raise NoIntersectionError
        return get_intersection_of_ini_math_ranges(ini_math_sets, set_index + 2, subrange_of_intersection)
    elif set_index < len(ini_math_sets):
        math_range_1 = ini_math_sets[set_index].get_formatted_math_set()
        subrange_of_intersection = math_range_1.intersection(subrange_of_intersection)
        if not subrange_of_intersection:
            raise NoIntersectionError
        return get_intersection_of_ini_math_ranges(ini_math_sets, set_index + 1, subrange_of_intersection)
    elif set_index == len(ini_math_sets):
        return subrange_of_intersection


def format_and_sort_math_intersection(math_intersection: set) -> list:
    """Returns the final set of math ranges and points.
    Duplicate endpoints of math ranges are removed.
    All math ranges and points sorted in ascending order"""
    math_ranges = set()
    math_ranges_endpoints = set()
    math_points = set()

    for subrange_of_intersection in math_intersection:
        if isinstance(subrange_of_intersection, tuple):
            math_ranges_endpoints.update(subrange_of_intersection)
            math_ranges.add(subrange_of_intersection)
        else:
            math_points.add(subrange_of_intersection)

    output_math_points = math_points.difference(math_ranges_endpoints)
    math_ranges.update(output_math_points)

    sorted_math_intersection = list(math_ranges)
    sorted_math_intersection = sorted(sorted_math_intersection, key=sorting_criterion)

    return sorted_math_intersection


def sorting_criterion(input_subrange):
    """Returns the starting endpoint for a numeric math range,
    or the numeric endpoint for a semi-infinite math range and a number for a math point."""
    if isinstance(input_subrange, tuple):
        if isinstance(input_subrange[0], str):
            return input_subrange[1]
        else:
            return input_subrange[0]
    else:
        return input_subrange


def determine_affiliation_of_point_to_intersection(config_data: 'ConfigData object', math_intersection: list) -> None:
    """Determines the subrange of the inputted math intersection that contains initial predetermined point,
    or the nearest endpoint(s) otherwise. Outputs a file with the result of the script running."""
    subrange_contains_point = None
    point_of_intersection_equal_to_point = None
    nearest_endpoint_to_point = None
    given_point = config_data.get_input_point()
    for subrange in math_intersection:
        if isinstance(subrange, tuple):
            endpoint_1, endpoint_2 = subrange
            if isinstance(endpoint_1, str) or isinstance(endpoint_2, str):
                subrange_contains_point = compare_point_and_infinity_range(subrange, given_point)
                if subrange_contains_point:
                    break
            elif given_point >= endpoint_1 and given_point <= endpoint_2:
                subrange_contains_point = subrange
                break
        else:
            if given_point == subrange:
                point_of_intersection_equal_to_point = subrange
                break

    if not subrange_contains_point:
        nearest_endpoint_to_point = determine_nearest_endpoint(math_intersection, given_point)

    if subrange_contains_point:
        script_result_title = 'The subrange of the initial math sets intersection with the predetermined point'
        output_script_data(config_data, script_result_title, [subrange_contains_point])
    elif point_of_intersection_equal_to_point:
        script_result_title = 'The point of the initial math sets intersection is the predetermined point'
        output_script_data(config_data, script_result_title, point_of_intersection_equal_to_point)
    else:  # elif nearest_endpoint_to_point:
        script_result_title = 'The nearest endpoint(s) to the predetermined point'
        output_script_data(config_data, script_result_title, list(nearest_endpoint_to_point))


def compare_point_and_infinity_range(input_subrange: tuple, input_point: float) -> tuple:
    """Returns the inputted infinite subrange, if it contains the predetermined point, or None otherwise."""
    if input_subrange[0] == '-inf' and input_point <= input_subrange[1]:
        return input_subrange
    elif input_subrange[1] == '+inf' and input_point >= input_subrange[0]:
        return input_subrange


def determine_nearest_endpoint(math_intersection: list, input_point: float) -> list:
    """Returns list of the nearest element(s) from the inputted list for the inputted point."""
    numeric_endpoints = set()
    nearest_endpoint_to_point = None

    for subrange_of_intersection in math_intersection:
        if isinstance(subrange_of_intersection, tuple):
            endpoint_1, endpoint_2 = subrange_of_intersection
            if not isinstance(endpoint_1, str):
                numeric_endpoints.add(endpoint_1)
            if not isinstance(endpoint_2, str):
                numeric_endpoints.add(endpoint_2)
        else:
            numeric_endpoints.add(subrange_of_intersection)

    numeric_endpoints = sorted(list(numeric_endpoints))

    for cnt in range(len(numeric_endpoints)):
        if cnt == len(numeric_endpoints) - 1:
            nearest_endpoint_to_point = [numeric_endpoints[-1]]
        else:  # cnt < len(numeric_endpoints)-1
            nearest_endpoint_to_point = compare_point_and_endpoints(numeric_endpoints[cnt],
                                                                    numeric_endpoints[cnt + 1],
                                                                    input_point)
            if nearest_endpoint_to_point:
                break
    return nearest_endpoint_to_point


def compare_point_and_endpoints(endpoint_current: float, endpoint_next: float, input_point: float) -> list:
    """Returns a list of one (both) of the inputted number(s),
    if it (they) is (are) the nearest to the given point, or None otherwise."""
    nearest_endpoint = list()
    diff_current = abs(endpoint_current - input_point)
    diff_next = abs(endpoint_next - input_point)
    if diff_current < diff_next:
        nearest_endpoint.append(endpoint_current)
    elif diff_current == diff_next:
        nearest_endpoint.extend([endpoint_current, endpoint_next])

    return nearest_endpoint


def output_script_data(config_data: 'ConfigData object', output_title: str, output_data: list):
    """Generates the output file with the inputted title and data.
    The file type and path are determined from the inputted ConfigData object."""
    output_file_format = config_data.get_output_file_format()
    output_file_path = config_data.get_output_file_path()

    try:
        output_file_path = choose_name_for_output_file(output_file_format, output_file_path)
        if output_file_format == 'json':
            generate_json_output_file(output_file_path, output_title, output_data)
        elif output_file_format == 'txt':
            generate_txt_output_file(output_file_path, output_title, output_data)
        else:  # elif output_file_format == 'xml':
            generate_xml_output_file(output_file_path, output_title, output_data)
    except Exception as err:
        raise OutputFileGeneratingError(output_file_path, err)


def choose_name_for_output_file(file_format: str, file_path: str) -> str:
    """Returns name of the output file, if the file with inputted name already exists then
    the output file will be renamed, "({num})" will be added to its name (for example: output_file(1).txt)."""
    temp_file_path = splitext(file_path)[0]
    if isfile(f'{temp_file_path}.{file_format}'):
        num = 1
        while isfile(f'{temp_file_path}({num}).{file_format}'):
            num += 1
        return f'{temp_file_path}({num}).{file_format}'
    else:
        return f'{temp_file_path}.{file_format}'


def generate_json_output_file(output_file_path: str, title: str, data: list) -> None:
    """Generates on given path the JSON file with inputted title and data."""
    with open(output_file_path, 'w') as json_data_file:
        json.dump({title: str(data)}, json_data_file)


def generate_txt_output_file(output_file_path: str, title: str, data: list) -> None:
    """Generates on given path the TXT file with inputted title and data."""
    with open(output_file_path, 'w') as txt_output_file:
        txt_output_file.write(f'{title}\n{data}')


def generate_xml_output_file(output_file_path: str, title: str, data: list) -> None:
    """Generates on given path the XML file with inputted title and data."""
    template = PageTemplateLoader(os_path_join(abspath(dirname(__file__)), 'math_analyser', 'templates'))
    tmpl = template['output_temp.pt']
    with open(output_file_path, 'w') as xml_output_file:
        data_for_xml = tmpl(output_title=title, output_data=data)
        xml_output_file.write(data_for_xml)
