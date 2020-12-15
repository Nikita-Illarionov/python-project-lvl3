import os
import requests
from page_loader.url import to_file_name
from page_loader.storage import save
from page_loader.loading import load_page


class PageLoadingError(requests.exceptions.HTTPError):
    def __init__(self, error_message):
        self.error_message = error_message


def download(base_url, output_path):
    path_to_file = os.path.join(output_path, to_file_name(base_url))
    try:
        request = requests.get(base_url)
        if request.status_code == 404:
            raise requests.exceptions.HTTPError
        if request.status_code == 500:
            raise requests.exceptions.HTTPError
    except requests.exceptions.HTTPError as e:
        raise PageLoadingError('500 or 400 code') from e
    save(request.text, path_to_file)
    load_page(base_url, path_to_file)
    return path_to_file
