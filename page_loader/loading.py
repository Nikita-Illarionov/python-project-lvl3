import os
import requests
import logging
#  from progress.bar import IncrementalBar
from page_loader.storage import save
from page_loader.assets import change_page


def load_page(base_url, file_path):
    with open(file_path, 'r') as file:
        page = file.read()

    dir_path = os.path.splitext(file_path)[0] + '_files'

    resources, new_page = change_page(base_url, page, dir_path)
    save(new_page, file_path)

    if not resources:
        return

    if os.path.isdir(dir_path):
        logging.warning(f'{dir_path} already exists. Content can be changed')
    else:
        os.mkdir(dir_path)

    for resource in resources:
        link, resource_path = resource
        save(requests.get(link).content, resource_path, mode='wb')
