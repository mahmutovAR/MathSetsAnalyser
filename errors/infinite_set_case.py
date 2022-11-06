class InfiniteSetError(Exception):
    def __init__(self):
        self.__description = f"""Error! All initial math sets are infinite: ["-inf", "+inf"]."""

    def __str__(self):
        return f'{self.__description}'
