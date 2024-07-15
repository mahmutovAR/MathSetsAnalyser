class ConfigFileError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'Error! The config file {self.error}'

