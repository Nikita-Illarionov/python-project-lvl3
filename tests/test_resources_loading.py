import tempfile
import sys
import requests_mock
from page_loader import download
import os
from urllib.parse import urljoin


url = 'https://test.com'
dir_name = 'test-com_files'
resources_url = [urljoin(url, '/assets/application.css'),
                 urljoin(url, '/assets/professions/nodejs.png'),
                 urljoin(url, '/runtime.js')]

expected_content = resources_url[:]


with open(sys.path[0] + '/fixtures/page_after.html', 'r') as file:
    expected_page = file.read()


def test_page_loading():
    with open(sys.path[0] + '/fixtures/page_before.html', 'r') as file:
        testing_page = file.read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(url, text=testing_page)
            [m.get(url, text=content) for url, content
             in zip(resources_url, expected_content)]
            file_path = download(url, tmpdirname)
            with open(file_path, 'r') as file:
                page = file.read()
            assert len(os.listdir(tmpdirname)) == 2
            assert len(os.listdir(os.path.join(tmpdirname, dir_name))) == 3
            assert page == expected_page
