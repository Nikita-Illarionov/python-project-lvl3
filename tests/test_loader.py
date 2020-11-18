from page_loader.loading_page import download, make_path
import tempfile
import sys
import requests_mock


url = 'http://test.com'
with open(sys.path[0] + '/fixtures/answer.html', 'r') as file:
    answer_page = file.read()


with tempfile.TemporaryDirectory() as tmpdirname:
    with requests_mock.Mocker() as m:
        m.get(url, text="It's ok.\n")
        download(url, tmpdirname)
    with open(make_path(url, tmpdirname), 'r') as file:
        loading_page = file.read()


def test_loader():
    assert loading_page == answer_page
