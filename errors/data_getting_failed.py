class DataGettingError(Exception):
    __slots__ = ['__data_id', '__error_id']

    def __init__(self, data_id, error_id):
        self.__data_id = data_id
        self.__error_id = error_id
        self.__description = f"""Error! Failed to get data from: {self.__data_id}\n{self.__error_id}"""

    def __str__(self):
        return f'{self.__description}'
