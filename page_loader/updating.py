import os
import requests
from bs4 import BeautifulSoup
import re
import logging
from progress.bar import IncrementalBar
from urllib.parse import urlparse, urljoin


tags = {'link': 'href', 'img': 'src', 'script': 'src'}


def load_resources(url, file_path):
    with open(file_path, 'r') as file:
        page = file.read()

    dir_path = os.path.splitext(file_path)[0] + '_files'
    dir_name = os.path.split(dir_path)[1]

    if os.path.isdir(dir_path):
        logging.warning(f'{dir_path} already exists. Content can be changed')
    else:
        os.mkdir(dir_path)

    download_resources(page, url, dir_path)
    new_page = change_page(page, url, dir_name)

    with open(file_path, 'w') as file:
        file.write(new_page)


def download_resources(page, url, dir_path):
    elements = get_elements(page, url)
    bar = IncrementalBar('Resource loading:', max=len(elements))
    for element in elements:
        tag = tags[element.name]
        link = element.get(tag)
        save(urljoin(url, link), dir_path)
        bar.next()
    bar.finish()


def change_page(page, url, dir_name):
    soup = BeautifulSoup(page, 'html.parser')
    elements = list(filter(lambda x: isLocal(x, url),
                    soup.find_all(list(tags))))
    for element in elements:
        tag = tags[element.name]
        link = element.get(tag)
        name = name_resource(urljoin(url, link))
        element[tag] = os.path.join(dir_name, name)
    return soup.prettify(formatter='html5')


def get_elements(page, url):
    soup = BeautifulSoup(page, 'html.parser')
    return list(filter(lambda x: isLocal(x, url),
                soup.find_all(list(tags))))


def isLocal(element, url):
    link = element.get(tags[element.name])
    scheme = urlparse(link).scheme
    netloc = urlparse(link).netloc
    condition1 = link and scheme == '' and netloc == ''
    condition2 = link == urljoin(url, link) and netloc == urlparse(url).netloc
    return condition1 or condition2


def save(url, dir_path):
    _, dir_name = os.path.split(dir_path)
    name = name_resource(url)
    resource_path = os.path.join(dir_path, name)
    with open(resource_path, 'wb') as file:
        file.write(requests.get(url).content)


def name_resource(url):
    url, ext = os.path.splitext(url)
    url_parts = re.split('[^a-zA-Z0-9]+', url)
    url_parts.pop(0)
    if ext == '':
        ext = '.html'
    while len(url_parts) > 10:
        url_parts.pop(0)
    return '-'.join(url_parts) + ext
