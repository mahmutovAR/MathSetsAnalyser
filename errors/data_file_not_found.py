class DataFileNotFoundError(Exception):
    __slots__ = ['__data_file']

    def __init__(self, data_file):
        self.__data_file = data_file
        self.__description = f'Error! The data file not found: {self.__data_file}'

    def __str__(self):
        return f'{self.__description}'
