class NoIntersectionError(Exception):
    def __init__(self):
        self.__description = f"Error! The initial math sets haven't intersection"

    def __str__(self):
        return f'{self.__description}'
