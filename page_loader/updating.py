import os
import requests
from bs4 import BeautifulSoup
import re
import logging
#  from progress.bar import IncrementalBar
from urllib.parse import urlparse, urljoin

tags = {'link': 'href', 'img': 'src', 'script': 'src'}


def load_resources(url, file_path):
    with open(file_path, 'r') as file:
        page = file.read()

    dir_path = os.path.splitext(file_path)[0] + '_files'
    path, dir_name = os.path.split(dir_path)

    if os.path.isdir(dir_path):
        logging.warning(f'{dir_path} already exists. Content can be changed')
    else:
        os.mkdir(dir_path)

    resources, new_page = change_page(url, page, dir_name)
    for resource in resources:
        link, way = resource
        save(requests.get(link).content, os.path.join(path, way))

    with open(file_path, 'w') as file:
        file.write(new_page)


def change_page(url, page, dir_name):
    soup = BeautifulSoup(page, 'html.parser')
    resources = []
    elements = list(filter(lambda x: isLocal(x, url),
                    soup.find_all(list(tags))))
    for element in elements:
        tag = tags[element.name]
        link = urljoin(url, element.get(tag))
        way = os.path.join(dir_name, name_resource(link))
        element[tag] = way
        resources.append((link, way))
    return resources, soup.prettify(formatter='html5')


def isLocal(element, base_url):
    link = element.get(tags[element.name])
    netloc1 = urlparse(base_url).netloc
    netloc2 = urlparse(urljoin(base_url, link)).netloc
    return netloc1 == netloc2


def save(content, path_to_resource):
    with open(path_to_resource, 'wb') as file:
        file.write(content)


def name_resource(url):
    url, ext = os.path.splitext(url)
    url_parts = re.split('[^a-zA-Z0-9]+', url)
    url_parts.pop(0)
    if ext == '':
        ext = '.html'
    while len(url_parts) > 10:
        url_parts.pop(0)
    return '-'.join(url_parts) + ext
