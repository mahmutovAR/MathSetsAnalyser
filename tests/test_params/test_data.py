from os.path import join as os_path_join

class TestData:
    __slots__ = ['__script_dir']

    def __init__(self, script_dir):
        self.__script_dir = script_dir

    def get_script_dir(self) -> str:
        return self.__script_dir

    def get_json_test_data_file(self) -> str:
        return os_path_join(self.__script_dir, 'tests', 'data files', 'data file.json')

    def get_txt_test_data_file(self) -> str:
        return os_path_join(self.__script_dir, 'tests', 'data files', 'data file.txt')

    def get_xml_test_data_file(self) -> str:
        return os_path_join(self.__script_dir, 'tests', 'data files', 'data file.xml')

    def get_output_file(self) -> str:
        return os_path_join(self.__script_dir, 'tests', 'output file')

    def get_invalid_file_path(self) -> str:
        return os_path_join(self.__script_dir, 'err', 'file path')
