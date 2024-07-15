from json import dump as json_dump

from os.path import abspath, dirname, isfile, splitext
from os.path import join as os_path_join

from chameleon import PageTemplateLoader

from errors import OutputDataError


def output_script_data(config_data: 'ConfigData object', output_data: list):
    """Generates the output file with the inputted title and data.
    The file type and path are determined from the inputted ConfigData object."""
    output_file_format = config_data.get_output_file_format()
    output_file_path = config_data.get_output_file_path()
    output_data = str(output_data)
    try:
        output_file_path = choose_name_for_output_file(output_file_format, output_file_path)
        with open(output_file_path, 'w') as file_to_write:
            if output_file_format == 'json':
                json_dump(output_data, file_to_write)

            elif output_file_format == 'txt':
                file_to_write.write(output_data)

            elif output_file_format == 'xml':
                template = PageTemplateLoader(os_path_join(abspath(dirname(__file__)), 'templates'))
                tmpl = template['output_temp.pt']
                data_for_xml = tmpl(output_data=output_data)
                file_to_write.write(data_for_xml)

            else:
                assert False, ('Internal error! output_script_data()'
                               '\noutput_file_format not JSON / TXT / XML')
    except Exception as err:
        raise OutputDataError(f'could not be generated in {output_file_path}\n{err}')


def choose_name_for_output_file(file_format: str, file_path: str) -> str:
    """Returns name of the output file, if the file with inputted name already exists then
    the output file will be renamed, "({num})" will be added to its name (for example: output_file(1).txt)."""
    temp_file_path = splitext(file_path)[0]
    if isfile(f'{temp_file_path}.{file_format}'):
        num = 1
        while isfile(f'{temp_file_path}({num}).{file_format}'):
            num += 1
        return f'{temp_file_path}({num}).{file_format}'
    else:
        return f'{temp_file_path}.{file_format}'
