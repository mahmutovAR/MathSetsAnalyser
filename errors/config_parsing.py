class ConfigFileParsingError(Exception):
    __slots__ = ['__config_id']

    def __init__(self, config_id):
        self.__config_id = config_id
        self.__description = f'Error! The {self.__config_id} not supplied or invalid.'

    def __str__(self):
        return f'{self.__description}'
