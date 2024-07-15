class DataFileError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'Error! The data file {self.error}'
