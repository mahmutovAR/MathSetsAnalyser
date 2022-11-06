class OutputDataError(Exception):
    def __init__(self):
        self.__description = f"Error! The script execution failed, there is no result."

    def __str__(self):
        return f'{self.__description}'
