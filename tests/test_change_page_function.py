import sys
import requests_mock
from page_loader.assets import change_page
import os
from urllib.parse import urljoin
import requests
import tempfile


base_url = 'https://test.com'
dir_name = 'test-com_files'
resources_url = [urljoin(base_url, '/assets/application.css'),
                 urljoin(base_url, '/assets/professions/nodejs.png'),
                 urljoin(base_url, '/runtime.js')]

expected_content = resources_url[:]


with open(sys.path[0] + '/fixtures/page_after.html', 'r') as file:
    expected_page = file.read()


def test_page_loading():
    with open(sys.path[0] + '/fixtures/page_before.html', 'r') as file:
        testing_page = file.read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(base_url, text=testing_page)
            [m.get(url, text=content) for url, content
             in zip(resources_url, expected_content)]
            resources, page = change_page(base_url, testing_page,
                                          os.path.join(tmpdirname, dir_name))
            for resource, content in zip(resources, expected_content):
                link, _ = resource
                assert requests.get(link).text == content
            assert page == expected_page
