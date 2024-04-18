from os import chdir as os_chdir
from os import system as os_system
from os.path import join as os_path_join
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent

TEST_DIR = os_path_join(SCRIPT_DIR, 'tests')

os_chdir(TEST_DIR)
command = 'python3 -m unittest'

os_system(command)
