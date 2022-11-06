class OutputDirectoryNotFoundError(Exception):
    __slots__ = ['__result_dir']

    def __init__(self, result_dir):
        self.__result_dir = result_dir
        self.__description = f'Error! The directory for output file not found: {self.__result_dir}'

    def __str__(self):
        return f'{self.__description}'
