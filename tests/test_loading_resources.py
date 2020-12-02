import tempfile
import sys
import requests_mock
from page_loader.loading_page import download
from page_loader.updating import load_resources
from urllib.parse import urljoin


url = 'https://resource.loading.test.com'
resource1_url = urljoin(url, '/assets/application.css')
resource2_url = urljoin(url, '/courses.html')
resource3_url = urljoin(url, '/assets/professions/nodejs.png')
resource4_url = urljoin(url, '/runtime.js')

with open(sys.path[0] + '/fixtures/testing_page.html', 'r') as file:
    testing_page = file.read()

with tempfile.TemporaryDirectory() as tmpdirname:
    with requests_mock.Mocker() as m:
        m.get(url, text=testing_page)
        m.get(resource1_url, text=resource1_url)
        m.get(resource2_url, text=resource2_url)
        m.get(resource3_url, text=resource3_url)
        m.get(resource4_url, text=resource4_url)
        file_path = download(url, tmpdirname)
        with open(file_path, 'r') as file:
            page_before_change = file.read()
        load_resources(url, file_path)
        with open(file_path, 'r') as file:
            page_after_change = file.read()


def test_changing_file():
    assert page_before_change != page_after_change
