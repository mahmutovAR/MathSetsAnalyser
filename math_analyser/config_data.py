from configparser import ConfigParser
from os.path import dirname, isdir, isfile, normpath, splitext

from errors import ConfigFileError, DataFileError, OutputDataError

PARSING_ERROR = 'contains data that is not specified or is invalid: '


class ConfigFileData:
    def __init__(self, data_format, data_file, output_file_format,
                 output_file_path, analysis_mode, math_point):
        """Creates an object of the ConfigData class,
        assigns values to the main script parameters from a configuration file."""
        self.data_format = data_format.upper()
        self.data_file = data_file
        self.output_file_format = output_file_format.lower()
        self.output_file_path = output_file_path
        self.analysis_mode = analysis_mode.upper()
        self.math_point = math_point

    def verify_config_data(self) -> None:
        """Validates configuration data.
        The data file type, output file type, analysis mode,
        and math point value (only for 'AFFL' mode) are checked for correctness.
        The data file and output file directory are checked for existence.
        If the check fails, an appropriate exception will be raised."""
        if self.analysis_mode == 'AFFL':
            if not self.math_point or self.math_point == float('-inf') or self.math_point == float('inf'):
                raise ConfigFileError(f'{PARSING_ERROR}"point" in the section [general]')
            try:
                self.math_point = float(self.math_point)
            except Exception:
                raise ConfigFileError(f'{PARSING_ERROR}"point" in the section [general]')
        elif self.analysis_mode == 'INTS':
            self.math_point = None
        else:
            raise ConfigFileError(f'{PARSING_ERROR}"mode" in the section [general]')

        if self.data_format not in ('JSON', 'TXT', 'XML'):
            raise ConfigFileError(f'{PARSING_ERROR}"format" in the section [input]')

        input_file_path, input_file_type = splitext(self.data_file)
        if input_file_type and input_file_type[1:] != self.data_format.lower():
            raise ConfigFileError(f'{PARSING_ERROR}"format" and "path" in the section [input]')

        if not self.data_file:
            raise ConfigFileError(f'{PARSING_ERROR}"path" in the section [input]')
        if not isfile(normpath(self.data_file)):
            raise DataFileError(f'not found in {self.data_file}')

        if self.output_file_format not in ('json', 'txt', 'xml'):
            raise ConfigFileError(f'{PARSING_ERROR}"format" in the section [output]')

        if not self.output_file_path:
            raise ConfigFileError(f'{PARSING_ERROR}"path" in the section [output]')
        output_dir = dirname(self.output_file_path)
        if not isdir(normpath(output_dir)):
            raise OutputDataError(f'directory not found in {output_dir}')

        output_file_path, output_file_type = splitext(self.output_file_path)
        if output_file_type and output_file_type[1:] != self.output_file_format.lower():
            raise ConfigFileError(f'{PARSING_ERROR}"format" and "path" in the section [output]')

    def get_data_format(self) -> str:
        """Returns the data file format."""
        return self.data_format

    def get_data_file(self) -> str:
        """Returns the path to the data file."""
        return self.data_file

    def get_output_file_format(self) -> str:
        """Returns the output file format."""
        return self.output_file_format

    def get_output_file_path(self) -> str:
        """Returns the path to the output file."""
        return self.output_file_path

    def get_analysis_mode(self) -> str:
        """Returns the analysis mode."""
        return self.analysis_mode

    def get_math_point(self) -> float:
        """Returns the math point value."""
        return self.math_point


def parse_configuration_file(input_file: str) -> ConfigFileData:
    """Checks for the presence of 'config.ini', if the file is not found ConfigFileNotFoundError will be raised.
    Validates the configuration data from the given configuration file.
    Returns ConfigData class object with the main configuration arguments."""
    if not isfile(input_file):
        raise ConfigFileError(f'not found: {input_file}')
    try:
        data_from_config_ini = ConfigParser()
        data_from_config_ini.read(input_file)

        section_general = data_from_config_ini['general']
        section_input = data_from_config_ini['input']
        section_output = data_from_config_ini['output']

        config_parameters = {'analysis_mode': section_general.get('mode'),
                             'math_point': section_general.getfloat('point'),
                             'data_format': section_input.get('format'),
                             'data_file': section_input.get('path'),
                             'output_file_format': section_output.get('format'),
                             'output_file_path': section_output.get('path')}
    except KeyError as err:
        raise ConfigFileError(f'{PARSING_ERROR}section [{err}]')
    except ValueError:
        raise ConfigFileError(f'{PARSING_ERROR}"point" in the section [general]')
    except Exception:
        print(f'Error! The parsing of the configuration file raised an exception:')
        raise
    else:
        config_file_data = ConfigFileData(**config_parameters)
        config_file_data.verify_config_data()
    return config_file_data
