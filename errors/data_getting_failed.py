class DataGettingError(Exception):
    __slots__ = ['__error_id']

    def __init__(self, error_id):
        self.__error_id = error_id
        self.__description = f"""Error! Failed to get initial math sets from data file:\n{self.__error_id}"""

    def __str__(self):
        return f'{self.__description}'
