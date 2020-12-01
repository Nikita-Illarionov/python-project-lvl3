import os
import requests
from bs4 import BeautifulSoup
import re
import logging
from progress.bar import IncrementalBar
from urllib.parse import urlparse, urljoin


def load_resources(url, file_path):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    dir_path, _ = os.path.splitext(file_path)
    dir_path += '_files'

    if os.path.isdir(dir_path):
        logging.warning(f'{dir_path} already exists. Content can be changed')
    else:
        os.mkdir(dir_path)

    _, dir_name = os.path.split(dir_path)

    elements = list(filter(IsLocal, soup.find_all(['img', 'link', 'script'])))
    bar = IncrementalBar('Resource loading:', max=len(elements))
    for element in elements:
        attribute = 'href' if element.name == 'link' else 'src'
        link = element.get(attribute)
        resource_path = save(urljoin(url, link), dir_path)
        element[attribute] = resource_path
        bar.next()
    bar.finish()

    with open(file_path, 'w') as file:
        file.write(str(soup))


def IsLocal(element):
    attribute = 'href' if element.name == 'link' else 'src'
    link = element.get(attribute)
    if link and (urlparse(link).netloc, urlparse(link).scheme) == ('', ''):
        return True
    return False


def save(url, dir_path):
    resource_path = os.path.join(dir_path, name_resource(url))
    with open(resource_path, 'wb') as file:
        file.write(requests.get(url).content)
    return resource_path


def name_resource(url):
    url, ext = os.path.splitext(url)
    url_parts = re.split('[^a-zA-Z0-9]+', url)
    url_parts.pop(0)
    while len(url_parts) > 5:
        url_parts.pop(0)
    return '-'.join(url_parts) + ext
