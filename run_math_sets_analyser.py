from pathlib import Path

from math_sets_analyser import *


def main(script_config_data: 'ConfigData object'):
    """Firstly, the script parses configuration data file (config.ini) and defines the main parameters:
        data file type
        path to data file
        output file type
        path to output file
        analysis mode
        math point for 'AFFL' mode only
    Then the intersection of the initial math sets is determined.

    The 'INTS' mode outputs the math intersection to a given file.

    The 'AFFL' mode checks  if a given point belongs to the math intersection,
    or determines the nearest endpoint(s) and outputs the result to a given file.
    """
    if script_config_data.get_analysis_mode() == 'INTS':
        process_mode_intersection(script_config_data)
    elif script_config_data.get_analysis_mode() == 'AFFL':
        process_mode_affiliation(script_config_data)
    else:
        assert False, ('Internal error! main()'
                       '\nscript_config_data.get_analysis_mode() not INTS / AFFL')


def determine_initial_math_sets_intersection(script_config_data: 'ConfigData object'):
    """Returns sorted intersection of initial math sets."""
    initial_math_sets = define_data_source_and_get_data(script_config_data)
    if len(initial_math_sets) == 1:
        return initial_math_sets[0].get_ini_math_ranges()

    all_ini_numeric_endpoints = get_all_initial_numeric_endpoints(initial_math_sets)
    format_ranges_using_all_ini_numeric_endpoints(all_ini_numeric_endpoints, initial_math_sets)
    ini_math_intersection = get_intersection_of_ini_math_ranges(initial_math_sets, 0, set())
    if ini_math_intersection:
        return format_and_sort_math_intersection(ini_math_intersection)
    else:
        raise NoIntersectionError


def process_mode_intersection(script_config_data: 'ConfigData object'):
    """Determines and outputs file with the intersection of initial math sets."""
    sorted_math_intersection = determine_initial_math_sets_intersection(script_config_data)
    result_title = 'The intersection of initial math sets'
    output_script_data(script_config_data, result_title, sorted_math_intersection)


def process_mode_affiliation(script_config_data: 'ConfigData object'):
    """Determines and outputs file with the nearest endpoint(s) to predetermined point."""
    sorted_math_intersection = determine_initial_math_sets_intersection(script_config_data)
    result_title, result_data = determine_affiliation_of_point_to_intersection(script_config_data,
                                                                               sorted_math_intersection)
    output_script_data(script_config_data, result_title, result_data)


if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parent
    configuration_file_path = os_path_join(base_dir, 'config.ini')
    configuration_data = parse_configuration_file(configuration_file_path)
    main(configuration_data)
