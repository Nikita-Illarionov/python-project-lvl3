import os
import requests
from bs4 import BeautifulSoup
import re


def load_pictures(address, path_to_file):
    path_to_dir, _ = os.path.splitext(path_to_file)
    path_to_dir += '_files'
    _, dir_name = os.path.split(path_to_dir)
    os.mkdir(path_to_dir)

    with open(path_to_file, 'rb') as file:
        soup = BeautifulSoup(file, 'html.parser')

    imgs = soup.find_all('img')
    for img in imgs:
        if img['src'][0] == '/' and img['src'][1] != '/':
            url = address + img['src']
            file_path = os.path.join(path_to_dir, make_path(url))
            with open(file_path, 'wb') as file:
                file.write(make_request(url))
            img['src'] = os.path.join(dir_name, make_path(url))
    with open(path_to_file, 'w') as file:
        file.write(str(soup))
        
        

def make_request(address):
    return requests.get(address).content


def make_path(url):
    url, ext = os.path.splitext(url)
    url_name = re.split('[^a-zA-z0-9]+', url)
    url_name.pop(0)
    while len(url_name) > 5:
        url_name.pop(0)
    return '-'.join(url_name) + ext
    
    
