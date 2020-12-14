import os
import re


def to_file_name(base_url):
    url, ext = os.path.splitext(base_url)
    url_parts = re.split('[^a-zA-Z0-9]+', url)
    url_parts.pop(0)
    if ext == '':
        ext = '.html'
    while len(url_parts) > 10:
        url_parts.pop(0)
    return '-'.join(url_parts) + ext
