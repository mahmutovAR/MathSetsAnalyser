class TestFailedError(Exception):
    __slots__ = ['__test_name', '__input_exception']

    def __init__(self, test_name, input_exception):
        self.__test_name = test_name
        self.__input_exception = input_exception
        self.__description = f'Error! The unit test failed: problem with {self.__test_name}\n{self.__input_exception}'

    def __str__(self):
        return f'{self.__description}'
