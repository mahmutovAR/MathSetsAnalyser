from json import load as json_load

from bs4 import BeautifulSoup

from errors import DataFileError


def get_initial_math_sets(config_data: 'ConfigData object') -> list:
    """Defines type of the data file and returns the initial data as the list of objects MathSet class.
    If the data is invalid or cannot be determined, a DataGettingError is raised."""
    data_file_path = config_data.get_data_file()
    data_format = config_data.get_data_format()
    try:
        with open(data_file_path) as file_to_read:
            if data_format == 'JSON':
                ini_math_sets = get_data_from_json_file(file_to_read)
            elif data_format == 'TXT':
                ini_math_sets = get_data_from_txt_file(file_to_read)
            elif data_format == 'XML':
                ini_math_sets = get_data_from_xml_file(file_to_read)
            else:
                assert False, ('Internal error! define_data_source_and_get_data()'
                               '\ndata_format not JSON / TXT / XML')
    except Exception as err:
        err.add_note('Initial Data Getting Error')
        raise
    else:
        return ini_math_sets


def get_data_from_json_file(input_data: '_io.TextIOWrapper object') -> list:
    """Returns initial math sets from JSON file."""
    ini_math_sets = list()
    for math_ranges in json_load(input_data):
        math_ranges = eval(math_ranges)
        verify_ini_math_sets(math_ranges)
        ini_math_sets.append(math_ranges)
    return ini_math_sets


def get_data_from_txt_file(input_data: '_io.TextIOWrapper object') -> list:
    """Returns initial math sets from TXT file."""
    ini_math_sets = list()
    for math_ranges in input_data.readlines():
        math_ranges = eval(math_ranges)
        verify_ini_math_sets(math_ranges)
        ini_math_sets.append(math_ranges)
    return ini_math_sets


def get_data_from_xml_file(input_data: '_io.TextIOWrapper object') -> list:
    """Returns initial math sets from XML file."""
    data_xml = input_data.read()
    bs_object = BeautifulSoup(data_xml, 'lxml')
    all_math_ranges = bs_object.find_all('value')
    ini_math_sets = list()
    for line in all_math_ranges:
        math_ranges = line.get_text()
        math_ranges = eval(math_ranges)
        verify_ini_math_sets(math_ranges)
        ini_math_sets.append(math_ranges)
    return ini_math_sets


def verify_ini_math_sets(input_ranges: list) -> None:
    """Validates input math set. There are two kinds of invalid data.
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
        raise DataFileError('No data in file')

    elif not isinstance(input_ranges, list):
        raise DataFileError(f'Math set is not represented as a list of ranges and points:\n{input_ranges}')

    for subrange in input_ranges:
        if subrange == (float('-inf'), float('inf')) and len(input_ranges) != 1:
            raise DataFileError(f'Math set must not contain any ranges if '
                                f'(float(\'-inf\'), float(\'inf\')) is given:\t{input_ranges}')
        
        elif not isinstance(subrange, tuple) and not isinstance(subrange, int) and not isinstance(subrange, float):
            raise DataFileError(f'Math ranges and math points must be given '
                                f'as "tuple" and "int"("float"):\n{input_ranges}')

        elif isinstance(subrange, tuple) and len(subrange) != 2:
            raise DataFileError(f'Math range must contain two endpoints::\n\t{input_ranges}')

        elif isinstance(subrange, tuple):
            endpoint_1, endpoint_2 = subrange
            if (endpoint_2 == float('-inf')
                    or endpoint_1 == float('inf')
                    or isinstance(endpoint_1, str)
                    or isinstance(endpoint_2, str)):
                raise DataFileError(f'Semi-infinite math range must be given as'
                                    f' (float(\'-inf\'), 12) or (23, float(\'inf\'):\n{input_ranges}')

            elif endpoint_1 >= endpoint_2:
                raise DataFileError(f'Start point in the math set must be less '
                                    f'than the end point:\n{input_ranges}')
