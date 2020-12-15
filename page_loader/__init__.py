import os
import requests
from page_loader.url import to_file_name
from page_loader.storage import save
from page_loader.loading import load_page


class PageLoadingError(Exception):
    def __init__(self, text):
        self.text = text


def download(base_url, output_path):
    path_to_file = os.path.join(output_path, to_file_name(base_url))
    request = requests.get(base_url)
    if request.status_code == 404:
        raise PageLoadingError('HTTP error 404: Not found')
    if request.status_code == 500:
        raise PageLoadingError('HTTP error 500 for : Internal Server Error')
    save(request.text, path_to_file)
    load_page(base_url, path_to_file)
    return path_to_file
