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
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    dir_path, _ = os.path.splitext(file_path)
    dir_path += '_files'

    if os.path.isdir(dir_path):
        logging.warning(f'{dir_path} already exists. Content can be changed')
    else:
        os.mkdir(dir_path)

    _, dir_name = os.path.split(dir_path)

    all_elements = get_all_elements(soup)
    elements = list(filter(isLocal, all_elements))
    some_box = []
    bar = IncrementalBar('Resource loading:', max=len(elements))
    for element in elements:
        tag = tags[element.name]
        link = element.get(tag)
        some_box.append(save(urljoin(url, link), dir_path))
        bar.next()
    bar.finish()
    for element, new_way in zip(elements, some_box):
        tag = tags[element.name]
        link = element.get(tag)
        element[tag] = new_way

    with open(file_path, 'w') as file:
        file.write(soup.prettify(formatter='html'))


def get_elements(page):
    soup_for_page = BeautifulSoup(page, 'html.parser')
    return list(filter(isLocal, soup_for_page.find_all(list(tags))))


def get_all_elements(soup):
    result = []
    search_elements(soup.find_all(list(tags)), result)
    return result


def search_elements(obj, listing):
    for item in obj:
        link = item.get(tags[item.name])
        if link:
            listing.append(item)
        if item.find_all(list(tags)):
            search_elements(item.find_all(list(tags)), listing)


def isLocal(element):
    link = element.get(tags[element.name])
    scheme = urlparse(link).scheme
    netloc = urlparse(link).netloc
    return link and scheme == '' and netloc == ''


def save(url, dir_path):
    _, dir_name = os.path.split(dir_path)
    name = name_resource(url)
    resource_path = os.path.join(dir_path, name)
    content = requests.get(url).content
    while os.path.isfile(resource_path):
        name = correct_name(name)
        resource_path = os.path.join(dir_path, name)
    with open(resource_path, 'wb') as file:
        file.write(content)
    return os.path.join(dir_name, name)


def correct_name(name):
    way, ext = os.path.splitext(name)
    return way + '1' + ext


def name_resource(url):
    url, ext = os.path.splitext(url)
    url_parts = re.split('[^a-zA-Z0-9]+', url)
    url_parts.pop(0)
    while len(url_parts) > 5:
        url_parts.pop(0)
    return '-'.join(url_parts) + ext
