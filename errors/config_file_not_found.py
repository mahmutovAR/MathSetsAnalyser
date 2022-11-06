class ConfigFileNotFoundError(Exception):
    __slots__ = ['__config_file']

    def __init__(self, config_file):
        self.__config_file = config_file
        self.__description = f'Error! The config file not found: {self.__config_file}'

    def __str__(self):
        return f'{self.__description}'
