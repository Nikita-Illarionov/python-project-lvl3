import tempfile
import sys
import requests_mock
from page_loader import download
from page_loader.updating import get_elements
from urllib.parse import urljoin
import os

tags = {'link': 'href', 'script': 'src', 'img': 'src'}

url = 'https://test.com'
resources_url = [urljoin(url, '/assets/application.css'),
                 urljoin(url, '/assets/professions/nodejs.png'),
                 urljoin(url, '/runtime.js')]
expected_content = ['content for "link" tag',
                    'content for "img" tag', 'content for "script" tag']
loading_content = []
with open(sys.path[0] + '/fixtures/page_with_resources.html', 'r') as file:
    testing_page = file.read()

with tempfile.TemporaryDirectory() as tmpdirname:
    with requests_mock.Mocker() as m:
        m.get(url, text=testing_page)
        [m.get(url, text=content) for url, content
         in zip(resources_url, expected_content)]
        #  ------------ download ------------------------------------
        file_path = download(url, tmpdirname)
        #  ----------------------------------------------------------
        with open(file_path, 'r') as file:
            loading_page = file.read()
            elements = get_elements(loading_page, url)
        for element in elements:
            tag = tags[element.name]
            link = element.get(tag)
            with open(os.path.join(tmpdirname, link), 'r') as file:
                loading_content.append(file.read())


def test_compare_resources():
    assert loading_content == expected_content