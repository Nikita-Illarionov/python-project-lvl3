import os
import logging


def save(content, path_to_file, mode='w'):
    if os.path.isfile(path_to_file):
        logging.warning(f'{path_to_file} already exists. It can be changed')
    with open(path_to_file, mode) as file:
        file.write(content)
