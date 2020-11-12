from page_loader.main import load_page, make_path
import tempfile
import sys
import requests_mock


address = 'http://test.com'
with open(sys.path[0] + '/fixtures/answer.html', 'r') as file:
    answer_page = file.read()


with tempfile.TemporaryDirectory() as tmpdirname:
    with requests_mock.Mocker() as m:
        m.get(address, text="It's ok.\n")
        load_page(address, tmpdirname)
    with open(make_path(address, tmpdirname), 'r') as file:
        loading_page = file.read()


def test_loader():
    assert loading_page == answer_page
