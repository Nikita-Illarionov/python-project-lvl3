import os
import requests
from page_loader.url import to_file_name
from page_loader.storage import save
from page_loader.loading import load_page


class PageLoadingError(requests.exceptions.HTTPError):
    def __init__(self, error_message):
        self.error_message = error_message


error_messages = {404: 'Not Found', 500: 'Internal Server'}


def download(base_url, output_path):
    path_to_file = os.path.join(output_path, to_file_name(base_url))
    try:
        request = requests.get(base_url)
        code = request.status_code
        if code in [500, 404]:
            raise requests.exceptions.HTTPError
    except requests.exceptions.HTTPError as e:
        raise PageLoadingError(f'{code} error: {error_messages[code]}') from e
    save(request.text, path_to_file)
    load_page(base_url, path_to_file)
    return path_to_file
