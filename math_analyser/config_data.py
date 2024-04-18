from configparser import ConfigParser
from os.path import dirname, isdir, isfile, normpath, splitext

from errors import (ConfigFileNotFoundError, ConfigFileParsingError,
                    DataFileNotFoundError, OutputDirectoryNotFoundError)


class ConfigFileData:
    __slots__ = ['__data_format', '__data_file', '__output_file_format',
                 '__output_file_path', '__analysis_mode', '__math_point']

    def __init__(self, data_format, data_file, output_file_format,
                 output_file_path, analysis_mode, math_point):
        """Creates an object of the ConfigData class,
        assigns values to the main script parameters from a configuration file."""
        self.__data_format = data_format.upper()
        self.__data_file = data_file
        self.__output_file_format = output_file_format.lower()
        self.__output_file_path = output_file_path
        self.__analysis_mode = analysis_mode.upper()
        self.__math_point = math_point

    def verify_config_data(self) -> None:
        """Validates configuration data.
        The data file type, output file type, analysis mode,
        and math point value (only for 'AFFL' mode) are checked for correctness.
        The data file and output file directory are checked for existence.
        If the check fails, an appropriate exception will be raised."""
        if self.__analysis_mode == 'AFFL':
            if not self.__math_point:
                raise ConfigFileParsingError('"point" in the section [general]')
            if self.__math_point == float('-inf') or self.__math_point == float('inf'):
                raise ConfigFileParsingError('"point" in the section [general]')
            try:
                self.__math_point = float(self.__math_point)
            except Exception:
                raise ConfigFileParsingError('"point" in the section [general]')
        elif self.__analysis_mode == 'INTS':
            self.__math_point = None
        else:
            raise ConfigFileParsingError('"mode" in the section [general]')

        if self.__data_format not in ('JSON', 'TXT', 'XML'):
            raise ConfigFileParsingError('"format" in the section [input]')

        input_file_path, input_file_type = splitext(self.__data_file)
        if input_file_type and input_file_type[1:] != self.__data_format.lower():
            raise ConfigFileParsingError('"format" and "path" in the section [input]')

        if not self.__data_file:
            raise ConfigFileParsingError('"path" in the section [input]')
        if not isfile(normpath(self.__data_file)):
            raise DataFileNotFoundError(self.__data_file)

        if self.__output_file_format not in ('json', 'txt', 'xml'):
            raise ConfigFileParsingError('"format" in the section [output]')

        if not self.__output_file_path:
            raise ConfigFileParsingError('"path" in the section [output]')
        output_dir = dirname(self.__output_file_path)
        if not isdir(normpath(output_dir)):
            raise OutputDirectoryNotFoundError(output_dir)

        output_file_path, output_file_type = splitext(self.__output_file_path)
        if output_file_type and output_file_type[1:] != self.__output_file_format.lower():
            raise ConfigFileParsingError('"format" and "path" in the section [output]')

    def get_data_format(self) -> str:
        """Returns the data file format."""
        return self.__data_format

    def get_data_file(self) -> str:
        """Returns the path to the data file."""
        return self.__data_file

    def get_output_file_format(self) -> str:
        """Returns the output file format."""
        return self.__output_file_format

    def get_output_file_path(self) -> str:
        """Returns the path to the output file."""
        return self.__output_file_path

    def get_analysis_mode(self) -> str:
        """Returns the analysis mode."""
        return self.__analysis_mode

    def get_math_point(self) -> float:
        """Returns the math point value."""
        return self.__math_point


def parse_configuration_file(input_file: str) -> ConfigFileData:
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

        config_parameters = {'analysis_mode': section_general.get('mode'),
                             'math_point': section_general.getfloat('point'),
                             'data_format': section_input.get('format'),
                             'data_file': section_input.get('path'),
                             'output_file_format': section_output.get('format'),
                             'output_file_path': section_output.get('path')}
    except KeyError as err:
        raise ConfigFileParsingError(f'section [{err}]')
    except ValueError:
        raise ConfigFileParsingError('"point" in the section [general]')
    except Exception:
        print(f'Error! The parsing of the configuration file raised an exception:')
        raise
    else:
        config_file_data = ConfigFileData(**config_parameters)
        config_file_data.verify_config_data()
    return config_file_data
