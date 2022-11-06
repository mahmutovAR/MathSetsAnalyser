class OutputFileGeneratingError(Exception):
    __slots__ = ['__data_id', '__input_exception']

    def __init__(self, data_id, input_exception):
        self.__data_id = data_id
        self.__input_exception = input_exception
        self.__description = f"""Error! Failed to create output file at: {self.__data_id}\n{self.__input_exception}"""

    def __str__(self):
        return f'{self.__description}'
