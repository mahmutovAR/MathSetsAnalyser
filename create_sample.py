from configparser import ConfigParser
from os.path import abspath, dirname
from os.path import join as os_path_join


def generate_config_file(input_file_path: str, input_data: dict) -> None:
    """Generates config file for AFFL mode at given path."""
    test_config_ini = ConfigParser()

    test_mode = input_data['analysis_mode']
    test_point = input_data['input_point']
    test_input_format = input_data['data_format']
    test_input_path = input_data['data_file']
    test_output_format = input_data['output_file_format']
    test_output_path = input_data['output_file_path']

    test_config_ini['general'] = {'mode': test_mode, 'point': test_point}
    test_config_ini['input'] = {'format': test_input_format,
                                'path': test_input_path}
    test_config_ini['output'] = {'format': test_output_format,
                                 'path': test_output_path}
    with open(input_file_path, 'w') as config_file:
        test_config_ini.write(config_file)


def generate_data_file(input_file: str) -> None:
    """Generates TXT data file at given path."""
    test_data = {'math set 1': [('-inf', -10), (10, '+inf')],
                 'math set 2': [(-77, 61)],
                 'math set 3': [(-89, -61), (-43, -12), (10, 27), (61, 72)]}
    with open(input_file, 'w') as txt_data_file:
        for math_set_name, math_subrange in test_data.items():
            txt_data_file.write(f'{math_set_name}\n{math_subrange}\n')


def main():
    """The script creates sample configuration and data files in the same directory as itself.
    Then running "run_math_sets_analyser" outputs a result file."""
    script_dir = abspath(dirname(__file__))
    config_file = os_path_join(script_dir, 'config.ini')
    data_file = os_path_join(script_dir, 'data file.txt')
    output_file = os_path_join(script_dir, 'script_result')
    config_parameters = {'analysis_mode': 'AFFL',
                         'input_point': -1.0,
                         'data_format': 'TXT',
                         'data_file': data_file,
                         'output_file_format': 'XML',
                         'output_file_path': output_file}
    try:
        generate_config_file(config_file, config_parameters)
        generate_data_file(data_file)
    except Exception:
        print(f'Error! Generating the "config.ini" and data file raised an exception:')
        raise
    else:
        print('Created configuration file "config.ini" and data file "data file.txt".')


if __name__ == '__main__':
    main()
