class OutputDataError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'Error! The output {self.error}'
