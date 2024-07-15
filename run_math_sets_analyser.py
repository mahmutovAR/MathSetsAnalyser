from pathlib import Path
from os.path import join as os_path_join

from math_analyser import *


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


def determine_initial_math_sets_intersection(script_config_data: 'ConfigData object') -> list:
    """Returns sorted intersection of initial math sets."""
    ini_math_sets = get_initial_math_sets(script_config_data)
    math_sets_intersection = determine_intersection_of_ini_math_ranges(ini_math_sets,
                                                                       0, list())
    if not math_sets_intersection:
        return [None]
    return math_sets_intersection


def process_mode_intersection(script_config_data: 'ConfigData object'):
    """Determines and outputs file with the intersection of initial math sets."""
    math_sets_intersection = determine_initial_math_sets_intersection(script_config_data)
    output_script_data(script_config_data, math_sets_intersection)


def process_mode_affiliation(script_config_data: 'ConfigData object'):
    """Determines and outputs file with the nearest endpoint(s) to predetermined point."""
    math_intersection = determine_initial_math_sets_intersection(script_config_data)
    math_point = script_config_data.get_math_point()
    result_data = determine_closest_point_of_math_intersection(math_point, math_intersection)
    output_script_data(script_config_data, result_data)


if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parent
    configuration_file_path = os_path_join(base_dir, 'config.ini')
    configuration_data = parse_configuration_file(configuration_file_path)
    main(configuration_data)
