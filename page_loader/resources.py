import os
import requests
from bs4 import BeautifulSoup
import re


def load_resources(address, path_to_file):
    path_to_dir, _ = os.path.splitext(path_to_file)
    path_to_dir += '_files'
    _, dir_name = os.path.split(path_to_dir)
    #  os.mkdir(path_to_dir)

    with open(path_to_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    links = soup.find_all('link')
    for link in links:
        if link.get('href') and link['href'][0] == '/' and link['href'][1] != '/':
            url = address + link['href']
            file_path = os.path.join(path_to_dir, make_path(url))
            with open(file_path, 'wb') as file:
                file.write(requests.get(url).content)
            link['href'] = '/' + os.path.join(dir_name, make_path(url))

    scripts = soup.find_all('script')
    for script in scripts:
        if  script.get('src') and script['src'][0] == '/' and script['src'][1] != '/':
            url = address + script['src']
            file_path = os.path.join(path_to_dir, make_path(url))
            with open(file_path, 'wb') as file:
                file.write(requests.get(url).content	)
            script['src'] = os.path.join(dir_name, make_path(url))
    with open(path_to_file, 'w') as file:
        file.write(soup.prettify())
        
        

def make_request(address):
    return requests.get(address).content


def make_path(url):
    url_name = re.split('[^a-zA-Z0-9]+', url)
    ext = '.' + url_name[-1]
    url_name = url_name[:-1]
    url_name.pop(0)
    while len(url_name) > 10:
        url_name.pop(0)
    print('-'.join(url_name) + ext)
    return '-'.join(url_name) + ext
    
    
