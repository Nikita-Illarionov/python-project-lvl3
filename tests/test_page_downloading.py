from page_loader import download
import tempfile
import sys
import requests_mock


url = 'http://test.com'
with open(sys.path[0] + '/fixtures/page_without_resources.html', 'r') as file:
    expected_page = file.read()


with tempfile.TemporaryDirectory() as tmpdirname:
    with requests_mock.Mocker() as m:
        m.get(url, text=expected_page)
        file_path = download(url, tmpdirname)
    with open(file_path, 'r') as file:
        loading_page = file.read()


def test_load():
    assert loading_page == expected_page
