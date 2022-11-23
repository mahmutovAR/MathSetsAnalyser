from errors import ConfigFileParsingError, DataFileNotFoundError, OutputDirectoryNotFoundError
from os.path import dirname, isdir, isfile, normpath, splitext


class ConfigData:
    __slots__ = ['__data_format', '__data_file', '__output_file_format',
                 '__output_file_path', '__analysis_mode', '__input_point']

    def __init__(self, data_format, data_file, output_file_format,
                 output_file_path, analysis_mode, input_point):
        """Creates an object of the ConfigData class,
        assigns values to the main script parameters from a configuration file."""
        self.__data_format = data_format.upper()
        self.__data_file = data_file
        self.__output_file_format = output_file_format.lower()
        self.__output_file_path = output_file_path
        self.__analysis_mode = analysis_mode.upper()
        self.__input_point = input_point

    def verify_config_data(self) -> None:
        """Validates configuration data.
        The data file type, output file type, analysis mode,
        and math point value (only for 'AFFL' mode) are checked for correctness.
        The data file and output file directory are checked for existence.
        If the check fails, an appropriate exception will be raised."""
        if self.__analysis_mode == 'AFFL':
            if not self.__input_point:
                raise ConfigFileParsingError('"point" in the section [general]')
            self.__input_point = float(self.__input_point)
        elif self.__analysis_mode == 'INTS':
            self.__input_point = None
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

    def get_input_point(self) -> float:
        """Returns the math point value."""
        return self.__input_point
