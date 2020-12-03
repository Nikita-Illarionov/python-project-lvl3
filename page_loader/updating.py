import os
import requests
from bs4 import BeautifulSoup
import re
import logging
from progress.bar import IncrementalBar
from urllib.parse import urlparse, urljoin


tags = {
            'link': 'href',
            'img': 'src',
            'script': 'src'
       }


def load_resources(url, file_path):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    dir_path, _ = os.path.splitext(file_path)
    dir_path += '_files'

    if os.path.isdir(dir_path):
        logging.warning(f'{dir_path} already exists. Content can be changed')
    else:
        os.mkdir(dir_path)

    _, dir_name = os.path.split(dir_path)

    elements = list(filter(lambda x: isLocal(x, url),
                    soup.find_all(list(tags))))
    bar = IncrementalBar('Resource loading:', max=len(elements))
    for element in elements:
        tag = tags[element.name]
        link = element.get(tag)
        element[tag] = save(urljoin(url, link), dir_path)
        bar.next()
    bar.finish()

    with open(file_path, 'w') as file:
        file.write(str(soup))


def get_elements(page, url):
    soup_for_page = BeautifulSoup(page, 'html.parser')
    return list(filter(lambda x: isLocal(x, url),
                soup_for_page.find_all(list(tags))))


def isLocal(element, url):
    link = element.get(tags[element.name])
    scheme = urlparse(link).scheme
    netloc = urlparse(link).netloc
    cond = link == urljoin(url, link) and netloc == urlparse(url).netloc
    return (link and scheme == '' and netloc == '') or cond


def save(url, dir_path):
    _, dir_name = os.path.split(dir_path)
    name = name_resource(url)
    resource_path = os.path.join(dir_path, name)
    with open(resource_path, 'wb') as file:
        file.write(requests.get(url).content)
    return os.path.join(dir_name, name)


def name_resource(url):
    url, ext = os.path.splitext(url)
    url_parts = re.split('[^a-zA-Z0-9]+', url)
    url_parts.pop(0)
    while len(url_parts) > 5:
        url_parts.pop(0)
    return '-'.join(url_parts) + ext
