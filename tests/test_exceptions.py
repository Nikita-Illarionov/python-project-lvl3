import pytest
import tempfile
import requests_mock
from page_loader import download, HTTPError500, HTTPError404


url = 'https://www.test.com'


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with requests_mock.Mocker() as m:
                m.get(url, text='test')
                download(url, tmpdirname + '/asdfasdf')


def test_exception500():
    with pytest.raises(HTTPError500):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with requests_mock.Mocker() as m:
                m.get(url, status_code=500)
                download(url, tmpdirname)


def test_exception404():
    with pytest.raises(HTTPError404):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with requests_mock.Mocker() as m:
                m.get(url, status_code=404)
                download(url, tmpdirname)
