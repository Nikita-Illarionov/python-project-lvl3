import re
import os
import requests
import logging
from page_loader.updating import load_resources


class HTTPError():
    description = ''


def download(url, output_path):
    path_to_file = make_path(url, output_path)
    request = requests.get(url)
    if request.status_code == 404:
        HTTPError.description = 'HTTP error 404: Not found'
        raise requests.exceptions.HTTPError
    if request.status_code == 500:
        HTTPError.description = 'HTTP error 500 for : Internal Server Error'
        raise requests.exceptions.HTTPError
    save(request.text, path_to_file)
    logging.info(f'page saved in {path_to_file}')
    load_resources(url, path_to_file)
    return path_to_file


def make_path(url, output_path):
    url_parts = re.split('[^a-zA-Z0-9]+', url)
    url_parts.pop(0)
    return os.path.join(output_path, '-'.join(url_parts) + '.html')


def save(content, path_to_file):
    if os.path.isfile(path_to_file):
        logging.warning(f'{path_to_file} already exists. It can be changed')
    with open(path_to_file, 'w') as file:
        file.write(content)
