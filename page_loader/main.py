import re
import os
import requests


def load_page(address, path):
    path_to_file = make_path(address, path)
    request_body = make_request(address)
    save_file(path_to_file, request_body)
    return path_to_file, request_body


def make_path(address, path):
    address_parts = re.split('[^a-zA-Z0-9]+', address)
    address_parts.pop(0)
    return os.path.join(path, '-'.join(address_parts) + '.html')


def make_request(address):
    return requests.get(address).text


def save_file(path_to_file, text):
    with open(path_to_file, 'w') as file:
        file.write(text)
