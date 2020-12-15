import pytest
import tempfile
import requests_mock
from page_loader import download, PageLoadingError


url = 'https://www.test.com'


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with requests_mock.Mocker() as m:
                m.get(url, text='test')
                download(url, tmpdirname + '/asdfasdf')


def test_exception():
    with pytest.raises(PageLoadingError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with requests_mock.Mocker() as m:
                m.get(url, status_code=500)
                download(url, tmpdirname)
