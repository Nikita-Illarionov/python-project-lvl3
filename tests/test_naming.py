from page_loader.url import to_file_name
import pytest


cases = [('https://ru.hexlet.io', 'ru-hexlet-io.html'),
         ('http://www.google.com', 'www-google-com.html'),
         ('https://test.com/file.txt', 'test-com-file.txt'),
         ('http://test.ru/a/b/c.pdf', 'test-ru-a-b-c.pdf')]


@pytest.mark.parametrize('url, expected_name', cases)
def test_naming_function(url, expected_name):
    assert to_file_name(url) == expected_name
