import os
import requests
from page_loader.url import to_file_name
from page_loader.storage import save


class HTTPError():
    description = ''


def download(base_url, output_path):
    path_to_file = os.path.join(output_path, to_file_name(base_url))
    request = requests.get(base_url)
    if request.status_code == 404:
        HTTPError.description = 'HTTP error 404: Not found'
        raise requests.exceptions.HTTPError
    if request.status_code == 500:
        HTTPError.description = 'HTTP error 500 for : Internal Server Error'
        raise requests.exceptions.HTTPError
    save(request.text, path_to_file)
    return path_to_file
